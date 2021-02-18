from functools import reduce

import dacite


def chain(*value_dicts):
    return reduce(_merge_dicts, value_dicts)


def _merge_dicts(a, b):
    return dict(_merge_dict_gen(a, b))


def _merge_dict_gen(a, b):
    for k in set(a.keys()).union(b.keys()):
        if k in a and k in b:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                yield k, dict(_merge_dict_gen(a[k], b[k]))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield k, b[k]
        elif k in a:
            yield k, a[k]
        else:
            yield k, b[k]


def select_path(value_dict, sub_path):
    if not sub_path:
        return value_dict
    keys = sub_path.split(".")
    return _select_path_rec(value_dict, keys)


def optional(func, valid_exceptions=(FileNotFoundError, )):
    try:
        return func()
    except valid_exceptions:
        return {}


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


def for_resource(package, resource):
    from importlib.resources import path as resource_path

    def wrapper(read_func):
        with resource_path(package, resource) as file_path:
            return read_func(file_path)

    return wrapper
