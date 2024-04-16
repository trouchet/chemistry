# Use python base image
FROM python:3.9-slim

# Create non-root user
RUN adduser --disabled-password appuser

# Set working directory
WORKDIR /app

# Copy application code and requirements
COPY . .

# Install dependencies
RUN pip install uv
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Switch to non-root user
USER appuser

# Get APP_COUNTS from environment
# Use default value if not set
ENV APP_COUNTS ${APP_COUNTS:-1}

# Run each app individually
CMD [ "/usr/local/bin/uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
