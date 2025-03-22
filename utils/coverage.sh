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

# Clean previous reports
rm -rf htmlcov/
rm -f .coverage

# Run tests with coverage
echo "Running tests with coverage..."
python -m pytest tests/ --cov=config_loader --cov-report=term-missing --cov-report=html

# Check if HTML report was created
if [ -d "htmlcov" ]; then
    echo -e "\nHTML coverage report has been created in htmlcov/"
    echo "To view the report, open htmlcov/index.html in your browser"
else
    echo "Error: Failed to create HTML report"
    exit 1
fi 