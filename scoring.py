"""Implementation of the scoring

"""

import ctypes
import random
import itertools


# Access the string comparison function implemented in C
COMPARE_STR_C_LIB = './compare_str.so'
c_func_compare_str = ctypes.cdll.LoadLibrary(COMPARE_STR_C_LIB).distance
c_func_compare_str.restype = ctypes.c_uint64  # specify output type

UINT8_MAX = 255  # comes from C stdint.h


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
