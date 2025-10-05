# Makefile for RAG Model Docker setup

.PHONY: help build up down logs clean setup-ollama status

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-consumer: ## Show consumer logs
	docker-compose logs -f consumer

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

setup-ollama: ## Pull the required Ollama model
	./scripts/setup-ollama.sh

status: ## Show status of all services
	docker-compose ps

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

restart: ## Restart all services
	docker-compose restart

restart-backend: ## Restart backend service
	docker-compose restart backend

restart-consumer: ## Restart consumer service
	docker-compose restart consumer

dev: ## Start services for development (with logs)
	docker-compose up

# Quick start command
start: build up setup-ollama ## Build, start services, and setup Ollama model
	@echo "All services started! Access the application at:"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "RabbitMQ Management: http://localhost:15672 (guest/guest)"
