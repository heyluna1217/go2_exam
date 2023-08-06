FROM python:3.10-bullseye as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

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

FROM base as final

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist .

RUN pip install *.whl
