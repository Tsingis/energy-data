FROM dhi.io/python:3.14.2-alpine3.23-dev AS base

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

FROM dhi.io/python:3.14.2-alpine3.23 AS final

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=build /app/.venv /app/.venv
COPY ./src ./src

CMD ["python", "-m", "src.main"]