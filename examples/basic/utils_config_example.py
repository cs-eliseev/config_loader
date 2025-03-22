"""
Example of using configuration loading utilities.
Demonstrates how to load configurations using utility functions.
"""

from config_loader.utils import yaml_load_config
from examples.resources.resource_path import config_path, env_path


def main():
    # Get configuration paths
    config_file = config_path("config2.yaml")
    env_file = env_path()

    # 1. Load configuration without environment variables
    print("1. Loading configuration without environment variables:")
    print(f"Config file: '{config_file}'")
    print(yaml_load_config(config_file))

    # 2. Load configuration with environment variables
    print("\n2. Loading configuration with environment variables:")
    print(f"Config file: '{config_file}'")
    print(f"Environment file: '{env_file}'")
    print(yaml_load_config(config_file, env_file))


if __name__ == "__main__":
    main()
