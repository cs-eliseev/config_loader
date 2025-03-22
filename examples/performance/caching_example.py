"""
Example of configuration caching.
Demonstrates how to optimize access to configurations using caching.
"""

import json
import time
from functools import lru_cache
from typing import Any, Dict, Optional

from config_loader.config import ConfigFactory


class CachedConfig:
    """Configuration with caching."""

    def __init__(self, config: Dict[str, Any], cache_ttl: int = 60):
        """Initialize configuration with caching."""
        self.config = ConfigFactory().create(config)
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple[Any, float]] = {}

    def _get_cached_value(self, path: str) -> Optional[Any]:
        """Get value from cache."""
        if path in self._cache:
            value, timestamp = self._cache[path]
            if time.time() - timestamp < self.cache_ttl:
                return value
        return None

    def _set_cached_value(self, path: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[path] = (value, time.time())

    def get(self, path: str, default: Any = None) -> Any:
        """Get value with caching."""
        # Check cache
        cached_value = self._get_cached_value(path)
        if cached_value is not None:
            return cached_value

        # Get value from configuration
        value = self.config.get(path, default)

        # Save to cache
        self._set_cached_value(path, value)
        return value

    def invalidate_cache(self, path: Optional[str] = None) -> None:
        """Invalidate cache."""
        if path:
            self._cache.pop(path, None)
        else:
            self._cache.clear()


@lru_cache(maxsize=100)
def get_cached_config(config_dict_str: str) -> CachedConfig:
    """Create cached configuration object."""
    config_dict = json.loads(config_dict_str)
    return CachedConfig(config_dict)


def measure_time(func):
    """Decorator for measuring execution time."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.6f} sec")
        return result

    return wrapper


@measure_time
def test_config_access(config: CachedConfig, path: str, iterations: int = 1000) -> None:
    """Test configuration access."""
    for _ in range(iterations):
        config.get(path)


def main():
    # Create test configuration
    config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {
                "debug": True,
                "log_level": "INFO",
            },
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb",
        },
        "api": {
            "url": "https://api.example.com",
            "endpoints": {
                "users": "/api/v1/users",
                "auth": "/api/v1/auth",
            },
        },
    }

    # Create cached configuration
    cached_config = CachedConfig(config)

    # Test performance with caching
    print("1. Testing performance with caching:")
    print("\nFirst access (without cache):")
    test_config_access(cached_config, "app.name")

    print("\nRepeated access (with cache):")
    test_config_access(cached_config, "app.name")

    # Test cache invalidation
    print("\n2. Testing cache invalidation:")
    print("\nAccess before invalidation:")
    test_config_access(cached_config, "database.host")

    cached_config.invalidate_cache("database.host")
    print("\nAccess after invalidation:")
    test_config_access(cached_config, "database.host")

    # Test caching with decorator
    print("\n3. Testing caching with decorator:")
    config_str = json.dumps(config, sort_keys=True)
    config1 = get_cached_config(config_str)
    config2 = get_cached_config(config_str)

    print("\nCreating first object:")
    test_config_access(config1, "api.url")

    print("\nCreating second object (should be from cache):")
    test_config_access(config2, "api.url")

    # Test access to nested values
    print("\n4. Testing access to nested values:")
    print("\nFirst access to nested value:")
    test_config_access(cached_config, "app.settings.log_level")

    print("\nRepeated access to nested value:")
    test_config_access(cached_config, "app.settings.log_level")

    # Test full cache invalidation
    print("\n5. Testing full cache invalidation:")
    cached_config.invalidate_cache()
    print("\nAccess after full invalidation:")
    test_config_access(cached_config, "app.name")


if __name__ == "__main__":
    main()
