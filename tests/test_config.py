import pytest
import yaml

from config_loader.config import ConfigCollection, ConfigFactory


@pytest.fixture
def sample_configs():
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {"username": "user", "password": "pass"},
        },
        "app": {
            "name": "test_app",
            "debug": True,
            "features": ["feature1", "feature2"],
            "limits": {"5": "five", "10": "ten"},
        },
        "empty_section": {},
        "array_section": [{"id": 1, "name": "first"}, {"id": 2, "name": "second"}],
    }


@pytest.fixture
def config_collection(sample_configs):
    return ConfigCollection(sample_configs)


@pytest.fixture
def temp_yaml_file(tmp_path):
    config_content = {"database": {"host": "${DB_HOST}", "port": 5432}}
    file_path = tmp_path / "config.yaml"
    with open(file_path, "w") as f:
        yaml.dump(config_content, f)
    return file_path


@pytest.fixture
def temp_yaml_dir(tmp_path):
    config1 = {"name": "config1", "value": "${VALUE1}"}
    config2 = {"name": "config2", "value": "${VALUE2}"}

    file1_path = tmp_path / "config1.yaml"
    file2_path = tmp_path / "config2.yaml"

    with open(file1_path, "w") as f:
        yaml.dump(config1, f)
    with open(file2_path, "w") as f:
        yaml.dump(config2, f)

    return tmp_path


def test_config_collection_all(config_collection, sample_configs):
    assert config_collection.all() == sample_configs


def test_config_collection_get_simple_key(config_collection):
    assert config_collection.get("app.name") == "test_app"
    assert config_collection.get("app.debug") is True


def test_config_collection_get_nested_key(config_collection):
    assert config_collection.get("database.credentials.username") == "user"
    assert config_collection.get("database.credentials.password") == "pass"


def test_config_collection_get_array_items(config_collection):
    assert config_collection.get("app.features.0") == "feature1"
    assert config_collection.get("app.features.1") == "feature2"
    assert config_collection.get("array_section.0.name") == "first"
    assert config_collection.get("array_section.1.id") == 2


def test_config_collection_get_numeric_keys(config_collection):
    assert config_collection.get("app.limits.5") == "five"
    assert config_collection.get("app.limits.10") == "ten"


def test_config_collection_get_empty_section(config_collection):
    assert config_collection.get("empty_section") == {}
    assert config_collection.get("empty_section.nonexistent") is None


def test_config_collection_get_nonexistent_key(config_collection):
    assert config_collection.get("nonexistent") is None
    assert config_collection.get("nonexistent.key") is None
    assert config_collection.get("app.nonexistent", "default") == "default"


def test_config_collection_get_invalid_path(config_collection):
    # Try to get value through non-existent path in dictionary
    assert config_collection.get("app.name.invalid") is None
    assert config_collection.get("database.host.invalid") is None


def test_config_collection_get_array_out_of_bounds(config_collection):
    assert config_collection.get("app.features.99") is None
    assert config_collection.get("array_section.99.name") is None


def test_config_collection_get_invalid_array_index():
    config = ConfigCollection({"array": [1, 2, 3], "nested": {"array": [4, 5, 6]}})

    # Test with invalid index (not a number)
    assert config.get("array.invalid", "default") == "default"
    assert config.get("nested.array.invalid", "default") == "default"

    # Test with invalid key type
    assert config.get("array.{invalid}", "default") == "default"


def test_config_factory_create(sample_configs):
    config = ConfigFactory.create(sample_configs)
    assert isinstance(config, ConfigCollection)
    assert config.all() == sample_configs


def test_config_factory_create_empty():
    config = ConfigFactory.create({})
    assert isinstance(config, ConfigCollection)
    assert config.all() == {}


def test_config_factory_create_by_path_file(temp_yaml_file, monkeypatch):
    monkeypatch.setenv("DB_HOST", "test_host")
    config = ConfigFactory.create_by_path(temp_yaml_file)
    assert isinstance(config, ConfigCollection)
    assert config.get("database.host") == "test_host"
    assert config.get("database.port") == 5432


def test_config_factory_create_by_path_directory(temp_yaml_dir, monkeypatch):
    monkeypatch.setenv("VALUE1", "val1")
    monkeypatch.setenv("VALUE2", "val2")
    config = ConfigFactory.create_by_path(temp_yaml_dir)
    assert isinstance(config, ConfigCollection)

    configs = config.all()
    assert configs["config1"]["name"] == "config1"
    assert configs["config1"]["value"] == "val1"
    assert configs["config2"]["name"] == "config2"
    assert configs["config2"]["value"] == "val2"
