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
python -c "import black" 2>/dev/null || pip install black
python -c "import isort" 2>/dev/null || pip install isort
python -c "import flake8" 2>/dev/null || pip install flake8
python -c "import mypy" 2>/dev/null || pip install mypy
python -c "import pylint" 2>/dev/null || pip install pylint

# Run linting tools
echo "Running code formatters and linters..."

echo "Running black (code formatter)..."
black --check . || exit 1

echo "Running isort (import sorter)..."
isort --check-only . || exit 1

echo "Running flake8 (style guide checker)..."
flake8 . || exit 1

echo "Running mypy (type checker)..."
mypy config_loader/ || exit 1

echo "Running pylint (code analyzer)..."
pylint config_loader/ || exit 1

echo "All checks passed successfully!" 