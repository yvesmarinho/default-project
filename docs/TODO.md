# ✅ TODO - Enterprise Default Project Template

**Last Updated**: 2026-03-05 — IMP-14 Fase A ✅ CONCLUÍDA — 8 sub-tarefas implementadas — zero erros de compilação
**Project**: Enterprise Default Project Template
**Status**: Active Development

---

## 🎯 Current Sprint

### 🚀 Próximas Ações — Implementação Domain Profiles (Sessão seguinte)

> Todas as 19 decisões de design estão resolvidas. Ver [`docs/copilot/DOMAIN-PROFILES-DECISIONS.md`](copilot/DOMAIN-PROFILES-DECISIONS.md)

- [x] **[IMP-01]** ✅ **CONCLUÍDO 2026-03-01** — Criar `scripts/scaffold.py` — Python interativo com fluxo condicional, absorvendo `init-new-project.sh`, `setup-project-links.sh`, `check-project-links.sh`
  - [x] Debate de funcionalidades gerado → `docs/SESSIONS/2026-02-28/IMP-01-DEBATE.md`
  - [x] Spec técnica gerada → `docs/SESSIONS/2026-02-28/IMP-01-SPEC.md`
  - [x] User Stories geradas → `docs/SESSIONS/2026-02-28/IMP-01-USER-STORIES.md`
  - [x] Implementar `scripts/lib/__init__.py`
  - [x] Implementar `scripts/lib/config.py`
  - [x] Implementar `scripts/lib/ui.py`
  - [x] Implementar `scripts/lib/project.py`
  - [x] Implementar `scripts/lib/links.py`
  - [x] Implementar `scripts/lib/git.py`
  - [x] Implementar `scripts/lib/templates.py`
  - [x] Implementar `scripts/lib/vscode.py`
  - [x] Implementar `scripts/scaffold.py` como entry point
- [x] **[IMP-02]** ✅ **CONCLUÍDO 2026-03-01** — Criar `.github/prompts/session-start.prompt.md` — ritual de início de sessão genérico
- [x] **[IMP-03]** ✅ **CONCLUÍDO 2026-03-01** — Criar `.github/prompts/session-start-first.prompt.md` — ritual de primeira vez
- [x] **[IMP-04]** ✅ **CONCLUÍDO 2026-03-01** — Criar `.github/prompts/session-end.prompt.md` — ritual de encerramento com `git push`
- [x] **[IMP-05]** ✅ **CONCLUÍDO 2026-03-01** — Criar `.github/prompts/domain/devops-programming.prompt.md` — Domain Profile programação
- [x] **[IMP-06]** ✅ **CONCLUÍDO 2026-03-01** — Criar `.github/prompts/domain/devops-infrastructure.prompt.md` — Domain Profile infra
- [x] **[IMP-07]** ✅ **CONCLUÍDO 2026-03-01** — Criar `.github/prompts/domain/devops-analysis.prompt.md` — Domain Profile análise
- [x] **[IMP-08]** ✅ **CONCLUÍDO 2026-03-01** — Redefinir `make init` no `Makefile` — de executor para **redirect** para `uv run scripts/scaffold.py` (sem duplicar lógica)
- [ ] **[IMP-09]** Criar template `.copilot-rules-[projeto].md` gerado pelo `scaffold.py` — específico por projeto
- [ ] **[IMP-10]** Criar documentação humana dos 3 domínios em `docs/copilot/DOMAIN-PROGRAMMING.md`, `DOMAIN-INFRASTRUCTURE.md`, `DOMAIN-ANALYSIS.md`
- [x] **[IMP-14]** ✅ **FASE A CONCLUÍDA 2026-03-05** — SpecKit instalado no projeto filho + Novos Domain Profiles + Perfis Profissionais
  - Debate: `docs/SESSIONS/2026-03-05/IMP-14-DEBATE.md`
  - Decisões: D-20..D-25 todas respondidas 🟢 (2026-03-05)
  - **Fase A (P0) ✅**: A.1 `SPECKIT_SYNC_DATE` em config.py • A.2 `copy_speckit()` • A.3 `generate_constitution()` • A.4 questão `[8]` em ui.py • A.5 integrar em scaffold.py • A.6 `devops-security.prompt.md` • A.7 extensões Review/Runbook nos 3 perfis • A.8 `constitution.md` v1.0.0
  - **Fase B (P1)** 🔵: `devops-cicd.prompt.md` + testes scaffold + docs de uso
  - **Fase C (P2)** 🔵: melhorias UX `ui.py`
