from config_loader.config import ConfigFactory

data = {
    "config1": {"key_1_1": "config 1", "key_1_2": "test env var = ${test_var_1}"},
    "config2": {
        "key_2_1": "config 2",
        "key_2_2": "test env var = ${test_var_2}",
        "key_2_3": {"key_2_3_1": {"key_2_3_1_1": {"key_2_3_1_1_1": "result"}}},
    },
}

config = ConfigFactory().create(data)
print(">>>> All configs")
print(config.all())

print(">>>> Get configs")
config_key = "config1"
print(f"config key: {config_key}")
print(config.get(config_key))
config_key = "config2.key_2_2"
print(f"config key: {config_key}")
print(config.get(config_key))
config_key = "config2.key_2_3.key_2_3_1.key_2_3_1_1.key_2_3_1_1_1"
print(f"config key: {config_key}")
print(config.get(config_key))
config_key = "config1.test"
print(f"config key: {config_key}")
print(config.get(config_key, "default"))
