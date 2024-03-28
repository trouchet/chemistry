CONTAINER_NAME := myapi-container

.PHONY: build run-webapp stop ps host

build:
	docker build -t myapi .

run-webapp:
	docker run -d --name $(CONTAINER_NAME) -p 8000:8000 myapi

stop-webapp:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

ps:
	docker ps

host:
	docker-compose up
