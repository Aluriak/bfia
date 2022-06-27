"""Implementation of a genetic algorithm step calculation.

Steps:
    - score current generation
    - select parents
    - build next generation

"""

import itertools
from multiprocessing import Pool
from collections import Counter, namedtuple

from case import Case
from unit import Unit
from utils import named_functions_interface_decorator


MULTIPROC_PROCESSES = 16
MULTIPROC_TASK_PER_CHILD = 32
# printing
MAX_PRINTED_PROPS = 10

StepResult = namedtuple('StepResult', 'pop, scored_old_pop, winners')


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return GA functions"""
    return {
        'DIV': step,
        # 'SCR': step_cross_first,  # TODO: DOESN'T WORK PROPERLY (LOGIC PROBLEM)
    }

def default_functions() -> tuple:
    """Return default GA functions"""
    return named_functions.as_tuple()


def step(pop, case, pop_size:int, score:callable,
         select:callable, reproduce:callable, cross: callable, mutate:callable,
         step_number:int=None, callback_stats:callable=(lambda sp, mx, mn: None)) -> 'pop':
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
    cross -- function used for crossing
    mutate -- function used for mutation
    step_number -- number of the current step ; only for cosmetic/logging purpose
    callback_stats -- a callback that will get (scored_pop, max, min)

    """
    assert callable(score)
    assert callable(select)
    assert callable(reproduce)
    assert callable(cross)
    assert callable(mutate)
    assert callable(callback_stats)
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

    # call the user defined data handling
    callback_stats(scored_pop, best_result, min(scored_pop.values()))

    proportions = Counter(r.score for r in scored_pop.values())
    print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
    print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3))
    print('OUTPUTS:', '"' + best_result.found + '"', '\t(expect {})'.format(best_result.expected),
          ('[SUCCESS]' if best_result.found == best_result.expected else ''))
    print('SOURCE:', best_unit.source)

    winners = ()
    if best_result.found == best_result.expected:
        winners = tuple(unit for unit, score in scored_pop.items() if score == best_result.score)

    selected = dict(select(scored_pop))
    assert len(selected) > 1, selected
    assert selected, "at least one individual must be selected"
    final = tuple(reproduce(selected, pop_size, cross, mutator=mutate))
    assert len(final) == pop_size, "new pop must have a size of {} ({}), not {}".format(pop_size, type(pop_size), len(final))
    return StepResult(final, scored_pop, winners)


def step_cross_first(pop, case, pop_size:int, score:callable,
                     select:callable, reproduce:callable, mutate:callable,
                     step_number:int=None) -> 'pop':
    """Compute one step, return the new population

    This implementation first produce the new generation, then select
    among the bests.
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

    # keep only the bests.  TODO: NEED SEARCH ABOUT HOW TO IMPLEMENT THIS.
    scored_pop = dict(itertool.islice(sorted(scored_pop.items(), reverse=True, key=itemgetter(1)), 0, pop_size))
    for score in sorted(pop_by_score, reverse=True):
        score

    best_unit = max(pop, key=lambda u: scored_pop[u].score)
    best_result = scored_pop[best_unit]
    print('SCORES:', sorted(tuple(set(round(r.score, 3) for u, r in scored_pop.items())), reverse=True))
    proportions = Counter(r.score for r in scored_pop.values())
    print('PROPS :', proportions.most_common(MAX_PRINTED_PROPS))
    print('OF', len(scored_pop), 'BEST:', round(best_result.score, 3))
    print(f"OUTPUTS: \"{best_result.found}\"\t(expect {best_result.expected})",
          ("[SUCCESS]" if best_result.found == best_result.expected else ''))
    print('SOURCE:', best_unit.source)
    return StepResult(tuple(select(scored_pop)), scored_pop)


def _multisolve_scoring(stdin, expected, pop, score:callable) -> dict:
    """Perform the scoring of given population for given stdin and
    expected result, using given scoring function.

    Return {individual: score}.

    """
    inputs = itertools.repeat((stdin, expected))
    with Pool(processes=MULTIPROC_PROCESSES, maxtasksperchild=MULTIPROC_TASK_PER_CHILD) as p:
        return dict(zip(pop, p.starmap(score, zip(pop, inputs))))
