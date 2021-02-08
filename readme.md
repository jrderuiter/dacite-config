# dacite-config

Helpers for creating typed, IDE-friendly configs in Python using dataclasses and `dacite`.

## Why use typed configs?

Consider a situation in which we're tasked with building a small web application. To keep things flexible, we'd like to make some options configurable, including the host address on which the application will listen.

To do so, we can create a simple (YAML) based config file that looks something like this:

```yaml
host: "localhost"
port: 1234
```

In a naive approach, we would probably load this config file using something like PyYAML:

```python
import yaml

with open("examples/config.yml") as file:
    config = yaml.safe_load(file)

print(config)
```

However, a drawback of this approach is that it only gives us a dict of values. We have no   garantee that what we loaded has the required keys and expected types, meaning things can easily break once we actually start running our application.  

### Building (typed) configs using dataclasses

We can avoid these issues by using Python's dataclass functionality to create config classes with clearly defined fields and types:

```python
from dataclasses import dataclass

@dataclass()
class Config:
    host: str
    port: int
```

This configuration class will be responsible for holding our configuration values. It also serves as a convenient reference for which configuration fields we expect and what their types will be!

We can use the dataclass as follows:

```python
config: Config = Config(host="localhost", port=1234)
print(config.host, config.port)
```

Unfortunately, the standard dataclass implementation does not do any type checking, meaning that we can easily construct configs with invalid types. Moreover, we don't have any easy mechanism to load values from different config sources (e.g. files, environment, etc.) into this new data class.

### Introducing dacite and dacite config

`dacite-config` aims to provide a flexible approach for loading config values into dataclass-based configs. This is acheived by providing a simple functional API that allow you to load and combine config values from different sources. The loaded values are then injected into your dataclass-based configs using the awesome `dacite` library, which checks for missing values and whether values have the correct types.   

As an example, the following code reads config values from a YAML file (using the `read_yaml` function) and loads the resulting values into our `Config` class using the `load_config` function. Internally, `load_config` calls `dacite.from_dict` to create the dataclass instance and check the loaded values against the dataclass:

```python
from dacite_config import read_yaml, load_config

config: Config = load_config(
  read_yaml("examples/config.yml"),
  config_class=Config,
)

print(config)
```

Besides this, you can also combine different config sources using the `chain` function. For example, this code loads config values from a YAML file and combines them with any environment variables that match the prefix `MYAPP_`:

```python
from dacite_config import read_yaml, read_env, chain, load_config

config: Config = load_config(
  chain(
    read_yaml("examples/config.yml"),
    read_env(prefix="MYAPP_")
  ),
  config_class=Config,
)

print(config)
```

This allows you to build configs that load their values from a static file but can also be overridden by environment variables.

Of course, you can also load configs from multiple files. This allows you to, for example, split config values for different environments (dev/test/prod) across different files:

```python
from dacite_config import read_yaml, chain, load_config

env = "prod"

config: Config = load_config(
  chain(
    read_yaml("examples/config.yml"),
    read_yaml(f"examples/config.{env}yml")
  ),
  config_class=Config,
)

print(config)
```

Of course, this is just a few small examples. Thanks to `dacite`, you can also create much more complicated configs with nested configuration classes, etc. Checkout the documentation for more examples. 

## Getting started

To get started, you can install dacite-config as follows:

```bash
python -m pip install git+https://github.com/jrderuiter/dacite-config.git
```

## Documentation

For more detailed use cases + API documentation, see: TODO.

## Contributing 

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

### Report Bugs

Report bugs at https://github.com/jrderuiter/dacite-config/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

We  could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/jrderuiter/dacite-config/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)