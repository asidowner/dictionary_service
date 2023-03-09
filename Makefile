MANAGE := poetry run python manage.py

.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: migrations
migrations:
	@$(MANAGE) makemigrations

.PHONE: create_superuser
create_superuser:
	@$(MANAGE) createsuperuser

.PHONY: setup
setup: install migrate create_superuser

.PHONY: start
start:
	@$(MANAGE) runserver localhost:8000

.PHONY: lint
lint:
	poetry run flake8

mypy:
	poetry run mypy manage.py server
	poetry run mypy tests

.PHONY: test
test:
	poetry run pytest --cov-fail-under=90

django-check:
	@$(MANAGE) check --fail-level WARNING

django-check-production:
	export DJANGO_ENV=production && $(MANAGE) check --deploy --fail-level WARNING

migration-check:
	@$(MANAGE) makemigrations --dry-run --check

safety-check:
	poetry run safety check --full-report --ignore=51457

poetry-check:
	poetry check

pip-check:
	poetry run pip check

.PHONY: check
check: lint mypy test django-check django-check-production migration-check safety-check poetry-check pip-check requirements.txt

.PHONY: secretkey
secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(60))'

.PHONY: transprepare
transprepare:
	@$(MANAGE) makemessages --all --add-location file

.PHONY: transcompile
transcompile:
	@$(MANAGE) compilemessages

.PHONY: requirements.txt
requirements.txt:
	poetry export --format requirements.txt --output requirements/base.txt --without-hashes --without dev
	poetry export --format requirements.txt --output requirements/local.txt --with dev --without-hashes