"""
Example of working with secrets in configurations.
Demonstrates secure storage and usage of secret data.
"""

import os
from typing import Any, Dict

from cryptography.fernet import Fernet

from config_loader.config import ConfigFactory


class SecretsManager:
    """Manager for working with secrets in configurations."""

    def __init__(self, encryption_key: str = None):
        """Initialize secrets manager."""
        self.encryption_key = encryption_key or os.getenv("ENCRYPTION_KEY")
        if not self.encryption_key:
            self.encryption_key = Fernet.generate_key()
            print(f"Generated new encryption key: {self.encryption_key.decode()}")
        self.cipher_suite = Fernet(self.encryption_key)

    def encrypt_value(self, value: str) -> str:
        """Encrypts value."""
        return self.cipher_suite.encrypt(value.encode()).decode()

    def decrypt_value(self, encrypted_value: str) -> str:
        """Decrypts value."""
        return self.cipher_suite.decrypt(encrypted_value.encode()).decode()

    def encrypt_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypts secret values in configuration."""
        encrypted_config = config.copy()

        # List of fields to encrypt
        secret_fields = ["password", "api_key", "token", "secret"]

        def encrypt_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            result = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    result[key] = encrypt_dict(value)
                elif isinstance(value, str) and any(
                    secret in key.lower() for secret in secret_fields
                ):
                    result[key] = self.encrypt_value(value)
                else:
                    result[key] = value
            return result

        return encrypt_dict(encrypted_config)

    def decrypt_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypts secret values in configuration."""
        decrypted_config = config.copy()

        # List of fields to decrypt
        secret_fields = ["password", "api_key", "token", "secret"]

        def decrypt_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            result = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    result[key] = decrypt_dict(value)
                elif isinstance(value, str) and any(
                    secret in key.lower() for secret in secret_fields
                ):
                    try:
                        result[key] = self.decrypt_value(value)
                    except Exception:
                        result[key] = value  # If decryption fails, keep as is
                else:
                    result[key] = value
            return result

        return decrypt_dict(decrypted_config)


def main():
    # Create secrets manager
    secrets_manager = SecretsManager()

    # Create configuration with secrets
    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "secret123",
        },
        "api": {
            "url": "https://api.example.com",
            "api_key": "sk_live_123456789",
            "secret": "super_secret_key",
        },
        "jwt": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        },
    }

    print("1. Original configuration:")
    print(config)

    # Encrypt configuration
    encrypted_config = secrets_manager.encrypt_config(config)
    print("\n2. Encrypted configuration:")
    print(encrypted_config)

    # Create configuration object with encrypted data
    config_obj = ConfigFactory().create(encrypted_config)

    # Try to access encrypted values
    print("\n3. Attempt to access encrypted values:")
    print(f"Database password: {config_obj.get('database.password')}")
    print(f"API key: {config_obj.get('api.api_key')}")

    # Decrypt configuration
    decrypted_config = secrets_manager.decrypt_config(encrypted_config)
    print("\n4. Decrypted configuration:")
    print(decrypted_config)

    # Create configuration object with decrypted data
    decrypted_config_obj = ConfigFactory().create(decrypted_config)

    # Access decrypted values
    print("\n5. Access to decrypted values:")
    print(f"Database password: {decrypted_config_obj.get('database.password')}")
    print(f"API key: {decrypted_config_obj.get('api.api_key')}")

    # Demonstrate secure key storage
    print("\n6. Secure key storage:")
    print("Encryption key can be stored in environment variable:")
    print(f"export ENCRYPTION_KEY='{secrets_manager.encryption_key.decode()}'")


if __name__ == "__main__":
    main()
