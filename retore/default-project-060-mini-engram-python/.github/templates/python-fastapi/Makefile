.DEFAULT_GOAL := help

# ============================================================
# {project_name} — Makefile
# Gerenciador: uv | Framework: FastAPI
# ============================================================

.PHONY: help install dev test lint format audit security sbom docker-build docker-up docker-down clean

# ------------------------------------------------------------
# Ajuda
# ------------------------------------------------------------
help: ## Mostra este menu de ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
install: ## Instala dependências de produção + dev (uv sync)
	uv sync

# ------------------------------------------------------------
# Desenvolvimento
# ------------------------------------------------------------
dev: ## Inicia servidor de desenvolvimento com hot-reload
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# ------------------------------------------------------------
# Testes
# ------------------------------------------------------------
test: ## Roda todos os testes com cobertura
	uv run pytest --cov=src --cov-report=term-missing

test-fast: ## Roda testes sem cobertura (mais rápido)
	uv run pytest -x -q

# ------------------------------------------------------------
# Qualidade de código
# ------------------------------------------------------------
lint: ## Verifica code style com ruff
	uv run ruff check src/ tests/

format: ## Formata código com ruff format
	uv run ruff format src/ tests/

format-check: ## Verifica formatação sem aplicar (CI)
	uv run ruff format --check src/ tests/

# ------------------------------------------------------------
# Segurança
# ------------------------------------------------------------
audit: ## Verifica CVEs nas dependências (pip-audit)
	uv run pip-audit

security: ## Análise estática de segurança (bandit)
	uv run bandit -r src/ -c pyproject.toml

security-full: audit security ## Roda audit + bandit

sbom: ## Gera Software Bill of Materials (CycloneDX JSON) — evidência CC8 SOC 2
	uv run cyclonedx-py requirements \
		--of JSON \
		-o sbom.json \
		<(uv pip freeze) 2>/dev/null || \
	uv run python -m cyclonedx_py requirements \
		--of JSON \
		-o sbom.json \
		<(uv pip freeze)
	@echo "✅ SBOM gerado em sbom.json"

# ------------------------------------------------------------
# Docker
# ------------------------------------------------------------
docker-build: ## Build da imagem Docker
	docker build --target runtime -t {project_name}:dev .

docker-up: ## Sobe app + postgres via docker-compose
	docker compose up -d

docker-down: ## Para e remove containers
	docker compose down

docker-logs: ## Exibe logs do container app
	docker compose logs -f app

# ------------------------------------------------------------
# CI (roda tudo — usar em pre-push ou GitHub Actions)
# ------------------------------------------------------------
ci: format-check lint security-full test sbom ## Checks completos de CI (inclui SBOM)

# ------------------------------------------------------------
# Limpeza
# ------------------------------------------------------------
clean: ## Remove arquivos temporários e caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
