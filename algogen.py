"""Implementation of a genetic algorithm.

Steps:
    - score current generation
    - select parents
    - build next generation

"""

import ctypes
import random
import itertools
from itertools import islice
from collections import namedtuple
from multiprocessing import Pool

import interpreter
import mutator
from scoring import compare_str
from unit import Unit


INTERPRETER = interpreter.load_interpreter()
MAX_OUT_SIZE = 32

DEFAULT_SELECTION = ((0, 40), )
DEFAULT_PARTHENOGENESIS = 0.01

MULTIPROC_PROCESSES = 16
MULTIPROC_TASK_PER_CHILD = 32

RunResult = namedtuple('RunResult', 'score expected found')


# if True:
if False:
    one = INTERPRETER.inline('-----------------------..[-<]+++++++++++++++++++++++++++++++-++.+<.')
    two = INTERPRETER.inline('------------------------.+.[-<]+++++++++++++++++++++++++++++++-++.+<.')
    expected = 'hi !'
    print('BSE:', expected, [c for c in expected.encode()])
    print('ONE:', one, [c for c in one.encode()])
    print('TWO:', two, [c for c in two.encode()])
    print(expected == one, 'ONE:', compare_str(expected, one))
    print(expected == two, 'TWO:', compare_str(expected, two))
    exit()




def select(scored_units:dict({'indiv': 'score'}), pattern=DEFAULT_SELECTION) -> frozenset:
    """Return a frozenset of selected individuals from given {unit: score}.

    Pattern is an iterable of 2-uplet (start, stop), where start and stop are
    percentage describing the unit to take.
    For each 2-uplet (X, Y), all unit in between the X and Y percent of the
    sorted-by-score distribution are kept.

    Default is ((0, 40), ), standing for the first 40%.

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


def pop_from(pop:iter, n:int, *, parthenogenesis:float=DEFAULT_PARTHENOGENESIS,
             mutators:iter=mutator.string_mutators(),
             best_parent:Unit=None) -> iter:
    """Yield population of size n, generated from given population.

    pop -- iterable of units used to build the new pop
    n -- size of the returned population
    parthenogenesis -- ratio giving the percentage of chance that an unit use
        clonage instead of seeking for parents.
    mutators -- list of mutator function. Default is the string related ones.
    best_parent -- the unit that will be used as supplementary parent in case of non-
                   choose randomly if not provided.

    """
    pop = list(pop)
    new = list(pop)
    best_parent = best_parent or random.choice(pop)
    assert len(new) < n
    while len(new) < n:
        random.shuffle(pop)
        chunks = [iter(pop)] * 2
        for parents in itertools.zip_longest(*chunks, fillvalue=best_parent):
            new.append(Unit.mutated(Unit.child_from_crossed(parents), mutators))
            if len(new) >= n: break
    yield from new


def score(unit) -> float:
    # hi !
    in_ = ''
    expected = 'hi !'
    # hello <input> !
    # in_ = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))
    # expected = 'hello {} !'.format(in_)
    # division by two
    # in_ = chr(random.randint(32, 120))
    # expected = chr(ord(in_) // 2)

    # compute and return score
    out = INTERPRETER.inline(unit.source, in_, max_output_size=MAX_OUT_SIZE)
    assert len(expected) < MAX_OUT_SIZE
    score = 10000 - compare_str(expected, out)
    return RunResult(score, expected, out)


def multisolve(pop):
    with Pool(processes=MULTIPROC_PROCESSES, maxtasksperchild=MULTIPROC_TASK_PER_CHILD) as p:
        return dict(zip(pop, p.map(score, pop)))



def run(pop:iter, score:callable, mutate:callable, cross:callable, mutation_rate:float):
    assert 0. <= mutation_rate <= 1.
    assert callable(score)
    assert callable(mutate)
    assert callable(cross)
    assert all(isinstance(unit, Unit) for unit in pop)
    assert pop
