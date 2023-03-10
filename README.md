Fastemplate
===========

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![CI](https://github.com/Mindflutter/fastemplate/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Mindflutter/fastemplate/branch/master/graph/badge.svg?token=JUL44CDR4U)](https://codecov.io/gh/Mindflutter/fastemplate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A template for backend services 

* Based on [FastAPI](https://fastapi.tiangolo.com/)
* Uses [SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/index.html) for database interaction
* Includes examples of:
  - API endpoints
  - DB initialization
  - DB requests  
  - Dockerizing the service
  - Useful Makefile targets

## Project setup

* Install `docker`, `docker-compose`, `poetry`
* Install project dependencies: `poetry install`
