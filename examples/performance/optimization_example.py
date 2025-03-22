"""
Example of optimizing large configurations.
Demonstrates various optimization techniques for working with large configurations.
"""

import time
from typing import Any, Dict, List

from config_loader.config import ConfigFactory


class OptimizedConfig:
    """Optimized configuration."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize optimized configuration."""
        self.config = ConfigFactory().create(config)
        self._path_cache: Dict[str, Any] = {}
        self._lazy_loaded: Dict[str, bool] = {}

    def _split_path(self, path: str) -> List[str]:
        """Split path into components."""
        return path.split(".")

    def _build_path_cache(self, path: str) -> None:
        """Build cache for path."""
        if path in self._path_cache:
            return

        parts = self._split_path(path)
        current = self.config.all()

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = None
                break

        self._path_cache[path] = current

    def get(self, path: str, default: Any = None) -> Any:
        """Get value with optimized access."""
        # Check cache
        if path in self._path_cache:
            return self._path_cache[path]

        # Build cache
        self._build_path_cache(path)
        return self._path_cache.get(path, default)

    def lazy_load(self, path: str) -> Any:
        """Lazy load value."""
        if path not in self._lazy_loaded:
            self._build_path_cache(path)
            self._lazy_loaded[path] = True
        return self._path_cache.get(path)

    def preload_paths(self, paths: List[str]) -> None:
        """Preload paths."""
        for path in paths:
            self._build_path_cache(path)

    def clear_cache(self) -> None:
        """Clear cache."""
        self._path_cache.clear()
        self._lazy_loaded.clear()


def generate_large_config(size: int = 1000) -> Dict[str, Any]:
    """Generate large test configuration."""
    config = {}
    for i in range(size):
        config[f"section_{i}"] = {f"key_{j}": f"value_{i}_{j}" for j in range(10)}
    return config


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
def test_config_access(config: OptimizedConfig, path: str, iterations: int = 1000) -> None:
    """Test configuration access."""
    for _ in range(iterations):
        config.get(path)


def main():
    # Generate large configuration
    print("Generating test configuration...")
    large_config = generate_large_config(1000)

    # Create optimized configuration
    optimized_config = OptimizedConfig(large_config)

    # Test performance without optimization
    print("\n1. Test performance without optimization:")
    test_config_access(optimized_config, "section_0.key_0")

    # Test performance with optimization
    print("\n2. Test performance with optimization:")
    test_config_access(optimized_config, "section_0.key_0")

    # Test lazy load
    print("\n3. Test lazy load:")
    print("First load:")
    test_config_access(optimized_config, "section_100.key_5")

    print("\nRepeat load (from cache):")
    test_config_access(optimized_config, "section_100.key_5")

    # Test preload
    print("\n4. Test preload:")
    paths_to_preload = [
        "section_0.key_0",
        "section_100.key_5",
        "section_500.key_2",
        "section_999.key_9",
    ]

    print("Preload paths...")
    optimized_config.preload_paths(paths_to_preload)

    print("\nAccess to preloaded paths:")
    for path in paths_to_preload:
        test_config_access(optimized_config, path)

    # Test cache clear
    print("\n5. Test cache clear:")
    print("Access before clear:")
    test_config_access(optimized_config, "section_0.key_0")

    optimized_config.clear_cache()
    print("\nAccess after clear:")
    test_config_access(optimized_config, "section_0.key_0")

    # Demonstrate real scenario usage
    print("\n6. Real scenario usage:")
    real_config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {"debug": True, "log_level": "INFO"},
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb",
            "users": {
                "admin": {"password": "secret123", "permissions": ["read", "write", "admin"]},
                "user": {"password": "user123", "permissions": ["read"]},
            },
        },
    }

    optimized_real_config = OptimizedConfig(real_config)

    # Preload frequently used paths
    optimized_real_config.preload_paths(
        ["app.name", "app.version", "database.host", "database.port"]
    )

    print("\nAccess to frequently used paths:")
    print(f"Application name: {optimized_real_config.get('app.name')}")
    print(f"Database host: {optimized_real_config.get('database.host')}")

    # Lazy load rarely used paths
    print("\nLazy load rarely used paths:")
    print(f"User permissions: {optimized_real_config.lazy_load('database.users.user.permissions')}")


if __name__ == "__main__":
    main()
