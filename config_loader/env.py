import re
from os import environ
from pathlib import Path
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv


class Env:
    ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)(?::([^}]+))?\}")  # Regexp: ${VAR_NAME:default}

    def __init__(self, env_path: Union[Path, str, None] = None) -> None:
        load_dotenv(dotenv_path=env_path)
        self.env_configs = environ

    def replace_vars(self, data: Any, default: Any = None) -> Any:
        """Recursively replaces environment variables in the data."""
        if isinstance(data, dict):
            return {key: self.replace_vars(value, default) for key, value in data.items()}
        if isinstance(data, list):
            return [self.replace_vars(item, default) for item in data]
        if isinstance(data, str):
            return self.replace_var(data, default)
        return data

    def replace_var(self, value: str, default: Any = None) -> Optional[str]:
        """Replaces ${VAR_NAME} or ${VAR_NAME:default} with the value of an environment variable."""

        def replace_match(match: re.Match) -> str:
            var_name = match.group(1)
            var_default = match.group(2) if match.group(2) is not None else default
            env_value = self.get(var_name)
            return (
                str(env_value)
                if env_value is not None
                else str(var_default) if var_default is not None else ""
            )

        result = self.ENV_VAR_PATTERN.sub(replace_match, value)
        return result if result != "" else None

    def get(self, key: str, default: Any = None) -> Any:
        return self.env_configs.get(key, default)

    def all(self) -> Dict[str, Any]:
        return dict(self.env_configs.items())


class EnvFactory:
    @staticmethod
    def create(env_path: Union[Path, str, None] = None) -> Env:
        return Env(env_path)
