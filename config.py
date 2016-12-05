"""

"""


import random
import functools
from functools import partial
from collections import namedtuple

import utils
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
        score = score or scoring.default_functions()
        select = select or selection.default_functions()
        mutate = mutate or mutator.default_functions()
        reproduce = reproduce or reproduction.default_functions()
        create = create or creation.default_functions()
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

    def __str__(self):
        out = ''
        for funcs, module, name in ((self._score, scoring, 'SCORE'),
                                    (self._select, selection, 'SELECT'),
                                    (self._mutate, mutator, 'MUTATE'),
                                    (self._reproduce, reproduction, 'REPRODUCE'),
                                    (self._create, creation, 'CREATE')):
            print(funcs, module, name)
            if not callable(funcs) and len(funcs) == 1:
                funcs = funcs[0]
            if callable(funcs):
                code = utils.key_of(funcs, module.named_functions(), '')
                out += '{}: {} {}\n'.format(name, utils.pretty_func(funcs), code)
            else:
                out += '{}:\n'.format(name)
                for func in funcs:
                    code = utils.key_of(func, module.named_functions(), '')
                    out += '\t{} {}\n'.format(utils.pretty_func(func), code)
        return out



    @staticmethod
    def from_codes(score:str=None, select:str=None, mutate:str=None,
                   reproduce:str=None, create:str=None):
        """Create configuration from given codes of named functions.

        if a code is None, the default will be used

        """
        score = (scoring.default_functions() if score is None
                 else scoring.named_functions(score))
        select = (selection.default_functions() if select is None
                  else selection.named_functions(select))
        mutate = (mutator.default_functions() if mutate is None
                  else mutator.named_functions(mutate))
        create = (creation.default_functions() if create is None
                  else creation.named_functions(create))
        reproduce = (reproduction.default_functions() if reproduce is None
                     else reproduction.named_functions(reproduce))
        return Configuration(score=score, select=select, mutate=mutate,
                             reproduce=reproduce, create=create)



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
