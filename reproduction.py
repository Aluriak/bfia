"""Function of reproduction, creating a population from another.

"""


import random
import itertools

import utils
import mutator
from unit import Unit
from utils import named_functions_interface_decorator, choices


DEFAULT_PARTHENOGENESIS = 0.01


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return reproduction functions"""
    return {
        **utils.make_named_functions('PR', pairing_with_replacement, {'keep_parents': 'P', 'parent_score_weight': 'W'}),
        **utils.make_named_functions('PA', pairing_all_parents, {'keep_parents': 'P'}),
    }


def default_functions() -> tuple:
    """Return default reproduction functions"""
    return named_functions.as_tuple()


def pairing_with_replacement(scored_parents:iter, n:int, crossing_func:callable, *,
                             parthenogenesis:float=0, mutator:callable=mutator.all_mutators(),
                             keep_parents:bool=True, parent_score_weight: bool = True) -> iter:
    """Yield population of size n, generated from given population,
    by repeateadly choose two parent randomly and compute their child.

    scored_parents -- map unit->score used to build the new pop (the parents)
    n -- size of the returned population
    parthenogenesis -- ratio giving the percentage of chance that an unit use
        clonage instead of seeking for parents.
    mutator -- a mutator function. Default is the full set of available mutations.
    keep_parents -- set to False to get only the childs and discard parents
                    from next generation.
    parent_score_weight -- whether or not the score of a parent have an impact of the likelihood of being chosen
    crossing_by_chromosomes -- whether to use the chromosome-based crossing, or the syntaxic one

    """
    assert scored_parents, "given parent population can't be empty"
    new = list(scored_parents) if keep_parents else []
    if len(new) == n:
        print(f"same_with_childs: population of {len(new)} parents can't reproduce, "
              f"because final population already have {n} individuals")
    assert len(new) <= n
    while len(new) < n:
        # pick two parents
        if parent_score_weight:
            weights = [v.score if v.score > 0 else 1 for v in scored_parents.values()]  # replace null and negative score by the minimal acceptable weight of 1
            print(scored_parents, weights)
            parents = choices(scored_parents.keys(), weights=weights, k=2, replacement=False)
        else:
            parents = choices(scored_parents.keys(), k=2, replacement=False)
        new.append(Unit.mutated(Unit.child_from_crossed(parents, crossing_func), mutator))
        if len(new) >= n: break
    yield from new


def pairing_all_parents(scored_parents:iter, n:int, crossing_func:callable, *,
                        parthenogenesis:float=0, mutator:callable=mutator.all_mutators(),
                        keep_parents:bool=True) -> iter:
    """Yield population of size n, generated from given population
    by pairing parents by two.

    scored_parents -- map unit->score used to build the new pop (the parents)
    n -- size of the returned population
    parthenogenesis -- ratio giving the percentage of chance that an unit use
        clonage instead of seeking for parents. [NOT IMPLEMENTED]
    mutator -- a mutator function. Default is the full set of available mutations.
    keep_parents -- set to False to get only the childs and discard parents
                    from next generation.
    crossing_by_chromosomes -- whether to use the chromosome-based crossing, or the syntaxic one

    """
    pop = list(scored_parents)
    assert pop, "given parent population can't be empty"
    new = list(pop) if keep_parents else []
    if len(new) == n:
        print(f"same_with_childs: population of {len(new)} parents can't reproduce, "
              f"because final population already have {n} individuals")
    assert len(new) <= n
    filler = random.choice(pop)
    while len(new) < n:
        random.shuffle(pop)
        chunks = [iter(pop)] * 2
        for parents in itertools.zip_longest(*chunks, fillvalue=filler):
            new.append(Unit.mutated(Unit.child_from_crossed(parents, crossing_func), mutator))
            if len(new) >= n: break
    yield from new
