

import random
from scoring import compare_str_c, compare_str_py, UINT8_MAX


def test_compare_str():
    for method in (compare_str_c, compare_str_py):
        assert method('a', 'b') == 1
        assert method('a', 'bc') == abs(ord('a') - ord('b')) + abs(UINT8_MAX)
