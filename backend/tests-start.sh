#! /usr/bin/env bash
set -e
set -x

python /app/app/backend_pre_start.py

bash ./scripts/test.sh "$@"
