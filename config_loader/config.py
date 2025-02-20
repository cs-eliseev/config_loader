from pathlib import Path
from typing import Any
from config_loader.utils import yaml_load_configs


class ConfigCollection:
    """Обертка для конфигов."""
    def __init__(self, configs: dict[str, Any]) -> None:
        self.configs = configs

    def all(self) -> dict[str, Any]:
        return self.configs

    def get(self, key: str, default=None):
        keys = key.split(".")
        value = self.all()
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value

class ConfigFactory:
    @staticmethod
    def create(configs: dict[str, Any]) -> ConfigCollection:
        return ConfigCollection(configs)

    @staticmethod
    def create_by_path(yaml_config_dir: str|Path, env_path: Path|str|None = None) -> ConfigCollection:
        return ConfigCollection(yaml_load_configs(yaml_config_dir, env_path))