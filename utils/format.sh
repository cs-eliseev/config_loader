#!/bin/bash

echo "Running code formatters..."
echo "Running black..."
black .

echo -e "\nRunning isort..."
isort .

echo -e "\nFormatting completed!" 