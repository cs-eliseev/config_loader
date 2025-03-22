"""
Example of error handling when working with configurations.
Demonstrates various error scenarios and how to handle them.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from config_loader.config import ConfigFactory
from config_loader.exceptions import ConfigError, ConfigFileNotFoundError, ValidationError


class ConfigErrorHandler:
    """Error handler for working with configurations."""

    def __init__(self):
        self.config_factory = ConfigFactory()

    def load_config_safely(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Safely loads configuration with error handling."""
        try:
            if not Path(file_path).exists():
                raise ConfigFileNotFoundError(f"Configuration file not found: {file_path}")

            with open(file_path, "r") as f:
                if file_path.endswith(".json"):
                    return json.load(f)
                elif file_path.endswith(".yaml"):
                    return yaml.safe_load(f)
                else:
                    raise ConfigError(f"Unsupported file format: {file_path}")
        except ConfigFileNotFoundError:
            raise  # Re-raise ConfigFileNotFoundError without wrapping
        except json.JSONDecodeError as e:
            raise ConfigError(f"JSON parsing error: {str(e)}")
        except yaml.YAMLError as e:
            raise ConfigError(f"YAML parsing error: {str(e)}")
        except Exception as e:
            raise ConfigError(f"Unexpected error: {str(e)}")

    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validates configuration with error handling."""
        required_fields = ["app_name", "version", "database"]

        for field in required_fields:
            if field not in config:
                raise ValidationError(f"Missing required field: {field}")

        if not isinstance(config["version"], str):
            raise ValidationError("Version field must be a string")

        if not isinstance(config["database"], dict):
            raise ValidationError("Database field must be a dictionary")

    def get_nested_value_safely(
        self, config: Dict[str, Any], path: str, default: Any = None
    ) -> Any:
        """Safely gets nested value."""
        try:
            current = config
            for key in path.split("."):
                if not isinstance(current, dict):
                    raise ConfigError(f"Invalid path: {path}")
                current = current[key]
            return current
        except KeyError:
            return default
        except Exception as e:
            raise ConfigError(f"Error getting value: {str(e)}")


def handle_missing_file():
    """Handle missing file example."""
    handler = ConfigErrorHandler()
    try:
        handler.load_config_safely("nonexistent.json")
    except ConfigFileNotFoundError as e:
        print("1. Handle missing file:")
        print(f"Error: {str(e)}")


def handle_invalid_json():
    """Handle invalid JSON example."""
    handler = ConfigErrorHandler()
    invalid_json = """
    {
        "app_name": "MyApp",
        "version": "1.0.0",
        "database": {
            "host": "localhost",
            "port": 5432
        }
    """
    try:
        with open("invalid.json", "w") as f:
            f.write(invalid_json)
        handler.load_config_safely("invalid.json")
    except ConfigError as e:
        print("\n2. Handle invalid JSON:")
        print(f"Error: {str(e)}")
    finally:
        Path("invalid.json").unlink(missing_ok=True)


def handle_validation():
    """Handle validation example."""
    handler = ConfigErrorHandler()
    invalid_config = {
        "app_name": "MyApp",
        "version": 1.0,  # should be string
        "database": "not_a_dict",  # should be dictionary
    }

    try:
        handler.validate_config(invalid_config)
    except ValidationError as e:
        print("\n3. Validate configuration:")
        print(f"Error: {str(e)}")


def handle_nested_values():
    """Handle nested values example."""
    handler = ConfigErrorHandler()
    config = {
        "app": {
            "name": "MyApp",
            "settings": {
                "debug": True,
            },
        },
    }

    print("\n4. Safely get values:")
    try:
        # Valid path
        debug_mode = handler.get_nested_value_safely(config, "app.settings.debug")
        print(f"Debug mode: {debug_mode}")

        # Non-existent path with default value
        log_level = handler.get_nested_value_safely(config, "app.settings.log_level", "INFO")
        print(f"Log level: {log_level}")

        # Invalid path
        handler.get_nested_value_safely(config, "app.settings")
    except ConfigError as e:
        print(f"Error: {str(e)}")


def handle_comprehensive_error():
    """Handle comprehensive error example."""
    handler = ConfigErrorHandler()
    print("\n5. Comprehensive error handling:")
    try:
        # Try to load configuration
        config = handler.load_config_safely("config.json")

        # Validate configuration
        handler.validate_config(config)

        # Get values
        db_host = handler.get_nested_value_safely(config, "database.host")
        print(f"Database host: {db_host}")

    except ConfigFileNotFoundError as e:
        print(f"File not found: {str(e)}")
    except ValidationError as e:
        print(f"Validation error: {str(e)}")
    except ConfigError as e:
        print(f"Configuration error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


def main():
    """Run all error handling examples."""
    handle_missing_file()
    handle_invalid_json()
    handle_validation()
    handle_nested_values()
    handle_comprehensive_error()


if __name__ == "__main__":
    main()
