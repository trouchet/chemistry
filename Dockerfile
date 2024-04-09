# Use python base image
FROM python:3.9-slim

# Create non-root user
RUN adduser --disabled-password appuser

# Set working directory
WORKDIR /app

# Copy application code and requirements
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install ElasticSearch and logstash
RUN apt update & apt install -y wget gnupg
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | \
    gpg --dearmor -o /usr/share/keyrings/elastic-keyring.gpg
RUN apt-get install apt-transport-https

RUN echo "deb [signed-by=/usr/share/keyrings/elastic-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | \
    tee -a /etc/apt/sources.list.d/elastic-8.x.list
RUN apt-get update && apt-get install logstash

# Switch to non-root user
USER appuser

# Get APP_COUNTS from environment
# Use default value if not set
ENV APP_COUNTS ${APP_COUNTS:-1}

# Run each app individually
CMD [\
    "/usr/local/bin/uvicorn", \
    "src.main:app", \
    "--reload", \
    "--workers", \ 
    "1", \
    "--host", \
    "0.0.0.0", \
    "--port", \
    "8000"
]


