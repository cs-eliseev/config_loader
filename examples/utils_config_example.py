from config_loader.utils import yaml_load_config
from examples.resources.resource_path import config_path, env_path

config_file = config_path("config2.yaml")
path = env_path()

print(">>>> Only load config:")
print(f"Config path '{config_file}':")
print(yaml_load_config(config_file))

print(">>>> Load config and load enc:")
print(f"Config path '{config_file}' env path '{path}':")
print(yaml_load_config(config_file, path))
