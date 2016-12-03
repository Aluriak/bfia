

import ctypes
from functools import partial


BFIA_C_LIB = './bfinterp.so'
BF_STATEMENTS = '<>+-[],.'


def load_interpreter():
    ret = ctypes.cdll.LoadLibrary(BFIA_C_LIB)
    ret.inline = partial(interprete, interpreter=ret)
    return ret


def interprete(source:str, input:str="", *, interpreter:ctypes.cdll=None,
               max_output_size:int=2**16) -> str:
    output = ('\0' * max_output_size).encode()
    # print(source)
    interpreter.interpret_bf(source.encode(), input.encode(), output, max_output_size)
    output = output.decode(encoding="ISO-8859-1")  # use ascii, because brainfuck
    return output.rstrip('\0')


def test_interprete():
    interp = load_interpreter()
    assert interp.inline("++++>,<[->+<]>.", 'a')  == 'e'
    # following tests are here to verify a particular limit case
    assert interp.inline(']') == ''
    assert interp.inline('[') == ''
    assert interp.inline('[]') == ''
    assert interp.inline('+[]') == ''
    assert interp.inline('+]') == ''
    assert interp.inline('+[[,,]-]') == ''


if __name__ == "__main__":
    interp = load_interpreter()

    # print('DEBUG TEST')
    # SOURCE = ''

    # print(interp.inline(SOURCE, ''))

    # exit()


    with open('sources/beer.bf') as fd:
        source = ''.join(line.strip() for line in fd if line.strip())
    print(source)
    print(interp.inline(source, 'a'))
