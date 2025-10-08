FROM python:3.14-alpine AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

FROM base AS build

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

COPY --from=build /app .
COPY ./src ./src

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

RUN rm -r /usr/local/lib/python3.13/site-packages/pip* && \
    addgroup -S app && \
    adduser -S -G app api

USER api

CMD ["python", "-m", "src.main"]