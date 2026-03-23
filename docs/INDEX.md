# 📑 Project Index - Enterprise Default Project Template

**Last Updated**: 2026-03-21 ▶️ Em andamento
**Project Status**: ✅ Production Ready Template
**Version**: 1.3.0
**Last Session**: 2026-03-21 — Session Manager Agent tested in production — first automated session

---

## 🎯 About This Template

This is a **production-ready, scalable project template** designed to accelerate development of enterprise applications. It provides:

- ✅ Complete project structure
- ✅ Shared configuration management via symlinks
- ✅ Automated initialization scripts
- ✅ 40+ Makefile commands
- ✅ Multi-language support (Python, TypeScript, Go)
- ✅ Docker and CI/CD pre-configured
- ✅ Testing infrastructure ready

### Using This Template

📘 **[Read the Template Usage Guide](TEMPLATE_USAGE.md)** for complete instructions

Quick start:
```bash
# Clone and initialize
git clone <template-url> my-new-project
cd my-new-project

# Usar scaffold.py (recomendado)
uv run scripts/scaffold.py new --name my-new-project

# Ou usar Makefile com script legado
make init-new-project NAME=my-new-project
```

---

## 📁 Project Structure

```
a-default-project/
├── .copilot-rules.md               # Copilot rules — consolidado (7 seções, ~193 linhas)
├── .git/                           # Git repository
├── .github/                        # GitHub configurations
│   ├── workflows/                 # CI/CD pipelines
│   └── ISSUE_TEMPLATE/           # Issue templates
├── .secrets/                       # Sensitive files (git-ignored)
│   └── README.md                  # Security guidelines
├── .specify/                       # Speckit configuration
│   ├── config.json               # Speckit settings
│   └── specs/                    # API specifications
├── .vscode/                        # VS Code settings
├── docs/                           # Documentation
│   ├── INDEX.md                  # This file
│   ├── TODO.md                   # Task list
│   ├── TODAY_ACTIVITIES.md       # Daily activities
│   ├── TEMPLATE_USAGE.md         # Template usage guide
│   ├── MIGRATION-GUIDE.md        # ✅ IMP-37 — guia de migração entre versões do template
│   ├── MAKEFILE.md               # Makefile documentation
│   ├── PROJECT-KNOWLEDGE-MAP.md  # Mapa de conhecimento: funcionalidades, menus, estruturas
│   ├── SHARED_CONFIGS_SOLUTION.md # Shared configs architecture
│   └── SESSIONS/                 # Session records
│       ├── 2026-01-27/          # Foundation session
│       ├── 2026-01-28/          # Testing session
│       ├── 2026-02-27/          # Domain Profiles — 19 decisões de design (encerrada)
│       ├── 2026-02-28/          # IMP-01 debate + IMP-13 consolidação copilot files (encerrada)
│       ├── 2026-03-01/          # IMP-01..08 concluídos: scaffold.py, prompts, domain profiles (encerrada)
│       ├── 2026-03-05/          # IMP-14 Fase A ✅ + IMP-17 debate (encerrada)
        ├── 2026-03-07/          # IMP-27 lgpd+soc2 (Layer4) + IMP-28 scaffold --upgrade (encerrada)
        ├── 2026-03-08/          # IMP-29..32 ✅ + Homologação + Plano IMP-33..44 (encerrada)
        ├── 2026-03-14/          # IMP-46 ✅ (testes integração estrutura+AppSec) + security/CI fixes (encerrada)
        ├── 2026-03-16/          # fix(session-start): MCP check via arquivo + projeto teste enterprise-infra-docker (encerrada)
        ├── 2026-03-20/          # Session Manager Agent v1.0.0 criado — automação de workflow de sessão (encerrada)
        └── 2026-03-21/          # Bug fix agentes + documentação scaffold upgrade (em andamento)
        └── 2026-03-21/          # Session Manager Agent tested in production — first automated session (em andamento)
├── .github/
│   └── agents/                   # Custom Copilot agents
│       └── session-manager.agent.md  # ✅ v1.0.0 — automação de inicialização de sessão
├── setup/                          # Setup & installation (legacy)
│   ├── README.md                 # Setup scripts documentation
│   ├── init-new-project.sh       # ⚠ DEPRECATED - Use scaffold.py
│   ├── setup-project-links.sh    # ⚠ DEPRECATED - Use scaffold.py
│   └── check-project-links.sh    # ⚠ DEPRECATED - Use scaffold.py
├── scripts/                        # Active automation scripts
│   ├── scaffold.py               # ✅ Main scaffolding tool (replaces legacy)
│   ├── manage.py                 # Project management TUI
│   ├── lib/                      # Python modules: config, ui, project, links, git, templates, vscode
│   ├── cleanup-tmp.sh            # Temporary files cleanup
│   └── validate-docs-links.sh    # Markdown links validation
├── src/                            # Source code
├── tests/                          # Test suites
├── Makefile                        # Build automation (40+ commands)
├── README.md                       # Main documentation
└── default-project.code-workspace # VS Code workspace
```

