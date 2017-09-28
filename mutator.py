"""

"""


import random
import itertools
import functools

from utils import named_functions_interface_decorator
import mutator_functions as mutfunc


MUT_FUNC_FUNCTIONAL = (mutfunc.loop_transposition, mutfunc.io_change,
                       mutfunc.io_transposition, mutfunc.output_interleaving,
                       mutfunc.group_transition, mutfunc.number_complementary)
MUT_FUNC_STRING = (mutfunc.transition, mutfunc.addition, mutfunc.deletion,
                   mutfunc.transposition, mutfunc.single_deletion,
                   mutfunc.single_addition, mutfunc.reversion)


@named_functions_interface_decorator
def named_functions() -> dict:
    """Return a mutator function."""
    return {
        'ALL': all_mutators(),
        'FMT': function_mutators(),
        'SMT': string_mutators(),
        'NO': mutfunc.null_mutator,
    }

def default_functions() -> tuple:
    """Return default mutation functions"""
    return named_functions.as_tuple() + anonymous_functions()

def anonymous_functions() -> tuple:
    """Return mutation functions that have no name"""
    return ()


def _apply_mutations_randomly(mutators, unit):
    """Apply randomly given mutators according to unit mutation rates"""
    if random.random() < unit.mutation_rate:
        random.choice(mutators)(unit)
        while random.random() < unit.additional_mutation_rate:
            random.choice(mutators)(unit)  # one more time !


def no_mutators() -> callable:
    """Return a function that never mutate input unit."""
    @functools.wraps(no_mutators)
    def no_mutators_wrapped(unit):  pass
    return no_mutators_wrapped


def all_mutators() -> callable:
    """Return a function that mutate input unit using a randomly choosen
    mutation method.

    """
    methods = MUT_FUNC_FUNCTIONAL + MUT_FUNC_STRING
    @functools.wraps(all_mutators)
    def all_mutators_wrapped(unit):
        _apply_mutations_randomly(methods, unit)
    return all_mutators_wrapped


def function_mutators() -> callable:
    """Return a function that mutate input unit using a randomly choosen
    mutation method oriented toward modification of functional parts.

    """
    @functools.wraps(function_mutators)
    def function_mutators_wrapped(unit):
        _apply_mutations_randomly(MUT_FUNC_FUNCTIONAL, unit)
    return function_mutators_wrapped


def string_mutators() -> tuple:
    """Return a function that mutate input unit using a randomly choosen
    mutation method oriented toward modification of source code as a string.

    These mutators works by modifying sequence, without any look into
    the consequences of the change.

    """
    @functools.wraps(string_mutators)
    def string_mutators_wrapped(unit):
        _apply_mutations_randomly(MUT_FUNC_STRING, unit)
    return string_mutators_wrapped
