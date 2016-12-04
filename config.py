"""

"""


import random
from functools import partial
from collections import namedtuple

import mutator
import scoring
import creation
import selection
import reproduction


class Configuration:
    """A Configuration object is a choice of functions for each role
    in the genetic algorithm.

    It is basically a group of callables that will be used
    by a genetic algorithm.

    """
    def __init__(self, score:callable=None, select:callable=None,
                 mutate:callable=None, reproduce:callable=None,
                 create:callable=None):
        if score is None:
            score = scoring.functions()
        if select is None:
            select = selection.functions()
        if mutate is None:
            mutate = mutator.functions()
        if reproduce is None:
            reproduce = reproduction.functions()
        if create is None:
            create = creation.functions()
        self._score = score if callable(score) else tuple(score)
        self._select = select if callable(select) else tuple(select)
        self._mutate = mutate if callable(mutate) else tuple(mutate)
        self._reproduce = reproduce if callable(reproduce) else tuple(reproduce)
        self._create = create if callable(create) else tuple(create)

    @property
    def score(self) -> callable:
        return self._score if callable(self._score) else random.choice(self._score)

    @property
    def select(self) -> callable:
        return self._select if callable(self._select) else random.choice(self._select)

    @property
    def mutate(self) -> callable:
        return self._mutate if callable(self._mutate) else random.choice(self._mutate)

    @property
    def reproduce(self) -> callable:
        return self._reproduce if callable(self._reproduce) else random.choice(self._reproduce)

    @property
    def create(self) -> callable:
        return self._create if callable(self._create) else random.choice(self._create)


    @staticmethod
    def recipe_showing_elistism():
        """Reproduction of the initial configuration that shows
        the side-effect of elitism

        """
        return Configuration(
            score=scoring.io_comparison,
            select=partial(selection.ranking_slices, pattern=[(0, 40)])
        )

    @staticmethod
    def recipe_best_solution_so_far():
        """Reproduction of the best known configuration.

        """
        return Configuration(
            score=scoring.io_comparison,
            select=partial(selection.poolling, pool_size=10, selection_size=0.4)
        )
