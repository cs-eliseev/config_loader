from config_loader.yaml_service import YamlReaderService, YamlLoaderFactory
from examples.resources.resource_path import config_path

yaml_reader = YamlReaderService()
config_dir = config_path()
config_path = config_path('config2.yaml')
print('>>>> YamlReaderService')
print(f"Load dir '{config_dir}':")
print(yaml_reader.load(config_path=config_dir))
print(f"Load file '{config_path}':")
print(yaml_reader.load(config_path=config_path))

yaml_loader = YamlLoaderFactory().create()
print('>>>> YamlLoaderService')
print(f"Load dir '{config_dir}':")
print(yaml_loader.load_configs(config_dir=config_dir))
