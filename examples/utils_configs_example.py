from config_loader.utils import yaml_load_configs
from examples.resources.resource_path import config_path, env_path

config_dir = config_path()
path = env_path()

print(">>>> Only load config:")
print(f"Config path '{config_dir}':")
print(yaml_load_configs(config_dir))

print(">>>> Load config and load enc:")
print(f"Config path '{config_dir}' env path '{path}':")
print(yaml_load_configs(config_dir, path))
