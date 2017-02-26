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
        self.config_template = config
        self._init_config()
        self.populations = [tuple(self.config.create(self.pop_size))]
        self.current_step = 1


    def _init_config(self):
        """Initialize the config, based on the template config"""
        self.config = self.config_template.specialize()
        print('MMH CONFIG:\n' + str(self.config))


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
        self.populations = tuple(
            tuple(self.algogen_call(pop))
            for pop in self.populations
        )
        self.current_step += 1


    def algogen_call(self, pop):
        """Call algogen step function"""
        return self.config.step(
            pop, self.case, self.pop_size,
            **self.genalg_functions,
            step_number=self.current_step
        )

