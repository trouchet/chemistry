$CONTAINER_NAME = "myapi-container"

# Clean logs
Remove-Item -Path "build\", "dist\", ".eggs\" -Force -Recurse
Get-ChildItem -Path "." -Filter "*.log" -Recurse | Remove-Item -Force

# Clean test artifacts
Remove-Item -Path ".tox\", ".testmondata*", ".coverage", "coverage.*", "htmlcov\", ".pytest_cache\" -Force -Recurse

# Clean cache
Get-ChildItem -Path "." -Filter "*cache*" -Recurse | Remove-Item -Force -Recurse

# Docker clean
docker system prune --volumes -f

# Build Docker image
docker build -t myapi .

# Run Docker container
docker run -d --name $CONTAINER_NAME -p 8000:8000 myapi

# Stop Docker container
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# Run tests
poetry run coverage run --rcfile=.coveragerc -m pytest -s

# Watch tests
ptw -- --cov=. --cov-report=term-missing --cov-config=pytest.ini -s

# Generate coverage report
poetry run coverage report --omit="tests/*,src/main.py,*/__init__.py,*/constants.py" --show-missing --capture=no

# List containers
docker ps -a

# Docker compose up
# $(DOCKER_COMPOSE) up

# Docker compose down
# $(DOCKER_COMPOSE) down
