"""
Example of configuration validation using various schemas and rules.
Demonstrates how to validate configurations before using them.
"""

from typing import Any, Dict

from config_loader.config import ConfigFactory
from config_loader.validators import ConfigValidator, ValidationError


class DatabaseConfigValidator(ConfigValidator):
    """Validator for database configuration."""

    def validate(self, config: Dict[str, Any]) -> None:
        """Validates database configuration."""
        required_fields = ["host", "port", "database"]

        for field in required_fields:
            if field not in config:
                raise ValidationError(f"Missing required field: {field}")

        if not isinstance(config["port"], int):
            raise ValidationError("Port must be an integer")

        if not config["host"]:
            raise ValidationError("Host cannot be empty")


def main():
    # Example of valid configuration
    valid_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "database": "mydb",
        },
    }

    # Example of invalid configuration
    invalid_config = {
        "database": {
            "host": "",
            "port": "5432",  # string instead of integer
            # missing database field
        },
    }

    # Create configurations
    config_factory = ConfigFactory()
    valid_config_obj = config_factory.create(valid_config)
    invalid_config_obj = config_factory.create(invalid_config)

    # Create validator
    validator = DatabaseConfigValidator()

    try:
        # Validate correct configuration
        validator.validate(valid_config_obj.get("database"))
        print("✅ Valid configuration passed validation")

        # Validate incorrect configuration
        validator.validate(invalid_config_obj.get("database"))
    except ValidationError as e:
        print(f"❌ Validation error: {str(e)}")


if __name__ == "__main__":
    main()
