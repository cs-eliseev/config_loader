"""
Example of YAML configuration loading.
Demonstrates how to load configurations from YAML files and directories.
"""

from config_loader.yaml_service import YamlLoaderFactory, YamlReaderService
from examples.resources.resource_path import config_path


def main():
    # Initialize YAML services
    yaml_reader = YamlReaderService()
    yaml_loader = YamlLoaderFactory().create()

    # Get configuration paths
    config_dir = config_path()
    config_file = config_path("config2.yaml")

    # 1. Load configuration using YamlReaderService
    print("1. Loading with YamlReaderService:")

    # Load from directory
    print(f"\nLoading directory '{config_dir}':")
    print(yaml_reader.load(config_path=config_dir))

    # Load from file
    print(f"\nLoading file '{config_file}':")
    print(yaml_reader.load(config_path=config_file))

    # 2. Load configuration using YamlLoaderService
    print("\n2. Loading with YamlLoaderService:")
    print(f"Loading directory '{config_dir}':")
    print(yaml_loader.load_configs(config_dir=config_dir))


if __name__ == "__main__":
    main()
