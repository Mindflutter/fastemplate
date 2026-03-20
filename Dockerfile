FROM python:3.13-alpine AS builder

WORKDIR /app/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock /app/

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-install-project --no-dev

COPY fastemplate /app/fastemplate
COPY migrations /app/migrations
COPY pyproject.toml /app/

FROM builder AS runtime

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

WORKDIR /app/

CMD ["python", "-m", "fastemplate.app"]
