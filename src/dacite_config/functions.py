from functools import reduce

import dacite


def chain(*value_dicts):
    return reduce(
        lambda d1, d2: {**d1, **d2}, value_dicts
    )


def select_path(value_dict, sub_path):
    if not sub_path:
        return value_dict
    keys = sub_path.split(".")
    return _select_path_rec(value_dict, keys)


def _select_path_rec(d, keys):
    if not keys:
        return d
    head, *tail = keys
    return _select_path_rec(d[head], tail)


def load_config(values, config_class, dacite_config=None):
    return dacite.from_dict(
        config_class,
        data=values,
        config=dacite_config
    )
