SERVICE_DIR = fastemplate
DOCKER_BUILD_TAG = $(USER)-$(shell git rev-parse --short HEAD)
REPORTS_DIR = ./tmp

setup:
	@poetry install --no-root

lint:
	@poetry run ruff check --fix --exit-non-zero-on-fix .
	@poetry run mypy $(SERVICE_DIR)/

format:
	@poetry run ruff format .

test:
	export COVERAGE_FILE=$(REPORTS_DIR)/.coverage && \
	poetry run pytest --junitxml=$(REPORTS_DIR)/junit.xml \
					  --cov-report term-missing \
					  --cov-report xml:$(REPORTS_DIR)/coverage.xml \
					  --cov=$(SERVICE_DIR) tests

clean:
	rm -rf ./tmp
	find . -type d -name "__pycache__" -print -exec rm -rv {} +

build-local:
	docker build -t $(SERVICE_DIR):$(DOCKER_BUILD_TAG) .