- [ ] **[IMP-15]** (futuro) Geração de `Dockerfile`, `docker-compose.yml`, workflows CI/CD pelo scaffold
- [ ] **[IMP-16]** (futuro) Testes para `scaffold.py` e `scripts/lib/`
- [ ] **[IMP-17]** 🔵 **Em debate (2026-03-05)** — Issue Templates + Script `load-mcp.sh` + VS Code `tasks.json`/`launch.json`/perfil
  - Debate: `docs/SESSIONS/2026-03-05/IMP-17-DEBATE.md`
  - Decisões abertas: D-26..D-34 (9 decisões)
  - **Fase A (P0)**: A.1–A.4 Issue Templates • A.5 `generate_load_mcp()` • A.6 `generate_tasks()` • A.7–A.9 integrações
  - **Fase B (P1)**: `launch.json` + `.code-workspace` enriquecido
  - **Fase C (P2)**: `.code-profile` exportável
- [x] **[IMP-11]** ~~Criar `.copilot-strict-rules.md`~~ → **CONCLUÍDO em IMP-13**: arquivo consolidado em `.copilot-rules.md`
- [x] **[IMP-12]** ~~Criar `.copilot-strict-enforcement.md`~~ → **CONCLUÍDO em IMP-13**: arquivo consolidado em `.copilot-rules.md`
- [x] **[IMP-13]** Consolidar arquivos `.copilot-*` — **CONCLUÍDO 2026-02-28** — 5 arquivos (1910 linhas) → 1 arquivo (`.copilot-rules.md`, ~180 linhas, 7 seções). Ver debate: `docs/SESSIONS/2026-02-28/COPILOT-FILES-DEBATE.md`
  - [x] Refatorar `.copilot-rules.md` — consolidar conteúdo único de todos os 5 arquivos
  - [x] Eliminar `.copilot-strict-rules.md` (migrar conteúdo único; remover lixo de n8n/k8s)
  - [x] Eliminar `.copilot-strict-enforcement.md` (migrar REGRA 0.A e REGRA 0.B para rules.md)
  - [x] Eliminar `.copilot-file-rules.sh` (100% duplicado)
  - [x] Reduzir `.copilot-git-rules.md` para seção em `rules.md`
  - [x] Atualizar `SHARED_COPILOT_FILES` em `lib/config.py` para lista de 1 item ✅ (pós-IMP-13: apenas `.copilot-rules.md`)

---

### ✅ Completed Recently

#### 2026-03-05 (Sessão atual)
- [x] Iniciar sessão MCP (2026-03-05)
- [x] Recuperar dados da sessão anterior (2026-03-01)
- [x] Carregar regras Copilot na memória (`.copilot-rules.md` ativo — único arquivo desde IMP-13)
- [x] Scan de credenciais/arquivos sensíveis → 🟢 LIMPO
- [x] Verificar `.secrets/` no `.gitignore` (confirmado)
- [x] Verificar organização da raiz (limpa — nenhum arquivo solto)
- [x] Criar `docs/SESSIONS/2026-03-05/SESSION_RECOVERY_2026-03-05.md`
- [x] Criar `docs/SESSIONS/2026-03-05/DAILY_ACTIVITIES_2026-03-05.md`
- [x] Atualizar `docs/TODO.md` e `docs/INDEX.md`
- [x] Análise de perfis profissionais e domain profiles faltantes
- [x] Abrir IMP-14 com debate estruturado (4 perspectivas, D-20..D-25)
- [x] Verificar e corrigir 3 gaps em `.copilot-rules.md` (Seção 3 + Seção 5)
- [x] **IMP-14 Fase A — 8 sub-tarefas implementadas (zero erros)**
  - [x] A.1 `config.py`: SPECKIT_SYNC_DATE, DOMAIN_DEFAULT_PROFILES, SPECKIT_TRANSVERSAL_PROFILES, extra_profiles
  - [x] A.2 `project.py`: `copy_speckit()` — idempotente, shutil+pathlib, logging
  - [x] A.3 `project.py`: `generate_constitution()` — placeholders resolvidos
  - [x] A.4 `ui.py`: questão [8] — `_collect_extra_profiles()`, `_parse_extra_profiles()`
  - [x] A.5 `scaffold.py`: passos 5+6 + `--extra-profiles` flag
  - [x] A.6 `.github/prompts/domain/devops-security.prompt.md` criado
  - [x] A.7 Review em programming+infrastructure, Runbook em analysis (v1.0→1.1)
  - [x] A.8 `.specify/memory/constitution.md` v1.0.0 ratificada

