FROM python:3.13-alpine AS base

ENV POETRY_VERSION=2.1.3 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS build

RUN --mount=type=cache,target=/root/.cache \
    pip install "poetry==$POETRY_VERSION"

WORKDIR $PYSETUP_PATH

COPY ./poetry.lock ./pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/cache \
    poetry install --no-interaction --no-root --without dev

FROM base AS final

WORKDIR /app

COPY --from=build $VENV_PATH $VENV_PATH
COPY ./src .

RUN rm -f "$VENV_PATH/bin/pip" && \
    rm -r "$VENV_PATH/lib/python3.13/site-packages"/pip* && \
    rm -r /usr/local/lib/python3.13/site-packages/pip* && \
    addgroup -S app && \
    adduser -S -G app api

USER api

CMD ["python", "main.py"]