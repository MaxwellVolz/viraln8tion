# Default target
.DEFAULT_GOAL := up

# Load .env vars
include .env
export

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Rebuild containers without cache
rebuild:
	docker-compose build --no-cache

# View logs (follow)
logs:
	docker-compose logs -f

# Restart a specific service, e.g. `make restart service=n8n`
restart:
	docker-compose restart $(service)

# Run a shell in a service container, e.g. `make sh service=n8n`
sh:
	docker-compose exec $(service) sh

# Show running containers
ps:
	docker-compose ps
