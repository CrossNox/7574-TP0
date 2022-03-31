SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/CrossNox/7574-TP0
DOCKER_BIN=docker
DOCKER_COMPOSE_BIN=docker-compose

default: build

all:

deps:
	go mod tidy
	go mod vendor

build: deps
	GOOS=linux go build -o bin/client $(GIT_REMOTE)/client
.PHONY: build

docker-image:
	$(DOCKER_BIN) build -f ./server/Dockerfile -t "server:latest" .
	$(DOCKER_BIN) build -f ./client/Dockerfile -t "client:latest" .
	# Execute this command from time to time to clean up intermediate stages generated
	# during client build (your hard drive will like this :) ). Don't left uncommented if you
	# want to avoid rebuilding client image every time the docker-compose-up command
	# is executed, even when client code has not changed
	# docker rmi `docker images --filter label=intermediateStageToBeDeleted=true -q`
.PHONY: docker-image

docker-compose-up-scale-client: docker-image
	local n_clients = 5
	if [ -z "$(NCLIENTS)" ]; then \
		n_clients = $(NCLIENTS)
	fi
	$(DOCKER_COMPOSE_BIN) -f docker-compose-dev.yaml up --scale client1=$(n_clients) -d --build
.PHONY: docker-compose-up-scale-client

docker-compose-up: docker-image
	$(DOCKER_COMPOSE_BIN) -f docker-compose-dev.yaml up -d --build
.PHONY: docker-compose-up

docker-compose-down:
	$(DOCKER_COMPOSE_BIN) -f docker-compose-dev.yaml stop -t 1
	$(DOCKER_COMPOSE_BIN) -f docker-compose-dev.yaml down
.PHONY: docker-compose-down

docker-compose-logs:
	$(DOCKER_COMPOSE_BIN) -f docker-compose-dev.yaml logs -f
.PHONY: docker-compose-logs
