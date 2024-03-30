# Stage 1: Build (non-root user)

FROM python:3.9 AS builder

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies as non-root user
RUN adduser --disabled-password --shell /bin/bash appuser && \
    chown -R appuser:appuser . && \
    su - appuser -c "pip install --no-cache-dir -r requirements.txt prometheus_client"

# Copy application code
COPY . .

# Stage 2: Run (non-root user)

FROM python:3.9-slim  # Use slim image for smaller size

# Copy dependencies from build stage
COPY --from=builder /app .

# Set working directory and user
WORKDIR /app
USER appuser

# Get APP_COUNTS from .env file (optional)
ARG APP_COUNTS

# Expose ports dynamically based on APP_COUNTS
EXPOSE $((8000 + 0))-$((8000 + APP_COUNTS - 1))

# Run each app individually
CMD ["bash", "-c", "for ((i=1; i <= $APP_COUNTS; i++)); do uvicorn src.main:create_app $i --host 0.0.0.0 --port $((8000 + i)) & done && wait"]