Fastemplate
===========

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![CI](https://github.com/Mindflutter/fastemplate/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Mindflutter/fastemplate/branch/master/graph/badge.svg?token=JUL44CDR4U)](https://codecov.io/gh/Mindflutter/fastemplate)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

A template for backend services

* Based on [FastAPI](https://fastapi.tiangolo.com/)
* Uses [SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/index.html) (Core, async) for database interaction
* Layered architecture: `api/` → `services/` → `repositories/` → database
* Dependency injection via FastAPI `Depends()`
* [Testcontainers](https://testcontainers-python.readthedocs.io/) for integration tests
* Includes examples of:
  - CRUD API endpoints
  - Database migrations (Alembic)
  - Dockerizing the service
  - CI with GitHub Actions

## Project setup

* Install `docker`, `docker-compose`, `poetry`
* Install project dependencies: `make setup`
* Start local services: `docker-compose up -d`
* Run migrations: `poetry run alembic upgrade head`
* Run tests: `make test`
* Lint: `make lint`
