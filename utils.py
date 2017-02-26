"""

"""

import itertools
import functools
from collections import defaultdict


def named_functions_interface_decorator(named_funcs:callable):
    """Allow a named_functions function to expose a more complete API"""
    # this trick limits the dictionnary to be computed only one time,
    #  avoiding multiple calls to partial in modules, therefore always
    #  using the same object to describe the same function.
    #  Comment this line, and suddenly the Configuration object will not
    #  be able to find all the codes for some functions.
    named_funcs = functools.lru_cache(maxsize=1)(named_funcs)
    functools.wraps(named_funcs)
    def wrapper(name:str=None):
        funcs = named_funcs()
        if name:
            if name in funcs:
                return funcs[name]
            else:
                raise ValueError("Function name {} is not know. Expecteds are: "
                                 "{}.".format(name, ', '.join(funcs.keys())))
        # expose the expected API
        return dict(funcs)
    return wrapper


def pretty_func(func:callable) -> str:
    """Pretty print of function, or a functools.partial object"""
    if type(func) is functools.partial:
        return "{}({}*, {})".format(
            func.func.__name__,
            ', '.join(func.args) + (', ' if func.args else ''),
            ', '.join('{}={}'.format(k, v) for k, v in func.keywords.items())
        )
    assert callable(func)
    return func.__name__


def key_of(value, mapping:dict, default=None):
    """Return the first key found having the given value"""
    keys = (key for key, mapped in mapping.items() if value is mapped)
    return next(keys, default)


def reversed_dict(mapping:dict, *, cast:type=None) -> dict:
    """Return a dict with keys and values inverted.

    Values of input dict should be hashable.
    To values are by default a read only iterable, but that behavior can be
    changed using the cast parameter.

    """
    cast = cast or iter
    ret = defaultdict(set)
    for key, value in mapping.items():
        ret[value].add(key)
    return {k: cast(v) for k, v in ret.items()}


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"  # from itertools doc
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    yield from itertools.zip_longest(*args, fillvalue=fillvalue)