#### 2026-03-01 (Sessão encerrada)
- [x] Iniciar sessão MCP (2026-03-01)
- [x] Recuperar dados da sessão anterior (2026-02-28)
- [x] Carregar regras Copilot na memória (`.copilot-rules.md` ativo — único arquivo desde IMP-13)
- [x] Scan de credenciais/arquivos sensíveis → 🟢 LIMPO
- [x] Verificar `.secrets/` no `.gitignore` (confirmado)
- [x] Verificar organização da raiz (limpa — nenhum arquivo solto)
- [x] Criar `docs/SESSIONS/2026-03-01/SESSION_RECOVERY_2026-03-01.md`
- [x] Criar `docs/SESSIONS/2026-03-01/DAILY_ACTIVITIES_2026-03-01.md`
- [x] Atualizar `docs/TODO.md` e `docs/INDEX.md`
- [x] **[IMP-01]** ✅ Implementar `scripts/scaffold.py` + 8 módulos em `scripts/lib/`
- [x] **[IMP-02]** ✅ Criar `.github/prompts/session-start.prompt.md`
- [x] **[IMP-03]** ✅ Criar `.github/prompts/session-start-first.prompt.md`
- [x] **[IMP-04]** ✅ Criar `.github/prompts/session-end.prompt.md`
- [x] **[IMP-05]** ✅ Criar `.github/prompts/domain/devops-programming.prompt.md`
- [x] **[IMP-06]** ✅ Criar `.github/prompts/domain/devops-infrastructure.prompt.md`
- [x] **[IMP-07]** ✅ Criar `.github/prompts/domain/devops-analysis.prompt.md`
- [x] **[IMP-08]** ✅ Redefinir `make init` → redirect para `uv run scripts/scaffold.py`

#### 2026-02-28 (Sessão encerrada)
- [x] Iniciar sessão MCP (2026-02-28)
- [x] Recuperar dados da sessão anterior (2026-02-27)
- [x] Carregar regras Copilot na memória (`.copilot-rules.md` ativo; strict-rules/enforcement não encontrados)
- [x] Scan de credenciais/arquivos sensíveis → LIMPO
- [x] Verificar `.secrets/` no `.gitignore` (confirmado)
- [x] Verificar organização da raiz (já limpa — nenhum arquivo solto)
- [x] Criar `docs/SESSIONS/2026-02-28/SESSION_RECOVERY_2026-02-28.md`
- [x] Criar `docs/SESSIONS/2026-02-28/DAILY_ACTIVITIES_2026-02-28.md`
- [x] Atualizar `docs/TODAY_ACTIVITIES.md` e `docs/TODO.md`
- [x] **[IMP-01]** Debate de funcionalidades (4 perspectivas: PM, Dev, FE, SE)
- [x] **[IMP-01]** Spec técnica gerada (`IMP-01-SPEC.md`)
- [x] **[IMP-01]** User Stories geradas (`IMP-01-USER-STORIES.md`)
- [x] **[IMP-13]** Debate sobre estrutura dos arquivos `.copilot-*` (`COPILOT-FILES-DEBATE.md`)
- [x] **[IMP-13]** Consolidar `.copilot-rules.md` — 5 arquivos (1910 linhas) → 1 arquivo (7 seções)
- [x] **[IMP-13]** Remover `.copilot-strict-rules.md`, `.copilot-strict-enforcement.md`, `.copilot-file-rules.sh`, `.copilot-git-rules.md`