---

## 📚 Documentation Index

### Main Documentation
- **[README.md](../README.md)** - Main project documentation
  - Overview and objectives
  - Features and architecture
  - Getting started guide
  - Configuration management
  - Development workflow
  - Testing strategy
  - CI/CD integration
  - Security best practices

### Template Documentation
- **[docs/TEMPLATE_USAGE.md](TEMPLATE_USAGE.md)** - ⭐ Complete template guide
  - How to use this template
  - Automatic initialization
  - Manual setup
  - Configuration management
  - Troubleshooting
  - Checklist

### Copilot / Speckit Strategy
- **[docs/copilot/DOMAIN-PROFILES-STRATEGY.md](copilot/DOMAIN-PROFILES-STRATEGY.md)** - ⭐ Templates adaptáveis por domínio DevOps
  - Arquitetura de três camadas (Foundation / Domain Profile / Context Injection)
  - Diferença entre os três modos: programação, infraestrutura, análise
  - Como o Speckit + MCP amplifica cada modo
  - Estrutura de arquivos proposta

- **[docs/copilot/DOMAIN-PROFILES-DECISIONS.md](copilot/DOMAIN-PROFILES-DECISIONS.md)** - Questões e decisões
  - 🟢 **19 decisões completamente resolvidas (D-01 a D-19)**
  - Implementação mapeada em IMP-01 a IMP-10 no TODO.md

### Technical Documentation
- **[docs/MAKEFILE.md](MAKEFILE.md)** - Complete Makefile guide
  - All commands reference (40+ commands)
  - Prerequisites
  - Quick start
  - Workflow examples
  - Troubleshooting
  - Customization

- **[docs/SHARED_CONFIGS_SOLUTION.md](SHARED_CONFIGS_SOLUTION.md)** - Shared configs architecture
  - Problem analysis (duplication across projects)
  - Solution approaches (symlinks, submodules, sync)
  - Implementation guide
  - Automation scripts
  - Benefits and metrics

### Security Documentation
- **[docs/ANSIBLE_VAULT_GUIDE.md](ANSIBLE_VAULT_GUIDE.md)** - ⭐ Complete Ansible Vault reference
  - Why use Ansible Vault (security benefits, compliance)
  - Initial configuration (.vault_pass setup, ansible.cfg)
  - Recommended structure (vault.yml + vars.yml pattern)
  - All essential commands (create, edit, view, encrypt, decrypt, rekey)
  - Playbook integration and best practices
  - Troubleshooting and CI/CD integration
  - Security checklist and compliance (SOC2, ISO27001, LGPD)

- **[docs/CREDENTIAL_ROTATION.md](CREDENTIAL_ROTATION.md)** - ⭐ Credential rotation procedures
  - Rotation policy (7 credential types with defined frequencies)
  - Immediate rotation triggers
  - Complete rotation procedures with bash scripts
  - Audit system and logging
  - Tool recommendations (1Password, HashiCorp Vault, AWS Secrets Manager)
  - Compliance mapping (SOC2, ISO27001, LGPD)

