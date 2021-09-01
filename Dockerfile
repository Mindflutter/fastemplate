FROM python:3.9-slim as builder

# install helper packages
RUN apt update && apt upgrade -y && \
    apt install -y curl nano htop

WORKDIR /opt/app/

# set envs
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.1.8

# install poetry
RUN pip install poetry==$POETRY_VERSION

# install package dependencies
COPY poetry.lock pyproject.toml ./
COPY src src/
RUN poetry config virtualenvs.create false && \
    poetry install --verbose

FROM builder AS runtime

COPY --from=builder /opt/app/ /opt/app/
WORKDIR /opt/app/

CMD poetry run app
