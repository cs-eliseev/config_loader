from pathlib import Path

def base_path() -> Path:
    return Path(__file__).parent

def config_path(config_file: str = '') -> Path:
    path = 'configs'
    if config_file != '':
        path += f"/{config_file}"
    return base_path() / path

def env_path() -> Path:
    return config_path('.env')