### Automation & Configuration Management
- **[docs/ANSIBLE_BEST_PRACTICES.md](ANSIBLE_BEST_PRACTICES.md)** - ⭐ Comprehensive Ansible guide
  - Core principles (idempotency, declarative design, module hierarchy, DRY)
  - Project structure (recommended directory layout, file naming conventions)
  - Inventory management (static, dynamic, best practices)
  - Playbook design (basic structure, conditionals, loops, tags)
  - Role development (structure, defaults, tasks, handlers, templates, meta)
  - Variable management (precedence hierarchy, naming, organization, vault)
  - Security best practices (Ansible Vault, privilege escalation, input validation)
  - Testing and validation (syntax check, ansible-lint, dry run, Molecule)
  - Performance optimization (facts, pipelining, caching, parallelism)
  - Error handling (failed_when, ignore_errors, block/rescue/always)
  - Documentation standards (playbook headers, role README)
  - CI/CD integration (GitHub Actions, GitLab CI examples)

- **[docs/MOLECULE_TESTING_GUIDE.md](MOLECULE_TESTING_GUIDE.md)** - ⭐ Testing Ansible roles with Molecule
  - What is Molecule (features, benefits, use cases)
  - Installation requirements (Python 3.8+, Docker, Ansible)
  - Quick start (initialize role, directory structure, run tests)
  - Project structure (molecule.yml, converge.yml, prepare.yml, verify.yml, tests/)
  - Configuration (platform configs, multiple platforms matrix, custom Dockerfile)
  - Testing workflow (complete test sequence, manual steps, development workflow)
  - Writing tests (Testinfra examples: file/package/service/socket/process tests)
  - Drivers comparison (Docker, Podman, Vagrant, EC2, GCE)
  - Scenarios (multiple scenarios, examples for default/SSL/cluster)
  - CI/CD integration (GitHub Actions matrix, GitLab CI parallel)
  - Best practices (pre-built images, idempotence testing, test organization)
  - Troubleshooting (Docker issues, Testinfra imports, idempotence failures)

- **[docs/ANSIBLE_PLAYBOOK_TEMPLATES.md](ANSIBLE_PLAYBOOK_TEMPLATES.md)** - ⭐ Ready-to-use playbook patterns
  - Docker management (installation, compose deployment, cleanup, health check)
  - Database operations (PostgreSQL backup/restore, MySQL management)
  - Application deployment (zero-downtime deployment, blue-green deployment)
  - Backup and restore (comprehensive system backup)
  - Monitoring and health checks (comprehensive health check)
  - Maintenance operations (system update and reboot)
  - Security operations (security hardening)
  - Network configuration

- **[.github/templates/ansible/](../.github/templates/ansible/)** - ⭐ Production-ready playbook examples
  - `README.md` - Template usage guide and customization tips
  - `deploy-app.yml` - Zero-downtime application deployment
  - `docker-deploy.yml` - Docker Compose stack deployment
  - `health-check-system.yml` - Comprehensive system health check
  - `backup-database.yml` - PostgreSQL database backup with rotation

### Testing Documentation
- **[docs/TESTING_GUIDE.md](TESTING_GUIDE.md)** - ⭐ Complete testing guide
  - Overview of testing infrastructure (pytest, coverage, mocking)
  - Quick start and basic commands
  - Test organization and directory structure
  - Writing tests (patterns, assertions, fixtures)
  - Running tests (selection, parallel execution, markers)
  - Code coverage configuration and targets (≥80%)
  - Test markers (unit, integration, smoke, security, slow)
  - Built-in and custom fixtures from conftest.py
  - Mocking strategies (unittest.mock, pytest-mock)
  - Best practices (isolation, descriptive names, AAA pattern)
  - CI/CD integration with GitHub Actions
  - Troubleshooting common issues

- **[tests/test_example.py](../tests/test_example.py)** - Example test patterns
  - Unit test examples with proper structure
  - Fixture usage demonstrations
  - Mocking and patching patterns
  - Parametrized tests
  - Integration test examples
  - Performance testing with benchmarks
  - Security test patterns

- **[tests/conftest.py](../tests/conftest.py)** - Shared test fixtures
  - Common fixtures (temp_file, mock_env, mock_subprocess)
  - Benchmark timer for performance tests
  - Test isolation fixtures
  - Logging capture utilities

- **[pytest.ini](../pytest.ini)** - Pytest configuration
  - Test discovery settings
  - Coverage configuration (≥80% target)
  - Test markers definition
  - Output formatting

### Session Documentation
- **[docs/SESSIONS/2026-01-27/](SESSIONS/2026-01-27/)** - Phase 1: Foundation
  - SESSION_RECOVERY - Complete session details
  - SESSION_REPORT - Progress and metrics
  - FINAL_STATUS - Final completion status

