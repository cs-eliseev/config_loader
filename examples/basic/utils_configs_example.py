"""
Example of using configuration loading utilities for multiple files.
Demonstrates how to load multiple configurations using utility functions.
"""

from config_loader.utils import yaml_load_configs
from examples.resources.resource_path import config_path, env_path


def main():
    # Get configuration paths
    config_dir = config_path()
    env_file = env_path()

    # 1. Load configurations without environment variables
    print("1. Loading configurations without environment variables:")
    print(f"Config directory: '{config_dir}'")
    print(yaml_load_configs(config_dir))

    # 2. Load configurations with environment variables
    print("\n2. Loading configurations with environment variables:")
    print(f"Config directory: '{config_dir}'")
    print(f"Environment file: '{env_file}'")
    print(yaml_load_configs(config_dir, env_file))


if __name__ == "__main__":
    main()
