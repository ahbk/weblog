FROM python:3.10.11-alpine3.18 AS weblog-api

# Configure Poetry
ENV POETRY_VERSION=1.5.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /api

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

CMD poetry run uvicorn --host 0.0.0.0 weblog.main:app --reload