- **[docs/SESSIONS/2026-01-28/](SESSIONS/2026-01-28/)** - Phase 2: Testing & Template
  - SESSION_RECOVERY - Context reload
  - TODAY_ACTIVITIES - Detailed timeline
  - Makefile tests (11 commands, 100% success)

- **[docs/SESSIONS/2026-02-27/](SESSIONS/2026-02-27/)** - Sessão: Domain Profiles Strategy (encerrada)
  - [SESSION_RECOVERY](SESSIONS/2026-02-27/SESSION_RECOVERY_2026-02-27.md) — Recuperação de contexto e regras
  - [TODAY_ACTIVITIES](SESSIONS/2026-02-27/TODAY_ACTIVITIES_2026-02-27.md) — Atividades do início
  - [DAILY_ACTIVITIES](SESSIONS/2026-02-27/DAILY_ACTIVITIES_2026-02-27.md) — Log detalhado completo
  - [SESSION_REPORT](SESSIONS/2026-02-27/SESSION_REPORT_2026-02-27.md) — Relatório e artefatos
  - [FINAL_STATUS](SESSIONS/2026-02-27/FINAL_STATUS_2026-02-27.md) — Status final 🏁

- **[docs/SESSIONS/2026-03-16/](SESSIONS/2026-03-16/)** - Sessão: fix(security) Dependabot + fix(session-start) MCP (encerrada)
  - [SESSION_RECOVERY](SESSIONS/2026-03-16/SESSION_RECOVERY_2026-03-16.md) — Contexto recuperado de 2026-03-14
  - [DAILY_ACTIVITIES](SESSIONS/2026-03-16/DAILY_ACTIVITIES_2026-03-16.md) — Log detalhado completo
  - [FINAL_STATUS](SESSIONS/2026-03-16/FINAL_STATUS_2026-03-16.md) — Status final 🏁

- **[docs/SESSIONS/2026-03-20/](SESSIONS/2026-03-20/)** - Sessão: Session Manager Agent v1.0.0 (encerrada)
  - [SESSION_RECOVERY](SESSIONS/2026-03-20/SESSION_RECOVERY_2026-03-20.md) — Contexto recuperado de 2026-03-16
  - [DAILY_ACTIVITIES](SESSIONS/2026-03-20/DAILY_ACTIVITIES_2026-03-20.md) — Log detalhado completo
  - [SESSION_REPORT](SESSIONS/2026-03-20/SESSION_REPORT_2026-03-20.md) — Relatório técnico
  - [FINAL_STATUS](SESSIONS/2026-03-20/FINAL_STATUS_2026-03-20.md) — Status final 🏁

- **[docs/SESSIONS/2026-03-21/](SESSIONS/2026-03-21/)** - Sessão: Bug Fix + Documentação (encerrada)
  - [SESSION_RECOVERY](SESSIONS/2026-03-21/SESSION_RECOVERY_2026-03-21.md) — Contexto recuperado de 2026-03-20
  - [DAILY_ACTIVITIES](SESSIONS/2026-03-21/DAILY_ACTIVITIES_2026-03-21.md) — Log detalhado (3 atividades)
  - [SCAFFOLD_UPGRADE_PROCESS](SESSIONS/2026-03-21/SCAFFOLD_UPGRADE_PROCESS.md) — ⭐ Documentação completa do processo de upgrade
  - **Destaques**:
    - 🐛 Bug fix crítico: padrão glob de agentes corrigido (`speckit.*` → `*`)
    - 📝 Documentação: processo completo de `scaffold.py upgrade` (270+ linhas)

