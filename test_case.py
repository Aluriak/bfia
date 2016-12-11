

import random
from case import Case


def build_random_id():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))


def test_case_basic_api():

    # hi !
    c = Case('', 'hi !')
    assert tuple(c) == ('', 'hi !')
    assert not c.callable_input
    assert not c.callable_output

    # hello <input> !
    c = Case(build_random_id, 'hello {stdin} !')
    assert not c.callable_input
    assert not c.callable_output
    stdin, stdout = c
    assert stdout.startswith('hello ')
    assert stdin == stdout[len('hello '):-2]

    # hello <tupni> !
    c = Case(build_random_id,
             (lambda stdin: 'hello {} !'.format(''.join(reversed(stdin)))))
    assert c.callable_input
    assert c.callable_output
    stdin, stdout = c
    assert stdout.startswith('hello ')
    assert stdin == ''.join(reversed(stdout[len('hello '):-2]))
