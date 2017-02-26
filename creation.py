"""Functions for creation of primary population.

All these expose the following parameters:

    pop_size -- size of the population to create

"""


import random
import itertools
from functools import partial

import mutator
from unit import Unit
from utils import named_functions_interface_decorator


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return creation functions"""
    return {
        'MOD': memory_oriented_diversity,
        'INP': stdin_printer,
        'AME': all_methods_equally,
    }
    return funcs

def default_functions() -> tuple:
    """Return default creation functions"""
    return (
        memory_oriented_diversity,
    )

def anonymous_functions() -> tuple:
    """Return creation functions that have no name"""
    return ()


def stdin_printer(pop_size:int) -> tuple:
    """Return pop_size new Unit instance. Source code is oriented toward
    printing of stdin with workarounds.

    """
    source = '+++.>,[.,]>+++.'
    chrom_size = 10
    return tuple(Unit(source, chrom_size) for _ in range(pop_size))


def memory_oriented_diversity(pop_size:int) -> tuple:
    """Return pop_size new Unit instance. Source code is oriented toward
    movement and memory management, with less brackets and IO

    """
    specs = range(30, 40), range(3, 20), '<<<>>>++--[],..'
    return tuple(Unit.from_spec(*specs) for _ in range(pop_size))


def all_methods_equally(pop_size:int) -> tuple:
    """Return pop_size new Unit instance, using all the others
    creation methods.

    """
    methods = frozenset(
        method
        for method in set(named_functions().values()) | set(anonymous_functions())
        if method is not all_methods_equally
    )
    unit_per_method = pop_size // len(methods)
    remaining = pop_size % len(methods)
    for method in methods:
        yield from method(unit_per_method)
    # choose one for each remaining unit to produce
    for _ in range(remaining):
        yield from random.choice(methods)(1)
