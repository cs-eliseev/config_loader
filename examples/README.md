# config_loader Examples

This directory contains examples of using the config_loader library. Examples are organized by categories for better understanding of functionality.

## Directory Structure

```
examples/
├── basic/           # Basic usage examples
├── advanced/        # Advanced examples
├── integration/     # Integration examples
├── security/        # Security examples
└── performance/     # Performance optimization examples
```

## Example Categories

### Basic
- `config_example.py` - Basic configuration handling
- `env_example.py` - Environment variables handling
- `yaml_example.py` - YAML file handling

### Advanced
- `validation_example.py` - Configuration validation
- `nested_config_example.py` - Nested configuration handling
- `dynamic_config_example.py` - Dynamic configuration handling

### Integration
- `multi_format_example.py` - Multiple format handling (JSON, YAML, INI)
- `migration_example.py` - Version migration examples
- `error_handling_example.py` - Error handling

### Security
- `secrets_example.py` - Secrets handling
- `access_control_example.py` - Access control
- `encryption_example.py` - Configuration encryption

### Performance
- `caching_example.py` - Configuration caching
- `async_loading_example.py` - Asynchronous loading
- `optimization_example.py` - Large configuration optimization

## How to Use Examples

1. Make sure you have all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the desired example:
   ```bash
   python examples/basic/config_example.py
   ```

## Notes

- All examples include detailed comments
- Each example demonstrates a specific aspect of functionality
- Additional setup is required for secrets and encryption examples 