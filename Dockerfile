# Use python base image
FROM python:3.9-slim

WORKDIR /code

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code"

# Create non-root user
RUN adduser --disabled-password appuser

# Copy application code and requirements
COPY . .

# Install dependencies
RUN pip install uv
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Switch to non-root user
USER appuser

# Run the application
CMD ["bash", "scripts/run.sh"]


