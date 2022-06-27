import pytest
import utils


def test_choices():
    c = utils.choices([1, 2, 3], k=2)
    print(c)
    assert len(c) == 2
    assert len(set(c)) == 2, "no replacement: should not draw the same twice"


def test_choices_with_weights():
    c = utils.choices([1, 2, 3], k=2, weights=[10, 1, 1])
    print(c)
    assert len(c) == 2
    assert len(set(c)) == 2, "no replacement: should not draw the same twice"


def test_choices_with_weights():
    c = utils.choices([1, 2, 3], k=2, weights=[10, 1, 1])
    print(c)
    assert len(c) == 2
    assert len(set(c)) == 2, "no replacement: should not draw the same twice"


def test_make_named_functions():
    d = utils.make_named_functions('A', print, {'end': {'E':'\n', 'T': '\t'}, 'sep': {'T': '\t', 'S': ' '}, 'flush': 'F'})
    print(d)
    assert set(d) == {'AET', 'AES', 'ATT', 'ATS', 'AETF', 'AESF', 'ATTF', 'ATSF'}
    assert d['AETF'].keywords == {'end': '\n', 'sep': '\t', 'flush': True}
    assert d['AET'].keywords == {'end': '\n', 'sep': '\t', 'flush': False}

    with pytest.raises(ValueError):
        utils.make_named_functions('A', print, {'end': ''})  # invalid value: cannot handle a value of empty string for keywords

    with pytest.raises(ValueError):
        utils.make_named_functions('A', print, {'end': 'A', 'sep': 'A'})  # invalid value: there is multiple functions for 'AA' key code


def test_utils_reversed_dict():
    dct = {1: 2, 3: 4, 5: 6, 7: 2}
    assert utils.reversed_dict(dct, cast=set) == {2: {1, 7}, 4: {3}, 6: {5}}
