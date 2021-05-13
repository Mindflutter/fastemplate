FROM python:3.9

RUN apt update && apt upgrade -y && \
    apt install curl

ENV PYTHONPATH=/opt/app/ \
    POETRY_HOME=/etc/poetry \
    POETRY_VERSION=1.1.6

WORKDIR /opt/app/

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | python - --version $POETRY_VERSION

# install package dependencies
COPY poetry.lock .
COPY pyproject.toml  .
RUN $POETRY_HOME/bin/poetry install --verbose --no-dev --no-root

COPY src /opt/app/

CMD $POETRY_HOME/bin/poetry run python main.py
