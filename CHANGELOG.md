# Changelog

All notable changes to the **Enterprise Default Project Template** will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

### Added

#### Sprint 3: Documentation P1 (ACTION_PLAN_TO_10 — Mar 2026)
- `docs/TROUBLESHOOTING.md` — comprehensive troubleshooting guide:
  - 8 major sections covering all common issues
  - 24 specific problems with symptoms and multiple solutions each
  - Categories: Setup & Initialization (symlinks, project init), Git & Version Control (pre-commit, Gitleaks, large files), Python Environment (pytest imports, Black/Ruff conflicts, MyPy errors), Testing (fixtures, coverage, performance), Security & Pre-commit (secrets committed, Bandit warnings, Ansible Vault), Documentation & Links (broken links, rendering), Scripts & Automation (Makefile, permissions, environment variables), VS Code Integration (settings, interpreter)
  - Additional resources: useful commands reference, log locations, documentation index
- `docs/CONVENTIONS.md` — technical standards and conventions guide:
  - 10 comprehensive sections defining project standards
  - Code Structure: Python (PEP 8, Black 88 chars, Python 3.12+), Markdown (ATX headers, line 80), YAML (2 spaces), Shell (bash, shellcheck)
  - Naming Conventions: comprehensive table with 15+ patterns (snake_case, PascalCase, kebab-case)
  - Python Standards: Type hints (required for public APIs), Docstrings (Google style), Imports (3 groups), Error handling (specific exceptions), Logging (module logger, 5 levels)
  - Testing Standards: Organization (AAA pattern), Coverage (≥80% target), Markers (9 markers: unit/integration/slow/smoke/security/skip_ci/requires_docker/requires_ssh/requires_network), Fixtures (shared conftest, 4 scopes)
  - Git Conventions: Conventional Commits (9 types with scopes), Branch naming (NNN-description, fix-, security-), PR templates
  - Documentation Standards: README structure (11 sections), Inline docs (explain WHY), Session docs (4 files per session)
  - Security Standards: Credentials (.secrets/ directory), Input validation, File permissions (600 secrets, 700 scripts)
  - File Organization: Root directory structure, .gitignore patterns
  - Automation Standards: Makefile (self-documenting help), Script headers (comprehensive template)
  - Enforcement Tools: Black, Ruff, MyPy, Bandit, pytest, pre-commit, Gitleaks, shellcheck
- `scripts/validate-docs-links.sh` — automated markdown link validation:
  - Extract markdown links: [text](url) and [ref]: url patterns
  - Validate relative/absolute links (skip external URLs: http/https/ftp/mailto)
  - Check file/directory existence with path normalization
  - Suggest fixes: find similar filenames, show relative paths
  - Summary: counters for files/links/broken with color-coded output (RED/GREEN/YELLOW/BLUE)
  - Options: --fix (suggestions), --help, --verbose
  - Exclusions: .git, node_modules, .venv, venv
  - Exit codes: 0 (valid), 1 (broken), 2 (invalid usage)

#### Sprint 2: Testing P0 (ACTION_PLAN_TO_10 — Mar 2026)
- `pytest.ini` — comprehensive pytest configuration:
  - 70 lines with markers, verbose output, coverage settings
  - 9 custom markers: unit, integration, slow, smoke, security, skip_ci, requires_docker, requires_ssh, requires_network
  - Coverage configuration: ≥80% threshold, term-missing, --cov-report=html
  - Discovery patterns: test_*.py and *_test.py
  - Python warnings and doctest integration
- `tests/conftest.py` — expanded shared fixtures (150+ lines):
  - 7 new fixtures: temp_file, temp_dir, mock_env, monkeypatch_dict, capture_logs, benchmark_timer, project_root
  - Each fixture with docstring and practical examples
  - Scopes: function (default), module, session
  - Integration with existing fixtures
- `tests/test_example.py` — comprehensive test examples (320+ lines):
  - Demonstrates all testing patterns and best practices
  - Sections: Fixtures usage, Parametrization (pytest.mark.parametrize with 3+ cases), Mocking (unittest.mock, pytest-mock), Exception testing (pytest.raises with match), Markers (all 9 custom markers with examples), AAA pattern (Arrange-Act-Assert), Coverage edge cases, Integration tests, Performance/Benchmark tests
  - Real-world scenarios for each pattern
  - Comments explaining best practices
