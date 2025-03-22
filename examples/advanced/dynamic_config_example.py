"""
Example of working with dynamic configurations.
Demonstrates how to create and update configurations at runtime.
"""

from typing import Any, Dict

from config_loader.config import ConfigFactory
from config_loader.env import EnvFactory


class DynamicConfigManager:
    """Manager for working with dynamic configurations."""

    def __init__(self):
        self.config_factory = ConfigFactory()
        self.env_factory = EnvFactory()
        self.config = self.config_factory.create({})
        self.env = self.env_factory.create()

    def update_config(self, new_values: Dict[str, Any]) -> None:
        """Updates configuration with new values."""
        current_config = self.config.all()
        current_config.update(new_values)
        self.config = self.config_factory.create(current_config)

    def add_environment_variables(self) -> None:
        """Adds environment variables to configuration."""
        env_vars = {
            "app_name": self.env.get("APP_NAME", "DefaultApp"),
            "debug_mode": self.env.get("DEBUG_MODE", "false").lower() == "true",
            "api_key": self.env.get("API_KEY", ""),
        }
        self.update_config({"environment": env_vars})

    def add_runtime_settings(self) -> None:
        """Adds runtime settings."""
        runtime_settings = {
            "runtime": {
                "timestamp": "2024-03-20T12:00:00",
                "memory_usage": "512MB",
                "active_users": 100,
            },
        }
        self.update_config(runtime_settings)


def main():
    # Create dynamic configuration manager
    manager = DynamicConfigManager()

    # Initialize base configuration
    initial_config = {
        "version": "1.0.0",
        "features": {
            "cache": True,
            "logging": True,
        },
    }
    manager.update_config(initial_config)
    print("1. Initial configuration:")
    print(manager.config.all())

    # Add environment variables
    manager.add_environment_variables()
    print("\n2. Configuration with environment variables:")
    print(manager.config.all())

    # Add runtime settings
    manager.add_runtime_settings()
    print("\n3. Configuration with runtime settings:")
    print(manager.config.all())

    # Update individual values
    manager.update_config(
        {
            "features": {
                "cache": False,
                "logging": True,
                "new_feature": True,
            },
        },
    )
    print("\n4. Updated configuration:")
    print(manager.config.all())

    # Demonstrate access to nested values
    print("\n5. Access to nested values:")
    print(f"Version: {manager.config.get('version')}")
    print(f"Debug mode: {manager.config.get('environment.debug_mode')}")
    print(f"Active users: {manager.config.get('runtime.active_users')}")


if __name__ == "__main__":
    main()
