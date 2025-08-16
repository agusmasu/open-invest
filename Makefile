.PHONY: help build up down logs clean restart test

help: ## Show this help message
	@echo "Open-Invest Docker Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker-compose build

up: ## Start the application
	docker-compose up -d

down: ## Stop the application
	docker-compose down

logs: ## View application logs
	docker-compose logs -f

clean: ## Clean up Docker resources
	docker-compose down -v --remove-orphans
	docker system prune -f

restart: ## Restart the application
	docker-compose restart

test: ## Test the API endpoints
	@echo "Testing API endpoints..."
	@curl -s http://localhost:8000/health | jq . || echo "Health check failed or jq not installed"
	@curl -s http://localhost:8000/ | jq . || echo "Root endpoint failed or jq not installed"

dev: ## Start in development mode with rebuild
	docker-compose up --build -d

status: ## Show container status
	docker-compose ps
