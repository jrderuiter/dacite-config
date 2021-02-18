import os
from pathlib import Path


def find_in_path(file_name, path=None):
    path = path or os.getcwd()

    for dir_name in _walk_to_root(path):
        file_path = os.path.join(dir_name, file_name)
        if os.path.isfile(file_path):
            return file_path

    raise FileNotFoundError(f"Config file '{file_name}' not found along path '{path}'")


def _walk_to_root(path):
    if not os.path.exists(path):
        raise IOError("Start path not found")

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def with_suffix(file_path: str, suffix: str):
    file_path = Path(file_path)
    suffixed_name = f"{file_path.stem}.{suffix}{file_path.suffix}"
    return file_path.parent / suffixed_name


def for_env(file_path, env_name):
    return with_suffix(file_path, suffix=env_name)