#### 2026-02-27 (Sessão encerrada)
- [x] Iniciar sessão MCP (2026-02-27)
- [x] Recuperar dados da sessão anterior (2026-01-28)
- [x] Carregar regras Copilot na memória (.copilot-strict-rules, .copilot-strict-enforcement, .copilot-rules)
- [x] Scan de credenciais/arquivos sensíveis (nenhum encontrado)
- [x] Criar `.secrets/` directory com README de segurança
- [x] Verificar `.secrets/` no `.gitignore` (confirmado)
- [x] Remover `temp.log` da raiz (arquivo órfão)
- [x] Organizar raiz do projeto
- [x] Criar `.vscode/mcp.json` com configuração MCP (memory + sequential-thinking ativos)
- [x] Criar `docs/SESSIONS/2026-02-27/SESSION_RECOVERY_2026-02-27.md`
- [x] Criar `docs/SESSIONS/2026-02-27/TODAY_ACTIVITIES_2026-02-27.md`
- [x] Debate arquitetural: Domain Profiles adaptáveis para DevOps
- [x] Criar `docs/copilot/DOMAIN-PROFILES-STRATEGY.md` — estratégia completa 3 camadas
- [x] Criar `docs/copilot/DOMAIN-PROFILES-DECISIONS.md` — 10 decisões iniciais
- [x] Analisar respostas D-01 a D-10, identificar D-11 a D-15
- [x] Analisar respostas D-11 a D-15, identificar D-16 a D-18
- [x] Analisar respostas D-16 a D-18, identificar D-19
- [x] D-19 respondida — **todas as 19 decisões de design resolvidas** 🟢
- [x] Atualizar INDEX.md, TODO.md, TODAY_ACTIVITIES.md, DECISIONS.md
- [x] Criar sessão de encerramento (DAILY_ACTIVITIES, SESSION_REPORT, FINAL_STATUS)

#### 2026-01-27
- [x] Generate comprehensive README.md
- [x] Create complete Makefile (40+ commands)
- [x] Write Makefile documentation
- [x] Implement .secrets security directory
- [x] Update project structure
- [x] Generate session documentation
- [x] Create INDEX, TODO, TODAY_ACTIVITIES

#### 2026-01-28 (Today)
- [x] Initialize MCP session
- [x] Recover previous session data from 2026-01-27
- [x] Load Copilot rules into memory (.copilot-*.md files)
- [x] Create session directory structure (docs/SESSIONS/2026-01-28/)
- [x] Generate session documentation (SESSION_RECOVERY, TODAY_ACTIVITIES)
- [x] Update INDEX, TODO, TODAY_ACTIVITIES with current status
- [x] Verify root directory organization (all files in correct locations)
- [x] Load all session context into MCP memory
- [x] Update workspace configuration (theme azul marinho)
- [x] Test all Makefile commands (15 commands tested)
- [x] Fix .gitignore to include .secrets directory
- [x] Validate project structure creation
- [x] Document Makefile test results

---

## 🚀 High Priority

### Testing & Validation
- [ ] Test `make init` command
- [ ] Verify directory structure creation
- [ ] Test Python setup (`make setup-python`)
- [ ] Test Node.js setup (`make setup-node`)
- [ ] Validate .gitignore rules
- [ ] Test Docker commands
- [ ] Verify security implementation

### Code Examples
- [ ] Add Python MVP example
- [ ] Add TypeScript/Node.js MVP example
- [ ] Add Factory pattern implementation examples
- [ ] Add Repository pattern implementation examples
- [ ] Add Service layer examples

---

## 📋 Medium Priority

### Documentation
- [ ] Add architecture decision records (ADRs)
- [ ] Create API documentation templates
- [ ] Write development guide
- [ ] Write deployment guide
- [ ] Add video tutorial
- [ ] Create contribution guidelines (CONTRIBUTING.md)

### CI/CD
- [ ] Implement GitHub Actions workflows
  - [ ] CI workflow (testing, linting)
  - [ ] CD workflow (deployment)
  - [ ] Security scanning workflow
- [ ] Add deployment scripts
- [ ] Create environment-specific configs

### Additional Language Support
- [ ] Add Java/Spring Boot template
- [ ] Add Go template
- [ ] Add Rust template
- [ ] Add Kotlin template

---

## 🔄 Low Priority

### Infrastructure
- [ ] Kubernetes deployment configurations
- [ ] Terraform/Pulumi IaC templates
- [ ] Monitoring setup (Prometheus/Grafana)
- [ ] Logging infrastructure (ELK stack)
- [ ] Tracing setup (Jaeger/Zipkin)

