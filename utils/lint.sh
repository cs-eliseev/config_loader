#!/bin/bash

echo "Running black..."
black --check . || exit 1

echo "Running isort..."
isort --check-only . || exit 1

echo "Running flake8..."
flake8 . || exit 1

echo "Running mypy..."
mypy config_loader/ || exit 1

echo "Running pylint..."
pylint config_loader/ || exit 1

echo "All checks passed successfully!" 