- `docs/TESTING_GUIDE.md` — complete testing guide (650+ lines):
  - 12 comprehensive sections
  - Quick Start: installation, basic commands, first test
  - Testing Philosophy: AAA pattern, test isolation, coverage goals
  - Test Organization: directory structure, naming conventions, test classes
  - Fixtures Deep Dive: built-in fixtures, custom fixtures, scopes, parametrization
  - Markers Explained: all 9 markers with usage examples and CLI commands
  - Mocking Strategies: unittest.mock vs pytest-mock, patching, side effects
  - Coverage Requirements: targets (≥80% overall, ≥90% critical, ≥95% utils), measurement, reports
  - Running Tests: 13 Makefile commands, pytest CLI, filtering, parallel execution
  - CI/CD Integration: GitHub Actions examples, status badges
  - Debugging Tests: pytest options (-vv, --pdb, --lf, --sw), logging
  - Best Practices: 12 guidelines (one assert per test, descriptive names, test data builders, avoid test interdependence)
  - Troubleshooting: 8 common issues with solutions
- `Makefile` — 13 new testing commands (90+ lines):
  - test: run all tests with coverage
  - test-unit / test-integration / test-smoke / test-security: filtered by marker
  - test-slow: only slow tests
  - test-fast: exclude slow tests
  - test-watch: continuous testing with pytest-watch
  - test-parallel: run tests in parallel with pytest-xdist
  - test-failed: rerun only failed tests (--lf)
  - coverage: detailed coverage report
  - coverage-html: generate HTML report and open in browser
  - benchmark: run performance tests
  - test-debug: run with --pdb for debugging
  - Each command with colored output, emojis, helpful messages
- `docs/INDEX.md` — added Testing Documentation section with 4 references

#### Sprint 1: Security P0 (ACTION_PLAN_TO_10 — Mar 2026)
- `.gitleaks.toml` — secret scanning configuration (60 lines):
  - 6 rule categories: generic-api-key, aws-access-key, private-key, password-in-url, vault-token, github-token
  - Entropy threshold: 3.5 for base64/hex detection
  - Path allowlist: tests/, docs/, .example files
  - Comprehensive regex patterns for secret detection
- `.pre-commit-config.yaml` — pre-commit hooks (70 lines):
  - 7 repos with multiple hooks: pre-commit-hooks (8 hooks: trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files 500KB, check-merge-conflict, check-case-conflict, mixed-line-ending, detect-private-key), gitleaks (secret scanning), shellcheck (shell script linting), black (Python formatting 88 chars), ruff (Python linting with security rules: S, flake8-bandit), mypy (type checking strict mode), bandit (Python security scanning)
  - Security focus: secret detection, large file prevention, security linting
  - Python 3.12+ compatibility
- `.github/workflows/security-scan.yml` — GitHub Actions security workflow (180 lines):
  - 7 security scanning jobs running in parallel
  - gitleaks-scan: Secret detection with gitleaks/gitleaks-action@v2, scans full history
  - dependency-check: Python Safety (pip-audit), Node.js audit (npm audit)
  - bandit-scan: Python security issues with bandit, SARIF output
  - checkov-scan: IaC security (Terraform, Docker, K8s) with bridgecrewio/checkov-action
  - trivy-scan: Container vulnerabilities with aquasecurity/trivy-action, CRITICAL/HIGH only
  - sast-codeql: Static analysis with github/codeql-action for Python/JavaScript
  - All jobs upload results to GitHub Security tab (SARIF format)
  - Triggers: push to main/develop, pull_request, schedule (weekly on Sundays 2 AM UTC)
- `docs/ANSIBLE_VAULT_GUIDE.md` — comprehensive Ansible Vault guide (600+ lines):
  - 8 major sections: What is Ansible Vault, When to Use, Quick Start, Encryption/Decryption, Editing Encrypted Files, Viewing Encrypted Files, Ansible Playbook Integration, Security Best Practices
  - 15 command examples with detailed explanations
  - Vault password management: file-based (.secrets/.vault_pass), environment variable, prompt
  - File permissions: chmod 600 for vault password files
  - Vault ID system: production, staging, development vaults
  - Rekeying procedures: rotating vault passwords
  - CI/CD integration: GitHub Actions secrets, GitLab CI variables
  - Security best practices: 12 guidelines (never commit unencrypted secrets, use .gitignore, rotate passwords quarterly, use vault IDs per environment, audit access logs)
  - Troubleshooting: 6 common issues with solutions
  - Real-world examples: encrypting group_vars, playbook execution with vault