- **[docs/SESSIONS/2026-03-23/](SESSIONS/2026-03-23/)** - Sessão: Upgrade Example + Documentation (em andamento)
  - [SESSION_RECOVERY](SESSIONS/2026-03-23/SESSION_RECOVERY_2026-03-23.md) — Contexto recuperado de 2026-03-21
  - [DAILY_ACTIVITIES](SESSIONS/2026-03-23/DAILY_ACTIVITIES_2026-03-23.md) — Log detalhado (3 atividades)
  - [SESSION_REPORT](SESSIONS/2026-03-23/SESSION_REPORT_2026-03-23.md) — Relatório técnico
  - [UPGRADE_EXAMPLE_ENTERPRISE_PYTHON_ANALYSIS](SESSIONS/2026-03-23/UPGRADE_EXAMPLE_ENTERPRISE_PYTHON_ANALYSIS.md) — ⭐ Exemplo prático de upgrade de projeto legacy
  - [BUG_ANALYSIS_UPGRADE_NESTED_FOLDER](SESSIONS/2026-03-23/BUG_ANALYSIS_UPGRADE_NESTED_FOLDER.md) — 🐛 Análise de bug crítico no upgrade
  - **Destaques**:
    - 📚 Documentação: exemplo completo de upgrade com projeto real (450+ linhas)
    - 🔍 Análise: comparação session manager v0.x → v1.1.0
    - 🐛 Bug crítico identificado: upgrade cria pasta aninhada do projeto
    - 🔧 Análise técnica: causa raiz + 4 soluções propostas (600+ linhas)
    - ✅ Workaround aplicado: pasta aninhada removida com sucesso
    - ✅ Criado: `.scaffold-state.yaml` para enterprise-python-analysis

---

## 🤖 Copilot Agents

### Custom Agents
- **[.github/agents/session-manager.agent.md](../.github/agents/session-manager.agent.md)** - ⭐ Session initialization & organization
  - **Version**: 1.2.0 (updated 2026-03-23)
  - **Purpose**: Automate session start/end workflows
  - **Features**:
    - MCP validation (memory, sequential-thinking)
    - Context recovery from previous sessions
    - Security scanning (credentials, sensitive files)
    - Project organization (file placement, structure validation)
    - **NEW**: Git push mandatory on session end (D-17)
    - Documentation generation (session files)
  - **Usage**: `/session-start`, `/first-time-setup`, `/recover-context`
  - **Tool Preferences**: Pylance tools (priority), native VS Code tools
  - **Workflows**:
    - Recurring session start (7 steps)
    - First-time setup (7 steps)

---

## 🛠️ Core Files

### Template Scripts
| File | Purpose | Status |
|------|---------|--------|
| `scripts/scaffold.py` | ✅ **CRIADO** — PEP 723, uv run, entry point principal | ✅ v1.0.0 |
| `scripts/lib/config.py` | `ProjectConfig` dataclass, constantes | ✅ Criado |
| `scripts/lib/ui.py` | Prompts Rich, menus interativos | ✅ Criado |
| `scripts/lib/project.py` | Cria estrutura: 13 pastas + 11 arquivos | ✅ Criado |
| `scripts/lib/links.py` | Symlinks relativos, verificação de status | ✅ Criado |
| `scripts/lib/git.py` | git init + remote add | ✅ Criado |
| `scripts/lib/templates.py` | Gera `.copilot-rules-[projeto].md` | ✅ Criado |
| `scripts/lib/vscode.py` | Gera `mcp.json`, `settings.json`, `extensions.json` | ✅ Criado |
| `scripts/validate-docs-links.sh` | ✅ **CRIADO** — Validate markdown links, suggest fixes | ✅ Sprint 3 |
| `scripts/manage.py` | TUI Python | 🟡 Legado |
| `setup/init-new-project.sh` | Initialize new project | ⚠ DEPRECATED (use scaffold.py) |
| `setup/setup-project-links.sh` | Setup symlinks | ⚠ DEPRECATED (use scaffold.py) |
| `setup/check-project-links.sh` | Verify symlink integrity | ⚠ DEPRECATED (use scaffold.py) |

### Prompt Files (GitHub Copilot)
| File | Purpose | Status |
|------|---------|--------|
| `.github/prompts/session-start.prompt.md` | Ritual início de sessão | ✅ Criado 2026-03-01 |
| `.github/prompts/session-start-first.prompt.md` | Ritual 1ª sessão | ✅ Criado 2026-03-01 |
| `.github/prompts/session-end.prompt.md` | Ritual encerramento | ✅ Criado 2026-03-01 |
| `.github/prompts/domain/devops-programming.prompt.md` | Domain Profile: Programação | ✅ Criado 2026-03-01 |
| `.github/prompts/domain/devops-infrastructure.prompt.md` | Domain Profile: Infraestrutura | ✅ Criado 2026-03-01 |
| `.github/prompts/domain/devops-analysis.prompt.md` | Domain Profile: Análise | ✅ Criado 2026-03-01 |
| `.github/prompts/domain/devops-security.prompt.md` | Domain Profile: Segurança (transversal) | ✅ Criado 2026-03-05 |
| `.github/copilot-instructions.md` | Auto-injeção de regras P0/P1 em todo chat | ✅ Criado 2026-03-07 |

