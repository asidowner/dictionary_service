# dictionary-service

[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/GB6Eki?referralCode=U5zXSw)

## Admin link:
[<img src="https://img.shields.io/website?label=Admin%20link&up_message=online&url=https%3A%2F%2Fdictionaryservice-production.up.railway.app%2Fadmin%2F">](https://dictionaryservice-production.up.railway.app/admin/)

## Swagger:
[<img src="https://img.shields.io/swagger/valid/3.0?specUrl=https://dictionaryservice-production.up.railway.app/api/schema/">](https://dictionaryservice-production.up.railway.app/api/schema/swagger-ui/)

## Разработка:

### Локальные переменные

Путь: config/.env. См. config/.env.example

### DJANGO_ENV

Допустимые значения:
* development
* local
* production

Для добавления дополнительных конфигураций см. server/settings/__init__.py

### Запуск:

Предварительно добавить файл server/settings/environments/local.py.
Используется для переопределения настройки локально

```shell
export DJANGO_ENV=development && make start

export DJANGO_ENV=local && make start
```

### Валидация проекта:

```shell
make check
```

Проверки:

* flake8, см. https://github.com/wemake-services/wemake-python-styleguide
* mypy - https://mypy.readthedocs.io/en/stable/
* pytest - https://docs.pytest.org/en/7.2.x/
* django-check - https://docs.djangoproject.com/en/4.1/ref/django-admin/#check
* migrations-check - https://docs.djangoproject.com/en/4.1/ref/django-admin/#makemigrations
* safety - https://docs.pyup.io/docs/getting-started-with-safety-cli
* poetry check - https://python-poetry.org/docs/cli/#check
* pip check - https://pip.pypa.io/en/stable/cli/pip_check/
