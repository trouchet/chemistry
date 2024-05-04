FROM python:3.11.3-slim-buster AS base

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code"

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

# Run the application
CMD ["bash", "scripts/run.sh"]
