
import random

from mmh import MMH
from case import Case
from config import Configuration
from statistics import Saver


# simulation
POP_SIZE = 400


def main(saver:Saver=None):
    # case = Case('', 'hi !')
    letters = tuple(chr(c) for c in range(32, 128))
    case = Case(lambda: random.choice(letters), 'hi {stdin} !')
    config = Configuration.from_codes(score='IOCBM', select='PLDD', mutate='ALL',
                                      reproduce='SCP', create='AME', step='DIV')
    # config = Configuration.recipe_best_solution_so_far()
    mmh = MMH(case, pop_size=POP_SIZE, config=config)
    while True:
        next(mmh.run())

if __name__ == "__main__":
    main()
    exit()
    with Saver(('scores', 'max_score', 'min_score')) as saver:
        try:
            main(saver)
        except KeyboardInterrupt:
            pass
    saver.commit()
    print('STOPPED')
    files = Saver.data_files()
    print('FILES:', files)
    Saver.plot(max(files))