### Database
- [ ] Database migration templates
- [ ] Seed data examples
- [ ] ORM configuration examples
- [ ] Database connection pooling

### Testing
- [ ] Unit test examples
- [ ] Integration test examples
- [ ] E2E test examples
- [ ] Performance test framework
- [ ] Test coverage reporting

---

## 💡 Ideas / Backlog

### Features
- [ ] GraphQL API template
- [ ] gRPC service template
- [ ] WebSocket implementation
- [ ] Event-driven architecture example
- [ ] Microservices template
- [ ] Serverless functions (AWS Lambda, Azure Functions)

### Mobile
- [ ] React Native template
- [ ] Flutter template
- [ ] Ionic template

### Tools Integration
- [ ] Prettier configuration
- [ ] ESLint configuration
- [ ] Pre-commit hooks (Husky)
- [ ] Commitlint setup
- [ ] Conventional commits

### Advanced Features
- [ ] Multi-tenancy support
- [ ] Feature flags implementation
- [ ] Rate limiting
- [ ] API versioning
- [ ] GraphQL subscriptions
- [ ] Redis caching examples

---

## 🐛 Known Issues

### None
- No blocking issues currently identified

---

## 📝 Notes

### Decisions Made
1. **Make over npm scripts**: Better cross-platform support
2. **Markdown for docs**: Universal and GitHub-friendly
3. **Security first**: .secrets directory from the start
4. **Multi-language**: Support 5+ languages initially

### Future Considerations
1. Add more CI/CD providers (GitLab CI, CircleCI)
2. Consider adding VS Code extension recommendations
3. Add development container (devcontainer.json)
4. Consider adding Nix flake for reproducibility

---

## 📊 Progress Tracking

### Overall Completion
- **Phase 1 - Foundation**: ✅ 100%
- **Phase 2 - Examples**: 🔄 0%
- **Phase 3 - Advanced**: 🔄 0%
- **Phase 4 - Documentation**: 🔄 30%

### By Category
| Category | Progress | Status |
|----------|----------|--------|
| Project Structure | 100% | ✅ |
| Documentation | 70% | 🔄 |
| Automation | 100% | ✅ |
| Security | 100% | ✅ |
| Examples | 0% | ⏳ |
| Testing | 0% | ⏳ |
| CI/CD | 10% | ⏳ |
| Multi-language | 40% | 🔄 |

---

## 🎯 Next Session Goals

### Immediate (Next Session)
1. **[IMP-01]** Implementar `scripts/scaffold.py` — Python interativo para scaffolding de projetos
2. **[IMP-02–04]** Criar os 3 prompt files de sessão (session-start, session-start-first, session-end)
3. **[IMP-05–07]** Criar os 3 Domain Profile files (programming, infrastructure, analysis)
4. **[IMP-08]** Atualizar Makefile (`make init` → redirect para `scaffold.py`)
5. **[IMP-09]** Criar template `.copilot-rules-[projeto].md`

### Short-term (This Week)
1. Complete code examples for all patterns
2. Add more language templates
3. Implement full CI/CD pipeline
4. Add database migration examples
5. Create video tutorial

### Medium-term (This Month)
1. Add Kubernetes configurations
2. Implement monitoring stack
3. Add advanced features
4. Create mobile templates
5. Community feedback integration

---

## ✅ Completion Criteria

### Ready for 1.0 Release
- [ ] All high-priority items completed
- [ ] Examples for all supported languages
- [ ] CI/CD fully functional
- [ ] Comprehensive documentation
- [ ] User testing completed
- [ ] Community feedback incorporated

### Ready for 2.0 Release
- [ ] Kubernetes support
- [ ] Multi-cloud deployment
- [ ] Advanced monitoring
- [ ] Mobile templates
- [ ] Microservices architecture

---

## 📞 Feedback & Contributions

### How to Contribute
1. Review TODO items
2. Pick an item to work on
3. Create feature branch
4. Implement with tests
5. Update documentation
6. Submit pull request

### Reporting Issues
- Check existing TODOs
- Create detailed issue
- Propose solution if possible
- Link related TODOs

---

**Maintained By**: Vya-Jobs Team
**Last Review**: 2026-01-27
**Next Review**: TBD
