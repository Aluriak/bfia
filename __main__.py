
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
    config = Configuration.recipe_using_standard_methods()
    for case_name, case in CASES.items():
        print('#'*80)
        print('#', case_name)
        mmh = MMH(case, pop_size=POP_SIZE, config=config, data_handler=saver.save)
        for pops in mmh.corun():
            assert len(pops) == 1  # currently multipop is not implemented
            pop = pops[0]
            assert len(pop) == POP_SIZE
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
        run_simple_cases,
        # (('score', 'step'), run_test_motif),
    )
    for method in methods:
        with Saver() as saver:
            try:
                method(saver)
            except KeyboardInterrupt:
                pass
        saver.commit()
        saver.discretize()
        saver.discretize(table=False)
        saver.plot()


if __name__ == "__main__":
    main()
