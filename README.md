Fastemplate
===========

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A template for backend services 

* Based on [FastAPI](https://fastapi.tiangolo.com/)
* Uses [async SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html) for database interaction
* Includes examples of:
  - API endpoints
  - DB initialization
  - DB requests  
  - Dockerizing the service
  - Useful Makefile targets

## Project setup

* Install `docker`, `docker-compose`, `poetry`
* Install project dependencies: `poetry install`
