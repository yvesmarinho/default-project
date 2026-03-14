# 📖 Profile Guide — Programming + Python Fastapi

> Guia gerado automaticamente por `scripts/scaffold.py` em 2026-03-14.
> **Combinação ativa**: `devops-programming` + `python-fastapi` + `devops-security`
> **Projeto**: `minha-api` (programming / python)

---

## 🎯 Combinação de Perfis

| Perfil | Camada | Descrição |
|--------|--------|-----------|
| `devops-programming` | Core / Layer 1 | Perfil base para projetos de programação (Python, TypeScript, Go, other). Ati... |
| `python-fastapi` | Layer 2 (Framework) | Layer 2 para projetos Python FastAPI. Gera estrutura src/api/v1/, app factory... |
| `devops-security` | Transversal | Perfil transversal de segurança — aplicado silenciosamente a todos os projeto... |

---

## 📁 Arquivos Gerados

### `devops-programming`

| Arquivo | Descrição |
|---------|----------|
| `.copilot-rules.md` | Regras genéricas compartilhadas do Copilot (symlink ou cópia) |
| `.copilot-rules-{project_name}.md` | Regras específicas do projeto: identidade, perfis ativos, estrutura de pastas, regras P0/P1 do domínio, convenções de linguagem, segurança, decisões técnicas.
 |
| `.github/copilot-instructions.md` | Instrução auto-injetada pelo VS Code em toda sessão Copilot. Referencia as regras completas e declara o perfil de domínio ativo.
 |
| `.github/prompts/session-start.prompt.md` | Ritual de início de sessão: carrega contexto, verifica .secrets/, abre TODOs |
| `.github/prompts/session-end.prompt.md` | Ritual de encerramento: gera relatório, atualiza TODO/INDEX, comita docs |
| `.github/prompts/domain/devops-programming.prompt.md` | Domain profile: comportamento do Copilot no modo PROGRAMMING |
| `.github/prompts/domain/devops-security.prompt.md` | Domain profile transversal: controles de segurança (aplicado sempre) |
| `docs/INDEX.md` | Índice do projeto com links para sessões, decisões e documentos |
| `docs/TODO.md` | Lista de tarefas incremental do projeto |
| `docs/SESSIONS/` | Diretório de sessões de trabalho (DAILY_ACTIVITIES, SESSION_REPORT, etc.) |
| `.vscode/settings.json` | Configurações VS Code: extensions recomendadas, formatação, Copilot |
| `.gitignore` | Gitignore padrão (node_modules, .venv, .data, .secrets, dist) |
| `pyproject.toml` | Configuração Python PEP 621: nome, versão, deps, ruff, pytest |
| `package.json` | Configuração Node.js: scripts, devDependencies básicas |
| `go.mod` | Módulo Go com versão fixada |

### `python-fastapi`

| Arquivo | Descrição |
|---------|----------|
| `src/main.py` | FastAPI app factory com lifespan e include_router |
| `src/api/__init__.py` | Pacote api |
| `src/api/router.py` | APIRouter principal que agrega sub-routers |
| `src/api/v1/__init__.py` | Pacote v1 |
| `src/api/v1/health.py` | GET /api/health — smoke endpoint |
| `src/core/__init__.py` | Pacote core |
| `src/core/config.py` | pydantic-settings: PROJECT_NAME, ENV, SECRET_KEY, DATABASE_URL |
| `tests/conftest.py` | Fixture AsyncClient via ASGITransport para testes HTTP em memória |
| `tests/test_health.py` | Smoke test do endpoint /api/health |
| `pyproject.toml` | PEP 621: fastapi, uvicorn, pydantic-settings, pytest-asyncio, ruff, bandit, pip-audit |
| `.env.example` | Variáveis de ambiente documentadas sem valores reais |
| `Dockerfile` | Multistage: builder (uv sync --frozen --no-dev) + runtime (usuário não-root) |
| `docker-compose.yml` | Serviços: app + postgres:16 com healthcheck |
| `Makefile` | Targets: install, dev, test, lint, format, audit, security, docker-*, ci, clean |
| `.github/prompts/domain/layer2-python-fastapi.prompt.md` | Domain profile: convenções FastAPI, padrões de teste, segurança |

### `devops-security`

| Arquivo | Descrição |
|---------|----------|
| `.github/prompts/domain/devops-security.prompt.md` | Domain profile transversal: comportamento do Copilot para revisões de segurança, IaC hardening, gestão de segredos, threat modeling e pre-commit hooks.
 |
| `scripts/load-mcp.sh` | Script de carregamento de variáveis de ambiente para servidores MCP. Verifica .secrets/.env, valida tokens obrigatórios, orienta abertura do VS Code. Nunca exibe o valor dos tokens (SPEC-11).
 |

---

## 🔐 Segurança — Requisitos Ativos

### `devops-programming`

- Secrets scan declarado em .copilot-rules.md seção P0 (varredura a cada sessão)
- Sem valores hardcoded — regra P0 injetada em .copilot-rules-{project_name}.md
- bandit scan recomendado para projetos Python (pre-commit ou CI)
- pip-audit recomendado para projetos Python (uv run pip-audit em Makefile)
- Sem credenciais em variáveis de ambiente inline — usar .secrets/.env

### `python-fastapi`

- SECRET_KEY via pydantic-settings + .env (nunca hardcoded)
- CORSMiddleware com allow_origins explícito (nunca ['*'] em produção)
- bandit -r src/ disponível via 'make security'
- pip-audit disponível via 'make audit'
- Dockerfile executa como usuário não-root (adduser app)
- uv sync --frozen --no-dev na imagem de produção (sem deps dev)
- Swagger/ReDoc desabilitado quando ENV=production
- POSTGRES_PASSWORD via variável de ambiente obrigatória no docker-compose

### `devops-security`

- tfsec: nenhum recurso Terraform com expose público não-intencional
- checkov: controles CKV_AWS_* aplicados em terraform-aws + checkov para k8s-helm
- bandit B201/B602 HIGH bloqueiam merge em Python
- semgrep ruleset p/owasp-top-ten para detecção de injection, XSS, SSRF
- gitleaks pré-commit: nenhum token/chave jamais entra no histórico git
- detect-secrets baseline: .secrets.baseline versionado no repositório
- mcp.json: tokens referenciados via ${env:VAR_NAME} — nunca hardcodados
- .secrets/ sempre no .gitignore
- THREAT-MODEL.md obrigatório em projetos com dados sensíveis (lgpd-baseline, soc2-baseline)
- pre-commit hook: detect-secrets + gitleaks + ruff (Python) / eslint (TS)

---

## ⚡ Quick Start

### Pré-requisitos

- `git installed`
- `uv installed`
- `python >= 3.11`
- `language == python`
- `domain == programming`
- `docker installed`

### Comandos Principais

```bash
# Instalar dependências
make install-deps

# Desenvolvimento
make dev

# Testes
make test

# Lint e formatação
make lint && make format
```

---

## 🔗 Referências por Stack

- [Python 3 Docs](https://docs.python.org/3)
- [uv Docs](https://docs.astral.sh/uv)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Go Docs](https://go.dev/doc)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [REST API Best Practices](https://restfulapi.net)
- [Docker Docs](https://docs.docker.com)

---

*Gerado por scripts/scaffold.py v1.0.0 | 2026-03-14*
