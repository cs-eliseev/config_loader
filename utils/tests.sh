#!/bin/bash

# Path to virtual environment
VENV_PATH=".venv"

# Activate virtual environment if not activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    if [ ! -d "$VENV_PATH" ]; then
        echo "Creating virtual environment..."
        python -m venv $VENV_PATH
    fi
    echo "Activating virtual environment..."
    source $VENV_PATH/bin/activate
fi

# Check for required packages
python -c "import pytest" 2>/dev/null || pip install pytest
python -c "import coverage" 2>/dev/null || pip install coverage
python -c "import pytest_cov" 2>/dev/null || pip install pytest-cov

# Run tests with verbose output
echo "Running tests..."
python -m pytest tests/ -v 