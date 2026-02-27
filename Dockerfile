FROM python:3.13-alpine AS builder

WORKDIR /app/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN pip --no-cache-dir install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY fastemplate /app/fastemplate
COPY pyproject.toml /app/

FROM builder AS runtime

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

WORKDIR /app/

CMD ["python", "-m", "fastemplate.app"]
