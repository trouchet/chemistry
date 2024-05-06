#!/bin/bash

# Load environment variables
source .env || { echo "Error loading .env file"; exit 1; }

# Determine worker count based on available CPUs
NUM_WORKERS=$(nproc)

# Launch Uvicorn server
uvicorn src.main:app \
    --host ${APP_HOST:-"localhost"} \
    --port ${APP_PORT:-"8000"} \
    --reload \
    --workers ${NUM_WORKERS:-"1"} \
    --loop asyncio \
    --log-level info \
    || { echo "Error launching Uvicorn server"; exit 1; }
