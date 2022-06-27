

from scoring import compare_str_c, compare_str_py, UINT8_MAX


def test_compare_str_c():
    assert compare_str_c('a', 'b') == 1
    assert compare_str_c('a', 'bc') == abs(ord('a') - ord('b')) + abs(UINT8_MAX)

def test_compare_str_py():
    assert compare_str_py('a', 'b') == 1
    assert compare_str_py('a', 'bc') == abs(ord('a') - ord('b')) + abs(UINT8_MAX)
