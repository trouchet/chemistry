#! /usr/bin/env sh

# Exit in case of error
set -e

sh ./scripts/build.sh

docker-compose -f docker-compose.yml push
