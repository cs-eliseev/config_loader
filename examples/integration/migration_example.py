"""
Example of configuration version migration.
Demonstrates how to update configurations when their structure changes.
"""

from typing import Any, Dict

from config_loader.config import ConfigFactory


class ConfigMigrationManager:
    """Manager for migrating configurations between versions."""

    def __init__(self):
        self.config_factory = ConfigFactory()

    def migrate_v1_to_v2(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Migrates configuration from version 1 to version 2."""
        # Create configuration copy
        new_config = config.copy()

        # Update structure
        if "database" in new_config:
            # Move database settings to new structure
            db_config = new_config.pop("database")
            new_config["databases"] = {
                "primary": db_config,
                "replica": {
                    "host": db_config.get("host", "localhost"),
                    "port": db_config.get("port", 5432),
                    "name": f"{db_config.get('name', 'db')}_replica",
                },
            }

        # Update version
        new_config["version"] = "2.0.0"
        return new_config

    def migrate_v2_to_v3(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Migrates configuration from version 2 to version 3."""
        # Create configuration copy
        new_config = config.copy()

        # Update structure
        if "databases" in new_config:
            # Add new database settings
            for db_name, db_config in new_config["databases"].items():
                db_config["pool_size"] = 10
                db_config["timeout"] = 30

        # Update version
        new_config["version"] = "3.0.0"
        return new_config

    def get_version(self, config: Dict[str, Any]) -> str:
        """Gets configuration version."""
        return config.get("version", "1.0.0")

    def migrate(self, config: Dict[str, Any], target_version: str) -> Dict[str, Any]:
        """Migrates configuration to target version."""
        current_version = self.get_version(config)

        if current_version == target_version:
            return config

        # Determine required migrations
        migrations = []
        if current_version == "1.0.0" and target_version in ["2.0.0", "3.0.0"]:
            migrations.append(self.migrate_v1_to_v2)
        if current_version == "2.0.0" and target_version == "3.0.0":
            migrations.append(self.migrate_v2_to_v3)

        # Apply migrations
        result = config
        for migration in migrations:
            result = migration(result)

        return result


def main():
    # Create migration manager
    migration_manager = ConfigMigrationManager()

    # Create version 1.0.0 configuration
    v1_config = {
        "version": "1.0.0",
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb",
        },
        "app": {
            "name": "MyApp",
            "debug": True,
        },
    }

    print("1. Version 1.0.0 configuration:")
    print(v1_config)

    # Migrate to version 2.0.0
    v2_config = migration_manager.migrate(v1_config, "2.0.0")
    print("\n2. Configuration after migration to version 2.0.0:")
    print(v2_config)

    # Migrate to version 3.0.0
    v3_config = migration_manager.migrate(v2_config, "3.0.0")
    print("\n3. Configuration after migration to version 3.0.0:")
    print(v3_config)

    # Create configuration objects for demonstration
    config_v1 = migration_manager.config_factory.create(v1_config)
    config_v2 = migration_manager.config_factory.create(v2_config)
    config_v3 = migration_manager.config_factory.create(v3_config)

    print("\n4. Access to values in different versions:")
    print("Version 1.0.0:")
    print(f"Database: {config_v1.get('database.name')}")
    print("\nVersion 2.0.0:")
    print(f"Primary DB: {config_v2.get('databases.primary.name')}")
    print(f"Replica DB: {config_v2.get('databases.replica.name')}")
    print("\nVersion 3.0.0:")
    print(f"Primary DB pool size: {config_v3.get('databases.primary.pool_size')}")
    print(f"Replica DB timeout: {config_v3.get('databases.replica.timeout')}")


if __name__ == "__main__":
    main()
