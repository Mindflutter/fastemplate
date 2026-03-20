SERVICE_DIR = fastemplate
DOCKER_BUILD_TAG = $(USER)-$(shell git rev-parse --short HEAD)
REPORTS_DIR = ./tmp

setup:
	@uv sync --no-install-project

lint:
	@uv run ruff check --fix --exit-non-zero-on-fix .
	@uv run mypy $(SERVICE_DIR)/

format:
	@uv run ruff format .

test:
	export COVERAGE_FILE=$(REPORTS_DIR)/.coverage && \
	uv run pytest --junitxml=$(REPORTS_DIR)/junit.xml \
				  --cov-report term-missing \
				  --cov-report xml:$(REPORTS_DIR)/coverage.xml \
				  --cov=$(SERVICE_DIR) tests

clean:
	rm -rf ./tmp
	find . -type d -name "__pycache__" -print -exec rm -rv {} +

build-local:
	docker build -t $(SERVICE_DIR):$(DOCKER_BUILD_TAG) .
