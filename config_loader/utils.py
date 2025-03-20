from pathlib import Path
from typing import Any, Dict, Union, cast

from config_loader.env import EnvFactory
from config_loader.yaml_service import YamlLoaderFactory, YamlReaderService


def yaml_load_configs(
    yaml_dir: Union[str, Path], env_path: Union[Path, str, None] = None
) -> Dict[str, Dict[str, Any]]:
    result = EnvFactory.create(env_path).replace_vars(
        YamlLoaderFactory.create().load_configs(yaml_dir)
    )
    return cast(Dict[str, Dict[str, Any]], result)


def yaml_load_config(
    yaml_file: Union[str, Path], env_path: Union[Path, str, None] = None
) -> Dict[str, Any]:
    result = EnvFactory.create(env_path).replace_vars(YamlReaderService.load(yaml_file))
    return cast(Dict[str, Any], result)
