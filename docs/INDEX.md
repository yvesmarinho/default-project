# 📑 Project Index - Enterprise Default Project Template

**Last Updated**: 2026-03-08 🏁 Encerrada
**Project Status**: ✅ Production Ready Template
**Version**: 1.3.0
**Last Session**: 2026-03-08 — IMP-29 ✅ + IMP-30 ✅ + IMP-31 ✅ + IMP-32 ✅ (410 testes)

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
./scripts/init-new-project.sh my-new-project

# Or use Makefile
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
        └── 2026-03-08/          # IMP-29..32 ✅ + Homologação + Plano IMP-33..44 (encerrada)
├── scripts/                        # Automation scripts
│   ├── scaffold.py               # ✅ CRIADO 2026-03-01 — PEP 723, uv run, entry point
│   ├── lib/                      # Módulos: config, ui, project, links, git, templates, vscode
│   ├── init-new-project.sh       # ⚠ Legado (absorvido pelo scaffold.py)
│   ├── setup-project-links.sh    # ⚠ Legado
│   ├── check-project-links.sh    # ⚠ Legado
│   └── manage.py                 # TUI Python (mantido temporariamente)
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
| `scripts/manage.py` | TUI Python | 🟡 Legado |
| `scripts/init-new-project.sh` | Initialize new project | ⚠ Legado (absorvido) |
| `scripts/setup-project-links.sh` | Setup symlinks | ⚠ Legado (absorvido) |
| `scripts/check-project-links.sh` | Verify symlink integrity | ⚠ Legado (absorvido) |

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
