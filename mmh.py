"""Implementation of the Meta meta heuristic.


"""


import itertools
from config import Configuration


class MMH:
    """Meta meta heuristic implementation.

    Provides a high level API to define possible states.
    Produce Configuration objects.

    """

    def __init__(self, case:'Case', pop_size:int, config:Configuration,
                 pop_number:int=1, data_handler:callable=None):
        """

        case -- a test case to validate
        pop_size -- size of the population (to remove/change when multipop is handled)
        config -- the Configuration instance describing the metaheuristic
        pop_number -- number of populations to spawn at start
        data_handler -- a callback called at each step with multiple parameters

        data_handler should expects:
        - current step number
        - map unit to score
        - best score
        - worst score
        - currently used config
        - identifier of currently used config

        """
        assert config
        self.case = case
        self.pop_size = int(pop_size)
        self.config_template = config
        self._init_config()
        self.populations = [tuple(self.config.create(self.pop_size)) for _ in range(pop_number)]
        self.current_step = 1
        self.change_config_at = lambda sn: sn % 5 == 0
        self.prompt_at = lambda sn: sn % 5 == 0
        self.data_handler = data_handler
        self.found_solutions = set()  # set of sources that succeed


    def _init_config(self):
        """Initialize the config, based on the template config"""
        self.config = self.config_template.specialize()
        print('MMH CONFIG:\n' + str(self.config))


    def get_specific_genalg_functions(self) -> dict:
        return {
            'score': self.config.score,
            'select': self.config.select,
            'mutate': self.config.mutate,
            'reproduce': self.config.reproduce,
            'cross': self.config.cross,
            # 'create': self.config.create,
        }


    def run(self, step:int=0):
        """Execute 'step' steps, yielding result at each step,
        expecting to receive nothing or a new template config.

        If step is <= 0, will run forever.

        """
        if step > 0:
            _range = range(self.current_step, self.current_step + step + 1)
        else:  # run forever
            _range = itertools.count(self.current_step)
        for step_num in _range:
            self.step()


    def corun(self, step:int=0):
        """Coroutine. Execute 'step' steps, yielding result at each step,
        expecting to receive nothing or a new template config.

        If step is <= 0, will run forever.

        """
        if step > 0:
            _range = range(self.current_step, self.current_step + step + 1)
        else:  # run forever
            _range = itertools.count(self.current_step)
        for step_num in _range:
            self.config_template = (yield self.step()) or self.config_template


    def step(self):
        """Compute next step"""
        self.changed_config = self.change_config_at(self.current_step)
        if self.changed_config:
            self._init_config()

        if self.prompt_at(self.current_step):
            input('?')

        new_pops = []
        for pop in self.populations:
            len_pop = len(pop)
            new_pop, scored_old_pop, winners = self.algogen_call(pop)
            assert len(pop) == len(new_pop)
            assert new_pop != pop
            new_pops.append(new_pop)
            self.found_solutions |= {winner.source for winner in winners}
        self.populations = tuple(new_pops)

        self.current_step += 1

        return self.populations


    def algogen_call(self, pop) -> tuple:
        """Call algogen step function, return the StepResult instance"""
        self.current_config = self.get_specific_genalg_functions()
        return self.config.step(
            pop, self.case, self.pop_size,
            **self.current_config,
            step_number=self.current_step,
            callback_stats=self.callback_stat_adaptator,
        )

    def callback_stat_adaptator(self, **data):
        self.data_handler(**data, **{'step': self.current_step, 'config': self.current_config})



    def create_populations(self, nb:int=1):
        """Add a population initialized with one create method"""
        self.populations.append(self.config.create(self.pop_size))
