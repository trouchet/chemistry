#!/bin/bash

python src/database/migrate.py
uvicorn api.app:app --reload --host "0.0.0.0" --port "8000"
