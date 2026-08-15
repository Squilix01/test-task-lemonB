# syntax=docker/dockerfile:1

# STAGE 1: Builder
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==2.4.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root


# STAGE 2: RUNTIME
FROM python:3.12-slim-bookworm AS runtime

ARG GIT_SHA=dev
LABEL org.opencontainers.image.title="lemon-b-backend" \
      org.opencontainers.image.revision="${GIT_SHA}"

RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 1001 app \
    && useradd --system --uid 1001 --gid app --create-home app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app" \
    PATH="/app/.venv/bin:$PATH" \
    PLAYWRIGHT_BROWSERS_PATH="/opt/pw-browsers"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

RUN playwright install --with-deps chromium \
    && mkdir -p /opt/pw-browsers \
    && chown -R app:app /opt/pw-browsers

RUN chown -R app:app /app

USER 1001:1001

EXPOSE 8000
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["sh", "-c", "alembic upgrade head && python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]