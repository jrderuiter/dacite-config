# typed-config

A dataclass-based approach for creating typesafe configs in Python.

## Why typed-config?

### Scenario

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

However, a drawback of this approach is that it gives us a dict of values. This means we don't have any garantee that what we loaded has the required config keys and expected types. (Not to mention that our IDE will be of little help as it also has no idea what to expect from this dict.)

### Introducting typed configs

To avoid these issues, we can use typed-config to load our config, validating any required keys and their types along the way.

The basic idea is to first define your configuration as a dataclass, which defines the required configuration fields together with their types:

```python
from dataclasses import dataclass

@dataclass()
class Config:
    host: str
    port: int
```

This configuration dataclass will be responsible for holding our configuration values and serves as a convenient reference for which configuration fields we expect and what their types will be.

Next, we can use the `YamlConfigReader` class to load values from our YAML file into this data class as follows: 
 
```python
from typed_config.readers import YamlConfigReader

config: Config = YamlConfigReader(
    file_path="examples/config.yml"
).read_config(Config)
```

This essentially creates a `Config` instance containing the values from the YAML file. When creating this instance, it also checks if any required values are missing from the YAML file or if they have the wrong type.

Once we have the config instance, we can use it as any other Python object:

```python
print(config.host)  # Prints 'localhost'
print(config.port)  # Prints 1234
```

Due to the typing/field information present in the dataclass, this should also play nicely with any auto-completion and type-checking functionality in your IDE!

Of course, this is just a small example to illustrate the idea. Besides this, typed-config also provides several other reader classes to support reading configs from various formats (e.g. JSON, environment variables, etc.) and allows you to combine configs from different locations/formats. More complex configs are also supported, including nested fields etc. 

## Getting started

To get started, you can install typed-config as follows:

```bash
python -m pip install git+https://github.com/jrderuiter/typed-config.git
```

## Documentation

For more detailed use cases + API documentation, see: TODO.

## Contributing 

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

### Report Bugs

Report bugs at https://github.com/jrderuiter/typed-config/issues.

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

The best way to send feedback is to file an issue at https://github.com/jrderuiter/typed-config/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)