### Automation
| File | Purpose | Status |
|------|---------|--------|
| `Makefile` | Build and automation (40+ commands) | ✅ Complete |
| `.github/workflows/` | CI/CD pipelines | 🔄 Template |

### Configuration
| File | Purpose | Status |
|------|---------|--------|
| `.env.example` | Environment template | 🔄 Generated by Makefile |
| `.editorconfig` | Editor configuration | 🔄 Generated by Makefile |
| `.gitignore` | Git ignore rules | 🔄 Generated by Makefile |
| `config/*.json` | Environment configs | 🔄 Generated by Makefile |

### Docker
| File | Purpose | Status |
|------|---------|--------|
| `docker/Dockerfile` | Container definition | 🔄 Generated by Makefile |
| `docker/docker-compose.yml` | Multi-container setup | 🔄 Generated by Makefile |

---

## 🎯 Makefile Commands Reference

### Template Management
```bash
make init-new-project NAME=my-project  # Initialize new project from template
make setup-shared-configs              # Setup shared configuration repository
make setup-project-links               # Setup symlinks to shared configs
make check-project-links               # Verify symlinks status
```

### Quick Commands
```bash
make help          # Show all available commands
make init          # Initialize complete project
make status        # Show project status
```

### Setup Commands
```bash
make setup-python  # Configure Python project
make setup-node    # Configure Node.js project
make install-deps  # Install dependencies
```

### Development Commands
```bash
make dev           # Start development server
make build         # Build for production
make test          # Run all tests
make lint          # Run code linting
make format        # Format code
```

### Docker Commands
```bash
make docker-build  # Build Docker image
make docker-up     # Start containers
make docker-down   # Stop containers
```

### Maintenance Commands
```bash
make clean         # Remove generated files
make structure     # Create directory structure
```

---

## 🏗️ Architecture

### Design Patterns
1. **MVP (Model-View-Presenter)**
   - Clean separation of concerns
   - Testable business logic
   - Flexible UI changes

2. **Factory Pattern**
   - Flexible object creation
   - Dependency injection support
   - Loose coupling

3. **Repository Pattern**
   - Abstract data access layer
   - Easy database switching
   - Testable data operations

4. **Service Layer Pattern**
   - Business logic encapsulation
   - Reusable services
   - Clear responsibility

### Folder Structure
```
src/
├── core/              # Business logic
│   ├── models/       # Domain models
│   ├── interfaces/   # Contracts
│   └── services/     # Business services
├── data/              # Data access
│   ├── repositories/ # Data repositories
│   ├── factories/    # Data factories
│   └── migrations/   # DB migrations
├── presentation/      # UI layer
│   ├── views/        # Views
│   ├── presenters/   # Presenters
│   └── viewmodels/   # View models
├── infrastructure/    # Infrastructure
│   ├── config/       # Configuration
│   ├── logging/      # Logging
│   └── security/     # Security
└── shared/            # Utilities
    ├── constants/
    ├── helpers/
    └── validators/
```

---

## 🌐 Supported Languages

### Primary Languages
1. **Python** 🐍
   - FastAPI/Django
   - Data science
   - Automation

2. **TypeScript/JavaScript** 📘
   - Node.js backend
   - React/Vue/Angular
   - Full-stack apps

3. **Java** ☕
   - Spring Boot
   - Microservices
   - Android

4. **C#/.NET** 🔷
   - ASP.NET Core
   - Desktop apps
   - Azure services

5. **Go** 🔵
   - Microservices
   - CLI tools
   - Cloud-native

---

## 🔐 Security

### Protected Directories
- `.secrets/` - Sensitive files
- `.env*` - Environment variables

### Protected File Types
- `*.key` - Private keys
- `*.pem` - Certificates
- `*.crt` - Certificates
- `*.p12` - Certificate stores

