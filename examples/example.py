from dataclasses import dataclass
from typing import Optional

from typed_config._readers import ChainedReader, JsonReader, YamlReader

@dataclass()
class DispatchConfig:
    dispatcher: str


@dataclass()
class Config:
    host: str
    port: int

    dispatching: Optional[DispatchConfig]


if __name__ == "__main__":
    yaml_config: Config = YamlReader("./config.yml").read_config(Config)
    print(yaml_config)

    json_config: Config = JsonReader("./config.json").read_config(Config)
    print(json_config)

    chained_config: Config = ChainedReader([
        YamlReader("./config.yml"),
        JsonReader("./config.json")
    ]).read_config(Config)
    print(chained_config)
