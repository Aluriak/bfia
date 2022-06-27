

import pytest
from interpreter import load_interpreter


@pytest.fixture
def interpret():
    return load_interpreter().inline


def test_basic_ops(interpret):
    for x in range(2, 127):
        assert ord(interpret(',.', input=chr(x))) == x
        assert ord(interpret(',+.', input=chr(x))) == x + 1
        assert ord(interpret(',-.', input=chr(x))) == x - 1


def test_basic_loop(interpret):
    for x in range(1, 127):
        assert ord(interpret(',[-]+.', input=chr(x))) == 1
        # equivalent using the SET_ZERO language extension
        assert ord(interpret(',0+.', input=chr(x))) == 1


def test_basic_move(interpret):
    assert ord(interpret(',>+.', input=chr(42))) == 1