- `docs/CREDENTIAL_ROTATION.md` — credential rotation procedures (500+ lines):
  - 6 major sections: Overview, Why Rotate, Rotation Schedule, Rotation Procedures, Automation, Compliance & Audit
  - Rotation schedules: Critical (quarterly), High (semi-annually), Medium (annually), Low (bi-annually)
  - 8 detailed rotation procedures: SSH keys, API tokens, Database passwords, Ansible Vault passwords, Cloud provider credentials (AWS/GCP/Azure), SSL/TLS certificates, Service account credentials, GitHub tokens
  - Each procedure: identification, generation, update, testing, revocation, verification (6 steps)
  - Automation section: scripts, tools (ansible-vault rekey, aws-vault, 1Password CLI), CI/CD integration
  - Compliance tracking: rotation log template, audit checklist, violation response
  - Emergency rotation: breach response, incident detection, forensics
- `pyproject.toml` — complete Python tooling configuration (140 lines):
  - Black: line-length=88, Python 3.12+, exclude patterns
  - Ruff: line-length=88, Python 3.12, 12 rule categories (E/F/I/N/D/UP/S/B/A/C4/SIM/RUF), ignore=["D203", "D213"], per-file-ignores for tests
  - MyPy: strict mode, Python 3.12, ignore missing imports, no implicit optionals
  - Bandit: exclude tests/docs, skips=["B101", "B601"]
  - isort: Black-compatible profile, known_first_party
  - pytest: markers, testpaths, python_files, addopts
  - coverage: source paths, omit patterns (tests, .venv, migrations), reporting
- `docs/INDEX.md` — added Security Documentation section with 5 references

### Changed
- `docs/INDEX.md` — restructured with 3 new sections: Security Documentation (5 items), Testing Documentation (4 items), Documentation Standards (3 items)

---

## [9.9.9] — 2026-03-14

---

## [9.9.9] — 2026-03-14

### Added

#### Validação de Profile Descriptors (IMP-32)
- `scripts/lib/validate.py` — módulo de validação de profile-descriptors:
  - `validate_descriptors(dir) → ValidationReport` — valida todos os `.yaml` em `profile-descriptors/`
  - 6 regras por descriptor: `name`, `description`, `version` (semver X.Y.Z), `last_tested`, `layer`, sintaxe YAML
  - Validação cruzada: nomes duplicados + `combines_with`/`excludes_with` com perfis inexistentes (warning)
  - Compatível com schema antigo (`VERSION`/`LAST_TESTED_DATE`) e novo (`version`/`last_tested`)
  - `combines_with` aceita lista de strings e lista de objetos `{name, notes}`
  - Exit code 0 se `valid=True` (erros=0; avisos são permitidos); exit code 1 se há erros
- `scripts/scaffold.py --validate` — flag CLI de validação; `--validate --json` para CI/automação
- `tests/test_smoke_imp32.py` — 42 testes (410 total)

#### CI/CD do Template (IMP-31)
- `.github/workflows/ci-template.yml` — workflow GitHub Actions completo com 3 jobs:
  - **test** — matrix Python 3.10 / 3.11 / 3.12 rodando `pytest tests/ --tb=short -q`
  - **cli-smoke** — `--list-profiles --json`, `--dry-run`, `--publish --json` contra código real
  - **lint** — `py_compile` em todos `scripts/lib/*.py` + `yaml.safe_load` em todos `profile-descriptors/*.yaml`
- Disparo em `pull_request` e `push` com filtro de paths (`scripts/**`, `tests/**`, `profile-descriptors/**`)
- `concurrency` com `cancel-in-progress: true` para PRs
- `tests/test_smoke_imp31.py` — 26 testes (368 total)

#### Release Publishing (IMP-30)
- `scripts/lib/publish.py` — módulo de publicação de release:
  - `publish_template(output_dir, project_root)` — gera `enterprise-template-v{version}-{YYYYMMDD}.tar.gz`
  - `_collect_files(project_root)` — coleta arquivos por padrões de inclusão, excluindo `__pycache__`, `.venv`, `.git`, `.secrets`, `dist`, `*.pyc`
  - Manifesto JSON (`release-manifest-v{version}-{YYYYMMDD}.json`) com `version`, `file_count`, `size_bytes`, `files`
  - Idempotente por data: chamadas múltiplas no mesmo dia sobrescrevem o tarball anterior
- `scripts/scaffold.py --publish` — flag CLI para gerar release tarball
- `scripts/scaffold.py --output-dir PATH` — diretório de saída configurável (default: `dist/`)
- `tests/test_smoke_imp30.py` — 35 testes (342 total)

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
