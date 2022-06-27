"""Implementation of crossing functions.

A crossing function maps two (or more) brainfuck sources (the parents)
to a source (the child).

Input of these functions are the following:

    parents -- an iterable of Unit instances.

As output, crossing functions return a single string of brainfuck source code.

"""

import utils
import random
import itertools

from unit import Unit
from utils import grouper, named_functions_interface_decorator


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return selection functions"""
    return {
        'CC': crossby_chromosomes,
        'CP': crossby_pivot,
        'CT': crossby_token,
        'CD': crossby_difference,
        # 'CU': crossby_output_unit,
    }

def default_functions() -> tuple:
    """Return default selection functions"""
    return named_functions.as_tuple()


def crossby_chromosomes(parents: [Unit]) -> str:
    """Use parent chromosome size. Takes chromosom_size tokens from the first parent,
    then the next, and loop until first parent is exhausted.
    """
    parent_chroms = tuple(
        tuple(grouper(parent.source, n=parent.chrom_size, fillvalue=' '))
        for parent in parents
    )
    childparts = []
    for idx, chroms in zip(itertools.count(0), itertools.cycle(parent_chroms)):
        if idx < len(chroms):
            childparts.append(''.join(chroms[idx]))
        else:
            break
    return ''.join(childparts)

def crossby_pivot(parents: [Unit]) -> str:
    """Choose a random index in the smallest source code of parents.
    then the next, and loop until first parent is exhausted.
    """
    nb_pivot = len(parents) - 1
    smallest_source = min(len(p.source) for p in parents)
    pivots = [0] + sorted(random.sample(range(1, smallest_source), k=nb_pivot))
    childparts = []
    prev_pivot = 0
    for parent, pivot in zip(parents, pivots):
        childparts.append(parent.source[prev_pivot:pivot])
        prev_pivot = pivot
    return ''.join(childparts)


def crossby_token(parents: [Unit]) -> str:
    """Take the first repeated tokens from first parent, then second, and loop until a parent is exhausted.
    This is like intertweaning parent's sources, but repeated tokens are taken together.

    So, with parents '++++>++' and '+--+--+', we got child '++++ -- ++ --'
    """
    def token_groups(source: str) -> [(str, int)]:
        prev = source[0]
        count = 0
        for char in source:
            if char == prev:
                count += 1
            else:
                yield prev, count
                prev = char
                count = 1
        if count:
            yield char, count
    parent_groups = tuple(tuple(token_groups(parent.source)) for parent in parents)

    childparts = []
    for idx, groups in zip(itertools.count(0), itertools.cycle(parent_groups)):
        if idx < len(groups):
            childparts.append(''.join(groups[idx][0]*groups[idx][1]))
        else:
            break
    return ''.join(childparts)


def crossby_output_unit(parents: [Unit]) -> str:
    ...


def crossby_difference(parents: [Unit]) -> str:
    """Keep tokens common between parents, randomly choose when different among parents."""
    return ''.join(random.choice([t for t in tokens if t]) for tokens in itertools.zip_longest(*(p.source for p in parents)))
