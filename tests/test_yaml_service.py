import os

import pytest
import yaml

from config_loader.yaml_service import YamlConfigLoaderError, YamlLoaderService, YamlReaderService


@pytest.fixture
def temp_yaml_file(tmp_path):
    config_content = {"database": {"host": "localhost", "port": 5432}}
    file_path = tmp_path / "config.yaml"
    with open(file_path, "w") as f:
        yaml.dump(config_content, f)
    return file_path


@pytest.fixture
def temp_yml_file(tmp_path):
    config_content = {"database": {"host": "localhost", "port": 5432}}
    file_path = tmp_path / "config.yml"
    with open(file_path, "w") as f:
        yaml.dump(config_content, f)
    return file_path


@pytest.fixture
def temp_empty_yaml_file(tmp_path):
    file_path = tmp_path / "empty.yaml"
    with open(file_path, "w") as f:
        f.write("")
    return file_path


@pytest.fixture
def temp_yaml_dir(tmp_path):
    config1 = {"name": "config1", "value": 1}
    config2 = {"name": "config2", "value": 2}

    file1_path = tmp_path / "config1.yaml"
    file2_path = tmp_path / "config2.yaml"

    with open(file1_path, "w") as f:
        yaml.dump(config1, f)
    with open(file2_path, "w") as f:
        yaml.dump(config2, f)

    return tmp_path


def test_yaml_reader_service_load_existing_file(temp_yaml_file):
    service = YamlReaderService()
    config = service.load(temp_yaml_file)
    assert config["database"]["host"] == "localhost"
    assert config["database"]["port"] == 5432


def test_yaml_reader_service_load_yml_extension(temp_yml_file):
    service = YamlReaderService()
    config = service.load(temp_yml_file)
    assert config["database"]["host"] == "localhost"
    assert config["database"]["port"] == 5432


def test_yaml_reader_service_load_empty_file(temp_empty_yaml_file):
    service = YamlReaderService()
    config = service.load(temp_empty_yaml_file)
    assert config == {}


def test_yaml_reader_service_load_nonexistent_file():
    service = YamlReaderService()
    config = service.load("nonexistent.yaml")
    assert config == {}


def test_yaml_reader_service_invalid_yaml(tmp_path):
    invalid_yaml = tmp_path / "invalid.yaml"
    with open(invalid_yaml, "w") as f:
        f.write("invalid: yaml: content:")

    service = YamlReaderService()
    with pytest.raises(YamlConfigLoaderError):
        service.load(invalid_yaml)


def test_yaml_reader_service_permission_denied(tmp_path):
    config_file = tmp_path / "restricted.yaml"
    with open(config_file, "w") as f:
        yaml.dump({"key": "value"}, f)

    # Remove read permissions
    os.chmod(config_file, 0o000)

    try:
        service = YamlReaderService()
        with pytest.raises(YamlConfigLoaderError):
            service.load(config_file)
    finally:
        # Restore permissions for cleanup
        os.chmod(config_file, 0o666)


def test_yaml_loader_service_load_configs(temp_yaml_dir):
    service = YamlLoaderService(YamlReaderService())
    configs = service.load_configs(temp_yaml_dir)

    assert len(configs) == 2
    assert configs["config1"]["name"] == "config1"
    assert configs["config1"]["value"] == 1
    assert configs["config2"]["name"] == "config2"
    assert configs["config2"]["value"] == 2


def test_yaml_loader_service_load_configs_empty_dir(tmp_path):
    service = YamlLoaderService(YamlReaderService())
    configs = service.load_configs(tmp_path)
    assert configs == {}


def test_yaml_loader_service_load_configs_nonexistent_dir():
    service = YamlLoaderService(YamlReaderService())
    configs = service.load_configs("nonexistent_dir")
    assert configs == {}


def test_yaml_loader_service_mixed_files(temp_yaml_dir):
    # Create file with .yml extension
    yml_file = temp_yaml_dir / "config3.yml"
    with open(yml_file, "w") as f:
        yaml.dump({"name": "config3", "value": 3}, f)

    # Create non-YAML file
    txt_file = temp_yaml_dir / "not_yaml.txt"
    with open(txt_file, "w") as f:
        f.write("not a yaml file")

    service = YamlLoaderService(YamlReaderService())
    configs = service.load_configs(temp_yaml_dir)

    assert len(configs) == 3
    assert "config3" in configs
    assert configs["config3"]["value"] == 3


def test_yaml_loader_service_skip_invalid_files(temp_yaml_dir):
    # Create invalid YAML file
    invalid_yaml = temp_yaml_dir / "invalid.yaml"
    with open(invalid_yaml, "w") as f:
        f.write("invalid: yaml: content:")

    # Create file without read permissions
    restricted_yaml = temp_yaml_dir / "restricted.yaml"
    with open(restricted_yaml, "w") as f:
        yaml.dump({"key": "value"}, f)
    os.chmod(restricted_yaml, 0o000)

    try:
        service = YamlLoaderService(YamlReaderService())
        configs = service.load_configs(temp_yaml_dir)

        # Check that valid files are loaded
        assert len(configs) == 2
        assert "config1" in configs
        assert "config2" in configs

        # Check that invalid files are skipped
        assert "invalid" not in configs
        assert "restricted" not in configs
    finally:
        # Restore permissions for cleanup
        os.chmod(restricted_yaml, 0o666)


def test_yaml_loader_service_directory_access_error(tmp_path):
    config_dir = tmp_path / "configs"
    config_dir.mkdir()

    # Remove directory read permissions
    os.chmod(config_dir, 0o000)

    try:
        service = YamlLoaderService(YamlReaderService())
        with pytest.raises(YamlConfigLoaderError):
            service.load_configs(config_dir)
    finally:
        # Restore permissions for cleanup
        os.chmod(config_dir, 0o755)
