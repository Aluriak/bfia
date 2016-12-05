"""Implementation of the scoring functions.

"""

import ctypes
import random
import itertools
from collections import namedtuple

import interpreter
from utils import named_functions_interface_decorator


INTERPRETER = interpreter.load_interpreter()
MAX_OUT_SIZE = 32  # maximal size of program output

# Access the string comparison function implemented in C
COMPARE_STR_C_LIB = './compare_str.so'
c_func_compare_str = ctypes.cdll.LoadLibrary(COMPARE_STR_C_LIB).distance
c_func_compare_str.restype = ctypes.c_uint64  # specify output type

RunResult = namedtuple('RunResult', 'score expected found')

UINT8_MAX = 255  # comes from C stdint.h


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return scoring functions.

    A scoring function maps a unit and a test with a score.

    """
    return {
        'IOC': io_comparison,
    }

def default_functions() -> tuple:
    """Return default scoring functions"""
    return (
        io_comparison,
    )

def anonymous_functions() -> tuple:
    """Return scoring functions that have no name"""
    return ()


def io_comparison(unit, test) -> float:
    stdin, expected = test
    # compute and return score
    found = INTERPRETER.inline(unit.source, stdin, max_output_size=MAX_OUT_SIZE)
    assert len(expected) < MAX_OUT_SIZE
    score = 10000 - compare_str(expected, found)
    return RunResult(score, expected, found)


def compare_str_c(one, two) -> int:
    """Wrapper around C function implementing string comparison"""
    one, two = one.encode(), two.encode()
    return c_func_compare_str(one, two, len(one), len(two))

def compare_str_py(one, two) -> int:
    """Implementation of the string comparator in python"""
    one, two = one.encode(), two.encode()
    return sum(UINT8_MAX if None in (a, b) else abs(a - b)
               for a, b in itertools.zip_longest(one, two))


# choose the implementation exposed to the outside
compare_str = compare_str_c
# compare_str = compare_str_py
