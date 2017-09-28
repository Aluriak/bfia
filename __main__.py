
import random

from mmh import MMH
from case import Case
from config import Configuration
from statistics import Saver, ScoreSaver


# simulation
POP_SIZE = 400


def run_interpreter_testing(_:Saver):
    """Just show that given code do not works except in a few cases
    for diving by 2"""
    def test_interpreter(source, stdin=''):
        from interpreter import load_interpreter
        interp = load_interpreter()
        return interp.inline(source, input=stdin)


    test = lambda x: ord(test_interpreter(
        '++++++-++++++++++++++++++[+++++<<+++++++++++++++++<+++++++.',
        chr(x)
    ))
    for x in range(64, 128):
        found, expected = test(x), x // 2
        print(x, found, expected, 'OK' if found == expected else '')


def run_simple_cases(saver:Saver):
    letters = tuple(chr(c) for c in range(32, 128))
    numbers = tuple(chr(c) for c in range(64, 128))
    CASES = {
        'hi !': Case('', 'hi !'),
        # 'hi {input} !': Case(lambda: random.choice(letters), 'hi {stdin} !'),
        # 'hello world': Case('', 'hello, world!'),
        # 'greetings': Case(lambda: random.choice(letters), 'hello {stdin} !'),
        # 'division by 2': Case(lambda: random.choice(numbers), lambda x: chr(ord(x) // 2)),
    }
    # build the motif
    config = Configuration.recipe_best_solution_so_far()
    config = Configuration()
    for case_name, case in CASES.items():
        print('#'*80)
        print('#', case_name)
        # current_step = 0
        # pop = config.create(POP_SIZE)
        # while True:
            # current_step += 1
            # pop, scored_pop = config.step(
                # pop, case, POP_SIZE,
                # score=config.score,
                # select=config.select,
                # mutate=config.mutate,
                # reproduce=config.reproduce,
                # step_number=current_step
            # )
            # saver.save([current_step, max(s.score for s in scored_pop.values())])
        mmh = MMH(case, pop_size=POP_SIZE, config=config)
        for pops in mmh.corun():
            assert len(pops) == 1  # currently multipop is not implemented
            pop = pops[0]
            assert len(pop) == POP_SIZE
            # print(pop)
            # scores = tuple(v.score for v in pop.values())
            # saver.save([mmh.current_step, max(scores)])
        print('#'*80)
        print()


MOTIF = r"""
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////\\\\\/////
"""



def run_test_motif(saver:Saver):
    case = Case('/\\\n', MOTIF)

    config = Configuration.from_codes(score='IOC', select='PLDD', mutate='ALL',
                                      reproduce='SCP', create='AME', step='DIV',
                                     )# manipulator='DAC')
    config = Configuration()
    # config = Configuration.recipe_best_solution_so_far()
    mmh = MMH(case, pop_size=POP_SIZE, config=config)
    for pops in mmh.corun():
        assert len(pops) == 1  # currently multipop is not implemented
        pop = pops[0]
        scores = tuple(v.score for v in pop.values())
        for score in scores:
            saver.save([score, mmh.current_step])


def main(saver:Saver=None):
    methods = (
        # ((), run_interpreter_testing),
        (('step', 'max_score'), run_simple_cases),
        # (('score', 'step'), run_test_motif),
    )
    for fields, method in methods:
        with Saver(fields=fields) as saver:
            try:
                method(saver)
            except KeyboardInterrupt:
                pass
        if fields:
            saver.commit()
        print('STOPPED')
        if fields:
            saver.plot()


if __name__ == "__main__":
    main()
