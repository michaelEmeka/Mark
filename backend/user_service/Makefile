.PHONY: install
install:
	uv sync --locked

.PHONY: install-pre-commit
install-pre-commit:
	uv run pre-commit uninstall; uv run pre-commit install

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: migrate
migrate:
	uv run python manage.py migrate

.PHONY: migrations
migrations:
	uv run python manage.py makemigrations

.PHONY: run-server
run-server:
	uv run python manage.py runserver

.PHONY: run_mqtt_worker
run_mqtt_worker:
	uv run manage.py run_mqtt_worker

.PHONY: shell
shell:
	uv run python manage.py shell

.PHONY: superuser
superuser:
	uv run python manage.py createsuperuser

.PHONY: test
test:
	uv run pytest -v -rs -n auto --show-capture=no

.PHONY: up-dependencies-only
up-dependencies-only:
	test -f .env || touch .env
	docker-compose -f docker-compose.dev.yml up --force-recreate db

.PHONY: update
update: install migrate install-pre-commit ;