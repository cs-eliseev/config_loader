"""
Example of access control for configurations.
Demonstrates how to implement access control for different parts of configuration.
"""

from enum import Enum
from typing import Any, Dict, List

from config_loader.config import ConfigFactory


class AccessLevel(Enum):
    """Access levels for configuration."""

    PUBLIC = 1  # Public access
    INTERNAL = 2  # Internal access
    PRIVATE = 3  # Private access
    SECRET = 4  # Secret access


class AccessControlConfig:
    """Configuration with access control."""

    def __init__(self, config: Dict[str, Any], access_rules: Dict[str, AccessLevel]):
        """Initialize configuration with access rules."""
        self.config = ConfigFactory().create(config)
        self.access_rules = access_rules
        self._user_access_level = AccessLevel.PUBLIC

    def set_user_access_level(self, level: AccessLevel) -> None:
        """Sets user access level."""
        self._user_access_level = level

    def can_access(self, path: str) -> bool:
        """Checks if user can access the path."""
        # Get access level for path
        path_level = self.access_rules.get(path, AccessLevel.PUBLIC)

        # Check if user's access level is sufficient
        return self._user_access_level.value >= path_level.value

    def get(self, path: str, default: Any = None) -> Any:
        """Gets value by path with access check."""
        if not self.can_access(path):
            raise PermissionError(f"No access to {path}")
        return self.config.get(path, default)

    def get_allowed_paths(self) -> List[str]:
        """Returns list of paths accessible to current user."""
        return [
            path
            for path, level in self.access_rules.items()
            if self._user_access_level.value >= level.value
        ]


def main():
    # Create configuration
    config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "description": "My Awesome Application",
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "secret123",
        },
        "api": {
            "url": "https://api.example.com",
            "api_key": "sk_live_123456789",
            "endpoints": {
                "users": "/api/v1/users",
                "auth": "/api/v1/auth",
            },
        },
        "internal": {
            "debug": True,
            "metrics": {
                "enabled": True,
                "interval": 60,
            },
        },
    }

    # Define access rules
    access_rules = {
        "app.name": AccessLevel.PUBLIC,
        "app.version": AccessLevel.PUBLIC,
        "app.description": AccessLevel.PUBLIC,
        "database.host": AccessLevel.INTERNAL,
        "database.port": AccessLevel.INTERNAL,
        "database.username": AccessLevel.PRIVATE,
        "database.password": AccessLevel.SECRET,
        "api.url": AccessLevel.PUBLIC,
        "api.endpoints": AccessLevel.INTERNAL,
        "api.api_key": AccessLevel.SECRET,
        "internal": AccessLevel.PRIVATE,
    }

    # Create configuration with access control
    access_config = AccessControlConfig(config, access_rules)

    # Demonstrate access with different permission levels

    # 1. Public access
    print("1. Public access:")
    access_config.set_user_access_level(AccessLevel.PUBLIC)
    try:
        print(f"Application name: {access_config.get('app.name')}")
        print(f"Version: {access_config.get('app.version')}")
        print(f"Description: {access_config.get('app.description')}")
        print(f"API URL: {access_config.get('api.url')}")
        print("\nAvailable paths:")
        print(access_config.get_allowed_paths())
    except PermissionError as e:
        print(f"Access error: {str(e)}")

    # 2. Internal access
    print("\n2. Internal access:")
    access_config.set_user_access_level(AccessLevel.INTERNAL)
    try:
        print(f"Database host: {access_config.get('database.host')}")
        print(f"Database port: {access_config.get('database.port')}")
        print(f"API endpoints: {access_config.get('api.endpoints')}")
        print("\nAvailable paths:")
        print(access_config.get_allowed_paths())
    except PermissionError as e:
        print(f"Access error: {str(e)}")

    # 3. Private access
    print("\n3. Private access:")
    access_config.set_user_access_level(AccessLevel.PRIVATE)
    try:
        print(f"Database username: {access_config.get('database.username')}")
        print(f"Debug settings: {access_config.get('internal.debug')}")
        print("\nAvailable paths:")
        print(access_config.get_allowed_paths())
    except PermissionError as e:
        print(f"Access error: {str(e)}")

    # 4. Secret access
    print("\n4. Secret access:")
    access_config.set_user_access_level(AccessLevel.SECRET)
    try:
        print(f"Database password: {access_config.get('database.password')}")
        print(f"API key: {access_config.get('api.api_key')}")
        print("\nAvailable paths:")
        print(access_config.get_allowed_paths())
    except PermissionError as e:
        print(f"Access error: {str(e)}")


if __name__ == "__main__":
    main()
