#!/bin/bash

# Load environment variables
source .env

# Determine worker count based on available CPUs
NUM_WORKERS=$(nproc)

# Run database migrations
python src/db/migrate.py

# Launch Uvicorn server
uvicorn src/api/main:app \
    --host ${APP_HOST} \
    --port ${APP_PORT} \
    --reload \
    --workers ${NUM_WORKERS} \
    --loop asyncio \
    --log-level info