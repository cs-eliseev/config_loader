"""
Example of working with different configuration formats (JSON, YAML, INI).
Demonstrates how to load and merge configurations from different sources.
"""

import configparser
import json
from pathlib import Path
from typing import Any, Dict

from config_loader.config import ConfigFactory
from config_loader.yaml_service import YamlLoaderFactory


class MultiFormatConfigLoader:
    """Loader for configurations from different formats."""

    def __init__(self):
        self.config_factory = ConfigFactory()
        self.yaml_loader = YamlLoaderFactory().create()

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """Loads configuration from JSON file."""
        with open(file_path, "r") as f:
            return json.load(f)

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Loads configuration from YAML file."""
        return self.yaml_loader.load_configs(file_path)

    def load_ini(self, file_path: str) -> Dict[str, Any]:
        """Loads configuration from INI file."""
        config = configparser.ConfigParser()
        config.read(file_path)

        # Convert INI to dictionary
        result = {}
        for section in config.sections():
            result[section] = dict(config.items(section))
        return result

    def merge_configs(self, configs: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Merges multiple configurations."""
        result = {}
        for config in configs:
            result.update(config)
        return result


def main():
    # Create test configuration files
    config_dir = Path("examples/resources/configs")
    config_dir.mkdir(parents=True, exist_ok=True)

    # JSON configuration
    json_config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
        },
        "features": {
            "cache": True,
            "logging": True,
        },
    }
    with open(config_dir / "config.json", "w") as f:
        json.dump(json_config, f)

    # YAML configuration
    yaml_config = """
    database:
      host: localhost
      port: 5432
      name: mydb
    logging:
      level: INFO
      file: app.log
    """
    with open(config_dir / "config.yaml", "w") as f:
        f.write(yaml_config)

    # INI configuration
    ini_config = """
    [security]
    api_key = secret123
    token_expiry = 3600

    [email]
    smtp_server = smtp.example.com
    port = 587
    """
    with open(config_dir / "config.ini", "w") as f:
        f.write(ini_config)

    # Create loader
    loader = MultiFormatConfigLoader()

    # Load configurations from different formats
    json_data = loader.load_json(str(config_dir / "config.json"))
    yaml_data = loader.load_yaml(str(config_dir / "config.yaml"))
    ini_data = loader.load_ini(str(config_dir / "config.ini"))

    print("1. JSON configuration:")
    print(json_data)
    print("\n2. YAML configuration:")
    print(yaml_data)
    print("\n3. INI configuration:")
    print(ini_data)

    # Merge configurations
    merged_config = loader.merge_configs([json_data, yaml_data, ini_data])
    print("\n4. Merged configuration:")
    print(merged_config)

    # Create configuration object
    config = loader.config_factory.create(merged_config)

    # Demonstrate access to values
    print("\n5. Access to values:")
    print(f"Application name: {config.get('app.name')}")
    print(f"Database host: {config.get('database.host')}")
    print(f"API key: {config.get('security.api_key')}")

    # Clean up test files
    for file in config_dir.glob("*"):
        file.unlink()
    config_dir.rmdir()


if __name__ == "__main__":
    main()
