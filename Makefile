APP_PATH=./application
TEST_PATH=./tests

init:
	pip install poetry
	poetry install

check-unused-code:
	vulture $(APP_PATH)

check-mypy:
	mypy $(APP_PATH)

check-pre-commit-hooks:
	poetry run pre-commit install && poetry run pre-commit run --all-files

run:
	cd application && uvicorn server.app:app --host 0.0.0.0 --port=8888

test:
	cd $(APP_PATH) && poetry run python -m pytest --cov=. --cov-report=xml --cov-append --no-cov-on-fail --verbose --color=yes $(TEST_PATH)

compose_build:
	docker-compose -f docker/docker-compose-dev.yml build

compose_up:
	docker-compose -f docker/docker-compose-dev.yml up

compose_stop:
	docker-compose -f docker/docker-compose-dev.yml stop

compose_destroy:
	docker-compose -f docker/docker-compose-dev.yml down

compose_shell:
	docker-compose -f docker/docker-compose-dev.yml run --rm api bash
