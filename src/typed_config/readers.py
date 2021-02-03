from functools import reduce
import os
import json
from typing import List

import dacite
import yaml
from toolz import compose_left, curry
from toolz.curried import keymap, keyfilter


class ConfigReader:

    def __init__(self, cast=None):
        self._cast = cast or []

    def read_values(self):
        raise NotImplementedError()

    def read_config(self, config_class, sub_path=None):
        return compose_left(
            curry(_select_path, sub_path=sub_path),
            lambda d: dacite.from_dict(
                config_class,
                data=d,
                config=dacite.Config(cast=self._cast)
            )
        )(self.read_values())

    def __repr__(self):
        return f"{self.__class__.__name__}()"


def _select_path(d, sub_path):
    if not sub_path:
        return d
    keys = sub_path.split(".")
    return _select_path_rec(d, keys)


def _select_path_rec(d, keys):
    if not keys:
        return d
    head, *tail = keys
    return _select_path_rec(d[head], tail)


class ChainedConfigReader(ConfigReader):

    def __init__(self, loaders: List[ConfigReader], cast=None):
        super().__init__(cast=cast)
        self._loaders = loaders

    def read_values(self):
        return reduce(
            lambda d1, d2: {**d1, **d2},
            (loader.read_values() for loader in self._loaders)
        )

class EnvConfigReader(ConfigReader):

    def __init__(self, prefix, separator="__", cast=None):
        super().__init__(cast=cast)
        self._prefix = prefix
        self._separator = separator

    def read_values(self):
        return compose_left(
            keyfilter(lambda k: k.startswith(self._prefix)),
            keymap(
                compose_left(
                    curry(_remove_prefix, prefix=self._prefix),
                    curry(_remove_prefix, prefix=self._separator),
                    lambda k: k.lower()
                )
            ),
            curry(_unflatten_dict, separator=self._separator)
        )(os.environ)


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


class JsonConfigReader(ConfigReader):

    def __init__(self, file_path: str, open_func=None):
        super().__init__()
        self._file_path = file_path
        self._open_func = open_func or open

    def read_values(self):
        with self._open_func(self._file_path) as file:
            return json.load(file)


class YamlConfigReader(ConfigReader):

    def __init__(self, file_path: str, open_func=None):
        super().__init__()
        self._file_path = file_path
        self._open_func = open_func or open

    def read_values(self):
        with self._open_func(self._file_path) as file:
            return yaml.safe_load(file)
