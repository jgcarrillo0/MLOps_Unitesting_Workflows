# Etapa base: uv resuelve dependencias; registrar uv.lock antes de CI.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

WORKDIR /workspace
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project
COPY app/ ./app/

# Etapa publicable: servidor HTTP para inferencia sencilla.
FROM base AS runtime
EXPOSE 8025
CMD ["uv", "run", "--frozen", "--no-dev", "uvicorn", \
     "app.main:app", "--host", "0.0.0.0", "--port", "8025"]

# Etapa predeterminada: ejecuta pytest sin intervención manual.
FROM base AS test
ENV UV_NO_DEV=0
COPY tests/ ./tests/
RUN uv sync --no-install-project
CMD ["uv", "run", "--frozen", "pytest", "-v"]

