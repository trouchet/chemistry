FROM python:3.11.3-slim-buster AS base

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

ENV PYTHONPATH=/app

WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

# Create non-root user
RUN adduser --disabled-password appuser

# Install uv
RUN pip install uv

# Copy application code and requirements (assuming requirements.txt is in the same directory)
COPY . .

# Install dependencies with uv
RUN uv pip install -r requirements.txt --system

# Switch to non-root user
USER appuser

ENV PYTHONPATH=/app

COPY ./scripts/ /app/

COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./tests-start.sh /app/

COPY ./app /app/app

# Run the application
CMD ["bash", "scripts/run.sh"]
