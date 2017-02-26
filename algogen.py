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
         select:callable, reproduce:callable, mutate:callable,
         step_number:int=None) -> 'pop':
    """Compute one step, return the new population

    This implementation first select the population, then produce
    the new generation.
    This behavior could tends to favorize diversity.

    pop -- individuals of current generation
    case -- Case instance
    pop_size -- number of individual in the next generation
    score -- function used for scoring
    select -- function used for selection
    reproduce -- function used for reproduction
    mutate -- function used for mutation
    step_number -- number of the current step ; only for cosmetic/logging purpose

    """
    assert callable(score)
    assert callable(select)
    assert callable(reproduce)
    assert isinstance(pop_size, int)
    assert all(isinstance(unit, Unit) for unit in pop)
    assert isinstance(case, Case)
    assert pop

    if step_number is not None:
        print('# {}'.format(step_number))

    stdin, expected = case

    with Pool(processes=MULTIPROC_PROCESSES, maxtasksperchild=MULTIPROC_TASK_PER_CHILD) as p:
        scored_pop = dict(zip(pop, p.starmap(score, zip(pop, itertools.repeat((stdin, expected))))))

    best_unit = max(pop, key=lambda u: scored_pop[u].score)
    best_result = scored_pop[best_unit]
    print('SCORES:', sorted(tuple(set(round(r.score, 3) for u, r in scored_pop.items())), reverse=True))
    proportions = Counter(r.score for r in scored_pop.values())
    print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
    print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3),
          '\tOUTPUTS:', '"' + best_result.found + '"', '\t(expect {})'.format(best_result.expected),
          ('[SUCCESS]' if best_result.found == best_result.expected else ''))
    print('SOURCE:', best_unit.source)

    selected = select(scored_pop)
    return reproduce(selected, pop_size, mutator=mutate)
