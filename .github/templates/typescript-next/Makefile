.DEFAULT_GOAL := help
PROJECT_NAME := {project_name}

.PHONY: help install dev build start lint lint-fix format format-check \
        test test-watch test-coverage audit docker-build docker-up docker-down ci

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências (pnpm install)
	pnpm install

dev: ## Inicia servidor de desenvolvimento com turbopack
	pnpm dev

build: ## Build de produção
	pnpm build

start: ## Inicia servidor de produção (requer build)
	pnpm start

lint: ## Lint + type-check
	pnpm lint

lint-fix: ## Lint com correção automática
	pnpm lint:fix

format: ## Formata código com Prettier
	pnpm format

format-check: ## Verifica formatação sem modificar
	pnpm format:check

test: ## Executa todos os testes
	pnpm test

test-watch: ## Executa testes em modo watch
	pnpm test:watch

test-coverage: ## Executa testes com relatório de cobertura
	pnpm test:coverage

audit: ## Auditoria de segurança das dependências
	pnpm audit --audit-level=high

docker-build: ## Build da imagem Docker
	docker compose build

docker-up: ## Sobe containers Docker
	docker compose up -d

docker-down: ## Para containers Docker
	docker compose down

ci: lint format-check test-coverage audit ## Pipeline CI completo (lint + format + test + audit)

clean: ## Remove artefatos de build
	rm -rf .next out coverage
