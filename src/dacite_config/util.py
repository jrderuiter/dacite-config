import os
from pathlib import Path


def find_config(file_name, path=None):
    path = path or os.getcwd()

    for dir_name in _walk_to_root(path):
        file_path = os.path.join(dir_name, file_name)
        if os.path.isfile(file_path):
            return file_path

    raise IOError(f"Config file '{file_name}' not found along path '{path}'")


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


def for_env(base_file_path: str, env: str):
    base_file_path = Path(base_file_path)
    env_file_name = f"{base_file_path.stem}.{env}{base_file_path.suffix}"
    return base_file_path.parent / env_file_name
