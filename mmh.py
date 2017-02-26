"""Implementation of the Meta meta heuristic.


"""


from config import Configuration


class MMH:
    """Meta meta heuristic implementation.

    Provides a high level API to define possible states.
    Produce Configuration objects.

    """

    def __init__(self, case:'Case', pop_size:int, config:Configuration):
        assert config
        self.case = case
        self.pop_size = int(pop_size)
        self.config = config
        self.populations = [tuple(self.config.create(self.pop_size))]
        self.current_step = 1

    @property
    def genalg_functions(self) -> dict:
        return {
            'score': self.config.score,
            'select': self.config.select,
            'mutate': self.config.mutate,
            'reproduce': self.config.reproduce,
            # 'create': self.config.create,
        }

    def run(self):
        while True:
            self.step()


    def step(self):
        """Compute next step"""
        new_pops = []
        for pop in self.populations:
            new = algogen.step(pop, self.case, self.pop_size,
                               **self.genalg_functions,
                               step_number=self.current_step)
            new_pops.append(tuple(new))
        self.populations = tuple(new_pops)
        self.current_step += 1
