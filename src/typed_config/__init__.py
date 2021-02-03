import os
import json

from dacite import from_dict
import yaml


def from_yaml(config_class, file_path, **kwargs):
    with open(file_path) as file:
        yaml_config = yaml.safe_load(file)
    return from_dict(data_class=config_class, data=yaml_config, **kwargs)


def from_json(config_class, file_path, **kwargs):
    with open(file_path) as file:
        json_config = json.load(file)
    return from_dict(data_class=config_class, data=yaml_config, **kwargs)
