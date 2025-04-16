.PHONY: help up down restart logs init apply destroy clean generate-datasources
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: generate-datasources ## docker compose up
	docker compose up -d

down: ## docker compose down
	docker compose down

restart: down up ## down and up
	
logs: ## show alloy logs
	docker compose logs grafana -f

init: ## initialize
	tofu init

apply: ## deploy the amp workspace
	tofu apply -auto-approve

destroy: ## remove the amp workspace
	tofu destroy -auto-approve

generate-datasources: ## generates datasources
	uv run generate_datasource.py

clean: ## removes everything
	rm -rf grafana
