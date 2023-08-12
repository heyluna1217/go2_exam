FROM python:3.10-bullseye AS base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

COPY orders_api ./orders_api
COPY README.md .

RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root && \
	poetry build

ENV PATH="/app/.venv/bin:${PATH}" \
	VIRTUAL_ENV="/app/.venv"

FROM base AS app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist .
COPY --from=builder /app/orders_api/staticfiles ./staticfiles
COPY ./docker/docker-entrypoint.sh .

ENTRYPOINT ["./docker-entrypoint.sh"]

RUN pip install --disable-pip-version-check --no-cache-dir ./*.whl

FROM base AS celery

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist .

COPY ./docker/docker-celery-entrypoint.sh .

ENTRYPOINT ["./docker-celery-entrypoint.sh"]

RUN pip install --disable-pip-version-check --no-cache-dir ./*.whl