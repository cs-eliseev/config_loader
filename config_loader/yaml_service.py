import os
from pathlib import Path
from typing import Any, Dict, Union

import yaml


class YamlConfigLoaderError(Exception):
    def __init__(self, error: Exception) -> None:
        super().__init__(f"Yaml configuration error: {error}")


class YamlReaderService:
    """Загружает конфиг из YAML и подставляет переменные окружения."""

    @staticmethod
    def load(config_path: Union[str, Path]) -> Dict[str, Any]:
        if isinstance(config_path, str):
            config_path = Path(config_path)

        if not config_path.is_file():
            return {}

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise YamlConfigLoaderError(e) from e


class YamlLoaderService:
    """Загружает все YAML конфиги из указанной папки."""

    def __init__(self, yaml_service: YamlReaderService) -> None:
        self.yaml_service = yaml_service

    def load_configs(self, config_dir: Union[str, Path]) -> Dict[str, Dict[str, Any]]:
        if isinstance(config_dir, str):
            config_dir = Path(config_dir)

        if not config_dir.is_dir():
            return {}

        configs: Dict[str, Dict[str, Any]] = {}
        for file_name in os.listdir(config_dir):
            if file_name.endswith(".yaml"):
                file_path = os.path.join(config_dir, file_name)
                config_name = file_name[:-5]  # удаляем ".yaml" из имени
                configs[config_name] = self.yaml_service.load(file_path)
        return configs


class YamlLoaderFactory:
    @staticmethod
    def create() -> YamlLoaderService:
        return YamlLoaderService(YamlReaderService())
