from dataclasses import dataclass
from typing import Optional

from typed_config.readers import ChainedConfigReader, JsonConfigReader, YamlConfigReader

@dataclass()
class DispatchConfig:
    dispatcher: str


@dataclass()
class Config:
    host: str
    port: int

    dispatching: Optional[DispatchConfig]


if __name__ == "__main__":
    yaml_config: Config = YamlConfigReader("./config.yml").read_config(Config)
    print(yaml_config)

    json_config: Config = JsonConfigReader("./config.json").read_config(Config)
    print(json_config)

    chained_config: Config = ChainedConfigReader([
        YamlConfigReader("./config.yml"),
        JsonConfigReader("./config.json")
    ]).read_config(Config)
    print(chained_config)
