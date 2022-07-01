"""Implementation of the scoring functions.

"""

import ctypes
import random
import itertools
from functools import partial
from collections import namedtuple

import interpreter
from utils import named_functions_interface_decorator


INTERPRETER = interpreter.load_interpreter()
MAX_OUT_SIZE = 2048  # maximal size of program output

# Access the string comparison function implemented in C
COMPARE_STR_C_LIB = './compare_str.so'
c_func_compare_str = ctypes.cdll.LoadLibrary(COMPARE_STR_C_LIB).distance
c_func_compare_str.restype = ctypes.c_uint64  # specify output type

RunResult = namedtuple('RunResult', 'score expected found')
SCORE_BASE = 10_000
SCORE_MINIMAL = 0  # any score below this threshold will be set to this threshold

UINT8_MAX = 255  # comes from C stdint.h


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return scoring functions.

    A scoring function maps a unit and a test with a score.

    """
    return {
        'IOC': io_comparison,
        'IOCB': io_comparison_with_bonus,
        'IOCM': io_comparison_with_size_malus,
        'IOCBM': io_comparison_with_bonus_and_size_malus,
    }

def default_functions() -> tuple:
    """Return default scoring functions"""
    return named_functions.as_tuple() + anonymous_functions()

def anonymous_functions() -> tuple:
    """Return scoring functions that have no name"""
    return ()


def io_comparison_with_bonus(unit, test, interpreter=INTERPRETER, bonus=SCORE_BASE) -> float:
    """Like io_comparison, but giving a bonus of score if found the
    expected result, so that finding the correct results ensure a large.

    """
    score, expected, found = io_comparison(unit, test, interpreter)
    if bonus and found == expected:
        score += bonus  # scores of successful units belong to another scoring level.
    return RunResult(max(SCORE_MINIMAL, int(score)), expected, found)


def io_comparison_with_size_malus(unit, test, interpreter=INTERPRETER, malus=1) -> float:
    """Like io_comparison, but giving a malus of malus*source code size.

    """
    score, expected, found = io_comparison(unit, test, interpreter)
    score -= len(unit.source) * malus
    return RunResult(max(SCORE_MINIMAL, int(score)), expected, found)


def io_comparison(unit, test, interpreter=INTERPRETER) -> float:
    stdin, expected = test
    # compute and return score
    found = interpreter.inline(unit.source, stdin, max_output_size=MAX_OUT_SIZE)
    # print('UOGHDP:', interpreter.inline.cache_info())
    assert len(expected) < MAX_OUT_SIZE
    score = SCORE_BASE - compare_str(expected, found)
    return RunResult(max(SCORE_MINIMAL, int(score)), expected, found)


def io_comparison_with_bonus_and_size_malus(unit, test, interpreter=INTERPRETER, bonus=SCORE_BASE, malus=1) -> float:
    """Like io_comparison, but giving a malus of malus*source code size, and a bonus for exact answers.

    """
    score, expected, found = io_comparison(unit, test, interpreter)
    if bonus and found == expected:
        score += bonus  # scores of successful units belong to another scoring level.
    score -= len(unit.source) * malus
    return RunResult(max(SCORE_MINIMAL, int(score)), expected, found)


def compare_str_c(one, two) -> int:
    """Wrapper around C function implementing string comparison"""
    one, two = one.encode(), two.encode()
    return c_func_compare_str(one, two, len(one), len(two), UINT8_MAX, 1, 0)

def compare_str_py(one, two, length_penalty:int=UINT8_MAX) -> int:
    """Implementation of the string comparator in python"""
    one, two = one.encode(), two.encode()
    return sum(length_penalty if None in (a, b) else abs(a - b)
               for a, b in itertools.zip_longest(one, two))


# choose the implementation exposed to the outside
compare_str = compare_str_c
# compare_str = compare_str_py
