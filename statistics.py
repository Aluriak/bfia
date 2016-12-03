"""Module working on saving and printing data about a simulation

"""


import time
import glob
import csv

import pandas as pd

import commons


class Saver:
    """Save data about a simulation.

    >>> s = Saver(('a', 'b', 'c'), defaults=[0])
    >>> s.save(3, 4, 5)  # a = 3, b = 4 and c = 5 for the first row
    >>> s.save(0, 5)     # a = 1, b = 5 and c = 0 (default value) for the second row

    """
    FILE_TEMPLATE = 'data_{}.csv'

    def __init__(self, fields:iter=['max_score'], defaults:iter=None,
                 fileid:str='', datadir:str=commons.DATA_DIR):
        """

        fields -- column name, in order expected by later save() calls.
        defaults -- default values for columns, if not provided in call params.
        fileid -- string added to filename in order to facilitate its
            identification when humans looks for it.

        """
        self.fileid = str(fileid)
        self.fields = tuple(str(_) for _ in fields)
        self.datadir = str(datadir)
        self.defaults = tuple(defaults) if defaults else ()
        self.commit(first_time=True)
        self.writer.writerow(self.fields)
        self.nb_row = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.commit()

    def save(self, fieldvalues:iter):
        """Save given values for registered fields in output file.
        If necessary, complete given values with defaults

        """
        self.nb_row += 1
        fieldvalues = list(fieldvalues)
        if len(fieldvalues) < len(self.fields):
            fieldvalues += list(self.defaults)[len(self.fields) - len(fieldvalues):]
        self.writer.writerow([self.nb_row] + fieldvalues)

    def commit(self, *, first_time=False):
        if not first_time:
            self.filedesc.close()
        self.filedesc = open(self.datadir + Saver.FILE_TEMPLATE.format(self.fileid), 'w' if first_time else 'a')
        self.writer = csv.writer(self.filedesc)


    @staticmethod
    def data_files() -> iter:
        """Return files available to plotting"""
        return glob.glob(commons.DATA_DIR_TEMPLATE.format('*') + 'data_*.csv')


    @staticmethod
    def plot(filename:str=None):
        """Plot data in given file.

        filename -- data is there. If not valid, seek for latest file, based on name.

        """
        if not filename:
            filename = max(data_files())
        # TODO
        df = pd.read_csv(filename, index_col=0)
        print('DATAFRAME:', df)
        plot = df.boxplot()
        print(type(plot), plot)
