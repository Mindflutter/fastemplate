PROJECT_NAME = fastemplate
DOCKER_BUILD_TAG = $(USER)-$(shell git rev-parse --short HEAD)
REPORTS_DIR = ./tmp

test:
	export COVERAGE_FILE=$(REPORTS_DIR)/.coverage && \
	poetry run pytest --junitxml=$(REPORTS_DIR)/junit.xml \
					  --cov-report term-missing \
					  --cov-report xml:$(REPORTS_DIR)/coverage.xml \
					  --cov=src tests

pylint:
	find . -type f -name "*.py" | xargs poetry run pylint

mypy:
	poetry run mypy .

black:
	poetry run black .

isort:
	poetry run isort .

docformatter:
	poetry run docformatter --recursive --in-place --wrap-summaries 120 --wrap-descriptions 120 .

# all formatters (note: this modifies files in-place)
format: black isort docformatter

# all linters
lint: pylint mypy

cleanup:
	rm -r ./tmp

build-local:
	docker build -t $(PROJECT_NAME):$(DOCKER_BUILD_TAG) .

# run only service in a container
# XXX: run the DB in the same network or make sure external DB is accessible
run-local-svc: build-local
	docker rm -f $(PROJECT_NAME)
	docker run -d --name $(PROJECT_NAME) $(PROJECT_NAME):$(DOCKER_BUILD_TAG)

# run all via docker-compose
run-local:
	docker-compose up -d --build --force-recreate
