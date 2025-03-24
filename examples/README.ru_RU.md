[English](https://github.com/cs-eliseev/config_loader/blob/master/examples/README.md) | Русский

# Примеры использования config_loader

Этот каталог содержит примеры использования библиотеки config_loader. Примеры разделены по категориям для лучшего понимания функциональности.

## Структура каталогов

```
examples/
├── basic/           # Базовые примеры использования
├── advanced/        # Продвинутые примеры
├── integration/     # Примеры интеграции
├── security/        # Примеры работы с безопасностью
└── performance/     # Примеры оптимизации производительности
```

## Категории примеров

### Basic
- `config_example.py` - Базовый пример работы с конфигурациями
- `env_example.py` - Пример работы с переменными окружения
- `yaml_example.py` - Пример работы с YAML файлами

### Advanced
- `validation_example.py` - Примеры валидации конфигураций
- `nested_config_example.py` - Работа с вложенными конфигурациями
- `dynamic_config_example.py` - Работа с динамическими конфигурациями

### Integration
- `multi_format_example.py` - Работа с разными форматами (JSON, YAML, INI)
- `migration_example.py` - Примеры миграции между версиями
- `error_handling_example.py` - Обработка ошибок

### Security
- `secrets_example.py` - Работа с секретами
- `access_control_example.py` - Управление доступом
- `encryption_example.py` - Шифрование конфигураций

### Performance
- `caching_example.py` - Кэширование конфигураций
- `async_loading_example.py` - Асинхронная загрузка
- `optimization_example.py` - Оптимизация больших конфигураций

## Как использовать примеры

1. Убедитесь, что у вас установлены все зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите нужный пример:
   ```bash
   python examples/basic/config_example.py
   ```

3. Скрипт для запуска примеров использованияЖ
   ```bash
   ./utils/examples.sh
   ```
## Примечания

- Все примеры содержат подробные комментарии
- Каждый пример демонстрирует определенный аспект функциональности
- Для работы с секретами и шифрованием требуется дополнительная настройка 