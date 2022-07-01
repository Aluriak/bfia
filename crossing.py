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
import collections

from unit import Unit
from utils import grouper, named_functions_interface_decorator


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return selection functions"""
    return {
        'CM': crossby_chromosomes,
        'CP': crossby_pivot,
        'CT': crossby_token,
        'CD': crossby_difference,
        'CR': crossby_random_draw,
        'CC': crossby_consensus,
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
    if smallest_source < len(parents):
        ok_parents = tuple(p for p in parents if len(p.source) > smallest_source)
        if len(ok_parents) <= 1:  # if there is zero or one parent with a not-too-short source code, let's merge everything.
            return ''.join(p.source for p in parents)
        else:  # many parents are long
            return crossby_pivot(ok_parents)
    pivots = sorted(random.sample(range(0, smallest_source), k=nb_pivot)) + [-1]
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


def crossby_consensus(parents: [Unit]) -> str:
    """For each index, takes randomly one of the most represented tokens in the parent.

    It's like crossby_random_draw, but where, if there is more than 2 parents,
    only tokens appearing the most are used.
    In other word, it's a consensus, with random draw to break ties.

    Example: for parents ++++, +-+- and ++--, only child is +++-.

    """
    acc = []
    for tokens in itertools.zip_longest(*(p.source for p in parents), fillvalue=''):
        c = collections.Counter(tokens)
        maxcount = max(c.values())
        acc.append(random.choice([t for t in tokens if c[t] == maxcount]))
    return ''.join(acc)


def crossby_random_draw(parents: [Unit]) -> str:
    """For each index, takes randomly one of the available tokens in the parent.

    Hence, parents +++- and +-++ may yield +++-, ++++, +-+- or +-++.

    """
    per_index_tokens = itertools.zip_longest(*(p.source for p in parents), fillvalue='')
    # inner join is needed so that empty string is not available for random.choice.
    return ''.join(random.choice(''.join(tokens)) for tokens in per_index_tokens)


def crossby_difference(parents: [Unit]) -> str:
    """Keep tokens common between parents, randomly choose when different among parents."""
    return ''.join(random.choice([t for t in tokens if t]) for tokens in itertools.zip_longest(*(p.source for p in parents)))
