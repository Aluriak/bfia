

from collections import defaultdict


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
