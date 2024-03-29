CONTAINER_NAME := myapi-container

.PHONY: build run-webapp stop ps host

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

