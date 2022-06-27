"""Contains all mutation functions.

See mutator.py for usage and interface.

"""

import re
import itertools
from random import choice, shuffle, randint, randrange, random
from collections import defaultdict

from interpreter import BF_STATEMENTS


MAX_INDEL_SIZE = 10


def loop_transposition(unit):
    """Change a loop of position in the code"""
    try:
        start, stop = choice(tuple(_loops(unit.source)))
        unit.source = _transpose_string(unit.source, start, stop)
    except IndexError:  # no loops in code
        transition(unit)  # call a normal transition


def output_interleaving(unit):
    reg = re.compile('\.\.')
    matches = tuple(match.start() for match in reg.finditer(unit.source))
    if matches:
        chars_pos = choice(matches)
        src = unit.source
        unit.source = src[:chars_pos] + choice(BF_STATEMENTS) + src[chars_pos:]
    else:
        io_transposition(unit)


def output_separation(unit):
    if '..' in unit.source:
        chars_pos = unit.source.find('..')
        src = unit.source
        unit.source = src[:chars_pos] + choice('+-<>') + src[chars_pos:]
    else:
        io_transposition(unit)


def io_change(unit):
    iochars = ['.', ',']
    shuffle(iochars)
    chars_pos = _character_positions(unit.source)[iochars[0]]
    if chars_pos:
        index = choice(chars_pos)
        unit.source = unit.source[:index] + iochars[1] + (unit.source[index+1:] if index < len(unit.source) else '')
    else:  # chars_pos is empty
        transposition(unit)


def io_transposition(unit):
    chars_pos = _character_positions(unit.source)
    try:
        indexes = choice(chars_pos['.']), choice(chars_pos[','])
    except IndexError:  # at least once is not present
        return transposition(unit)
    index1, index2 = sorted(indexes)
    unit.source = ''.join((
        unit.source[:index1],
        unit.source[index2],
        unit.source[index1+1:index2],
        unit.source[index1],
        unit.source[index2+1:],
    ))


def group_transition(unit):
    MAPS = {'+': '-', '>': '<', '[': ']', '.': ','}
    MAPS.update({v: k for k, v in MAPS.items()})
    PROB = 0.01
    unit.source = ''.join(itertools.chain.from_iterable(
        nb * (MAPS.get(char, char) if random() < PROB else char)
        for char, nb in _grouped_characters(unit.source)
    ))


def number_complementary(unit, max_int:int=128, likelihood:float=0.5):
    src = ''
    for char, nb in _grouped_characters(unit.source):
        if char == '+' and random() < likelihood:  # replace by minus to achieve the same number
            src += (max_int - nb) * '-'
        elif char == '-' and random() < likelihood:  # replace by plus to achive the same number
            src += (max_int - nb) * '+'
        else:  # regular behavior
            src += nb * char
    unit.source = src


def transition(unit):
    index = randrange(0, len(unit.source))
    unit.source = unit.source[:index] + choice(BF_STATEMENTS) + unit.source[index+1:]


def addition(unit):
    index = randrange(0, len(unit.source))
    statement = choice(BF_STATEMENTS)
    insert = statement * randint(1, MAX_INDEL_SIZE)
    unit.source = unit.source[:index] + insert + unit.source[index:]


def single_addition(unit):
    index = randrange(0, len(unit.source))
    statement = choice(BF_STATEMENTS)
    unit.source = unit.source[:index] + statement + unit.source[index:]


def single_deletion(unit):
    if len(unit.source) > 1:
        index = randrange(0, len(unit.source))
        unit.source = unit.source[:index] + unit.source[index+1:]
    else:
        single_addition(unit)

def deletion(unit):
    size = randint(1, MAX_INDEL_SIZE)
    if len(unit.source) > size:
        index = randint(0, len(unit.source) - size)
        unit.source = unit.source[:index] + unit.source[index+size:]
    else:
        single_deletion(unit)


def transposition(unit):
    size = randint(1, MAX_INDEL_SIZE)
    if len(unit.source) > size + 1:
        start = randrange(0, len(unit.source) - size)
        unit.source = _transpose_string(unit.source, start, start + size)
    else:
        single_deletion(unit)


def reversion(unit):
    size = randint(2, MAX_INDEL_SIZE)
    if len(unit.source) > size + 1:
        start = randrange(0, len(unit.source) - size)
        unit.source = unit.source[:start] + ''.join(reversed(unit.source[start:start+size])) + unit.source[start+size:]
    else:
        single_deletion(unit)


def null_mutator(unit):
    """Do nothing."""
    pass


def _transpose_string(string:str, start:int, stop:int) -> str:
    """Return a new string, where the substring string[start:stop+1]
    have been moved to another place in the the string. (without loss)

    """
    assert stop < len(string), "end bound is larger than given string"
    assert start < stop, "end bound is larger than start bound"

    insert_pos = randrange(0, len(string) - (stop - start) - 1)
    moved = string[start:stop+1]
    string = string[:start] + string[stop+1:]
    string = string[:insert_pos] + moved + string[insert_pos:]
    return string


def _character_positions(string:str) -> dict:
    """Return dict {character: {positions in given string}}"""
    out = defaultdict(list)
    for idx, char in enumerate(string):
        out[char].append(idx)
    return out


def _loops(source_code:str) -> iter:
    """Yield pairs (position opening bracket, position matching bracket)

    >>> dict(_loops('[][][[]]'))
    {0: 1, 2:3, 4:7, 5:6}

    """
    stack = []
    for idx, char in enumerate(source_code):
        if char == '[':
            stack.append(idx)
        elif char == ']' and stack:
            yield stack.pop(), idx


def _grouped_characters(string:str) -> iter:
    """Yield pairs (char, number of consecutive chars)"""
    yield from ((c, len(tuple(s))) for c, s in itertools.groupby(string))
