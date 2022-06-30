"""Module working on saving and printing data about a simulation

"""


import time
import glob
import csv

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

import utils
import commons



def plotter(df, config_change_steps: list[int]):
    ax = df.plot(x='step', y=['max_score', 'min_score'])
    ax = df.plot(x='step', y='diversity',secondary_y=True, ax=ax)
    for step in config_change_steps:
        ax.axvline(x=step, color='red', linestyle='--', label='Config change')


class Saver:
    """Save data about a simulation.

    >>> s = Saver(('a', 'b', 'c'), defaults=[0])
    >>> s.save(3, 4, 5)  # a = 3, b = 4 and c = 5 for the first row
    >>> s.save(1, 5)     # a = 1, b = 5 and c = 0 (default value) for the second row

    """
    FILE_TEMPLATE = 'data_{}.csv'

    def __init__(self, fields:iter=commons.DEFAULT_DATASAVE_FIELDS, defaults:iter=None,
                 fileid:str='', datadir:str=commons.DATA_DIR, index: str = 'step',
                 plotter:callable=plotter):

        """

        fields -- column name, in order expected by later save() calls.
        defaults -- default values for columns, if not provided in call params.
        fileid -- string added to filename in order to facilitate its
            identification when humans looks for it.
        plotter -- dataframe to plot function used by plot() method

        """
        assert callable(plotter)
        self.plotter = plotter
        self.fileid = str(fileid)
        self.fields = (index,) + tuple(str(_) for _ in fields)
        self.datadir = str(datadir)
        self.defaults = tuple(defaults) if defaults else ()
        self.commit(first_time=True)
        self.writer.writerow(self.fields)
        self.nb_row = 0
        self.last_config = None  # to detect configuration changes
        self.config_change_steps = []  # steps at which config was changed

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.commit()

    def save(self, **fieldvalues):
        """Save given values for registered fields in output file.
        If necessary, complete given values with defaults

        """
        self.nb_row += 1

        current_config = fieldvalues['config']
        if current_config != self.last_config:
            self.last_config = current_config
            self.config_change_steps.append(self.nb_row)

        fieldvalues = [self.nb_row] + list(fieldvalues[f] for f in self.fields)
        if len(fieldvalues) < len(self.fields):
            fieldvalues += list(self.defaults)[len(self.fields) - len(fieldvalues):]
        self.writer.writerow(fieldvalues)

    def commit(self, *, first_time=False):
        if not first_time:
            self.filedesc.close()
        self.filedesc = open(self.datadir + Saver.FILE_TEMPLATE.format(self.fileid), 'w' if first_time else 'a')
        self.writer = csv.writer(self.filedesc)


    @staticmethod
    def data_files() -> iter:
        """Return files available to plotting"""
        return glob.glob(commons.DATA_DIR_TEMPLATE.format('*') + 'data_*.csv')


    def plot(self, filename:str=None):
        """Plot data in given file.

        filename -- data is there. If not valid, seek for latest file, based on name.

        """
        if not filename:
            filename = max(Saver.data_files())
        df = pd.read_csv(filename)
        print('DATAFRAME:')
        print(df)
        plot = self.plotter(df, self.config_change_steps)
        plt.show()


class ScoreSaver(Saver):
    """Override specific methods of Saver in order to manage data
    as a 3-uplet (scores:tuple, min:int, max:int).

    """

    def __init__(self, fields:iter=['scores', 'min_score', 'max_score'], defaults:iter=None,
                 fileid:str='', datadir:str=commons.DATA_DIR,
                 plotter:callable=lambda df: df.boxplot('max_score', by=['step'])):
        super().__init__(fields, defaults, fileid, datadir, plotter)
