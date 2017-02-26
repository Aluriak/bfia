"""

"""

import random
import itertools

import utils
from interpreter import BF_STATEMENTS


class Unit:
    MUTATION_RATE = 0.05
    ADDITIONAL_MUTATION_RATE = 0.1

    def __init__(self, bf_source:str, chrom_size:int=8):
        self.source = str(bf_source)
        self.chrom_size = chrom_size

    def __iter__(self):
        """Iteration over its chromosomes, allowing creation of childs"""
        return iter(utils.grouper(self.source, self.chrom_size, '\0'))

    def mutate(self, mutator:callable) -> 'self':
        """Modify the source code in a random way"""
        if random.random() < Unit.MUTATION_RATE:
            mutator(self)
        while random.random() < Unit.ADDITIONAL_MUTATION_RATE:
            mutator(self)  # one more time !
        return self

    @staticmethod
    def from_spec(source_size:int, chrom_size:int,
                  weighted_bf_statements:str=BF_STATEMENTS) -> object:
        """Return a new Unit, based on given spec. Could be range"""
        if isinstance(source_size, range):
            size = random.choice(tuple(source_size))
        else:
            size = source_size
        if isinstance(chrom_size, range):
            chrom = random.choice(tuple(chrom_size))
        else:
            chrom = chrom_size
        # source = itertools.islice(itertools.cycle('+.>'), 0, size)
        source = (random.choice(weighted_bf_statements) for _ in range(size))
        return Unit(''.join(source), int(chrom))


    @staticmethod
    def child_from_plain_crossed(parents:iter, chrom_size:int=None):
        """Return a child produced from parents."""
        return Unit(
            bf_source=''.join(
                random.choice(chars)
                for chars in itertools.zip_longest(*[iter(parent.source) for parent in parents], fillvalue='')
            ),
            chrom_size=chrom_size or random.choice([parent.chrom_size for parent in parents])
        )

    @staticmethod
    def child_from_crossed(parents:iter, chrom_size:int=None):
        """Return a child produced from parents"""
        assert len(parents) == 2
        cross = random.randrange(1, min((len(p.source) for p in parents)) - 1)
        return Unit(
            bf_source=parents[0].source[:cross] + parents[1].source[cross:],
            chrom_size=chrom_size or random.choice([parent.chrom_size for parent in parents])
        )

    @staticmethod
    def child_from_fragmented(parents:iter, chrom_size:int=None):
        return Unit(
            bf_source=''.join(
                ''.join(random.choice(chroms))
                for chroms in itertools.zip_longest(*[iter(parent) for parent in parents], fillvalue='')
            ),
            chrom_size=chrom_size or random.choice([parent.chrom_size for parent in parents])
        )

    @staticmethod
    def mutated(unit, mutators:iter) -> 'unit':
        new = Unit(unit.source, unit.chrom_size)
        new.mutate(mutators)
        return new


def test_Unit():
    assert tuple(Unit('abcde', 2)) == (('a', 'b'), ('c', 'd'), ('e', '\0'))

