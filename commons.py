

import os
import time


DATA_DIR_TEMPLATE = 'output/run_{}/'
DATA_DIR = DATA_DIR_TEMPLATE.format(int(time.time()))
os.mkdir(DATA_DIR)


# data that is saved in statistics file
DEFAULT_DATASAVE_FIELDS = ['popsize', 'max_score', 'min_score', 'diversity', 'config']
