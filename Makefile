APP_PATH=./application
TEST_PATH=./tests

init:
	pip install poetry
	poetry install

pre-commit:
	pre-commit install

black:
	black application/

test:
	cd $(APP_PATH) && poetry run python -m pytest --cov=application --verbose --color=yes $(TEST_PATH)

compose_build:
	docker-compose -f docker/docker-compose-dev.yml build

compose_up:
	docker-compose -f docker/docker-compose-dev.yml up

compose_stop:
	docker-compose -f docker/docker-compose-dev.yml stop

compose_destroy:
	docker-compose -f docker/docker-compose-dev.yml rm

compose_shell:
	docker-compose -f docker/docker-compose-dev.yml run --rm api bash
