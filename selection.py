"""Implementation of selection functions.

A selection function maps a scored population with a set of unit,
which is subset of the input population.

A good selection function keeps the best unit
without compromising the diversity.

Input of these functions are the following:

    scored_pop -- a map {unit: score}, giving its score for each unit in population
    other -- supplementary parameters that depends of the selection method

As output, selection functions return an iterable of (Unit, score),
taken from the initial population.
The size of this output set depends of the selection function, but always has at least 2 elements.
No selection function should returns two times the same units in a single call.

"""


import random
from functools import partial

import utils
from utils import reversed_dict, named_functions_interface_decorator


DEFAULT_SELECTION = ((0, 40), )
DEFAULT_POOL_SIZE = 10
DEFAULT_SELECTION_SIZE = 0.4

DEFAULT_PROB_FUNCTION = lambda x, mn, mx: (x - (mn-1)) / ((mx - (mn-1))+1)


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return selection functions"""
    return {
        **utils.make_named_functions('RS', ranking_slices, {'pattern': {'D': DEFAULT_SELECTION, '2': ((0, 30), (45, 55)), 'B1': ((0, 50),)}}),
        **utils.make_named_functions('PL', poolling, {'pool_size': {'S': 2, 'M': 10, 'L': 20, 'D': DEFAULT_POOL_SIZE}, 'selection_size': {'1': 0.1, 'D': DEFAULT_SELECTION_SIZE, '6': 0.6}, 'unique': 'U'}),
        'PF': non_linear_likelihood,
    }

def default_functions() -> tuple:
    """Return default selection functions"""
    return named_functions.as_tuple()


def ranking_slices(scored_units:dict({'indiv': 'score'}),
                   pattern=DEFAULT_SELECTION) -> frozenset:
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
                returned.add((unt, scored_units[unt]))
    while len(returned) < 2:
        returned.add(random.choice(list(scored_units.items())))
    return frozenset(returned)


def poolling(scored_units:dict({'indiv': 'score'}),
             pool_size:int=DEFAULT_POOL_SIZE,
             selection_size:int or float=DEFAULT_SELECTION_SIZE, unique: bool = False) -> iter:
    """Yield selected individuals from given {unit: score}.

    Seek for groups of units having the same score,
    beginning by the highest score, and randomly select pool_size units of that pool.

    pool_size -- number of units of the same score to get
    selection_size -- final number of unit to return
    unique -- try not yielding two units of same source code

    if selection_size is a float in [0;1], it is assumed to be a percentage
    of the input population size that should be select.
    Ex: if selection_size == 0.4 and input population contains 100 units,
    the output frozenset will contains 40 units.

    """
    if not isinstance(selection_size, int):
        assert isinstance(selection_size, float), "Input selection_size should be int or float"
        assert 0. <= selection_size <= 1., "Input selection_size should be in [0;1]"
        selection_size = max(1, int(round(selection_size * len(scored_units))))
    assert selection_size > 0, "selection_size can't be equal to {} ({})".format(selection_size, type(selection_size))

    if selection_size > len(scored_units):
        raise ValueError(f"Can't select {selection_size} of {len(scored_units)} scored units.")

    sorted_scores = sorted(list(set(scored_units.values())), reverse=True)

    sorted_units = []  # list[list[unit]], where first list is unit of greater scores
    units_per_score = reversed_dict(scored_units, cast=list)  # score -> list[unit]
    for score in sorted_scores:
        # Note that the shuffle is necessary while two units of the same score
        #  could remain different. (by chromosome size for instance)
        #  this enforce that units will always be treated equally.
        units = units_per_score[score]
        random.shuffle(units)
        sorted_units.append(list(units))

    nb_yield = 0
    for idx in range(len(sorted_units)):  # we will edit the list during loop
        units = sorted_units[idx]
        if unique:
            to_send = set()
            seen_sources = set()
            for unit in list(units):
                if unit.source not in seen_sources:
                    seen_sources.add(unit.source)
                    to_send.add(unit)

        else:  # two selected units may have the same source code
            to_send = set(units[:pool_size])  # take the first pool_size units in the pool

        # now yield the data
        yield from ((unit, scored_units[unit]) for unit in to_send)
        nb_yield += len(to_send)
        if nb_yield >= selection_size:
            return  # selection size is reached
        # edit the remaining data in list
        sorted_units[idx] = [u for u in sorted_units[idx] if u not in to_send]

    else:  # at this point, there is yield remaining, but no unit fitting the given parameters was found
        assert nb_yield < selection_size, (nb_yield, selection_size)
        yield from poolling({u: s for s, us in units_per_score.items() for u in us}, pool_size=pool_size, selection_size=selection_size - nb_yield, unique=False)


def non_linear_likelihood(scored_units: dict['indiv', 'score'], selection_size:int or float=DEFAULT_SELECTION_SIZE, *, prob_func = DEFAULT_PROB_FUNCTION) -> iter:
    """Yield selected individuals"""
    # ensure selection_size is (or can be translated to) an integer giving the exact amount of units to return
    if not isinstance(selection_size, int):
        assert isinstance(selection_size, float), "Input selection_size should be int or float"
        assert 0. <= selection_size <= 1., "Input selection_size should be in [0;1]"
        selection_size = max(1, int(round(selection_size * len(scored_units))))
    assert selection_size > 0, "selection_size can't be equal to {} ({})".format(selection_size, type(selection_size))

    if selection_size > len(scored_units):
        raise ValueError(f"Can't select {selection_size} of {len(scored_units)} scored units.")

    minscore, maxscore = min(scored_units.values()).score, max(scored_units.values()).score  # RunResult instances must only provide their score
    pfunc = partial(prob_func, mn=minscore, mx=maxscore)

    nb_yield = 0
    while nb_yield < selection_size:
        for unit, score in scored_units.items():
            if random.random() < pfunc(score.score):
                nb_yield += 1
                yield unit, score
