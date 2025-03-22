import os
import re
from pathlib import Path
from typing import Any, Dict, Union

import yaml


class YamlConfigLoaderError(Exception):
    def __init__(self, error: Exception) -> None:
        super().__init__(f"Yaml configuration error: {error}")


class YamlReaderService:
    """Loads config from YAML and substitutes environment variables."""

    @staticmethod
    def load(config_path: Union[str, Path]) -> Dict[str, Any]:
        if isinstance(config_path, str):
            config_path = Path(config_path)

        try:
            if not config_path.is_file():
                return {}

            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError, PermissionError, OSError) as e:
            raise YamlConfigLoaderError(e) from e


class YamlLoaderService:
    """Loads all YAML configs from the specified directory."""

    def __init__(self, yaml_service: YamlReaderService) -> None:
        self.yaml_service = yaml_service

    def load_configs(self, config_dir: Union[str, Path]) -> Dict[str, Dict[str, Any]]:
        if isinstance(config_dir, str):
            config_dir = Path(config_dir)

        if not config_dir.is_dir():
            return {}

        configs: Dict[str, Dict[str, Any]] = {}
        try:
            for file_name in os.listdir(config_dir):
                if not re.match(r".*\.ya?ml$", file_name):
                    continue
                try:
                    file_path = os.path.join(config_dir, file_name)
                    config_name = re.sub(r"\.ya?ml$", "", file_name)  # Remove .yaml or .yml
                    configs[config_name] = self.yaml_service.load(file_path)
                except YamlConfigLoaderError:
                    # Skip files that cannot be loaded
                    continue
        except OSError as e:
            raise YamlConfigLoaderError(e) from e

        return configs


class YamlLoaderFactory:
    @staticmethod
    def create() -> YamlLoaderService:
        return YamlLoaderService(YamlReaderService())
