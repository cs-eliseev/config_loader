from pathlib import Path
from typing import Any, Dict, Union

from config_loader.utils import yaml_load_config, yaml_load_configs


class ConfigCollection:
    def __init__(self, configs: Dict[str, Any]) -> None:
        self.configs = configs

    def all(self) -> Dict[str, Any]:
        return self.configs

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from nested dictionary using dot notation.

        Args:
            key: Key in dot notation (e.g. 'parent.child.key' or 'array.0.name')
            default: Default value to return if key not found

        Returns:
            Value from dictionary or default if not found
        """
        keys = key.split(".")
        current: Any = self.all()

        for k in keys:
            if not isinstance(current, (dict, list)):
                return default

            if isinstance(current, list):
                try:
                    idx = int(k)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return default
                except (ValueError, TypeError):
                    return default
            else:
                if k not in current:
                    return default
                current = current[k]

        return current


class ConfigFactory:
    @staticmethod
    def create(configs: Dict[str, Any]) -> ConfigCollection:
        return ConfigCollection(configs)

    @staticmethod
    def create_by_path(
        yaml_config_path: Path, env_path: Union[Path, str, None] = None
    ) -> ConfigCollection:
        if yaml_config_path.is_file():
            return ConfigCollection(yaml_load_config(yaml_config_path, env_path))
        return ConfigCollection(yaml_load_configs(yaml_config_path, env_path))
