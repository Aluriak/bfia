"""

"""

import random
import itertools

import utils
from interpreter import BF_STATEMENTS


class Unit:

    def __init__(self, bf_source:str, chrom_size:int=8, mutation_rate:float=0.05,
                 additional_mutation_rate:float=0.1):
        self.source = str(bf_source)
        self.chrom_size = chrom_size
        self.mutation_rate = float(mutation_rate)
        self.additional_mutation_rate = float(additional_mutation_rate)
        assert 0. <= self.mutation_rate <= 1.
        assert 0. <= self.additional_mutation_rate <= 1.


    def __iter__(self):
        """Iteration over its chromosomes, allowing creation of childs"""
        return iter(utils.grouper(self.source, self.chrom_size, '\0'))


    def mutate(self, mutator:callable) -> 'self':
        """Maybe modify the source code in a random way"""
        mutator(self)
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
    def child_from_crossed(parents:iter, crossing_func: callable, chrom_size:int=None):
        """Return a child produced from parents"""
        source = crossing_func(parents)
        if not source:
            raise ValueError(f"Crossing function {crossing_func} returned an empty source for given parents {parents} of sources: {' and '.join(p.source for p in parents)}.")
        return Unit(
            bf_source=crossing_func(parents),
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

