# Changelog

All notable changes to the **Enterprise Default Project Template** will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

### Added

#### Documentação por Perfil (IMP-29)
- `scripts/lib/templates.py` — `generate_profile_guide()` — gera `docs/PROFILE-GUIDE-{combo}.md` no projeto destino:
  - Tabela de perfis ativos com camada e descrição
  - Inventário de arquivos gerados por perfil (de `generates.files` / `templates`)
  - Requisitos de segurança consolidados (de `security.enforces`)
  - Quick Start com pré-requisitos e pré-requisitos agregados
  - Referências por stack (baseadas nas `tags` dos perfis)
  - Idempotente — não sobrescreve se já existe
- `_compute_combo_slug()` — slug derivado dos perfis layer2+ (exclui core e transversais)
- `_layer_order_int()` / `_layer_display_name()` — helpers de mapeamento de camada
- `scripts/scaffold.py` — integração: guia gerado após composição e após `--upgrade`
- `tests/test_smoke_imp29.py` — 33 testes (307 total)

---

## [1.3.0] — 2026-03-07

### Added

#### Infraestrutura e Composição (IMP-15, IMP-24)
- `scripts/lib/infra.py` — motor de geração de artefatos de infraestrutura:
  - `generate_ci_workflow()` — `.github/workflows/ci.yml` por linguagem (Python/uv, TypeScript/pnpm, Go)
  - `generate_dockerfile()` — Dockerfile multistage por linguagem (python:3.12-slim, node:20-slim/pnpm, golang:1.23-alpine+distroless)
  - `generate_docker_compose()` — `docker-compose.yml` com app + PostgreSQL/Redis comentados
  - `generate_runbook()` — `docs/RUNBOOK.md` template operacional
- `scripts/scaffold.py --infra` — nova flag para gerar artefatos de infra em CI
- `scripts/lib/composer.py` — Motor de Composição de Perfis:
  - `load_all_descriptors()` — carrega todos os `*.yaml` de `profile-descriptors/`
  - `resolve_order()` — ordena por camada (core → layer2 → layer3 → transversal)
  - `check_conflicts()` — detecta pares proibidos via `excludes_with`
  - `get_template_entries()` — normaliza Schema A (`templates_path`) e Schema B (`generates.files`)
  - `ProfileComposer.compose()` — copia templates com rollback em erro parcial
- `scripts/scaffold.py --compose PROFILES` — aplica perfis ao projeto alvo
- 21 novos testes (`test_smoke_infra.py`) + 18 novos testes (`test_smoke_composer.py`)

#### Governança (IMP-25)
- `docs/TEMPLATE-VERSIONS.md` — versionamento por perfil com histórico e convenções semver
- `docs/COMPATIBILITY-MATRIX.md` — matriz perfis × perfis com regras de composição
- `CHANGELOG.md` — este arquivo (histórico desde v0.1.0)
- `docs/DEPRECATION-POLICY.md` — política de depreciação com períodos de aviso e procedimento

#### Perfis Layer 2 (IMP-20, IMP-20b, IMP-21)
- `profile-descriptors/python-fastapi.yaml` — descriptor v1.0.0
- `profile-descriptors/python-flask.yaml` — descriptor v1.0.0
- `profile-descriptors/typescript-next.yaml` — descriptor v1.0.0
- `.github/prompts/domain/layer2-python-fastapi.prompt.md`
- `.github/prompts/domain/layer2-python-flask.prompt.md`
- `.github/prompts/domain/layer2-typescript-next.prompt.md`
- `.github/templates/python-fastapi/` — 11 arquivos (src, tests, pyproject.toml, Dockerfile, docker-compose.yml, Makefile, .env.example)
- `.github/templates/python-flask/` — 12 arquivos
- `.github/templates/typescript-next/` — 14 arquivos (app, lib, tests, tsconfig, jest, eslint, prettier, Dockerfile, docker-compose.yml, Makefile)

#### Profile Descriptor Schema (IMP-19a)
- `docs/copilot/PROFILE-DESCRIPTOR-SCHEMA.md` — schema 1.0.0 com todos os campos anotados
- `profile-descriptors/devops-programming.yaml` — descriptor do perfil core
- `profile-descriptors/README.md` — índice de perfis disponíveis

#### scaffold.py flags (IMP-19b)
- `--list-profiles` — tabela Rich ou JSON com perfis disponíveis
- `--dry-run` — manifesto de operações sem criar arquivos
- `--json` — output JSON para CI/automação
- `--config FILE` — configuração não-interativa via YAML

### Changed
- Suite de testes: 58 → 97 testes passando
- `profile-descriptors/README.md` — atualizado com typescript-next

---

## [1.2.0] — 2026-03-05

### Added

#### Testes (IMP-16)
- `tests/test_smoke.py` — 54 smoke tests: 9 combos domínio × linguagem × 2 funções × 3 assertions
- `tests/test_templates_snapshot.py` — 4 snapshot tests para `programming × python`
- `tests/conftest.py` — fixtures `make_project_config` e `update_snapshots`
- `tests/snapshots/` — baseline snapshots para CI

#### Scaffold Python (IMP-05, IMP-06, IMP-07, IMP-08, IMP-09)
- `scripts/scaffold.py` — script interativo com fluxo condicional
- `scripts/lib/config.py` — `ProjectConfig` dataclass, constantes, paths
- `scripts/lib/templates.py` — `generate_copilot_rules()`, `generate_copilot_instructions()`
- `scripts/lib/project.py` — `create_structure()`, `copy_speckit()`, `generate_constitution()`
- `scripts/lib/links.py` — `setup_symlinks()`, `check_symlinks()`
- `scripts/lib/git.py` — `init_repository()`
- `scripts/lib/vscode.py` — `generate_settings()`, `generate_mcp()`, `generate_extensions()`
- `scripts/lib/ui.py` — `collect_project_info()`, `show_banner()`, `show_menu()`

---

## [1.1.0] — 2026-02-28

### Added
- `.github/prompts/domain/devops-programming.prompt.md` — domain profile de programação
- `.github/prompts/domain/devops-infrastructure.prompt.md`
- `.github/prompts/domain/devops-analysis.prompt.md`
- `.github/prompts/domain/devops-security.prompt.md` — transversal
- `.github/prompts/session-start.prompt.md` — ritual de início de sessão
- `.github/prompts/session-end.prompt.md` — ritual de encerramento
- `.github/copilot-instructions.md` — instrução auto-injetada
- `.github/agents/template-architect.agent.md`
- `.specify/` — integração SpecKit

### Changed
- `.copilot-rules.md` consolidado (5 arquivos → 1 arquivo) — IMP-13

---

## [1.0.0] — 2026-01-27

### Added
- Estrutura inicial do template: `docs/`, `scripts/`, `Makefile`, `README.md`
- `Makefile` com 40+ targets: init, setup-python, setup-node, dev, build, test, lint, format, docker-*, status, clean
- `scripts/init-new-project.sh` — inicialização de projetos
- `scripts/setup-project-links.sh` — gestão de symlinks `.copilot-*`
- `scripts/check-project-links.sh` — verificação de symlinks
- `docs/INDEX.md`, `docs/TODO.md` — documentação incremental
- `default-project.code-workspace` — workspace VS Code

---

[Unreleased]: https://github.com/vyajobs/a-default-project/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/vyajobs/a-default-project/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/vyajobs/a-default-project/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/vyajobs/a-default-project/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/vyajobs/a-default-project/releases/tag/v1.0.0
