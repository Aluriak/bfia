"""Function of reproduction, creating a population from another.

"""


import random
import itertools
from functools import partial

import mutator
from unit import Unit


DEFAULT_PARTHENOGENESIS = 0.01


def functions() -> iter:
    """Return reproduction functions"""
    return (
        same_with_childs,
    )


def same_with_childs(pop:iter, n:int, *, parthenogenesis:float=DEFAULT_PARTHENOGENESIS,
                     mutators:iter=mutator.all_mutators(),
                     best_parent:Unit=None) -> iter:
    """Yield population of size n, generated from given population.

    pop -- iterable of units used to build the new pop
    n -- size of the returned population
    parthenogenesis -- ratio giving the percentage of chance that an unit use
        clonage instead of seeking for parents. [NOT IMPLEMENTED]
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
