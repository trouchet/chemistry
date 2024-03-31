CONTAINER_NAME := myapi-container

.PHONY: build run-webapp stop ps host

clean-logs: # Add a rule to remove log info
	rm -fr build/ dist/ .eggs/
	find . -name '*.log' -o -name '*.log' -exec rm -fr {} +

clean-test: # remove test and coverage artifacts
	rm -fr .tox/ .testmondata* .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*cache*' -exec rm -rf {} +

sanitize:
	docker system prune --volumes -f
	docker images --filter 'dangling=true' -q --no-trunc | xargs -r docker rmi

clean: clean-logs clean-pyc clean-test clean-cache ## Add a rule to remove unnecessary assets
	docker system prune --volumes -f

create-env: ## Add a rule to create a virtual environment
	pip install virtualenv
	virtualenv venv
	@echo "Run 'source venv/bin/activate' to activate the virtual environment"
	@echo "Run 'deactivate' to deactivate the virtual environment"

build: sanitize ## Add a rule to build the application	
	docker-compose build --no-cache

run-webapp:
	docker run -d --name $(CONTAINER_NAME) -p 8000:8000 myapi

stop-webapp:	
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)	

test: ## Add a rule to test the application
	poetry run coverage run --rcfile=.coveragerc -m pytest

generate-minimal-requirements:
	pip-compile --output-file=requirements-minimal.txt requirements.txt
	grep -B1 '# via -r requirements.txt' requirements-minimal.txt | grep -v '\-\-' | cut -d'#' -f1 | sed -e 's/^[[:space:]]*//' -e 's/ //' | tr -s '\n' > requirements.txt
	rm requirements-minimal.txt

ptw-watch: ## run tests on watchdog mode
	ptw --quiet --spool 200 --clear --nobeep --config pytest.ini --ext=.py --onfail="echo Tests failed, fix the issues" -v

script-watch: ## run tests on watchdog mode
	./scripts/watch_tests.sh

report: test ## Add a rule to generate coverage report
	coverage report --omit="tests/*,src/main.py,*/__init__.py,*/constants.py" --show-missing

ps: ## Add a rule to list containers
	docker ps -a

up: ## Add a rule to docker up containers
	docker-compose up -d

down: ## Add a rule to docker down containers
	docker-compose down

