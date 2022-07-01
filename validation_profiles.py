
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

from collections import defaultdict
from pprint import pprint
import utils

SIZE = 6
AMPLITUDE = 10

profiles = {
        '.........XXXXXX...': 'mountain',
        '......XXXXXX......': 'constant',
        '....XX...X..XXX...': 'mitigated raise',
        '....XX..XX..XX....': 'bounded rise',
        '...X......X.XXX..X': 'failed soar',
        '...X......XXXXX...': 'mountain',
        '...X...X..X.X.X..X': 'fall',
        '...XX.......XXX..X': 'falling unstable',
        '...XX......XXXX...': 'constant unstable',
        '...XX..X....X.X..X': 'mitigated fall',
        '...XX..XX..XX.....': 'trench',
        '...XXX......XXX...': 'raising unstable',
        '...XXX..X...XX....': 'raising unstable',
}

counts = defaultdict(int)


def create_curve():

    max, min = random.randint(0, AMPLITUDE), random.randint(0, AMPLITUDE)
    if min > max:
        min, max = max, min

    start = random.randint(min, max)
    stop = random.randint(min, max)

    series = [start] + [None] * (SIZE-2) + [stop]
    idx_min, idx_max = random.sample(list(range(1, SIZE-1)), k=2)
    series[idx_max], series[idx_min] = max, min
    return [random.randint(min, max) if elem is None else elem for elem in series]



def create_and_show_curve():
    df = pd.DataFrame({'step': list(range(SIZE)), 'score':list(create_curve())})


    profile = utils.get_series_profile(list(df['score']))
    profile_name = utils.profile_name_from(profile, names=profiles)
    print(profile)
    print(utils.get_series_profile(list(df['score']), human_readable=True))
    print(profile_name)


    df.plot(x='step', y=['score'])
    # plt.show()
    plt.savefig('test.png')
    return df, profile, profile_name


def ask_profile_name(df, profile, profile_name):
    profrepr = ''.join('X' if v else '.' for v in profile)
    if profile_name == '?':
        prop = input(f'How should i name {profrepr} ?\n?> ').strip()
        if prop:
            profile_name = profiles[profrepr] = prop.lower()
        counts['?'] += 1  # also count number of newly found profiles
        pprint(profiles)
    else:
        print(f'I would name {profrepr} "{profile_name}"')
    counts[profile_name] += 1


try:
    while True:
        c = create_and_show_curve()
        try:
            ask_profile_name(*c)
        except (EOFError, KeyboardInterrupt):
            break
except (EOFError, KeyboardInterrupt):
    pass
print()
pprint(profiles)
pprint(counts)


FOUND = """
{'.........XXXXXX...': 'mountain',
 '......XXXXXX......': 'constant',
 '....X....X.XXXX...': 'mountain',
 '....XX...X..XXX...': 'mitigated raise',
 '....XX..XX..XX....': 'bounded rise',
 '...X......X.XXX..X': 'failed soar',
 '...X......XXXXX...': 'mountain',
 '...X...X..X.X.X..X': 'fall',
 '...XX.......XXX..X': 'falling unstable',
 '...XX......XXXX...': 'constant unstable',
 '...XX...X..XXX....': 'trench',
 '...XX..X....X.X..X': 'mitigated fall',
 '...XX..X...XX.X...': 'trench',
 '...XX..XX..XX.....': 'trench',
 '...XXX......XXX...': 'raising unstable',
 '...XXX..X...XX....': 'raising unstable'}
defaultdict(<class 'int'>,
            {'?': 3,
             'bounded rise': 66,
             'constant': 35,
             'constant unstable': 339,
             'failed soar': 278,
             'fall': 56,
             'falling unstable': 1418,
             'mitigated fall': 257,
             'mitigated raise': 261,
             'mountain': 89,
             'raising unstable': 1684,
             'trench': 79})
"""
