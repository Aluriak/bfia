"""Implementation of a genetic algorithm step calculation.

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
from utils import named_functions_interface_decorator


MULTIPROC_PROCESSES = 16
MULTIPROC_TASK_PER_CHILD = 32
# printing
MAX_PRINTED_PROPS = 10


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return GA functions"""
    return {
        'DIV': step,
        'SCR': step_cross_first,
    }

def default_functions() -> tuple:
    """Return default GA functions"""
    return named_functions.as_tuple() + anonymous_functions()

def anonymous_functions() -> tuple:
    """Return GA functions that have no name"""
    return ()


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
    assert callable(mutate)
    assert isinstance(pop_size, int)
    assert all(isinstance(unit, Unit) for unit in pop)
    assert isinstance(case, Case)
    assert pop

    if step_number is not None:
        print('\n\n# Step {}'.format(step_number))

    stdin, expected = case
    scored_pop = _multisolve_scoring(stdin, expected, pop, score)

    best_unit = max(pop, key=lambda u: scored_pop[u].score)
    best_result = scored_pop[best_unit]
    print('SCORES:', sorted(tuple(set(round(r.score, 3) for u, r in scored_pop.items())), reverse=True))
    proportions = Counter(r.score for r in scored_pop.values())
    print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
    print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3))
    print('OUTPUTS:', '"' + best_result.found + '"', '\t(expect {})'.format(best_result.expected),
          ('[SUCCESS]' if best_result.found == best_result.expected else ''))
    print('SOURCE:', best_unit.source)

    selected = select(scored_pop)
    return reproduce(selected, pop_size, mutator=mutate)


def step_cross_first(pop, case, pop_size:int, score:callable,
                     select:callable, reproduce:callable, mutate:callable,
                     step_number:int=None) -> 'pop':
    """Compute one step, return the new population

    This implementation first produce the new generation, then select.
    This behavior could tends to favorize mean score increasing.

    """
    assert callable(score)
    assert callable(select)
    assert callable(reproduce)
    assert callable(mutate)
    assert isinstance(pop_size, int)
    assert all(isinstance(unit, Unit) for unit in pop)
    assert isinstance(case, Case)
    assert pop

    if step_number is not None:
        print('\n\n# Step {}'.format(step_number))

    pop = tuple(reproduce(pop, pop_size * 2, mutator=mutate))
    assert pop

    stdin, expected = case
    scored_pop = _multisolve_scoring(stdin, expected, pop, score)

    best_unit = max(pop, key=lambda u: scored_pop[u].score)
    best_result = scored_pop[best_unit]
    print('SCORES:', sorted(tuple(set(round(r.score, 3) for u, r in scored_pop.items())), reverse=True))
    proportions = Counter(r.score for r in scored_pop.values())
    print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
    print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3))
    print('OUTPUTS:', '"' + best_result.found + '"', '\t(expect {})'.format(best_result.expected),
          ('[SUCCESS]' if best_result.found == best_result.expected else ''))
    print('SOURCE:', best_unit.source)
    return select(scored_pop)


def _multisolve_scoring(stdin, expected, pop, score:callable) -> dict:
    """Perform the scoring of given population for given stdin and
    expected result, using given scoring function.

    Return {individual: score}.

    """
    inputs = itertools.repeat((stdin, expected))
    with Pool(processes=MULTIPROC_PROCESSES, maxtasksperchild=MULTIPROC_TASK_PER_CHILD) as p:
        return dict(zip(pop, p.starmap(score, zip(pop, inputs))))
