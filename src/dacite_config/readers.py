import configparser
import json
import os

from toolz import compose_left, curry
from toolz.curried import keymap, keyfilter


def read_env(prefix, separator="__", env=os.environ):
    return compose_left(
        keyfilter(lambda k: k.startswith(prefix)),
        keymap(
            compose_left(
                curry(_remove_prefix, prefix=prefix),
                curry(_remove_prefix, prefix=separator),
                lambda k: k.lower()
            )
        ),
        curry(_unflatten_dict, separator=separator)
    )(env)


def _remove_prefix(value, prefix):
    if value.startswith(prefix):
        return value[len(prefix):]
    return value


def _unflatten_dict(flat, separator):
    result = {}
    for k, v in flat.items():
        _unflatten_dict_rec(k, v, result, separator)
    return result


def _unflatten_dict_rec(k, v, out, sep):
    k, *rest = k.split(sep, 1)
    if rest:
        _unflatten_dict_rec(rest[0], v, out.setdefault(k, {}), sep=sep)
    else:
        out[k] = v


def read_ini(file_path, section):
    config = configparser.ConfigParser()
    config.read(file_path)

    separator = "."
    sections = {s: dict(config.items(s)) for s in config.sections()
                if s == section or s.startswith(section + separator)}
    unflattened = _unflatten_dict(sections, separator=separator)

    return unflattened[section]


def read_json(file_path):
    with open(file_path) as file:
        return json.load(file)


def read_toml(file_path):
    try:
        import toml
    except ImportError:
        raise ImportError("toml needs to be installed to load toml files")
    with open(file_path) as file:
        return toml.load(file)


def read_yaml(file_path):
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML needs to be installed to load yaml files")
    with open(file_path) as file:
        return yaml.safe_load(file)
