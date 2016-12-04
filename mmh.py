"""Implementation of the Meta meta heuristic.


"""


import algogen
import mutator
import scoring
import selection
import reproduction
from config import Configuration


class MMH:
    """Meta meta heuristic implementation.

    Provides a high level API to define possible states.
    Produce Configuration objects.

    """

    def __init__(self, case:'Case', pop_size:int, config:Configuration=None):
        self.case = case
        self.pop_size = int(pop_size)
        if config is None:
            config = Configuration(
                score=scoring.functions(),
                mutate=mutator.functions(),
                select=selection.functions(),
                reproduce=reproduction.functions(),
            )
        self.config = config
        self.populations = [self.config.create(self.pop_size)]

    @property
    def genalg_functions(self) -> dict:
        return {
            'score': self.config.score,
            'select': self.config.select,
            'reproduce': self.config.reproduce,
        }

    def run(self):
        while True:
            self.step()


    def step(self):
        """Compute next step"""
        new_pops = []
        for pop in self.populations:
            new = algogen.step(pop, self.case, self.pop_size, **self.genalg_functions)
            new_pops.append(tuple(new))
        self.populations = tuple(new_pops)
