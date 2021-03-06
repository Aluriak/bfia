"""Function of reproduction, creating a population from another.

"""


import random
import itertools
from functools import partial

import mutator
from unit import Unit
from utils import named_functions_interface_decorator


DEFAULT_PARTHENOGENESIS = 0.01


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return reproduction functions"""
    return {
        'SCP':  partial(same_with_childs, keep_parents=True),
        'SCNP': partial(same_with_childs, keep_parents=False),
    }


def default_functions() -> tuple:
    """Return default reproduction functions"""
    return named_functions.as_tuple() + anonymous_functions()

def anonymous_functions() -> tuple:
    """Return reproduction functions that have no name"""
    return ()


def same_with_childs(pop:iter, n:int, *, parthenogenesis:float=DEFAULT_PARTHENOGENESIS,
                     mutator:callable=mutator.all_mutators(),
                     best_parent:Unit=None, keep_parents:bool=True) -> iter:
    """Yield population of size n, generated from given population.

    pop -- iterable of units used to build the new pop
    n -- size of the returned population
    parthenogenesis -- ratio giving the percentage of chance that an unit use
        clonage instead of seeking for parents. [NOT IMPLEMENTED]
    mutator -- a mutator function. Default is the full set of available mutations.
    best_parent -- the unit that will be used as supplementary parent in case of non-
                   choose randomly if not provided.
    keep_parents -- set to False to get only the childs and discard parents
                    from next generation.

    """
    pop = list(pop)
    assert pop, "given pop can't be empty"

    remain_to_yield = n
    if keep_parents:
        yield from pop
        remain_to_yield -= len(pop)

    best_parent = best_parent or random.choice(pop)
    while remain_to_yield:
        random.shuffle(pop)
        chunks = [iter(pop)] * 2
        for parents in itertools.zip_longest(*chunks, fillvalue=best_parent):
            yield Unit.mutated(Unit.child_from_crossed(parents), mutator)
            remain_to_yield -= 1
            if not remain_to_yield: break
