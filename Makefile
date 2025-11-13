# Makefile for FastAPI Docker Management

.PHONY: help dev prod dev-build prod-build dev-up prod-up dev-down prod-down dev-logs prod-logs clean

# Default target
help:
	@echo "FastAPI Docker Management Commands:"
	@echo ""
	@echo "Development:"
	@echo "  dev-build    Build development environment"
	@echo "  dev-up       Start development environment"
	@echo "  dev-down     Stop development environment"
	@echo "  dev-logs     Show development logs"
	@echo "  dev-shell    Access development app container shell"
	@echo ""
	@echo "Production:"
	@echo "  prod-build   Build production environment"
	@echo "  prod-up      Start production environment"
	@echo "  prod-down    Stop production environment"
	@echo "  prod-logs    Show production logs"
	@echo ""
	@echo "Utilities:"
	@echo "  clean        Remove all containers, volumes, and images"
	@echo "  redis-cli    Connect to Redis CLI (development)"
	@echo "  health       Check health of all services"

# Development commands
dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-up:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Development environment started!"
	@echo "API available at: http://localhost:8000"
	@echo "Redis Commander available at: http://localhost:8081"

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-shell:
	docker-compose -f docker-compose.dev.yml exec app /bin/bash

# Production commands
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Production environment started!"
	@echo "API available at: http://localhost:80"
	@echo "Direct app access: http://localhost:8000"

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

# Utility commands
clean:
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans
	docker-compose -f docker-compose.prod.yml down -v --remove-orphans
	docker system prune -f

redis-cli:
	docker-compose -f docker-compose.dev.yml exec redis redis-cli

# Check health of services
health:
	@echo "Checking service health..."
	@curl -f http://localhost:8000/health 2>/dev/null && echo "✅ API healthy" || echo "❌ API down"
	@docker-compose -f docker-compose.dev.yml exec redis redis-cli ping 2>/dev/null && echo "✅ Redis healthy" || echo "❌ Redis down"