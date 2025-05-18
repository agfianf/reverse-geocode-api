# if tags are not found, fallback to version in pyproject.toml
VERSION := $(shell git describe --tags --abbrev=0 2>/dev/null || cat pyproject.toml | awk '/version =/ {gsub(/"/, "", $$3); print $$3}')
DOCKER_IMAGE = reverse-geo-api:$(VERSION)
REDIS_PASSWORD = "your_redis_password"

# Default target
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Environment setup with `uv` ==========================================
install: ## Install dependencies with uv
	uv sync --all-extras --all-groups

sync-all: ## Sync all dependencies
	uv sync --all-extras

sync-docs:
	uv sync --only-group={docs,dev}

# Docker tasks =========================================================
run-docker-app: ## Run Docker app (backend) container
	@echo "Running Docker image $(DOCKER_IMAGE)"
	docker run \
	--rm \
	-it \
	--name reverse-geo-api \
	-p 8080:8080 \
	-v $(PWD)/src:/application/src \
	$(DOCKER_IMAGE) bash

build: ## Build Docker app (backend) images
	@echo "Building Docker image $(DOCKER_IMAGE)"
	docker build \
	-f Dockerfile.dev \
	--build-arg USER_UID=$$(id -u) \
	--build-arg USER_GID=$$(id -g) \
	-t $(DOCKER_IMAGE) .

build-compose: ## Build Docker Compose images
	@echo "VERSION is $(VERSION)"
	@echo "Building Docker Compose images with tags $(DOCKER_IMAGE)"
	DOCKER_IMAGE=$(DOCKER_IMAGE) \
	USER_UID=$$(id -u) \
	USER_GID=$$(id -g) \
	docker-compose build
	docker-compose pull

up: ## Start Docker containers
	@echo "VERSION is $(VERSION)"
	@echo "Building Docker Compose images with tags $(DOCKER_IMAGE)"
	DOCKER_IMAGE=$(DOCKER_IMAGE) \
	USER_UID=$$(id -u) \
	USER_GID=$$(id -g) \
	docker-compose up -d

up-with-nginx: ## Start Docker containers with Nginx
	@echo "Starting Docker containers with Nginx"
	DOCKER_IMAGE=$(DOCKER_IMAGE) \
	USER_UID=$$(id -u) \
	USER_GID=$$(id -g) \
	REDIS_PASSWORD=$(REDIS_PASSWORD) \
	docker-compose -f docker-compose.nginx.yml up

down: ## Stop and remove Docker containers
	docker-compose down

down-with-nginx: ## Stop and remove Docker containers
	docker-compose -f docker-compose.nginx.yml down

# Development tasks ====================================================
.PHONY: test
test: ## Run tests
	uv run pytest src/tests

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	uv run pre-commit run --all-files

logs:
	@echo "Showing logs for Docker containers"
	docker-compose logs -f

# Cleanup
.PHONY: shell
shell: ## Open a shell in the app container
	docker-compose exec app bash
