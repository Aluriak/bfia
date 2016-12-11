
import random

from mmh import MMH
from case import Case
from config import Configuration
from statistics import Saver


# simulation
POP_SIZE = 400


def main(saver:Saver=None):
    # case = Case('', 'hi !')
    case = Case(lambda: random.choice('abcd'), 'hi {stdin} !')
    config = Configuration.from_codes(score='IOC', select='PLDD', mutate='ALL', reproduce='SCP', create='AME')
    # config = Configuration.recipe_best_solution_so_far()
    print('CONFIG:', config)
    print()
    mmh = MMH(case, pop_size=POP_SIZE,
              config=config)
    mmh.run()

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
