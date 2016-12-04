

import random
from case import Case


def test_case_basic_api():

    # hi !
    c = Case('', 'hi !')
    assert tuple(c) == ('', 'hi !')

    # hello <input> !
    c = Case((lambda: ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))),
             'hello {stdin} !')
    stdin, stdout = c
    assert stdout.startswith('hello ')
    assert stdin == stdout[len('hello '):-2]

    # hello <tupni> !
    c = Case((lambda: ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))),
             (lambda stdin: 'hello {} !'.format(''.join(reversed(stdin)))))
    stdin, stdout = c
    assert stdout.startswith('hello ')
    assert stdin == ''.join(reversed(stdout[len('hello '):-2]))
