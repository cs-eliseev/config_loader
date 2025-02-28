import re
from os import environ
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

class Env:
    ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")  # Regexp: ${VAR_NAME}

    def __init__(self, env_path: Path|str|None = None) -> None:
        load_dotenv(dotenv_path=env_path)
        self.env_configs = environ

    def replace_vars(self, data: Any, default: Any = None) -> Any:
        """Recursively replaces environment variables in the data."""
        if isinstance(data, dict):
            return {key: self.replace_vars(value, default) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.replace_vars(item, default) for item in data]
        elif isinstance(data, str):
            return self.replace_var(data, default)
        return data

    def replace_var(self, value: str, default: Any = None) -> Any:
        """Replaces ${VAR_NAME} with the value of an environment variable."""
        return self.ENV_VAR_PATTERN.sub(lambda match: self.get(match.group(1), default), value)

    def get(self, key: str, default = None) -> Any:
        return self.env_configs.get(key, default)

    def all(self) -> dict[str, Any]:
        return dict(self.env_configs.items())


class EnvFactory:
    @staticmethod
    def create(env_path: Path|str|None = None) -> Env:
        return Env(env_path)
