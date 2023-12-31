# Executables (local)
DOCKER_COMP = docker compose

# Docker containers
API = $(DOCKER_COMP) exec api
NEST = $(DOCKER_COMP) exec pwa
KEYCLOAK = $(DOCKER_COMP) exec keycloak

help: ## Outputs this help screen
	@grep -E '(^[a-zA-Z0-9\./_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

## —— Docker ————————————————————————————————————————————————————————————————
build: ## Builds the Docker images
	@$(DOCKER_COMP) build --pull --no-cache

up: ## Start the docker hub in detached mode (no logs)
	@$(DOCKER_COMP) up --detach

start: build up ## Build and start the containers

down: ## Stop the docker hub
	@$(DOCKER_COMP) down --remove-orphans

reset: ## Stops the docker hub and deletes all its data including all images
	@$(DOCKER_COMP) down --remove-orphans --volumes --rmi all

logs: ## Show live logs
	@$(DOCKER_COMP) logs --tail=0 --follow

## —— Api ————————————————————————————————————————————————————————————————
sh: ## Connect to the fastapi container
	@$(API) sh

## —— Keycloak ————————————————————————————————————————————————————————————————
keycloak-config: ## Connect to the fastapi container
	@$(KEYCLOAK) /opt/keycloak/bin/kc.sh show-config