### Best Practices
- Never commit secrets
- Use environment variables
- Rotate credentials regularly
- Use secret management tools
- Document required secrets

---

## 📊 Project Statistics

### Files Created
- **Total**: 4 major files
- **Documentation**: 3 comprehensive docs
- **Configuration**: Auto-generated files

### Code Metrics
- **Lines**: ~1,500+
- **Makefile Commands**: 40+
- **Documentation Pages**: 3

### Coverage
- **Documentation**: 100%
- **Automation**: 100%
- **Security**: Implemented

---

## 🚀 Getting Started

### Quick Start
```bash
# 1. Initialize project
make init

# 2. Choose language
make setup-python  # or make setup-node

# 3. Install dependencies
make install-deps

# 4. Start development
make dev
```

### Prerequisites
- Git
- Docker & Docker Compose (optional)
- Language runtime (Python/Node.js/Java/etc.)
- Make

---

## 📅 Version History

### Version 1.1.0 (2026-02-27)
- ✅ MCP configurado (`.vscode/mcp.json`) — `memory` + `sequential-thinking`
- ✅ `.secrets/` directory criado com guia de segurança
- ✅ `.gitignore` atualizado com exceções `.vscode/`
- ✅ Arquitetura Domain Profiles definida (estratégia 3 camadas)
- ✅ 19 decisões de design arquitetural resolvidas
- ✅ `scripts/manage.py` adicionado (versão inicial TUI Python)
- ✅ `docs/copilot/` — Strategy + Decisions documentados

### Version 1.0.0 (2026-01-27)
- ✅ Initial project structure
- ✅ Complete README documentation
- ✅ Makefile automation (40+ commands)
- ✅ Makefile documentation
- ✅ Security implementation (.secrets)
- ✅ Multi-language support
- ✅ Docker configuration templates
- ✅ CI/CD templates
- ✅ Session documentation

---

## 🔗 Quick Links

### Documentation
- [Main README](../README.md)
- [Makefile Guide](MAKEFILE.md)
- [Session Reports](SESSIONS/2026-01-27/)
- [README Best Practices](README_BEST_PRACTICES.md) - Comprehensive guide to writing excellent READMEs
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Solutions to common issues across 8 categories
- [Conventions](CONVENTIONS.md) - Technical standards for code, testing, git, security, automation
- [Security Documentation](#security-documentation) - See Security Documentation section below
- [Testing Documentation](#testing-documentation) - See Testing Documentation section below

### Key Commands
- `make help` - View all commands
- `make init` - Start new project
- `make status` - Check project status

---

## 📝 Notes

### Current Status
- ✅ Project template complete
- ✅ Documentation comprehensive
- ✅ Security implemented
- ✅ MCP configured
- ✅ Domain Profiles — strategy, decisions (19 D-xx) E implementação (IMP-05/06/07) concluídas
- ✅ `scripts/scaffold.py` — 9 módulos, PEP 723, modo interativo e CI
- ✅ Rituais de sessão (IMP-02/03/04) criados
- 🔵 IMP-09 — melhorar template `.copilot-rules-[projeto].md` em `templates.py`
- 🔵 IMP-10 — `docs/copilot/DOMAIN-*.md` (docs humanos dos domínios)
- ✅ IMP-14 Fase A — SpecKit no projeto filho + novos Domain Profiles (2026-03-05)
- 🟡 IMP-17 — Issue Templates + load-mcp.sh + VS Code tasks/launch (em debate D-26..D-34)
- 📁 `docs/GITHUB-COPILOT-AGENTS-RESOURCES.md` — Renomeado de "GitHub Copilot Recursos de Agents etc.md" (2026-03-07)

### Next Actions
1. IMP-17: Confirmar D-26..D-34 e implementar Fase A
2. IMP-14 Fase B: `devops-cicd.prompt.md` + docs de uso do scaffold
3. IMP-09: Enriquecer `generate_copilot_rules()` em `scripts/lib/templates.py`
4. IMP-10: Criar `docs/copilot/DOMAIN-PROGRAMMING.md`, `DOMAIN-INFRASTRUCTURE.md`, `DOMAIN-ANALYSIS.md`
3. Testar `scaffold.py` em projeto real

---

**Last Modified**: 2026-03-01
**Maintained By**: Vya-Jobs Team
**License**: MIT
