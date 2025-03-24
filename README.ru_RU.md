[English](https://github.com/cs-eliseev/config_loader/blob/master/README.md) | Русский

# Simple Config Loader

Простой и удобный загрузчик конфигураций для Python-приложений, поддерживающий YAML и переменные окружения.

## Возможности

- Загрузка конфигураций из YAML файлов
- Поддержка переменных окружения
- Типизация данных
- Простой и понятный API
- Поддержка вложенных конфигураций
- Обработка ошибок

## Установка

### Напрямую из GitHub

```bash
pip install git+https://github.com/cs-eliseev/config_loader/config-loader.git
```

## Использование

### Загрузка YAML конфигурации

```python
from pathlib import Path
from config_loader import ConfigFactory

config = ConfigFactory.create_by_path(Path('config.yaml'))
value = config.get('some.nested.key')

configs = ConfigFactory.create_by_path(Path('config_dir/'))
value = configs.get('some.nested.key')
```

### Работа с переменными окружения

```python
from config_loader import EnvFactory

env = EnvFactory.create('.env')
value = env.get('ENV_VARIABLE')

all_vars = env.all()

data = {
    'db_url': '${DATABASE_URL:sqlite:///default.db}',
    'api_key': '${API_KEY}'
}
processed_data = env.replace_vars(data)
```

### Комбинированное использование

```python
from pathlib import Path
from config_loader import ConfigFactory

config = ConfigFactory.create_by_path(
    yaml_config_path=Path('config.yaml'),
    env_path='.env'
)
value = config.get('database.url')
```

### Подробные примеры

Для более детального знакомства с возможностями библиотеки, посмотрите [примеры использования](examples/README.md), которые включают:
- Базовые примеры
- Продвинутые сценарии использования
- Интеграционные примеры
- Примеры безопасности
- Тесты производительности

## Разработка

### Требования

- Python 3.8+
- Зависимости указаны в `requirements.txt`
- Для разработки: зависимости из `dev-requirements.txt`

### Установка зависимостей для разработки

```bash
pip install -r dev-requirements.txt
```

### Запуск тестов

```bash
pytest
```

### Проверка типов

```bash
mypy .
```

### Линтинг

```bash
flake8
pylint config_loader
```

### Утилиты для разработки

В папке `utils/` находятся скрипты для автоматизации различных задач разработки:

- `lint.sh` - запускает все проверки кода (black, isort, flake8, mypy, pylint)
- `format.sh` - форматирует код с помощью black и isort
- `tests.sh` - запускает тесты с подробным выводом
- `coverage.sh` - запускает тесты с измерением покрытия кода и генерирует HTML-отчет
- `examples.sh` - скрипт для запуска примеров использования

Все скрипты автоматически создают и активируют виртуальное окружение при необходимости.

## Лицензия

MIT License - см. файл [LICENSE](LICENSE) для подробностей.