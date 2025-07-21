# Makefile for managing local LLMs with vLLM

# Paths to docker compose files
COMPOSE_MISTRAL=docker-compose.mistral.yml
COMPOSE_DEEPSEEKCODE=docker-compose.deepseekcode.yml
COMPOSE_TINYLLAMA=docker-compose.tinyllama.yml

# Default target
help:
	@echo "Usage:"
	@echo "  make deepseekcode    # Start DeepSeekCode model"
	@echo "  make tinyllama    # Start tinyllama model"
	@echo "  make mistral         # Start Mistral model"
	@echo "  make stop        # Stop all containers"
	@echo "  make prune           # Stop and prune all containers"


tinyllama:
	docker compose -f $(COMPOSE_TINYLLAMA) up

tinyllama-down:
	docker compose -f $(COMPOSE_TINYLLAMA) down

deepseekcode:
	docker compose -f $(COMPOSE_DEEPSEEKCODE) up

deepseekcode-down:
	docker compose -f $(COMPOSE_DEEPSEEKCODE) down

mistral:
	docker compose -f $(COMPOSE_MISTRAL) up

mistral-down:
	docker compose -f $(COMPOSE_MISTRAL) down

stop-all:
	docker stop $$(docker ps -q)

prune:
	docker stop $$(docker ps -q)
	docker system prune -f
