English | [Русский](https://github.com/cs-eliseev/config_loader/blob/master/README.ru_RU.md)

# Simple Config Loader

A simple and convenient configuration loader for Python applications, supporting YAML files and environment variables.

## Features

- Load configurations from YAML files
- Environment variables support
- Type validation
- Simple and intuitive API
- Nested configurations support
- Error handling

## Installation

### Directly from GitHub

```bash
pip install git+https://github.com/cs-eliseev/config_loader/config-loader.git
```

## Usage

### Loading YAML Configuration

```python
from pathlib import Path
from config_loader import ConfigFactory

config = ConfigFactory.create_by_path(Path('config.yaml'))
value = config.get('some.nested.key')

configs = ConfigFactory.create_by_path(Path('config_dir/'))
value = configs.get('some.nested.key')
```

### Working with Environment Variables

```python
from config_loader import EnvFactory

env = EnvFactory.create('.env')
value = env.get('ENV_VARIABLE')

all_vars = env.all()

data = {
    'db_url': '${DATABASE_URL:sqlite:///default.db}',
    'api_key': '${API_KEY}'
}
processed_data = env.replace_vars(data)
```

### Combined Usage

```python
from pathlib import Path
from config_loader import ConfigFactory

config = ConfigFactory.create_by_path(
    yaml_config_path=Path('config.yaml'),
    env_path='.env'
)
value = config.get('database.url')
```

### Detailed Examples

For a more detailed look at the library's capabilities, check out the [usage examples](examples/README.md), which include:
- Basic examples
- Advanced usage scenarios
- Integration examples
- Security examples
- Performance tests

## Development

### Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- For development: dependencies from `dev-requirements.txt`

### Installing Development Dependencies

```bash
pip install -r dev-requirements.txt
```

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy .
```

### Linting

```bash
flake8
pylint config_loader
```

### Development Utilities

The `utils/` folder contains scripts to automate various development tasks:

- `lint.sh` - runs all code checks (black, isort, flake8, mypy, pylint)
- `format.sh` - formats code using black and isort
- `tests.sh` - runs tests with verbose output
- `coverage.sh` - runs tests with code coverage measurement and generates HTML report
- `examples.sh` - script for running examples

All scripts automatically create and activate virtual environment when needed.

## License

MIT License - see [LICENSE](LICENSE) file for details.