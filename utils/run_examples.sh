#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для запуска примера
run_example() {
    echo -e "${BLUE}Running $1...${NC}"
    echo "----------------------------------------"
    PYTHONPATH=$PYTHONPATH:$(pwd) python3 "examples/$1"
    echo "----------------------------------------"
    echo -e "${GREEN}Finished $1${NC}\n"
}

# Переходим в корневую директорию проекта
cd "$(dirname "$0")/.." || exit 1

# Запускаем все примеры
run_example "env_example.py"
run_example "yaml_example.py"
run_example "config_example.py"
run_example "utils_config_example.py"
run_example "utils_configs_example.py"

echo -e "${GREEN}All examples completed successfully!${NC}" 