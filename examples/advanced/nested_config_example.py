"""
Example of working with nested configurations.
Demonstrates how to work with deeply nested configuration structures.
"""

from config_loader.config import ConfigFactory


def main():
    # Create a complex nested configuration
    nested_config = {
        "application": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {
                "debug": True,
                "log_level": "INFO",
                "features": {
                    "cache": True,
                    "api": {
                        "enabled": True,
                        "endpoints": {
                            "users": "/api/v1/users",
                            "auth": "/api/v1/auth",
                        },
                    },
                },
            },
        },
    }

    # Create configuration object
    config = ConfigFactory().create(nested_config)

    # Demonstrate various ways to access nested values

    # 1. Direct access using dot notation
    print("1. Direct access:")
    print(f"Application name: {config.get('application.name')}")
    print(f"Version: {config.get('application.version')}")

    # 2. Access to nested settings
    print("\n2. Nested settings:")
    print(f"Debug mode: {config.get('application.settings.debug')}")
    print(f"Log level: {config.get('application.settings.log_level')}")

    # 3. Access to deeply nested values
    print("\n3. Deeply nested values:")
    print(f"Cache enabled: {config.get('application.settings.features.cache')}")
    print(f"API enabled: {config.get('application.settings.features.api.enabled')}")

    # 4. Access to values with default value
    print("\n4. Default values:")
    print(f"Non-existent path: {config.get('application.nonexistent', 'default value')}")

    # 5. Get entire configuration object
    print("\n5. Full configuration:")
    print(config.all())

    # 6. Get part of configuration
    print("\n6. Configuration part:")
    print(config.get("application.settings.features.api"))


if __name__ == "__main__":
    main()
