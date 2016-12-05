"""Implementation of a genetic algorithm.

Steps:
    - score current generation
    - select parents
    - build next generation

"""

import itertools
from multiprocessing import Pool
from collections import Counter

from case import Case
from unit import Unit


MULTIPROC_PROCESSES = 16
MULTIPROC_TASK_PER_CHILD = 32
# printing
MAX_PRINTED_PROPS = 10


def step(pop, case, pop_size:int, score:callable,
         select:callable, reproduce:callable, step_number:int=None) -> 'pop':
    """Compute one step, return the new population"""
    assert callable(score)
    assert callable(select)
    assert callable(reproduce)
    assert isinstance(pop_size, int)
    assert all(isinstance(unit, Unit) for unit in pop)
    assert isinstance(case, Case)
    assert pop

    if step_number is not None:
        print('# {}'.format(step_number))

    with Pool(processes=MULTIPROC_PROCESSES, maxtasksperchild=MULTIPROC_TASK_PER_CHILD) as p:
        scored_pop = dict(zip(pop, p.starmap(score, zip(pop, itertools.repeat(case)))))

    best_unit = max(pop, key=lambda u: scored_pop[u].score)
    best_result = scored_pop[best_unit]
    print('SCORES:', sorted(tuple(set(round(r.score, 3) for u, r in scored_pop.items())), reverse=True))
    proportions = Counter(r.score for r in scored_pop.values())
    print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
    print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3), '\tOUTPUTS:', '"' + best_result.found + '"', '\t(expect {})'.format(best_result.expected))
    print('SOURCE:', best_unit.source)

    selected = select(scored_pop)
    return reproduce(selected, pop_size)
