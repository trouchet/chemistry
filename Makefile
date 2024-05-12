CONTAINER_NAME := api-backend-1

.PHONY: build run stop ps host

OMIT_PATHS := "backend/tests/*"

define PRINT_HELP_PYSCRIPT
import re, sys

regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'

for line in sys.stdin:
	match = re.match(regex_pattern, line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-logs: # Removes log info. Usage: make clean-logs
	rm -fr build/ dist/ .eggs/
	find . -name '*.log' -o -name '*.log' -exec rm -fr {} +

clean-test: # Remove test and coverage artifacts
	rm -fr .tox/ .testmondata* .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*cache*' -exec rm -rf {} +

sanitize: # Remove dangling images and volumes
	docker system prune --volumes -f
	docker images --filter 'dangling=true' -q --no-trunc | xargs -r docker rmi

clean: clean-logs clean-test clean-cache sanitize ## Add a rule to remove unnecessary assets. Usage: make clean

env: ## Creates a virtual environment. Usage: make env
	pip install uv
	uv venv

install: ## Installs the python requirements. Usage: make install
	uv pip install -r requirements.txt

build: sanitize ## Builds the application. Usage: make build
	docker-compose build --no-cache

run: ## Run the application. Usage: make run
	uvicorn backend.app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

search: ## Searchs for a token in the code. Usage: make search token=your_token
	grep -rnw . \
	--exclude-dir=venv \
	--exclude-dir=.git \
	--exclude=poetry.lock \
	-e "$(token)"

replace: ## Replaces a token in the code. Usage: make replace token=your_token
	sed -i 's/$(token)/$(new_token)/g' $$(grep -rl "$(token)" . \
		--exclude-dir=venv \
		--exclude-dir=.git \
		--exclude=poetry.lock)

test: ## Test the application. Usage: make test
	poetry run coverage run --rcfile=.coveragerc -m pytest backend/

minimal-requirements: ## Generates minimal requirements. Usage: make requirements
	python3 scripts/clean_packages.py requirements.txt requirements.txt

lint: ## perform inplace lint fixes
	black --skip-string-normalization .
	ruff check --fix .
	find . -name "*.py" -exec autopep8 --in-place --aggressive --aggressive {} \;

ptw-watch: ## Run tests on watchdog mode. Usage: make ptw-watch
	ptw --quiet --spool 200 --clear --nobeep \
    --config pytest.ini --ext=.py \
    --onfail="echo Tests failed, fix the issues"

script-watch: ## Run tests on watchdog mode. Usage: make script-watch
	./scripts/watch_tests.sh

report: test ## Generate coverage report. Usage: make report
	coverage report --omit=$(OMIT_PATHS) --show-missing

logs: ## Show logs. Usage: make logs
	docker logs -f ${CONTAINER_NAME}

enter: ## Enter the container. Usage: make enter
	docker exec -it $(CONTAINER_NAME) /bin/bash

ps: ## List containers. Usage: make ps
	docker ps -a

up: ## Docker up containers. Usage: make up
	docker-compose up -d

down: ## Docker down containers. Usage: make down
	docker-compose down

migrate: ## Run migrations. Usage: make migrate
	python scripts/migrate.py

restart: down build up ## Add a rule to docker restart containers. Usage: make restart
