from pathlib import Path
from typing import Any
from config_loader.env import EnvFactory
from config_loader.yaml_service import YamlLoaderFactory

def yaml_load_configs(yaml_dir: str|Path, env_path: Path|str|None = None) -> dict[str, Any]:
    return EnvFactory.create(env_path).replace_vars(YamlLoaderFactory.create().load_configs(yaml_dir))