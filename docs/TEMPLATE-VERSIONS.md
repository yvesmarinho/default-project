# TEMPLATE-VERSIONS — Versionamento por Perfil

> Rastreabilidade de versão, status e histórico de cada perfil do Enterprise Default Project Template.
> Atualizar esta tabela sempre que um perfil receber nova versão ou mudar de status.

**Schema de referência**: [docs/copilot/PROFILE-DESCRIPTOR-SCHEMA.md](copilot/PROFILE-DESCRIPTOR-SCHEMA.md)
**Política de depreciação**: [docs/DEPRECATION-POLICY.md](DEPRECATION-POLICY.md)
**Changelog do template**: [CHANGELOG.md](../CHANGELOG.md)

---

## Índice de Perfis

| Perfil | Layer | Versão | Status | Última validação | Testado com |
|--------|-------|--------|--------|-----------------|-------------|
| `devops-programming` | core | 1.0.0 | ✅ stable | 2026-03-07 | Python 3.12, TS 5.5, Go 1.23 |
| `python-fastapi` | layer2 | 1.0.0 | ✅ stable | 2026-03-07 | FastAPI 0.115, Python 3.12, uv 0.5 |
| `python-flask` | layer2 | 1.0.0 | ✅ stable | 2026-03-07 | Flask 3.1, Python 3.12, uv 0.5 |
| `typescript-next` | layer2 | 1.0.0 | ✅ stable | 2026-03-07 | Next.js 15, TypeScript 5.5, Node 20 |

> **Perfis plannedados** (ainda não implementados):
> - `k8s-helm` (layer3) — IMP-22
> - `terraform-aws` (layer3) — IMP-23
> - `go-chi` (layer2) — backlog
> - `data-pipeline-airflow` (layer3) — IMP-26

---

## Detalhamento por Perfil

### `devops-programming` — v1.0.0

**Layer**: core
**Status**: ✅ stable
**Descriptor**: [`profile-descriptors/devops-programming.yaml`](../profile-descriptors/devops-programming.yaml)
**Prompt**: [`.github/prompts/domain/devops-programming.prompt.md`](../.github/prompts/domain/devops-programming.prompt.md)

| Versão | Data | O que mudou |
|--------|------|-------------|
| 1.0.0 | 2026-03-01 | Versão inicial — criação do schema 1.0.0, descriptor, prompt domain |

**Requer**: git, uv (Python), node >= 20 (TS), go >= 1.22 (Go)
**Exclui com**: `devops-infrastructure`, `devops-analysis`
**Combina com**: qualquer perfil layer2 de programação

---

### `python-fastapi` — v1.0.0

**Layer**: layer2
**Status**: ✅ stable
**Descriptor**: [`profile-descriptors/python-fastapi.yaml`](../profile-descriptors/python-fastapi.yaml)
**Templates**: [`.github/templates/python-fastapi/`](../.github/templates/python-fastapi/)
**Prompt**: [`.github/prompts/domain/layer2-python-fastapi.prompt.md`](../.github/prompts/domain/layer2-python-fastapi.prompt.md)

| Versão | Data | O que mudou |
|--------|------|-------------|
| 1.0.0 | 2026-03-07 | Versão inicial — app factory + lifespan, pydantic-settings, pytest-asyncio, Dockerfile multistage, Makefile 12 targets |

**Stack**: FastAPI ^0.115, Uvicorn, Pydantic-settings, pytest-asyncio, httpx (AsyncClient), ruff, bandit, pip-audit
**Requer**: devops-programming + language == python
**Exclui com**: `python-flask`

---

### `python-flask` — v1.0.0

**Layer**: layer2
**Status**: ✅ stable
**Descriptor**: [`profile-descriptors/python-flask.yaml`](../profile-descriptors/python-flask.yaml)
**Templates**: [`.github/templates/python-flask/`](../.github/templates/python-flask/)
**Prompt**: [`.github/prompts/domain/layer2-python-flask.prompt.md`](../.github/prompts/domain/layer2-python-flask.prompt.md)

| Versão | Data | O que mudou |
|--------|------|-------------|
| 1.0.0 | 2026-03-07 | Versão inicial — application factory, blueprints, flask-wtf CSRF, flask-talisman, gunicorn, Dockerfile multistage |

**Stack**: Flask ^3.1, Flask-WTF, Flask-Talisman, Gunicorn, pytest, ruff, bandit, pip-audit
**Requer**: devops-programming + language == python
**Exclui com**: `python-fastapi`

---

### `typescript-next` — v1.0.0

**Layer**: layer2
**Status**: ✅ stable
**Descriptor**: [`profile-descriptors/typescript-next.yaml`](../profile-descriptors/typescript-next.yaml)
**Templates**: [`.github/templates/typescript-next/`](../.github/templates/typescript-next/)
**Prompt**: [`.github/prompts/domain/layer2-typescript-next.prompt.md`](../.github/prompts/domain/layer2-typescript-next.prompt.md)

| Versão | Data | O que mudou |
|--------|------|-------------|
| 1.0.0 | 2026-03-07 | Versão inicial — App Router, Server Components, TypeScript strict, Jest + RTL, Dockerfile multistage pnpm |

**Stack**: Next.js ^15, React ^19, TypeScript ^5.5, zod, Jest ^29, ESLint 9, Prettier 3, pnpm
**Requer**: devops-programming + language == typescript

---

## Convenções de Versionamento

Este projeto segue **Semantic Versioning 2.0.0** (semver.org) adaptado para templates:

| Tipo de mudança | MAJOR | MINOR | PATCH |
|----------------|-------|-------|-------|
| Mudança no schema do descriptor que quebra compatibilidade | ✅ | | |
| Remoção de campo obrigatório de template | ✅ | | |
| Novo perfil adicionado | | ✅ | |
| Novo campo opcional em descriptor | | ✅ | |
| Nova template adicionada a perfil existente | | ✅ | |
| Atualização de dependência (sem quebrar) | | | ✅ |
| Correção de bug em template | | | ✅ |
| Atualização de documentação | | | ✅ |

**Regra de ouro**: se um projeto gerado com versão anterior parar de funcionar após atualizar o perfil → é MAJOR.

---

## Procedimento de Atualização

Ao lançar nova versão de um perfil:

1. Atualizar `VERSION` / `version` no descriptor YAML
2. Atualizar `LAST_TESTED_DATE` / `last_tested` no descriptor
3. Adicionar entrada na tabela de histórico deste arquivo
4. Adicionar entrada no `CHANGELOG.md` (seção `[Unreleased]` → nova versão)
5. Atualizar `COMPATIBILITY-MATRIX.md` se a compatibilidade mudou
6. Executar `uv run pytest tests/ -q` — todos os testes devem passar
7. Commit com mensagem: `chore(profile): bump {nome}-profile to vX.Y.Z`
