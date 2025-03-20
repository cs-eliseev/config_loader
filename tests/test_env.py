from pathlib import Path

import pytest

from config_loader.env import Env, EnvFactory


@pytest.fixture
def temp_env_file(tmp_path):
    env_content = """
TEST_VAR=test_value
TEST_NUMBER=42
TEST_EMPTY=
NESTED_VAR=${TEST_VAR}
    """
    env_file = tmp_path / ".env"
    with open(env_file, "w") as f:
        f.write(env_content)
    return env_file


@pytest.fixture
def temp_invalid_env_file(tmp_path):
    env_content = """
INVALID_FORMAT
TEST_VAR=value=with=equals
NO_VALUE=
    """
    env_file = tmp_path / ".env"
    with open(env_file, "w") as f:
        f.write(env_content)
    return env_file


@pytest.fixture
def env_with_vars(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "test_value")
    monkeypatch.setenv("TEST_NUMBER", "123")
    monkeypatch.setenv("NESTED_VAR", "nested_value")
    monkeypatch.setenv("PREFIX", "prefix")
    monkeypatch.setenv("SUFFIX", "suffix")
    return Env()


def test_env_load_from_file(temp_env_file):
    env = Env(temp_env_file)
    assert env.get("TEST_VAR") == "test_value"
    assert env.get("TEST_NUMBER") == "42"
    assert env.get("TEST_EMPTY") == ""
    assert env.get("NESTED_VAR") == "test_value"


def test_env_load_from_invalid_file(temp_invalid_env_file):
    env = Env(temp_invalid_env_file)
    assert env.get("TEST_VAR") == "value=with=equals"
    assert env.get("NO_VALUE") == ""
    assert env.get("INVALID_FORMAT") is None


def test_env_get_with_default():
    env = Env()
    assert env.get("NON_EXISTENT", "default") == "default"


def test_env_replace_var(env_with_vars):
    assert env_with_vars.replace_var("Value is ${TEST_VAR}") == "Value is test_value"
    assert env_with_vars.replace_var("Number is ${TEST_NUMBER}") == "Number is 123"


def test_env_replace_var_with_default(env_with_vars):
    assert env_with_vars.replace_var("${NON_EXISTENT}", "default") == "default"


def test_env_replace_multiple_vars(env_with_vars):
    template = "${PREFIX}_${TEST_VAR}_${SUFFIX}"
    assert env_with_vars.replace_var(template) == "prefix_test_value_suffix"


def test_env_replace_vars_dict(env_with_vars):
    test_dict = {"simple": "${TEST_VAR}", "nested": {"value": "${NESTED_VAR}"}}
    result = env_with_vars.replace_vars(test_dict)
    assert result["simple"] == "test_value"
    assert result["nested"]["value"] == "nested_value"


def test_env_replace_vars_list(env_with_vars):
    test_list = ["${TEST_VAR}", "${TEST_NUMBER}"]
    result = env_with_vars.replace_vars(test_list)
    assert result == ["test_value", "123"]


def test_env_replace_vars_mixed_types(env_with_vars):
    test_data = {
        "string": "${TEST_VAR}",
        "number": 42,
        "list": ["${TEST_NUMBER}", 123],
        "nested": {"env_var": "${NESTED_VAR}", "static": "static_value"},
    }
    result = env_with_vars.replace_vars(test_data)
    assert result["string"] == "test_value"
    assert result["number"] == 42
    assert result["list"] == ["123", 123]
    assert result["nested"]["env_var"] == "nested_value"
    assert result["nested"]["static"] == "static_value"


def test_env_replace_vars_with_arrays():
    env = Env()
    test_data = {"array": [{"name": "${TEST_VAR1}"}, {"name": "${TEST_VAR2}"}]}
    result = env.replace_vars(test_data, "default")
    assert result["array"][0]["name"] == "default"
    assert result["array"][1]["name"] == "default"


def test_env_all(env_with_vars):
    env_vars = env_with_vars.all()
    assert isinstance(env_vars, dict)
    assert env_vars["TEST_VAR"] == "test_value"
    assert env_vars["TEST_NUMBER"] == "123"
    assert env_vars["NESTED_VAR"] == "nested_value"


def test_env_factory():
    env = EnvFactory.create()
    assert isinstance(env, Env)

    test_path = Path(".env")
    env_with_path = EnvFactory.create(test_path)
    assert isinstance(env_with_path, Env)


def test_env_empty_string_vars(env_with_vars):
    test_data = {"empty": "${EMPTY_VAR}", "with_default": "${EMPTY_VAR:default}"}
    result = env_with_vars.replace_vars(test_data)
    assert result["empty"] is None
    assert result["with_default"] == "default"
