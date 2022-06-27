"""

"""


import random
import functools
from functools import partial
from collections import namedtuple

import utils
import mutator
import scoring
import stepping
import creation
import selection
import reproduction


class Configuration:
    """A Configuration object is a set of functions for each role
    in the genetic algorithm.

    It is basically a group of callables that will be used
    by a genetic algorithm.

    In other word, a Configuration instance yield different functions
    at each access to the same attribute (score, select,…), because
    choosing them randomly in the set given to the constructor.

    It provides the specialize method, that return a new configuration
    with only one choice of function, allowing one to generate a configuration

    """
    def __init__(self, score:callable=None, select:callable=None,
                 mutate:callable=None, reproduce:callable=None,
                 create:callable=None, step:callable=None):
        score = score or scoring.default_functions()
        select = select or selection.default_functions()
        mutate = mutate or mutator.default_functions()
        reproduce = reproduce or reproduction.default_functions()
        create = create or creation.default_functions()
        step = step or stepping.default_functions()
        self._score = (score,) if callable(score) else tuple(score)
        self._select = (select,) if callable(select) else tuple(select)
        self._mutate = (mutate,) if callable(mutate) else tuple(mutate)
        self._reproduce = (reproduce,) if callable(reproduce) else tuple(reproduce)
        self._create = (create,) if callable(create) else tuple(create)
        self._step = (step,) if callable(step) else tuple(step)


    def specialize(self) -> 'Configuration':
        """Return a new Configuration where all sets of functions are fixed to a
        unique function.

        This is a great way to get a specific Configuration, in order to
        get the same GA implementation for multiple iterations or simulations.

        Note that functions themselves are not modified ; for instance the
        mutate method will not be fixed to a specific mutation, as the mutate
        methods sent to the Configuration object usually are functions calling
        randomly one among many mutators.

        """
        return Configuration(score=self.score, select=self.select,
                             mutate=self.mutate, reproduce=self.reproduce,
                             create=self.create, step=self.step)

    @property
    def score(self) -> callable:
        return random.choice(self._score)

    @property
    def select(self) -> callable:
        return random.choice(self._select)

    @property
    def mutate(self) -> callable:
        return random.choice(self._mutate)

    @property
    def reproduce(self) -> callable:
        return random.choice(self._reproduce)

    @property
    def create(self) -> callable:
        return random.choice(self._create)

    @property
    def step(self) -> callable:
        return random.choice(self._step)

    def __str__(self):
        out = ''
        for funcs, module, name in ((self._score, scoring, 'SCORE'),
                                    (self._select, selection, 'SELECT'),
                                    (self._mutate, mutator, 'MUTATE'),
                                    (self._reproduce, reproduction, 'REPRODUCE'),
                                    (self._create, creation, 'CREATE'),
                                    (self._step, stepping, 'STEP')):
            out += '{}:\n'.format(name)
            for func in funcs:
                code = utils.key_of(func, module.named_functions(), '')
                out += '\t{} {}\n'.format(utils.pretty_func(func), code)
        return out


    @staticmethod
    def from_codes(score:str=None, select:str=None, mutate:str=None,
                   reproduce:str=None, create:str=None, step:str=None):
        """Create configuration from given codes of named functions.

        Code can be either None, a valid codename, or an iterable of
        valid codename.
        if a code is None, the default will be used.

        """
        kwargs = {}
        for param, value, module in (('score', score, scoring),
                                     ('select', select, selection),
                                     ('mutate', mutate, mutator),
                                     ('reproduce', reproduce, reproduction),
                                     ('create', create, creation),
                                     ('step', step, stepping)):
            if isinstance(value, str):  # it's a code name
                kwargs[param] = module.named_functions(value)
            elif value is None:  # user wants default
                kwargs[param] = module.default_functions()
            else:  # it's an iterable of code name
                kwargs[param] = tuple(module.named_functions(name) for name in value)
        return Configuration(**kwargs)


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
