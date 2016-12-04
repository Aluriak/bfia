"""Functions for creation of primary population.

"""


import random
import itertools
from functools import partial

import mutator
from unit import Unit


def functions() -> iter:
    """Return reproduction functions"""
    return (
        oriented_diversity,
    )


def oriented_diversity(pop_size:int):
    """Return pop_size new Unit instance. Source code is oriented toward
    movement and memory management, with less brackets and IO

    """
    specs = range(30, 40), range(3, 20), '<<<>>>++--[],..'
    return tuple(Unit.from_spec(*specs) for _ in range(pop_size))
