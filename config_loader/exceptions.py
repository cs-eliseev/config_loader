"""
Exceptions for the config_loader package.
"""


class ConfigError(Exception):
    """Base exception for configuration errors."""


class ValidationError(ConfigError):
    """Exception raised when configuration validation fails."""


class ConfigFileNotFoundError(ConfigError):
    """Exception raised when a configuration file is not found."""
