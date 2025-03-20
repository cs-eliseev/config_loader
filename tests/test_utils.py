import pytest
import yaml

from config_loader.utils import yaml_load_config, yaml_load_configs


@pytest.fixture
def temp_yaml_file(tmp_path):
    config_content = {
        "database": {
            "host": "${DB_HOST}",
            "port": "${DB_PORT}",
            "name": "test_db",
            "settings": {
                "timeout": 30,
                "max_connections": 100,
                "enabled": True,
                "rates": [1.1, 2.2, 3.3],
                "tags": ["primary", "replica"],
            },
        }
    }
    file_path = tmp_path / "config.yaml"
    with open(file_path, "w") as f:
        yaml.dump(config_content, f)
    return file_path


@pytest.fixture
def temp_yaml_dir(tmp_path):
    config1 = {
        "service1": {
            "url": "${SERVICE1_URL}",
            "port": "${SERVICE1_PORT}",
            "retries": 3,
            "timeout": 5.5,
            "enabled": True,
        }
    }
    config2 = {
        "service2": {
            "url": "${SERVICE2_URL}",
            "port": "${SERVICE2_PORT}",
            "options": ["opt1", "opt2"],
            "limits": {"memory": 1024, "cpu": 2.5},
        }
    }

    file1_path = tmp_path / "config1.yaml"
    file2_path = tmp_path / "config2.yaml"

    with open(file1_path, "w") as f:
        yaml.dump(config1, f)
    with open(file2_path, "w") as f:
        yaml.dump(config2, f)

    return tmp_path


@pytest.fixture
def temp_env_file(tmp_path):
    env_content = """
DB_HOST=localhost
DB_PORT=5432
SERVICE1_URL=http://service1
SERVICE1_PORT=8081
SERVICE2_URL=http://service2
SERVICE2_PORT=8082
    """
    env_file = tmp_path / ".env"
    with open(env_file, "w") as f:
        f.write(env_content)
    return env_file


def test_yaml_load_config_with_env_vars(temp_yaml_file, temp_env_file):
    config = yaml_load_config(temp_yaml_file, temp_env_file)
    assert config["database"]["host"] == "localhost"
    assert config["database"]["port"] == "5432"
    assert config["database"]["name"] == "test_db"

    # Data type checks
    settings = config["database"]["settings"]
    assert isinstance(settings["timeout"], int)
    assert isinstance(settings["max_connections"], int)
    assert isinstance(settings["enabled"], bool)
    assert isinstance(settings["rates"], list)
    assert all(isinstance(x, float) for x in settings["rates"])
    assert isinstance(settings["tags"], list)
    assert all(isinstance(x, str) for x in settings["tags"])


def test_yaml_load_config_without_env_file(temp_yaml_file, monkeypatch):
    monkeypatch.setenv("DB_HOST", "test_host")
    monkeypatch.setenv("DB_PORT", "1234")

    config = yaml_load_config(temp_yaml_file)
    assert config["database"]["host"] == "test_host"
    assert config["database"]["port"] == "1234"
    assert config["database"]["name"] == "test_db"


def test_yaml_load_config_nonexistent_file():
    config = yaml_load_config("nonexistent.yaml")
    assert config == {}


def test_yaml_load_configs_with_env_vars(temp_yaml_dir, temp_env_file):
    configs = yaml_load_configs(temp_yaml_dir, temp_env_file)

    # Data type checks
    assert isinstance(configs, dict)
    assert isinstance(configs["config1"], dict)
    assert isinstance(configs["config2"], dict)

    # Check values and types for first service
    assert configs["config1"]["service1"]["url"] == "http://service1"
    assert configs["config1"]["service1"]["port"] == "8081"

    # Check values and types for second service
    assert configs["config2"]["service2"]["url"] == "http://service2"
    assert configs["config2"]["service2"]["port"] == "8082"


def test_yaml_load_configs_without_env_file(temp_yaml_dir, monkeypatch):
    monkeypatch.setenv("SERVICE1_URL", "http://test1")
    monkeypatch.setenv("SERVICE1_PORT", "9091")
    monkeypatch.setenv("SERVICE2_URL", "http://test2")
    monkeypatch.setenv("SERVICE2_PORT", "9092")

    configs = yaml_load_configs(temp_yaml_dir)

    assert configs["config1"]["service1"]["url"] == "http://test1"
    assert configs["config1"]["service1"]["port"] == "9091"
    assert configs["config2"]["service2"]["url"] == "http://test2"
    assert configs["config2"]["service2"]["port"] == "9092"


def test_yaml_load_configs_nonexistent_directory():
    configs = yaml_load_configs("nonexistent_dir")
    assert configs == {}
