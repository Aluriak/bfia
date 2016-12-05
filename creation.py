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
def named_functions(name:str=None) -> dict:
    """Return creation functions"""
    return {
        'MOD': memory_oriented_diversity,
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


def memory_oriented_diversity(pop_size:int):
    """Return pop_size new Unit instance. Source code is oriented toward
    movement and memory management, with less brackets and IO

    """
    specs = range(30, 40), range(3, 20), '<<<>>>++--[],..'
    return tuple(Unit.from_spec(*specs) for _ in range(pop_size))
