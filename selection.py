"""Implementation of selection functions.

A selection function maps a scored population with a set of unit,
which is subset of the input population.

A good selection function keeps the best unit
without compromising the diversity.

Input of these functions are the following:

    scored_pop -- a map {unit: score}, giving its score for each unit in population
    other -- supplementary parameters that depends of the selection method

As output, selection functions return an iterable of units,
taken from the initial population.
The size of this output set depends of the selection function.
No selection function should returns two times the same units in a single call.

"""


import random
from functools import partial

from utils import reversed_dict


DEFAULT_SELECTION = ((0, 40), )
DEFAULT_POOL_SIZE = 10
DEFAULT_SELECTION_SIZE = 0.4


def functions() -> iter:
    """Return selection functions"""
    return (
        partial(ranking_slices, pattern=DEFAULT_SELECTION),
        partial(ranking_slices, pattern=((0, 30), (45, 55))),
        partial(ranking_slices, pattern=((0, 50),)),
        partial(poolling, pool_size=DEFAULT_POOL_SIZE, selection_size=DEFAULT_SELECTION),
        partial(poolling, pool_size=1, selection_size=DEFAULT_SELECTION),
        partial(poolling, pool_size=10, selection_size=0.1),
        partial(poolling, pool_size=1, selection_size=0.1),
        partial(poolling, pool_size=20, selection_size=0.6),
    )


def ranking_slices(scored_units:dict({'indiv': 'score'}), pattern=DEFAULT_SELECTION) -> frozenset:
    """Return a frozenset of selected individuals from given {unit: score}.

    Pattern is an iterable of 2-uplet (start, stop), where start and stop are
    percentage describing the unit range to take.
    For each 2-uplet (X, Y), all unit in between the X and Y percent of the
    sorted-by-score distribution are kept.

    Default is ((0, 40), ), meaning that the first 40% will be returned.

    This allows client to choose (1) the quantity of unit kept by selection,
    and (2) the ratio elitism/permissivity.

    """
    ordered = sorted(tuple(scored_units.keys()), key=lambda k: scored_units[k], reverse=True)  # ordered units
    total_number = len(ordered)
    by_percent = tuple((u, rank / total_number) for rank, u in enumerate(ordered, start=1))
    pattern = sorted(pattern, key=lambda x: x[0])  # sort on start bound
    returned = set()
    for start, stop in pattern:
        while not (0. <= start <= 1.): start /= 10
        while not (0. <= stop <= 1.): stop /= 10
        for unt, percent in by_percent:
            if start <= percent <= stop:
                returned.add(unt)
    return frozenset(returned)


def poolling(scored_units:dict({'indiv': 'score'}),
             pool_size:int=DEFAULT_POOL_SIZE,
             selection_size:int or float=DEFAULT_SELECTION_SIZE) -> iter:
    """Yield selected individuals from given {unit: score}.

    Seek for groups of pool_size units having the same score,
    beginning by the highest score, until selection_size units have been
    choosed.

    pool_size -- number of units of the same score to get
    selection_size -- final number of unit to return

    if selection_size is a float in [0;1], it is assumed to be a percentage
    of the input population size that should be select.
    Ex: if selection_size == 0.4 and input population contains 100 units,
    the output frozenset will contains 40 units.

    """
    if not isinstance(selection_size, int):
        assert isinstance(selection_size, float), "Input selection_size should be int or float"
        assert 0. <= selection_size <= 1., "Input selection_size should be in [0;1]"
        selection_size = int(round(selection_size * len(scored_units)))

    units_per_score = {}  # {score: iter(units)}
    for score, units in reversed_dict(scored_units, cast=list).items():
        # Note that the shuffle is necessary while two units of the same score
        #  could remain different. (by chromosome size for instance)
        #  this enforce that units will always be treated equally.
        random.shuffle(units)
        units_per_score[score] = iter(units)
    scores = tuple(sorted(tuple(units_per_score.keys()), reverse=True))

    nb_ret = 0
    while nb_ret < selection_size:
        empty_scores = set()
        for score in scores:
            for _ in range(pool_size):
                try:
                    yield next(units_per_score[score])
                    nb_ret += 1
                    if nb_ret >= selection_size:
                        return  # selection size is reached
                except StopIteration:
                    # there is no more unit at this score.
                    empty_scores.add(score)
        # ignore emptyied scores
        scores = tuple(score for score in scores if score not in empty_scores)



