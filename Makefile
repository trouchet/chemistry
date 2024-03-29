CONTAINER_NAME := myapi-container

.PHONY: build run-webapp stop ps host

clean-logs: # Add a rule to remove log info
	rm -fr build/ dist/ .eggs/
	find . -name '*.log' -o -name '*.log' -exec rm -fr {} +

clean-pyc: # Add a rule to remove pyc files
	find . -name '*.pyc' -o -name '*.pyo' -o -name '*~' -exec rm -rf {} +

clean-test: # remove test and coverage artifacts
	rm -fr .tox/ .testmondata* .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*cache*' -exec rm -rf {} +

clean: clean-logs clean-pyc clean-test clean-cache ## Add a rule to remove unnecessary assets
	docker system prune --volumes -f

build:
	docker build -t myapi .

run-webapp:
	docker run -d --name $(CONTAINER_NAME) -p 8000:8000 myapi

stop-webapp:	
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)	

test: ## Add a rule to test the application
	poetry run coverage run --rcfile=.coveragerc -m pytest --ignore=src/migrations

watch: env ## run tests on watchdog mode
	ptw . -- pytest --ignore=src/migrations

report: clean test ## Add a rule to generate coverage report
	coverage report --omit="src/migrations/*" --show-missing

ps: ## Add a rule to list containers
	docker ps -a

up: ## Add a rule to docker up containers
	$(DOCKER_COMPOSE) up

down: ## Add a rule to docker down containers
	$(DOCKER_COMPOSE) down

