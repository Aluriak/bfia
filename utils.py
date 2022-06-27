"""

"""

import itertools
import functools
from collections import defaultdict

from numpy.random import default_rng
np_rng = default_rng()  # replace np.random ; see https://numpy.org/doc/stable/reference/random/index.html#random-quick-start


def named_functions_interface_decorator(named_funcs:callable):
    """Allow a named_functions function to expose a more complete API"""
    # this trick limits the dictionnary to be computed only one time,
    #  avoiding multiple calls to partial in modules, therefore always
    #  using the same object to describe the same function.
    #  Comment this line, and suddenly the Configuration object will not
    #  be able to find all the codes for some functions.
    named_funcs = functools.lru_cache(maxsize=1)(named_funcs)
    @functools.wraps(named_funcs)
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
    wrapper.as_tuple = lambda: tuple(wrapper.__wrapped__().values())
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


def make_named_functions(basecode: str, func: callable, kwargs: dict) -> dict:
    """This is an helper for function modules, when there is multiple keyword args to provide.

    Example: calling make_functions('PR', pairing_with_replacement, {'keep_parents': 'P', 'parent_score_weight': 'W'})
    will provide the four combination of calls of function pairing_with_replacement, with given kwargs as boolean values.
    Hence, we will get something like:

        {
            'PRW': partial(pairing_with_replacement, keep_parents=False, parent_score_weight=True),
            'PRPW':  partial(pairing_with_replacement, keep_parents=True, parent_score_weight=True),
            'PR': partial(pairing_with_replacement, keep_parents=False, parent_score_weight=False),
            'PRP': partial(pairing_with_replacement, keep_parents=True, parent_score_weight=False),
        }

    Kwargs values may be strings, or dict of strings to value.
    Internally, a string is converted to its dict equivalent,
    e.g. 'P' become {'P': True, '': False}. Hence the argument will have two possible values,
    True and False, with True associated to given string, and False to empty string.

    """
    for kwarg, val in tuple(kwargs.items()):
        if val == '':
            raise ValueError(f"Cannot handle a value of empty string (for kwarg {kwarg}).")
        if isinstance(val, str):
            kwargs[kwarg] = {val: True, '': False}
    out = {}

    for args in itertools.product(*map(list, kwargs.values())):
        kw = {kwarg: kwargs[kwarg][val] for kwarg, val in zip(kwargs, args)}
        code = basecode + ''.join(map(str, args))
        partialized_func = functools.partial(func, **kw)
        if code in out:
            raise ValueError(f"cannot add '{pretty_func(partialized_func)}' as {code}, since it is already associated with '{pretty_func(out[code])}'")
        out[code] = partialized_func

    return out


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


def choices(population: iter, weights = None, k: int = 1, replacement: bool = False) -> list:
    """Like random.choices, but without replacement, unless asked to"""
    # turn weights from int to float
    if weights:
        total_weight = sum(weights)
        weights = [w/total_weight for w in weights]
    assert len(population) >= k, (len(population), k)
    return np_rng.choice(list(population), size=k, replace=replacement, p=weights)

