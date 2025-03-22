import os

import pytest


@pytest.fixture(autouse=True)
def clean_env():
    """Cleans environment variables before each test."""
    # Save original environment variables
    original_env = dict(os.environ)

    # Clean all test variables
    for key in list(os.environ.keys()):
        if key.startswith(("TEST_", "DB_", "APP_")):
            del os.environ[key]

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
