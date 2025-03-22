"""
Example of basic configuration usage.
Demonstrates how to create and access configuration values.
"""

from config_loader.config import ConfigFactory


def main():
    # Create a simple configuration
    data = {
        "config1": {"key_1_1": "config 1", "key_1_2": "test env var = ${test_var_1}"},
        "config2": {
            "key_2_1": "config 2",
            "key_2_2": "test env var = ${test_var_2}",
            "key_2_3": {"key_2_3_1": {"key_2_3_1_1": {"key_2_3_1_1_1": "result"}}},
        },
    }

    # Create configuration object
    config = ConfigFactory().create(data)

    # 1. Display all configurations
    print("1. All configurations:")
    print(config.all())

    # 2. Access configuration values
    print("\n2. Access configuration values:")

    # Access simple key
    config_key = "config1"
    print(f"Config key: {config_key}")
    print(config.get(config_key))

    # Access nested key
    config_key = "config2.key_2_2"
    print(f"\nConfig key: {config_key}")
    print(config.get(config_key))

    # Access deeply nested key
    config_key = "config2.key_2_3.key_2_3_1.key_2_3_1_1.key_2_3_1_1_1"
    print(f"\nConfig key: {config_key}")
    print(config.get(config_key))

    # 3. Access with default value
    print("\n3. Access with default value:")
    config_key = "config1.test"
    print(f"Config key: {config_key}")
    print(config.get(config_key, "default"))


if __name__ == "__main__":
    main()
