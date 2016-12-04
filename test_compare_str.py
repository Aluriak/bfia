

import random
import utils
from scoring import compare_str_c, compare_str_py, UINT8_MAX


def test_compare_str():
    for method in (compare_str_c, compare_str_py):
        assert method('a', 'b') == 1
        assert method('a', 'bc') == abs(ord('a') - ord('b')) + abs(UINT8_MAX)

def test_utils_reversed_dict():
    dct = {1: 2, 3: 4, 5: 6, 7: 2}
    assert utils.reversed_dict(dct, cast=set) == {2: {1, 7}, 4: {3}, 6: {5}}
