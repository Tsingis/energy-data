FROM python:3.13-alpine AS setup

WORKDIR /app

ENV POETRY_HOME="/opt/poetry"
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apk update && apk add curl \
    && curl --proto "=https" -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry config virtualenvs.in-project false \
    && poetry install --no-interaction --no-root \
    && poetry export -f requirements.txt --without-hashes > requirements.txt

FROM python:3.13-alpine AS build

WORKDIR /app

COPY --from=setup /app/requirements.txt ./

RUN pip install --prefer-binary --disable-pip-version-check --no-cache-dir -r requirements.txt && \
    python -m pip uninstall -y setuptools wheel pip

FROM python:3.13-alpine

WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY ./src .

RUN rm -r /usr/local/lib/python3.13/site-packages/pip* && \
    addgroup -S app && \
    adduser -S -G app api

USER api

CMD ["python", "main.py"]