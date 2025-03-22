"""
Example of asynchronous configuration loading.
Demonstrates how to asynchronously load configurations from different sources.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List

import aiohttp
import yaml

from config_loader.config import ConfigFactory


class AsyncConfigLoader:
    """Asynchronous configuration loader."""

    def __init__(self):
        self.config_factory = ConfigFactory()

    async def load_file(self, file_path: str) -> Dict[str, Any]:
        """Asynchronously loads configuration from a file."""
        loop = asyncio.get_event_loop()

        async def read_file():
            with open(file_path, "r") as f:
                if file_path.endswith(".json"):
                    return json.load(f)
                elif file_path.endswith(".yaml"):
                    return yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported file format: {file_path}")

        return await loop.run_in_executor(None, lambda: asyncio.run(read_file()))

    async def load_url(self, url: str) -> Dict[str, Any]:
        """Asynchronously loads configuration from a URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise ValueError(f"Loading error: {response.status}")

    async def load_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Asynchronously loads multiple configurations from files."""
        tasks = [self.load_file(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Merge results
        merged_config = {}
        for result in results:
            if isinstance(result, Exception):
                print(f"Loading error: {str(result)}")
            else:
                merged_config.update(result)

        return merged_config

    async def load_multiple_sources(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """Asynchronously loads configurations from different sources."""
        tasks = []
        for source in sources:
            if source["type"] == "file":
                tasks.append(self.load_file(source["path"]))
            elif source["type"] == "url":
                tasks.append(self.load_url(source["path"]))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Merge results
        merged_config = {}
        for result in results:
            if isinstance(result, Exception):
                print(f"Loading error: {str(result)}")
            else:
                merged_config.update(result)

        return merged_config


async def main():
    # Create loader
    loader = AsyncConfigLoader()

    # Create test configuration files
    config_dir = Path("examples/resources/configs")
    config_dir.mkdir(parents=True, exist_ok=True)

    # JSON configuration
    json_config = {"app": {"name": "MyApp", "version": "1.0.0"}}
    with open(config_dir / "config1.json", "w") as f:
        json.dump(json_config, f)

    # YAML configuration
    yaml_config = """
    database:
      host: localhost
      port: 5432
      name: mydb
    """
    with open(config_dir / "config2.yaml", "w") as f:
        f.write(yaml_config)

    # Test loading a single file
    print("1. Loading a single file:")
    config = await loader.load_file(str(config_dir / "config1.json"))
    print(config)

    # Test loading multiple files
    print("\n2. Loading multiple files:")
    configs = await loader.load_multiple_files(
        [str(config_dir / "config1.json"), str(config_dir / "config2.yaml")]
    )
    print(configs)

    # Test loading from different sources
    print("\n3. Loading from different sources:")
    sources = [
        {"type": "file", "path": str(config_dir / "config1.json")},
        {"type": "file", "path": str(config_dir / "config2.yaml")},
        {"type": "url", "path": "https://api.example.com/config"},
    ]

    try:
        configs = await loader.load_multiple_sources(sources)
        print(configs)
    except Exception as e:
        print(f"Error loading from URL: {str(e)}")

    # Create configuration object
    config_obj = loader.config_factory.create(configs)

    # Demonstrate access to values
    print("\n4. Access to values:")
    print(f"Application name: {config_obj.get('app.name')}")
    print(f"Database host: {config_obj.get('database.host')}")

    # Clean up test files
    for file in config_dir.glob("*"):
        file.unlink()
    config_dir.rmdir()


if __name__ == "__main__":
    asyncio.run(main())
