### Create migration

Run `poetry run alembic revision --message="<revision message here>" --autogenerate`

### Apply migration
Run `poetry run alembic upgrade head`
