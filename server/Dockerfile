FROM python:3.14.2-alpine3.23 AS base

FROM base AS build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY requirements.txt ./

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

WORKDIR /app

COPY ./uv.lock ./pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-group dev

FROM base AS final

WORKDIR /app

COPY --from=build ./app/.venv ./.venv
COPY ./src ./src

ENV PATH="/app/.venv/bin:$PATH"

RUN rm -r /usr/local/lib/python*/site-packages/pip* && \
    addgroup -S app && \
    adduser -S -G app nonroot

USER nonroot

CMD ["python", "-m", "src.main"]