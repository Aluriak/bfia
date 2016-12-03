

import os
import time


DATA_DIR_TEMPLATE = 'output/run_{}/'
DATA_DIR = DATA_DIR_TEMPLATE.format(int(time.time()))
os.mkdir(DATA_DIR)
