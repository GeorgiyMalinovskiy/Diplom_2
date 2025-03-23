# Тесты API Stellar Burgers

Этот проект содержит автоматизированные тесты для API сервиса Stellar Burgers.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

Для запуска тестов с генерацией отчета Allure:

```bash
pytest --alluredir=target/allure-results
```

## Генерация отчета Allure

```bash
allure serve target/allure-results
```

## Структура проекта

- `configuration.py` - конфигурационные параметры
- `helpers.py` - вспомогательные функции
- `tests/` - тесты API сервиса
