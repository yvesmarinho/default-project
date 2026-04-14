# ✅ TODO - Enterprise Default Project Template

**Last Updated**: 2026-04-14 — IMP-65 Template Synchronization System criada (P1, 256h, 4 fases)
**Project**: Enterprise Default Project Template
**Status**: 🟡 Active Development (CI/CD disabled temporarily)

---

> **✅ SESSION 2026-04-05 UPDATE — DEBATES ESTRATÉGICOS:**
> - **DEBATE NOVO**: Engram MCP Integration — Memória Persistente
>   - Documentação: [`DEBATE_ENGRAM_INTEGRATION_2026-04-05.md`](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md)
>   - Decisão: APROVADO — Implementação faseada (Cenário 3)
>   - 7 perspectivas debateram: template-architect, session-manager, constitution, Platform Tooling, DevEx, AppSec, SRE
>   - Issues criadas: IMP-57 (estender IMP-51), IMP-58 (avaliar necessidade), IMP-59 (mini-Engram Python), IMP-45 (renomeado para fallback)
>   - Próximo: Fase 1 (IMP-57) — estender session search para indexar README, TODO, specs
> - **DEBATE:** Spec Driven Development e 4 Camadas
>   - Validação de mercado: Score 78% (BOM) — alinhado com DDD, ADRs, BDD, TDD
>   - Issues criadas: IMP-53 (objetivo.yaml), IMP-54 (ADRs), IMP-55 (CHAT capture), IMP-56 (quality gates)
> - **IMP-51 ✅ CONCLUÍDO**: Session Search System (full-text search SQLite FTS5)
> - **IMP-50 ✅ CONCLUÍDO**: Session Documentation Adoption complete with migration toolkit
>
> **✅ SESSION 2026-04-05 UPDATE:**
> - **IMP-51 CONCLUÍDO**: Session Search System (full-text search SQLite FTS5)
> - Criados: scripts/lib/search.py (550 lines), session-index.py, session-search.py
> - Tests: 21/21 passing (100%), performance <0.1s/query
> - **IMP-50 CONCLUÍDO**: Session Documentation Adoption complete with migration toolkit
> - Criados: scripts/migrate-daily-activities.py (600 lines), tests (22 tests, 100% passing)
> - **DEBATE NOVO**: Spec Driven Development e 4 Camadas (Negócio → Produto → Arquitetura → Implementação)
> - Issues criadas: IMP-53 (objetivo.yaml), IMP-54 (ADRs), IMP-55 (CHAT capture), IMP-56 (quality gates)
> - Commits: 4a3e059 (IMP-50), 84bc0fa (IMP-51), 0af2779 (docs)
>
> **✅ SESSION 2026-04-03 UPDATE:**
> - **IMP-52 CONCLUÍDO**: yamllint/jsonschema documentation and Makefile targets
> - **IMP-49 CONCLUÍDO**: Session docs integration (prompts, validation, security, tests)
> - **IMP-50 PROGRESSO (60%)**: Adoption guide documentation
> - Criados: SESSION_DOCS_ADOPTION.md (~1500 lines), SECURITY_SESSION_DOCS.md (~800 lines)
> - Criados: .gitleaks-session-docs.toml, scripts/session-validate.py (420 lines)
> - Criados: tests/test_session_integration.py (20 tests, 100% passing)
> - Commits: bd43bc2 (IMP-52), 284a499 (IMP-49), 47ba9ac (IMP-50 partial)
>
> **✅ SESSION 2026-04-02 UPDATE:**
> - **BUG-01 RESOLVIDO**: Duplicação de diretório corrigida com property logic
> - Modificados: `scripts/lib/config.py` (project_path), `scripts/lib/ui.py` (warning)
> - Testes: 6 BUG-01 tests + 9 smoke tests passando (279 total)
> - Commit: `66a2a31` — ready for push (7 commits ahead)
>
> **⚠️ SESSION 2026-03-31 UPDATE:**
> - CI/CD workflows temporariamente removidos (commit 33e40a3)
> - Workflows preservados em commit dce227b (TOTALMENTE FUNCIONAIS)
> - Guia de restauração: `docs/CI-CD-RESTORATION-GUIDE.md`
> - Foco imediato: IMPs 49-51 (documentação incremental)

---

## 🎯 Current Sprint

### 🚀 Próximas Ações — Sistema de Documentação Incremental (concluído) + SpecKit Evolution

> **IMP-48 ✅ CONCLUÍDO** (2026-03-29) — Fundação (lib + templates + style guide + 36 tests)
> **IMP-49 ✅ CONCLUÍDO** (2026-04-03) — Integração com prompts, CI, gitleaks, validação
> **IMP-50 ✅ CONCLUÍDO** (2026-04-05) — Adoption + security guides + migration toolkit
> **IMP-51 ✅ CONCLUÍDO** (2026-04-05) — Busca/indexação FTS5 (objetivo B: memória aprimorada)
>
> **Origem**: Debate 2026-03-29 — [`DEBATE_INCREMENTAL_DOCUMENTATION_2026-03-29.md`](SESSIONS/2026-03-29/DEBATE_INCREMENTAL_DOCUMENTATION_2026-03-29.md)
>
> **Novo foco**: Spec Driven Development (IMP-53 a IMP-56)
>
> **IMP-53 ✅ CONCLUÍDO** (P1, 2h real vs 1 semana estimado, 95% faster) — objetivo.yaml + speckit.clarify (Camada 1: Negócio)
> **IMP-54 ✅ CONCLUÍDO** (P1, implementado junto com IMP-53) — ADRs no plan-template.md (Camada 3: Arquitetura)
> **IMP-55 🔵 PENDENTE** (P2, 1 semana) — Sistema de captura CHAT-*.md
> **IMP-56 🔵 PENDENTE** (P1, 1 semana) — speckit.validate quality gates
>
> **Origem**: Debate 2026-04-05 — [`DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md`](debates/DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md)

---

### 📋 Itens Recentes (2026-04-14)

- [x] **[IMP-53]** Implementar objetivo.yaml e speckit.clarify + ADRs (4-Layer Spec Driven Development) ✅ **CONCLUÍDO** (2026-04-14)
  - **Contexto**: SpecKit não tinha artefato estruturado para Camada 1 (Business) e Camada 3 (Architecture) não tinha ADRs formais
  - **Objetivo**: Implementar Spec Driven Development (4 camadas: Negócio → Produto → Arquitetura → Implementação)
  - **Escopo implementado**:
    - ✅ Template: `.specify/templates/objetivo-template.yaml` (~200 linhas)
      - Estrutura completa: feature, negocio (problema, valor, contexto), produto (visao, personas, jornadas P1/P2/P3), decisoes_iniciais, perguntas_abertas, metadata
      - Bounded contexts field (DDD support)
      - Quality gates annotations (validation criteria)
      - Rich comments: Every field has examples
    - ✅ Agent: `.github/agents/speckit.clarify.agent.md` (+200 linhas)
      - **Mode 1 (NEW)**: Generate objetivo.yaml via interactive interview (max 10 questions)
        - Intelligent recommendations: Agent suggests best-practice answers
        - Multi-line support: Complex fields (problema.descricao, visao_alto_nivel)
        - Smart defaults: Infers tags from domain, owner from git config
        - Flexible stopping: User can signal "done" early → unanswered questions → perguntas_abertas
      - **Mode 2 (PRESERVED)**: Clarify existing spec.md (original functionality)
        - Ambiguity detection via taxonomy scan
        - Up to 5 clarification questions
        - Incremental spec.md updates
    - ✅ Template: `.specify/templates/spec-template.md` (+20 linhas)
      - Business Context section added (auto-populated from objetivo.yaml)
      - Links: problema, valor, metricas_sucesso, personas, jornadas_criticas P1, decisoes_iniciais
      - Backward compatible: If no objetivo.yaml, section can be filled manually
    - ✅ Template: `.specify/templates/plan-template.md` (+80 linhas)
      - **Architecture Decision Records (ADRs)** section added (IMP-54 completed)
      - Format: Status, Context, Decision, Rationale, Consequences, Alternatives Considered
      - Example ADR: ADR-001 SQLite FTS5 (from IMP-51 Session Search)
      - Links to objetivo.yaml → decisoes_iniciais (bridge Layer 1 → Layer 3)
  - **4-Layer Workflow**:
    ```
    Layer 1 (Business):     speckit.clarify Mode 1 → objetivo.yaml
    Layer 2 (Product):      speckit.specify → spec.md (references objetivo.yaml)
    Layer 3 (Architecture): speckit.plan → plan.md (ADRs + decisoes_iniciais)
    Layer 4 (Implementation): speckit.tasks → tasks.md → código
    ```
  - **Quality Gates**:
    - Layer 1→2: >=1 metrica_sucesso, >=1 persona, jornadas P1/P2/P3
    - Layer 2→3: >=1 user story P1, acceptance criteria defined
    - Layer 3→4: >=1 ADR (architectural features), component design complete
  - **Performance**: 
    - Estimated: 1 week (40h)
    - Actual: ~2h
    - **95% faster** (20x productivity multiplier)
  - **Arquivos criados**: 1
    - `.specify/templates/objetivo-template.yaml` (~200 lines)
  - **Arquivos modificados**: 3
    - `.github/agents/speckit.clarify.agent.md` (+200 lines)
    - `.specify/templates/spec-template.md` (+20 lines)
    - `.specify/templates/plan-template.md` (+80 lines)
  - **Docs**: 
    - `docs/IMP-53_IMPLEMENTATION.md` (~600 lines - complete implementation report)
  - **Breaking changes**: NENHUM (100% backward compatible)
    - objetivo.yaml is optional (existing workflows unchanged)
    - spec-template Business Context can be filled manually if no objetivo.yaml
    - speckit.clarify Mode 2 preserved exactly as before
    - plan-template ADRs are advisory (non-architectural features can skip)
  - **Nota**: IMP-54 (ADRs in plan-template.md) implemented together with IMP-53 (both foundational for 4-layer model)
  - **Commits**: [pending]
  - *Reportado em*: 2026-04-05 | *Concluído em*: 2026-04-14 | *Estimativa*: 40h | *Tempo real*: 2h

---

### 📋 Itens Recentes (2026-04-03)

- [x] **[IMP-52]** Adicionar instruções de uso para jsonschema e yamllint ✅ **CONCLUÍDO** (2026-04-03)
  - **Contexto**: Ferramentas `jsonschema` e `yamllint` já estão disponíveis no ambiente, mas não há documentação de uso
  - **Implementação realizada**:
    - ✅ README.md: Nova seção "Configuration Validation" (~150 linhas após "Development Commands")
      - yamllint: instalação (uv/pip), uso, configuração (.yamllint.yml template)
      - jsonschema: validação Python e Node.js (ajv-cli) com exemplos completos
      - Pre-commit hooks: exemplo de script bash para automação
    - ✅ Makefile: Três novos targets após `format` (linha ~75):
      - `lint-yaml`: Valida .github/workflows/, profile-descriptors/, .scaffold-state.yaml
      - `lint-json`: Valida todos arquivos .json com Python (fallback gracioso)
      - `lint-config`: Target agregador que chama lint-yaml + lint-json
    - ✅ Validação funcional: `make lint-config` executado com sucesso
  - **Arquivos modificados**:
    - `README.md` (seção Configuration Validation inserida linha ~570)
    - `Makefile` (targets lint-yaml, lint-json, lint-config adicionados linha ~75)
  - **Resultado**: Ferramentas documentadas e integradas ao workflow de desenvolvimento
  - *Reportado em*: 2026-04-03 | *Concluído em*: 2026-04-03 | *Estimativa original*: 2h | *Tempo real*: 1.5h
  - **Commit**: `bd43bc2`

- [x] **[IMP-49]** Integração Session Documentation System ✅ **CONCLUÍDO** (2026-04-03)
  - **Contexto**: Sistema de documentação de sessão criado (IMP-48), precisa integração com workflows existentes
  - **Implementação realizada**:
    - ✅ Session Prompts: Atualizados session-start.prompt.md e session-end.prompt.md
    - ✅ Security Config: .gitleaks-session-docs.toml com 25+ padrões de segurança
    - ✅ Validation Tool: scripts/session-validate.py (420 linhas)
    - ✅ Test Suite: tests/test_session_integration.py (20 testes, 100% passando)
    - ✅ Makefile Targets: session-log, session-validate, session-sanitize
    - ✅ Scaffold Config: .scaffold-config.json com features.session_docs
  - **Arquivos criados**:
    - `.gitleaks-session-docs.toml` (~150 linhas)
    - `scripts/session-validate.py` (420 linhas)
    - `tests/test_session_integration.py` (~600 linhas)
  - **Arquivos modificados**:
    - `.github/prompts/session-start.prompt.md`
    - `.github/prompts/session-end.prompt.md`
    - `Makefile` (3 novos targets)
    - `.scaffold-config.json`
  - **Resultado**: Sistema completo integrado com prompts, CI/CD, validação e segurança
  - *Reportado em*: 2026-03-29 | *Concluído em*: 2026-04-03 | *Estimativa original*: 6h | *Tempo real*: 5.5h
  - **Commit**: `284a499`

- [x] **[IMP-50]** Session Documentation Adoption ✅ **CONCLUÍDO** (2026-04-05)
  - **Contexto**: Sistema implementado, precisa documentação de adoção e guias de migração
  - **Implementação completa**:
    - ✅ SESSION_DOCS_ADOPTION.md (~1700 linhas - atualizado):
      - Part 1: Foundation (system overview, architecture, lifecycle)
      - Part 2: File Structure and Naming
      - Part 3: Implementation Guide (5 fases incluindo migração)
      - Part 4: Migration Script Guide (seção 2.5 adicionada)
      - Part 5: Style Guide Quick Reference
      - Part 6: FAQ and Troubleshooting
    - ✅ SECURITY_SESSION_DOCS.md (~800 linhas):
      - Threat model and risk categories
      - Security patterns and sanitization
      - Validation and scanning procedures
      - Incident response protocols
      - Security checklists
    - ✅ scripts/migrate-daily-activities.py (~600 linhas):
      - Detecção automática de formato (4 tipos: very old, old, semi-canonical, canonical)
      - Conversão inteligente para formato canônico
      - Backup automático (.backup)
      - Dry-run mode
      - CLI completo com --all, --force
    - ✅ tests/test_migrate_daily_activities.py (~500 linhas):
      - 22 testes cobrindo todas as funcionalidades
      - Testes de parsing para 3 formatos legados
      - Testes de conversão e validação
      - 100% de cobertura das funções públicas
    - ✅ docs/SESSIONS/EXAMPLE-MIGRATION/:
      - Exemplo real de migração (TODAY_ACTIVITIES → DAILY_ACTIVITIES)
      - README.md explicativo com antes/depois
      - Arquivo original preservado como .backup
  - **Arquivos criados**:
    - `scripts/migrate-daily-activities.py` (~600 linhas)
    - `tests/test_migrate_daily_activities.py` (~500 linhas)
    - `docs/SESSIONS/EXAMPLE-MIGRATION/README.md` (~200 linhas)
    - `docs/SESSIONS/EXAMPLE-MIGRATION/TODAY_ACTIVITIES_2026-01-28.md` (migrado)
  - **Arquivos modificados**:
    - `docs/SESSION_DOCS_ADOPTION.md` (+200 linhas, seção 2.5 migration guide)
  - **Resultado**: Sistema de documentação 100% completo com ferramentas de migração e exemplos
  - *Reportado em*: 2026-03-29 | *Iniciado em*: 2026-04-03 | *Concluído em*: 2026-04-05 | *Tempo total*: 4h
  - **Commits**: `47ba9ac` (docs), `4a3e059` (migration toolkit)

- [x] **[IMP-51]** MCP Search Integration for Session History ✅ **CONCLUÍDO**
  - **Contexto**: Sistema de documentação implementado, precisa busca semântica via MCP
  - **Objetivo**: Objetivo B do debate - memória aprimorada do sistema
  - **Escopo**:
    - Implementar busca FTS (Full-Text Search) em histórico de sessões
    - Criar CLI tools para indexação e queries
    - Integração com SQLite FTS5 (preparado para futura integração MCP)
  - **Implementação realizada**:
    - ✅ scripts/lib/search.py (~550 linhas):
      - Classes: SessionIndexer, SessionSearcher, ActivityBlock, SearchResult
      - Parser para formatos canonical e legacy
      - SQLite FTS5 com tokenização Porter + Unicode61
      - Busca com ranking BM25, snippets, highlighting
      - Suporte a boolean operators (AND, OR, NOT, NEAR), phrase search, date filters
    - ✅ scripts/session-index.py (~200 linhas):
      - CLI para construir e manter índice de busca
      - Modos: incremental, rebuild, specific session, stats
      - Indexação de 21 arquivos, 107 blocos em <1s
    - ✅ scripts/session-search.py (~210 linhas):
      - CLI para busca interativa com sintaxe FTS5
      - Resultados com snippets highlighted (ANSI colors)
      - Opções: limit, date range, full context
    - ✅ tests/test_session_search.py (~400 linhas, 21 testes):
      - TestActivityBlock (4 tests): parsing, searchable_text, day_of_week
      - TestSessionIndexer (7 tests): schema, parsing (canonical/legacy), indexing, rebuild, stats
      - TestSessionSearcher (9 tests): keyword, phrase, boolean, date filters, context, errors
      - TestSearchResult (1 test): string representation
      - **Coverage**: 100% das classes principais
    - ✅ Makefile (4 targets):
      - `make session-index`: Build/update index (incremental)
      - `make session-index-rebuild`: Full rebuild
      - `make session-search QUERY="text"`: Interactive search
      - `make session-index-stats`: Show statistics
    - ✅ docs/SESSION_SEARCH_GUIDE.md (~500 linhas):
      - Quick start, search syntax (keywords, phrases, boolean, NEAR, column-specific)
      - Advanced usage (date range, limits, context expansion)
      - Common search patterns, troubleshooting
      - Architecture documentation, performance metrics
  - **Arquivos criados**:
    - `scripts/lib/search.py` (~550 linhas)
    - `scripts/session-index.py` (~200 linhas)
    - `scripts/session-search.py` (~210 linhas)
    - `tests/test_session_search.py` (~400 linhas)
    - `docs/SESSION_SEARCH_GUIDE.md` (~500 linhas)
  - **Arquivos modificados**:
    - `Makefile` (+35 linhas, 4 novos targets)
  - **Resultado**: Sistema de busca full-text operacional com 21/21 testes passando, performance <0.1s/query
  - **Performance**:
    - Indexação inicial: ~1s para 21 arquivos (107 blocos)
    - Query simples: <0.05s
    - Query complexa (boolean + date filter): <0.1s
    - Tamanho do índice: ~100KB (107 blocos)
  - *Reportado em*: 2026-03-29 | *Iniciado em*: 2026-04-05 | *Concluído em*: 2026-04-05 | *Tempo total*: ~3.5h
  - **Commits**: `84bc0fa` (feat), `0af2779` (docs update)

---

### 🎯 Spec Driven Development — SpecKit Evolution (2026-04-05)

> **Origem**: Debate 2026-04-05 — [`DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md`](debates/DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md)
> **Contexto**: Integrar as 4 Camadas de Desenvolvimento (Negócio → Produto → Arquitetura → Implementação) no SpecKit
> **Referência**: [Spec Driven Development é o Caminho?](https://www.youtube.com/watch?v=DJE0LL0CuUQ)
> **Validação de mercado**: Score 78% (BOM) — Alinhado com DDD, ADRs, BDD, TDD, C4 Model, DORA Metrics

---

### 🧠 Engram MCP Integration — Memória Persistente (2026-04-05)

> **Origem**: Debate 2026-04-05 — [`DEBATE_ENGRAM_INTEGRATION_2026-04-05.md`](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md)
> **Contexto**: Avaliar integração Engram após conclusão de IMP-51 (session search)
> **Decisão**: APROVADO — Implementação faseada (Cenário 3)
> **Participantes**: 7 perspectivas (template-architect, session-manager, constitution, Platform Tooling, DevEx, AppSec, SRE)
> **Veredicto**: Prudência arquitetural — estender IMP-51 antes de adicionar Engram

- [x] **[IMP-57]** Estender IMP-51: Indexação além de DAILY_ACTIVITIES ✅ **CONCLUÍDO** (Fase 1)
  - **Contexto**: IMP-51 v1.0 indexava só DAILY_ACTIVITIES; IMP-57 estende para docs e specs
  - **Objetivo**: Aumentar cobertura de memória passiva antes de introduzir memória ativa (Engram)
  - **Descoberta**: 90% do código já existia mas nunca foi testado/documentado formalmente!
  - **Implementação realizada**:
    - ✅ Bugs corrigidos: 2 (parsing de canonical + legacy formats)
    - ✅ Testes criados: 5 novos testes em TestMultiScopeIndexing
    - ✅ Validação prática: 71 arquivos, 754 blocos/seções indexados com sucesso
    - ✅ Documentação: IMP-57_IMPLEMENTATION.md (~500 linhas)
  - **Escopo**:
    - ✅ `index_docs()`: indexa docs/*.md (README, TODO, guides)
    - ✅ `index_specs()`: indexa .specify/specs/*/*.md (spec, plan, tasks)
    - ✅ `index_by_scope()`: indexação unificada (sessions|docs|specs|all)
    - ✅ `SessionSearcher.search(scope=...)`: filtro por document_type
    - ✅ `session-index.py --scope`: CLI para indexação seletiva
    - ✅ `session-search.py --scope`: CLI para busca filtrada
  - **Funcionalidades**:
    - Indexação multi-scope: sessions (DAILY_ACTIVITIES) + docs (README, TODO, etc) + specs (SpecKit)
    - Busca com escopo: --scope sessions|docs|specs|all
    - Section splitting: divide documentos por ## headers
    - Document type badges: [SESSION], [DOC], [SPEC] nos resultados
    - Zero dependências: Python puro + SQLite FTS5
  - **Performance**:
    - Indexação: 71 arquivos (754 blocos) em <1s
    - Busca: <0.1s por query (mesmo com scope filter)
    - Tamanho DB: ~200KB para 754 entradas
  - **Bugs corrigidos**:
    - Bug #1: Parsing canonical format pulava primeira atividade (line 165)
    - Bug #2: Parsing legacy não capturava atividades no início do arquivo (line 184)
  - **Arquivos modificados**:
    - `scripts/lib/search.py` (+20 linhas, 2 bug fixes)
    - `tests/test_session_search.py` (+180 linhas, 5 novos testes)
    - `docs/IMP-57_IMPLEMENTATION.md` (novo, ~500 linhas)
    - `docs/TODO.md` (este arquivo)
  - **Testes**: 25/26 passing (96%) — 5 novos testes IMP-57, 1 falha pré-existente
  - **Resultado**: Sistema de busca completo (sessions + docs + specs) com zero dependências externas
  - **Tempo real**: 3h (vs 16h estimado = **81% mais rápido**, 5.3x produtividade)
  - **Impact**: Memória passiva ampliada — ready para IMP-58 evaluation phase
  - *Reportado em*: 2026-04-05 | *Iniciado em*: 2026-04-14 | *Concluído em*: 2026-04-14 | *Tempo total*: 3h
  - **Commits**: [pending]

- [ ] **[IMP-58]** Avaliar necessidade de memória ativa � **EM ANDAMENTO** (Fase 2 — Coleta iniciada)
  - **Contexto**: IMP-51 v2.0 (IMP-57 ✅ concluído) oferece memória passiva ampliada; validar se suficiente
  - **Objetivo**: Coletar dados de uso real para decisão fundamentada sobre Engram
  - **Escopo**:
    - ✅ Criar survey (5 perguntas): frequência de busca, perda de contexto, onboarding, interesse em memória ativa
    - ✅ Criar script de logging: `scripts/imp58-usage-logger.py` (wrapper de session-search)
    - ✅ Criar template de entrevista: 30-45 min estruturado, 5 seções
    - ✅ Criar report template: `IMP-58_MEMORY_ASSESSMENT_REPORT.md`
    - 🟡 **Coletar dados** (2-4 semanas): surveys, logs, entrevistas
    - ⏸️ Análise de dados + report consolidado (1 semana após coleta)
    - ⏸️ **Decision gate**: ≥2 critérios alta necessidade → Fase 3a; <2 → manter IMP-51 v2.0
  - **Critérios**:
    - Frequência busca manual ≥5x/dia → necessidade alta
    - Queixas perda de contexto ≥3x/semana → necessidade alta
    - Onboarding lento >2h para encontrar info → necessidade alta
  - **Arquivos criados**:
    - `docs/IMP-58_MEMORY_ASSESSMENT_SURVEY.md` (survey template)
    - `docs/IMP-58_INTERVIEW_TEMPLATE.md` (entrevista estruturada)
    - `docs/IMP-58_MEMORY_ASSESSMENT_REPORT.md` (report consolidado)
    - `docs/IMP-58_README.md` (instruções de uso)
    - `scripts/imp58-usage-logger.py` (usage analytics)
  - **Timeline**:
    - Preparação: 2026-04-05 ✅
    - Distribuição: 2026-04-05 a 04-07
    - Coleta: 2026-04-05 a 05-03 (2-4 semanas) 🟡
    - Análise: 2026-05-03 a 05-10 (1 semana) ⏸️
    - Decisão: 2026-05-10 ⏸️
  - **Estimativa**: 16h distribuído em 4 semanas + 8h análise
  - **Prioridade**: P1
  - *Reportado em*: 2026-04-05 | *Status*: 🟡 Em andamento (coleta iniciada 2026-04-05)

- [ ] **[IMP-59]** Mini-Engram Python — Memória ativa sem deps externas � **EM PREPARAÇÃO** (Fase 3a — condicional)
  - **Contexto**: SE IMP-58 decision gate = GO, implementar memória ativa em Python puro
  - **Objetivo**: RAG-like memory (mem_save, mem_search, mem_context) sem binário externo
  - **Escopo**:
    - Estrutura: `.memory/memories/*.md` (fonte commitável), `.memory/index/memory.db` (cache SQLite)
    - CLI: `scripts/mem_save.py`, `scripts/mem_search.py`
    - MCP server: `scripts/mem_mcp_server.py` (Python, package `mcp`)
    - Security: `scripts/lib/sanitize.py` (PII/secrets), `.gitleaks-memory.toml`, pre-commit hook
    - Policy: `.memory/MEMORY_POLICY.md` (seções: Secrets Management, Data Privacy, Usage Guidelines)
    - Tests: `tests/test_memory_*.py` (20 tests: search, save, security, integration)
    - Integration: atualizar `session-start.prompt.md` (mem_search step), `session-end.prompt.md` (mem_save step)
  - **Benefícios**:
    - Zero dependência externa (100% Python)
    - Reutiliza código IMP-51 (SQLite + FTS5)
    - 100% controle e manutenibilidade
  - **Trabalho em paralelo** (enquanto IMP-58 coleta dados):
    - ✅ Documento de design/arquitetura (`docs/IMP-59_DESIGN.md`)
    - ✅ POC isolado (`poc/mem_poc.py` — 500 linhas, standalone)
    - ⏸️ Validação POC (executar e medir critérios de sucesso)
    - ⏸️ Decisão final aguarda IMP-58 (2026-05-10)
  - **Estimativa**: 40h (implementação completa SE GO)
  - **Prioridade**: P1 (SE decision gate GO)
  - *Reportado em*: 2026-04-05 | *Status*: 🟡 Em preparação (design + POC pronto, aguarda IMP-58)

- [ ] **[IMP-65]** Template Synchronization System � **FASE 2 COMPLETA** (P1, 2-6 semanas faseado)
  - **Contexto**: Templates do SpecKit (`.specify/templates/*.md`) são copiados uma vez na criação do projeto; quando upstream evolui, projetos existentes não recebem melhorias/correções
  - **Problema (Template Drift)**:
    - Projetos customizam templates localmente (ex: adicionar seção "Security Review")
    - Upstream evolui templates (ex: adiciona "Performance Criteria", "Cost Estimation")
    - `scaffold.py upgrade` pula arquivos existentes → **melhorias do upstream são perdidas**
    - Impacto: projetos ficam desatualizados, perdem melhores práticas, bugs não são corrigidos
  - **Escopo** (4 fases incrementais):
    - **Fase 1** ✅ **COMPLETA** (P0, 2-3 dias): Versionamento e detecção de drift
      - Adicionar metadado `template_version: X.Y.Z` em todos templates `.specify/templates/*.md`
      - Comando `scaffold.py check-templates` — detecta templates desatualizados
      - Relatório: "3 templates desatualizados, 12 melhorias disponíveis desde v1.0"
      - Arquivo `.scaffold-state.yaml`: adicionar campo `template_versions: {...}`
      - **Implementado**: template_version.py, flow check_templates, 36 testes (100% pass)
      - **Documentação**: TEMPLATE_DRIFT_DETECTION.md (370 linhas)
      - **Tempo real**: 8h (vs 16h estimado = 2x mais rápido)
    - **Fase 2** ✅ **COMPLETA** (P1, 1 semana): Diff e visualização
      - Comando `scaffold.py diff-template <nome>` — mostra diferenças upstream vs local
      - Unified diff (git-style) + HTML side-by-side + stats
      - Detecção de customizações vs melhorias upstream (heurística)
      - Impact report com recomendações
      - 3 formatos de output: colored terminal, markdown, HTML
      - Backup automático antes de qualquer merge (`template.md.backup-TIMESTAMP`)
      - **Implementado**: template_diff.py (~420 linhas), flow diff_template (~130 linhas)
      - **Testes**: 18 testes (100% pass) — diff, stats, customizations, formats
      - **Documentação**: TEMPLATE_DRIFT_DETECTION.md atualizado (~600 linhas)
      - **Tempo real**: 6h (vs 40h estimado = 6.7x mais rápido)
    - **Fase 3** ✅ **COMPLETA** (P1, 2 semanas): Three-way merge automático
      - Guardar versão original (base) de cada template em `.scaffold-state.yaml`
      - Three-way merge: `git merge-file local.md base.md upstream.md`
      - Detecção automática de conflitos com sugestões de resolução
      - Modos: `--auto` (sem conflitos), `--force` (com conflitos), `--dry-run` (preview)
      - `--interactive` mode para resolver conflitos manualmente (Fase 3.1 futuro)
      - **Implementado**: template_merge.py (~440 linhas), flow merge_template (~200 linhas)
      - **Extensões**: template_version.py +3 funções (save/load/save_all bases)
      - **State**: `.scaffold-state.yaml` agora tem campo `template_bases`
      - **Testes**: 16 testes (100% pass) — merge, conflicts, backup, base storage
      - **Documentação**: TEMPLATE_DRIFT_DETECTION.md (~900 linhas)
      - **Tempo real**: 8h (vs 80h estimado = 10x mais rápido)
    - **Fase 3.1** ✅ **COMPLETA** (P1, 1 semana): Interactive Conflict Resolution
      - `--interactive` mode para resolver conflitos passo a passo
      - Side-by-side diff viewer com Rich console UI
      - Opções de resolução: local, upstream, both, edit, skip
      - Validação automática e progress tracking
      - **Implementado**: interactive_merge.py (~370 linhas)
      - **Integração**: merge_template.py flow atualizado
      - **Testes**: 18 testes (100% pass) — resolution, validation, edge cases
      - **Documentação**: TEMPLATE_DRIFT_DETECTION.md atualizado (~1100 linhas)
      - **Tempo real**: 3h (vs 30h estimado = 10x mais rápido)
    - **Fase 4** (P2, futuro): Templates modulares
      - Reestruturar templates como blocos reutilizáveis
      - `.specify/templates/blocks/user-scenarios-v2.0.md`
      - `.specify/templates/spec-template.md` importa blocos
      - Sistema de "patches" para customizações isoladas
  - **Benefícios**:
    - Projetos recebem melhorias de templates sem perder customizações
    - Correções de bugs propagam automaticamente
    - Consistência entre projetos mantida ao longo do tempo
    - Reduz risco de "template drift" (divergência descontrolada)
  - **Estimativa**: Fase 1: 16h (✅ 8h real), Fase 2: 40h (✅ 6h real), Fase 3: 80h (✅ 8h real), Fase 3.1: 30h (✅ 3h real), Fase 4: 120h (total original: ~286h)
  - **Prioridade**: P1 (critical for long-term template maintenance)
  - **Origem**: Session 2026-04-14 — discussão sobre proteção de customizações vs recebimento de updates
  - *Reportado em*: 2026-04-14 | *Status*: 🟢 Fase 3.1 completa (Fase 4 pendente) | *Última atualização*: 2026-04-14 20:15

- [ ] **[IMP-45]** Engram MCP oficial — Fallback se Python inadequado 🔵 **PENDENTE** (Fase 3b — fallback)
  - **Contexto**: SE mini-Engram Python (IMP-59) tiver bugs críticos, performance ruim, ou manutenibilidade difícil
  - **Objetivo**: Integrar Engram oficial (Gentleman-Programming/engram) como fallback
  - **Escopo** (implementação completa conforme Cenário 1 do debate):
    - **Security controls** (P0 — blockers obrigatórios):
      - `.gitignore`: patterns de secrets em `.engram/memory/`
      - `.gitleaks-engram.toml`: scan configurado e testado
      - `scripts/lib/engram.py`: sanitização de PII/secrets
      - Pre-commit hook: scan automático antes de commit
      - `.engram/AGENT_MEMORY_POLICY.md`: seções "Secrets Management" + "Data Privacy"
      - `tests/test_engram_security.py`: test de segurança (simular saves com secrets, verificar bloqueio)
    - **Operational controls**:
      - `make setup-engram`: automação de instalação do binário
      - `make engram-health`: health check (binário, DB integrity)
      - `make engram-rebuild`: disaster recovery (rebuild DB from .md files)
      - `make engram-stats`: observability (total memories, tags, size)
      - `.engram/OPERATIONS.md`: troubleshooting guide
    - **Integration**:
      - `.vscode/mcp.json`: config MCP server
      - `.engram/scripts/engram_mcp.sh`: wrapper script
      - `session-start.prompt.md`: adicionar `mem_search` step
      - `session-end.prompt.md`: adicionar `mem_save` step
      - `.engram/memory/.examples/`: templates de memórias exemplo
    - **Tests**:
      - `tests/test_engram_integration.py`: integração com session system
      - `tests/test_engram_security.py`: security compliance
    - **Docs**:
      - `.engram/README.md`: casos de uso e quickstart
      - `docs/COMPATIBILITY-MATRIX.md`: adicionar coluna "Engram MCP"
  - **Estimativa**: 80h
  - **Prioridade**: P2 (fallback — baixa prioridade se IMP-59 funcionar)
  - **Blocker crítico**: AppSec sign-off obrigatório (todos security controls implementados)
  - *Reportado em*: 2026-03-XX | *Reescrito em*: 2026-04-05 | *Status*: Pendente (blocker: IMP-59 inadequado)

- [ ] **[IMP-53]** Implementar objetivo.yaml e speckit.clarify (Camada 1: Negócio) 🔵 **PENDENTE**
  - **Contexto**: SpecKit não tem artefato estruturado para Camada 1 (contexto de negócio)
  - **Objetivo**: Capturar problema, valor, stakeholders, métricas antes de especificação técnica
  - **Escopo**:
    - Criar template: `.specify/templates/objetivo-template.yaml`
    - Criar agent: `.github/agents/speckit.clarify.agent.md` (entrevista usuário → gera objetivo.yaml)
    - Atualizar `spec-template.md` para referenciar objetivo.yaml
    - Atualizar fluxo SpecKit: objetivo.yaml → spec.md → plan.md → tasks.md
  - **Estrutura objetivo.yaml**:
    - `negocio:` problema, valor, métricas, stakeholders, constraints
    - `produto:` visão, personas, jornadas críticas (P1/P2/P3)
    - `decisoes_iniciais:` decisões conhecidas (D-01, D-02, ...)
    - `perguntas_abertas:` questões não resolvidas
  - **Estimativa**: 1 semana (Fase 1)
  - *Reportado em*: 2026-04-05 | *Status*: Pendente (depende de aprovação do debate)

- [ ] **[IMP-54]** Integrar ADRs no plan-template.md (Camada 3: Arquitetura) 🔵 **PENDENTE**
  - **Contexto**: plan.md documenta "o quê", mas não "por quê" de decisões arquiteturais
  - **Objetivo**: Formalizar Architecture Decision Records (ADRs) no SpecKit
  - **Escopo**:
    - Atualizar `.specify/templates/plan-template.md` com seção ADRs obrigatória
    - Template ADR: Status, Context, Decision, Rationale, Consequences, Alternatives Considered
    - Adicionar comando: `python scripts/manage.py speckit adr add --title "..." --feature IMP-XX`
    - Validação: `speckit.validate` exige >=1 ADR para features arquiteturais
  - **Benefícios**:
    - Onboarding mais rápido (explicita decisões passadas)
    - Evita re-debates de decisões já tomadas
    - Facilita revisão e evolução de arquitetura
  - **Estimativa**: 3 dias
  - *Reportado em*: 2026-04-05 | *Status*: Pendente (depende de aprovação do debate)

- [ ] **[IMP-55]** Sistema de captura de conversas (CHAT-*.md) 🔵 **PENDENTE**
  - **Contexto**: Conversas com Copilot contêm decisões/clarificações valiosas que se perdem
  - **Objetivo**: Capturar e indexar conversas importantes como memória do projeto
  - **Escopo**:
    - Template: `CHAT-YYYYMMDD-HHMMSS.md` (context, conversation, decisions, artifacts, next steps)
    - Fase 1: Adicionar instrução em `.github/copilot-instructions.md` (Copilot oferece criar arquivo)
    - Fase 2: Comando `python scripts/manage.py chat capture --feature IMP-XX`
    - Fase 3: Integração Engram (captura automática)
  - **Localização**:
    - Session-scoped: `docs/SESSIONS/YYYY-MM-DD/CHAT-*.md`
    - Feature-scoped: `.specify/specs/<feature>/CHAT-*.md`
  - **Estimativa**: 1 semana (Fase 3)
  - *Reportado em*: 2026-04-05 | *Status*: Pendente — Prioridade P2 (após IMP-53, IMP-54)

- [ ] **[IMP-56]** Agent speckit.validate para quality gates 🔵 **PENDENTE**
  - **Contexto**: Avanço entre camadas sem validação pode gerar specs incompletos
  - **Objetivo**: Criar gates de qualidade para validar cada camada antes de avançar
  - **Escopo**:
    - Agent: `.github/agents/speckit.validate.agent.md`
    - Comando: `python scripts/manage.py speckit validate --layer [business|product|architecture|implementation]`
    - Quality Gates:
      - business → product: objetivo.yaml completo, >= 1 métrica de sucesso
      - product → architecture: spec.md com >= 1 user story P1, acceptance criteria
      - architecture → implementation: plan.md com >= 1 ADR, component design
      - implementation → done: tasks.md completo, testes passando, checklist aprovado
  - **Estimativa**: 1 semana (Fase 2)
  - *Reportado em*: 2026-04-05 | *Status*: Pendente — Prioridade P1 (após IMP-53, IMP-54)

---

### 📋 Itens Recentes (2026-04-02)
  - **Contexto**: Ferramentas `jsonschema` e `yamllint` já estão disponíveis no ambiente, mas não há documentação de uso
  - **Implementação realizada**:
    - ✅ README.md: Nova seção "Configuration Validation" (~150 linhas após "Development Commands")
      - yamllint: instalação (uv/pip), uso, configuração (.yamllint.yml template)
      - jsonschema: validação Python e Node.js (ajv-cli) com exemplos completos
      - Pre-commit hooks: exemplo de script bash para automação
    - ✅ Makefile: Três novos targets após `format` (linha ~75):
      - `lint-yaml`: Valida .github/workflows/, profile-descriptors/, .scaffold-state.yaml
      - `lint-json`: Valida todos arquivos .json com Python (fallback gracioso)
      - `lint-config`: Target agregador que chama lint-yaml + lint-json
    - ✅ Validação funcional: `make lint-config` executado com sucesso
  - **Arquivos modificados**:
    - `README.md` (seção Configuration Validation inserida linha ~570)
    - `Makefile` (targets lint-yaml, lint-json, lint-config adicionados linha ~75)
  - **Resultado**: Ferramentas documentadas e integradas ao workflow de desenvolvimento
  - *Reportado em*: 2026-04-03 | *Concluído em*: 2026-04-03 | *Estimativa original*: 2h | *Tempo real*: 1.5h

---

## 📋 Plano de Ação Pós-Homologação

> **Origem**: Debate de homologação 2026-03-08 — 6 perspectivas profissionais analisaram IMPs 01–32.
> **Documento completo**: [`docs/SESSIONS/2026-03-08/HOMOLOGATION-DEBATE-2026-03-08.md`](SESSIONS/2026-03-08/HOMOLOGATION-DEBATE-2026-03-08.md)

---

## 🔧 Correções e Melhorias (Sessão 2026-03-20)

### ✅ Concluído nesta sessão

- [x] **Reorganização estrutural**: `setup/` movido para raiz do projeto
  - Separação clara entre scripts ativos (`scripts/`) e legados (`setup/`)
  - Makefile e documentação atualizados
  - Commit: `6a1bfbc`

- [x] **Sistema de configuração JSON**: .scaffold-config.json
  - Defaults customizáveis sem modificar código
  - Seções: defaults, paths, features, prompts
  - Documentação completa em .scaffold-config.README.md
  - Commit: `2ee005f`

- [x] **Bug fix**: JSON defaults não carregavam em prompts interativos
  - `collect_project_info()` agora faz merge correto: CLI > JSON > hardcoded
  - Teste de validação criado (tmp/test-json-defaults.py)
  - Commit: `01a25f3`

- [x] **Bug fix CRÍTICO**: Projeto criado em diretório incorreto
  - Adicionada propriedade `project_path` ao ProjectConfig
  - 18 arquivos corrigidos: `target_dir` → `project_path`
  - Script de limpeza criado: `scripts/cleanup-wrong-scaffold.py`
  - Commit: `9767677`

### ✅ Concluído na sessão 2026-03-21

- [x] **Bug fix**: Padrão glob de agentes no scaffold
  - Função `copy_speckit()` usava padrão `"speckit.*.agent.md"` muito restritivo
  - Agentes não-SpecKit (`session-manager`, `template-architect`) não eram copiados
  - Corrigido para `"*.agent.md"` em `scripts/lib/project.py:558`
  - Impacto: P1 (projetos novos ficavam sem session-manager)
  - Commit: `f93afb8`

### ✅ Concluído na sessão 2026-03-30

- [x] **Security scanner configuration**: GitGuardian + Gitleaks exceptions for test files
  - Criado `.gitguardian.yaml` com path exclusions para `tests/test_session_lib.py`
  - Atualizado `.gitleaks.toml` com allowlist expandida (patterns + paths)
  - Testes de sanitização agora podem usar valores realistas sem falsos positivos
  - Proteção mantida para código de produção (`src/`, `scripts/`)
  - Commit: `ca1e58e`

---

### 🔴 P0 — Quick wins (baixo esforço, alto impacto) — executar na próxima sessão

- [x] **[BUG-01]** Scaffold cria estrutura de diretórios duplicada ✅ **RESOLVIDO** (2026-04-02)
  - **Problema**: Executar `scaffold.py new --name X` de dentro de pasta chamada `X/` cria `X/X/` (estrutura duplicada)
  - **Causa raiz**: `project_path = target_dir / project_name` onde `target_dir = cwd()` e `cwd().name == project_name`
  - **Correção implementada**:
    - Adicionada função `_validate_directory_conflict()` em `lib/ui.py`
    - Validação integrada em modo interativo e CI
    - 4 testes unitários criados (100% passou)
  - **Arquivos modificados**: `scripts/lib/ui.py` (+33 linhas)
  - **Testes**: `tests/test_bug01_directory_conflict.py` (4 casos)
  - **Documentação**: [`docs/SESSIONS/2026-04-01/BUG_SCAFFOLD_DUPLICATE_DIRECTORY.md`](SESSIONS/2026-04-01/BUG_SCAFFOLD_DUPLICATE_DIRECTORY.md)
  - *Reportado em*: 2026-04-01 | *Resolvido em*: 2026-04-02

- [x] **[BUG-01 Recurrence]** Tilde expansion missing in CI mode ✅ **RESOLVIDO** (2026-04-03)
  - **Problema**: Modo CI não expande `~` em `--target-dir` e `--shared-dir`, criando estrutura literal `~/Documentos/...`
  - **Causa raiz**: `_collect_ci()` em `scripts/lib/ui.py` usava `Path(overrides["target_dir"])` sem `.expanduser()`
  - **Correção implementada**:
    - Adicionado `.expanduser()` em ambos `target_dir` e `shared_dir` na linha ~172
    - Modo interativo já tinha o fix (linha ~251), mas modo CI não
  - **Arquivos modificados**: `scripts/lib/ui.py` (+2 `.expanduser()` calls)
  - **Teste de validação**: Test project `tmp/projeto-teste` created successfully with `~` paths
  - *Reportado em*: 2026-04-03 | *Resolvido em*: 2026-04-03

- [x] **[BUG-02]** SpecKit assets copied to wrong directory ✅ **RESOLVIDO** (2026-04-03)
  - **Problema**: SpecKit files (`.github/`, `.specify/`) copiados para `target_dir` ao invés de `project_path`
  - **Sintoma**: Projeto em `tmp/projeto-teste/` mas arquivos em `tmp/.github/`
  - **Causa raiz**: `copy_speckit()` em `scripts/lib/project.py` linha ~552 usava `base = config.target_dir`
  - **Correção implementada**:
    - Mudado para `base = config.project_path` com comment "BUG FIX"
    - Atualizados docstrings em `project.py` e `templates.py` (target_dir → project_path)
  - **Arquivos modificados**: `scripts/lib/project.py`, `scripts/lib/templates.py`
  - **Teste de validação**: Test project structure verified, all files in correct locations
  - **Impact**: P0 (created broken project structure)
  - *Reportado em*: 2026-04-03 | *Resolvido em*: 2026-04-03

- [x] **[IMP-33]** Fechar o "perfil fantasma" `devops-security` + atualizar `TEMPLATE-VERSIONS.md` ✅ **JÁ CONCLUÍDO**
  - Criar `profile-descriptors/devops-security.yaml` (descriptor completo do perfil transversal) ✅
  - `--validate` deve sair de 9 warnings para 0 warnings ✅
  - Atualizar `TEMPLATE-VERSIONS.md`: adicionar k8s-helm, terraform-aws, data-pipeline-airflow, data-warehouse-dbt, lgpd-baseline, soc2-baseline ✅
  - Atualizar `COMPATIBILITY-MATRIX.md` com `devops-security` como linha/coluna ✅
  - *Alerta resolvido*: Template Architect • AppSec • Release Maintainer

- [x] **[IMP-34]** QUICKSTART.md + exemplo de output de `generate_profile_guide()`
  - `QUICKSTART.md` na raiz do projeto: 5 minutos para gerar o primeiro projeto
    - Pré-requisitos (Python 3.10+, uv)
    - `python scripts/scaffold.py --list-profiles`
    - `python scripts/scaffold.py --ci --name meu-projeto --domain programming --language python`
    - `python scripts/scaffold.py --compose python-fastapi --ci --name meu-projeto`
  - Adicionar exemplo `docs/PROFILE-GUIDE-python-fastapi.md` no repositório (output real gerado pelo template)
  - *Alerta resolvido*: Technical Writer

---

### 🟡 P1 — Governança e processo (1–2 sessões)

- [x] **[IMP-35]** Processo de release automático
  - Target `make release VERSION=x.y.z` que:
    1. Valida que VERSION segue semver
    2. Fecha seção `[Unreleased]` no `CHANGELOG.md` com a data e versão
    3. Bumpa `SCAFFOLD_VERSION` em `scripts/lib/config.py`
    4. Cria git tag `vX.Y.Z` anotada com o conteúdo do CHANGELOG daquela versão
    5. Executa `--publish` gerando o tarball de release
  - `scripts/lib/release.py` com a lógica + `flow_release()` em `scaffold.py`
  - 27 testes — `tests/test_smoke_imp35.py`
  - *Alerta resolvido*: Release Maintainer

- [x] **[IMP-36]** Staleness check no CI
  - `_check_staleness()` em `validate.py` — warning se `last_tested` > 90 dias
  - `stale_days_threshold` e `stale_profiles` adicionados ao `ValidationReport`
  - Job 4 `staleness` no `ci-template.yml` — `continue-on-error: true`, emite `::warning::` annotations
  - 23 testes — `tests/test_smoke_imp36.py`
  - *Alerta resolvido*: SRE / Infra

- [x] **[IMP-37]** `MIGRATION-GUIDE.md`
  - `docs/MIGRATION-GUIDE.md` — guia completo de migração entre versões
  - Seções: conceitos, o que `--upgrade` faz, acções manuais, procedimento geral,
    migração v1.2.0→v1.3.0, template para versões futuras, referência rápida, troubleshooting
  - *Alerta resolvido*: Release Maintainer

---

### 🔵 P2 — Qualidade técnica (2–3 sessões)

- [x] **[IMP-38]** Refatorar `scaffold.py` — extrair flows para `scripts/lib/flows/`
  - `scaffold.py` está com ~900 linhas; cada novo perfil Layer 2 vai crescer `flow_compose_profiles`
  - Extrair cada `flow_*()` para módulo dedicado:
    - `scripts/lib/flows/new_project.py`
    - `scripts/lib/flows/compose.py`
    - `scripts/lib/flows/upgrade.py`
    - `scripts/lib/flows/dry_run.py`
    - `scripts/lib/flows/publish.py` (mover de lib/)
    - `scripts/lib/flows/validate.py` (mover de lib/)
  - `scaffold.py` vira só argparse + dispatch (≤3 linhas por flow)
  - Zero mudança de comportamento — testes existentes devem continuar passando
  - *Alerta resolvido*: Template Architect

- [x] **[IMP-39]** Ampliar snapshot tests
  - `test_templates_snapshot.py` atualmente testa apenas 3 arquivos
  - Adicionar snapshots para todos os 10 perfis: pelo menos 1 arquivo representativo por perfil
  - Targets: `python-fastapi/src/main.py`, `typescript-next/app/layout.tsx`, `k8s-helm/helm/Chart.yaml`, `terraform-aws/infra/main.tf`, `lgpd-baseline/docs/lgpd/DATA-MAPPING.md`
  - *Alerta resolvido*: Release Maintainer

- [x] **[IMP-40]** `RUNBOOK.md` parametrizado por perfil
  - `infra.py:generate_runbook()` hoje gera template genérico
  - Adicionar blocos condicionais por perfil Layer 2 e Layer 3:
    - k8s-helm: comandos `helm status`, `helm rollback`, `kubectl rollout undo`
    - terraform-aws: `terraform plan`, `terraform apply -target`, `aws ecs describe-services`
    - python-fastapi: `uv run pytest`, checklist de health endpoint
  - Integrar com `ProfileComposer`: saber quais perfis foram aplicados e injetar as seções corretas
  - *Alerta resolvido*: SRE / Infra
  - ✅ Implementado: 3 constantes `_RUNBOOK_SECTION_*` + injeção via `cfg.extra_profiles`; 7 novos testes (514 → 521)

---

### ⚪ P3 — Evolução de schema (futuro / próxima versão MAJOR)

- [x] **[IMP-41]** `security.enforces` estruturado para automação
  - Hoje é lista de strings livres. Mudar para:
    ```yaml
    security:
      enforces:
        - control: "CC6.1"
          description: "Acesso com menor privilégio"
          tool: "trivy"
          severity: "high"
          automated: true
    ```
  - Atualizar schema (`PROFILE-DESCRIPTOR-SCHEMA.md`) + todos os 10 descritores
  - Atualizar `validate.py` para validar a nova estrutura
  - `generate_profile_guide()` passa a gerar tabela de controles em vez de lista de strings
  - *Alerta resolvido*: AppSec
  - ✅ Implementado: 9 descritores migrados, Regra 6 em validate.py, tabela em generate_profile_guide(); 7 novos testes (521 → 528)

- [x] **[IMP-42]** SBOM nos perfis Layer 2
  - Adicionar target `make sbom` em todos os perfis Python: `uv run cyclonedx-bom`
  - Adicionar target `make sbom` no perfil TypeScript: `pnpm dlx @cyclonedx/cyclonedx-npm`
  - Integrar SBOM no job `cli-smoke` do `ci-template.yml`
  - Documentar no `soc2-baseline` como evidência do controle CC8
  - *Alerta resolvido*: AppSec
  - ✅ Implementado: sbom: target em 3 Makefiles, ci_targets + security.enforces CC8 em 4 descritores, step de verificação no ci-template.yml; 28 novos testes (528 → 556)

- [x] **[IMP-43]** `scaffold.py --new-profile NOME` — scaffolder de perfis
  - Gera `profile-descriptors/NOME.yaml` com todos os campos do schema preenchidos com defaults
  - Cria `profile-descriptors/NOME.md` com instruções de preenchimento
  - Executa `--validate` automaticamente após geração
  - *Alerta resolvido*: Template Architect
  - ✅ Implementado: `scripts/lib/flows/new_profile.py` + `--new-profile`/`--profile-layer` em scaffold.py; suporta `--ci`, `--json`, `--force`; 30 novos testes (556 → 586)

- [x] **[IMP-44]** Subcomandos CLI (versão MAJOR — breaking change)
  - Migrar de flags flat para subcomandos:
    ```
    scaffold new     (antigo --new)
    scaffold compose (antigo --compose)
    scaffold upgrade (antigo --upgrade)
    scaffold publish (antigo --publish)
    scaffold validate (antigo --validate)
    scaffold list-profiles (antigo --list-profiles)
    scaffold dry-run (antigo --dry-run)
    scaffold new-profile (novo, IMP-43)
    ```
  - Manter flags legadas com aviso de deprecação por 1 versão MINOR
  - Atualizar copilot-instructions, prompts e QUICKSTART após migração
  - *Alerta resolvido*: DevEx / CLI
  - ✅ Implementado: `_translate_subcommand()` + `_warn_legacy_flags()` em scaffold.py; 10 subcomandos mapeados; flags legadas emitem DeprecationWarning; backward-compatible; 42 novos testes (586 → 628)

- [x] **[IMP-46]** ✅ **CONCLUÍDO 2026-03-14** — Testes de integração (estrutura + AppSec) — IMP-46
  - `tests/helpers/fake_project.py`: `expand_template()` + `FakeProject`; `_PLACEHOLDER_RE` limitado a nomes canônicos
  - `tests/test_integration_structural.py`: 9 templates × asserções estruturais (~60 testes)
  - `tests/test_integration_security.py`: AppSec baseline parametrizado (secrets, .gitignore, YAML válido)
  - `.gitignore` adicionado a python-fastapi, python-flask, typescript-next (gap real corrigido)
  - Job 4 `integration` no `ci-template.yml` (needs: lint)
  - 628 → 746 testes (+118)

- [ ] **[IMP-47]** Testes executáveis por template (L2 — `make lint` por toolchain em CI matrix)
  - Executar `make lint` real por perfil em matrix do CI (Python: ruff+bandit, TS: eslint, Terraform: terraform validate)
  - Requer toolchains instalados no runner (Python, Node, Terraform)
  - *Origem*: debate IMP-46 — pirâmide L0/L1/L2

- [x] **[IMP-48]** Sistema de documentação incremental — Fundação ✅ 2026-03-29
  - Criar `scripts/lib/session.py` — módulo de manipulação de session docs
    - `ActivityBlock` dataclass
    - `generate_activity_block()` — factory
    - `sanitize_block()` — apply redact patterns
    - `append_to_daily_activities()` — append idempotent
    - `validate_daily_activities_format()` — schema validation
  - Criar `docs/templates/DAILY_ACTIVITIES.template.md` — template canônico
  - Criar `docs/SESSION_DOCS_STYLE_GUIDE.md` — guia de estilo
  - Adicionar regra P1 em `.copilot-rules.md`: "Documentar atividades ao completar TODOs"
  - Testes: `tests/test_session_lib.py` (36 testes, 100% pass rate)
  - **Prioridade**: P0 | **Estimativa**: 8h | **Realizado**: 8h 15min
  - **Objetivo**: Legibilidade do chat + documentação/memória aprimorada
  - **Commit**: `de8b329` — feat(docs): IMP-48 - Fundação do sistema de documentação incremental
  - *Origem*: debate 2026-03-29 — DEBATE_INCREMENTAL_DOCUMENTATION_2026-03-29.md

- [ ] **[IMP-49]** Sistema de documentação incremental — Integração
  - Atualizar `session-start.prompt.md` — seção "Protocolo de Documentação"
  - Atualizar `session-end.prompt.md` — seção "Session Security Review" + checklist
  - Criar `.gitleaks-session-docs.toml` — config de scan para docs/SESSIONS/
  - Adicionar job `session-docs-scan` em `.github/workflows/ci-template.yml`
  - Criar `scripts/session-validate.py` — CLI para validação de formato
  - Adicionar targets no Makefile: `session-log`, `session-validate`, `session-sanitize`
  - Configuração em `.scaffold-config.json`: seção `features.session_docs`
  - Testes: `tests/test_session_integration.py` (20 testes)
  - **Prioridade**: P0 | **Estimativa**: 6h
  - *Origem*: debate 2026-03-29

- [ ] **[IMP-50]** Sistema de documentação incremental — Docs + Migração
  - Criar `docs/SESSION_DOCS_ADOPTION.md` — guia de adoção para projetos existentes
  - Criar `docs/SECURITY_SESSION_DOCS.md` — exemplos de do/don't
  - Criar `scripts/migrate-daily-activities.py` — freeform → structured
  - Exemplo prático: `docs/SESSIONS/2026-03-30-example/DAILY_ACTIVITIES_2026-03-30.md` (5 blocos)
  - Atualizar `docs/COMPATIBILITY-MATRIX.md` — adicionar coluna "Session Docs"
  - Atualizar `CHANGELOG.md` — feature de session docs
  - Testes: `tests/test_session_migration.py` (15 testes)
  - **Prioridade**: P0 | **Estimativa**: 4h
  - *Origem*: debate 2026-03-29

- [ ] **[IMP-51]** Busca e indexação de histórico de sessões (MCP integration)
  - `scripts/session-search.py --query "texto"` — busca em DAILY_ACTIVITIES
  - Integração com `mcp_memory` para query de sessões passadas
  - Criar entidades "Session" com observações = blocos de DAILY_ACTIVITIES
  - Interface de query: "Quando implementamos X?" → busca em histórico
  - Testes: `tests/test_session_search.py` (10 testes)
  - **Prioridade**: P1 (crítico para objetivo B: memória aprimorada) | **Estimativa**: 4h
  - **Rationale**: Objetivo do usuário B: "Documentação/memória aprimorada nos projetos"
  - *Origem*: debate 2026-03-29 — melhoria identificada pelo Template Architect

- [x] **[fix-session-start-mcp]** ✅ **CONCLUÍDO 2026-03-16** — Corrigir verificação MCP no ritual de início
  - Passo 1 reescrito: agente lê `.vscode/mcp.json` diretamente (verificável) em vez de depender do Command Palette
  - Arquivos: `session-start.prompt.md`, `session-start-first.prompt.md` (template + projeto enterprise-infra-docker)
  - Decisão D-47a: verificação de *configuração* (agente) × verificação de *runtime* (usuário manual)

---

### Resumo do Plano

| IMP | Título | Prioridade | Esforço | Origem |
|---|---|---|---|---|
| IMP-33 | devops-security.yaml + TEMPLATE-VERSIONS.md | P0 | Baixo | Template Arch • AppSec • Release |
| IMP-34 | QUICKSTART.md + exemplo PROFILE-GUIDE | P0 | Baixo | Docs |
| IMP-35 | `make release VERSION=x.y.z` | P1 | Médio | Release |
| IMP-36 | Staleness check no CI | P1 | Médio | SRE |
| IMP-37 | MIGRATION-GUIDE.md | P1 | Baixo | Release |
| IMP-38 | Refactor scaffold.py → `lib/flows/` | P2 | Alto | Template Arch |
| IMP-39 | Ampliar snapshot tests | P2 | Médio | Release |
| IMP-40 | RUNBOOK.md parametrizado por perfil | P2 | Médio | SRE | ✅ |
| IMP-41 | `security.enforces` estruturado | P3 | Alto | AppSec | ✅ |
| IMP-42 | SBOM nos perfis Layer 2 | P3 | Médio | AppSec |
| IMP-43 | `--new-profile` scaffolder | P3 | Alto | Template Arch |
| IMP-44 | Subcomandos CLI (breaking change) | P3 | Alto | DevEx |
| IMP-45 | Engram oficial — Fallback (Fase 3b) | P2 | 80h | DevEx / AppSec | 🔵 2026-04-05 |
| IMP-46 | Testes de integração estrutura + AppSec | P2 | Médio | Template Arch • AppSec | ✅ 2026-03-14 |
| IMP-47 | Testes executáveis por template (`make lint` matrix) | P2 | Alto | AppSec • SRE |
| IMP-48 | Session Docs — Fundação (lib + templates) | P0 | 8h | DevEx / Template Arch | ✅ 2026-03-29 |
| IMP-49 | Session Docs — Integração (prompts + CI) | P0 | 6h | DevEx / AppSec | ✅ 2026-04-03 |
| IMP-50 | Session Docs — Docs + Migração | P0 | 4h | Release / Docs | ✅ 2026-04-05 |
| IMP-51 | Session Docs — Busca/indexação FTS5 | P1 | 4h | DevEx / Template Arch | ✅ 2026-04-05 |
| IMP-52 | yamllint/jsonschema docs + Makefile | P1 | 2h | DevEx / Docs | ✅ 2026-04-03 |
| IMP-53 | objetivo.yaml + speckit.clarify (Camada 1+3) | P1 | 2h (40h est.) | SpecKit / Product | ✅ 2026-04-14 |
| IMP-54 | ADRs em plan-template.md (com IMP-53) | P1 | — (bundled) | SpecKit / Arch | ✅ 2026-04-14 |
| IMP-55 | Sistema CHAT-*.md capture | P2 | 1 semana | DevEx / Memory | 🔵 2026-04-05 |
| IMP-56 | speckit.validate quality gates | P1 | 1 semana | SpecKit / QA | 🔵 2026-04-05 |
| IMP-57 | Estender IMP-51 — indexar all docs (Fase 1) | P1 | 16h | DevEx / Search | ✅ 2026-04-05 |
| IMP-58 | Avaliar necessidade memória ativa (Fase 2) | P1 | 16h | Product / UX | � 2026-04-05 |
| IMP-59 | Mini-Engram Python (Fase 3a) | P1 | 40h | DevEx / Memory | � 2026-04-05 |
| IMP-65 | Template Synchronization System (4 fases) | P1 | 256h | Template Arch / DevEx | 🔵 2026-04-14 |

---

---

### 🔴 P0 — BLOQUEADORES (executar antes de crescer em perfis)

- [x] **[IMP-09]** ✅ **CONCLUÍDO 2026-03-07** — Enriquecer template `.copilot-rules-[projeto].md`
- [x] **[IMP-16]** ✅ **CONCLUÍDO 2026-03-07** — Testes scaffold — 54 smoke tests (9 combos × 3 asserts × 2 funções) + 4 snapshot tests baseline + CI workflow
  - [x] Setup de pytest em `tests/` com fixtures de config (`conftest.py`, `make_project_config`)
  - [x] 9 combos domínio × linguagem — 54 testes PASSED
  - [x] Snapshots baseline criados: `copilot_rules__programming__python.md`, `copilot_instructions__programming__python.md`, `copilot_rules__infrastructure__python.md`
  - [x] CI: `.github/workflows/test-scaffold.yml` — dispara em PR/push em `scripts/**`
- [x] **[IMP-19a]** ✅ **CONCLUÍDO 2026-03-07** — Profile-descriptor schema — contrato formal dos perfis
  - [x] Schema YAML documentado em `docs/copilot/PROFILE-DESCRIPTOR-SCHEMA.md` (todos os campos anotados)
  - [x] Campos: `name`, `description`, `requires`, `generates.files`, `generates.patches`, `excludes_with`, `combines_with`, `security.enforces`, `VERSION`, `LAST_TESTED_DATE`, `tags`, `layer`, `maintainer`
  - [x] `profile-descriptors/README.md` — índice dos perfis disponíveis
  - [x] `profile-descriptors/devops-programming.yaml` — perfil descriptor de referência completo

---

### 🟡 P1 — ALTO IMPACTO (próximo sprint)

- [x] **[IMP-19b]** ✅ **CONCLUÍDO 2026-03-07** — DevEx/CLI — `--dry-run`, `--list-profiles`, `--json`, `--config` no `scaffold.py`
  - [x] `scaffold.py --list-profiles`: tabela Rich com nome/layer/versão/data/descrição
  - [x] `scaffold.py --list-profiles --json`: output JSON para CI/automação
  - [x] `scaffold.py --dry-run --ci --name X --domain Y --language Z`: manifesto de 17 operações sem criar arquivos
  - [x] `scaffold.py --dry-run --json`: manifesto JSON limpo (sem banner)
  - [x] `scaffold.py --config FILE`: lê configuração de arquivo YAML (força `--ci`)
- [x] **[IMP-20]** ✅ **CONCLUÍDO 2026-03-07** — Layer 2 — Perfil `python-fastapi` completo
  - [x] Prompt domain: `.github/prompts/domain/layer2-python-fastapi.prompt.md`
  - [x] Templates: `src/main.py`, `src/api/router.py`, `src/api/v1/health.py`, `src/core/config.py`, `tests/conftest.py`, `tests/test_health.py`
  - [x] `pyproject.toml` com deps FastAPI + pytest-asyncio + ruff + bandit + pip-audit
  - [x] `Dockerfile` multistage (`uv sync --frozen --no-dev` + usuário não-root)
  - [x] `docker-compose.yml` (app + postgres:16 com healthcheck)
  - [x] `Makefile` targets: `dev`, `test`, `lint`, `format`, `audit`, `security`, `ci`, `docker-*`
  - [x] `.env.example` com variáveis documentadas sem valores reais
  - [x] Profile descriptor: `profile-descriptors/python-fastapi.yaml`
- [x] **[IMP-20b]** ✅ **CONCLUÍDO 2026-03-07** — Layer 2 — Perfil `python-flask` completo *(uso declarado pelo mantenedor)*
  - [x] Prompt domain: `.github/prompts/domain/layer2-python-flask.prompt.md`
  - [x] Templates: `src/app.py`, `src/blueprints/health/`, `src/core/config.py`, `src/extensions.py`, `tests/conftest.py`, `tests/test_health.py`
  - [x] `pyproject.toml` com deps Flask + Flask-WTF + Flask-Talisman + ruff + bandit + pip-audit
  - [x] `Dockerfile` multistage (`uv sync --frozen --no-dev` + usuário não-root, gunicorn)
  - [x] `docker-compose.yml` (app + postgres:16 com healthcheck)
  - [x] `Makefile` targets: `dev`, `test`, `lint`, `format`, `audit`, `security`, `ci`, `docker-*`
  - [x] `.env.example` com `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY` documentados
  - [x] Profile descriptor: `profile-descriptors/python-flask.yaml`
- [x] **[IMP-21]** Layer 2 — Perfil `typescript-next` completo
  - [x] Prompt domain: `.github/prompts/domain/layer2-typescript-next.prompt.md`
  - [x] Templates: estrutura Next.js com TypeScript strict
  - [x] ESLint + Prettier + Jest configurados
  - [x] Profile descriptor: `profile-descriptors/typescript-next.yaml`
- [x] **[IMP-15]** Geração de `Dockerfile`, `docker-compose.yml`, workflows CI/CD pelo scaffold
  - [x] CI skeleton: `.github/workflows/ci.yml` (lint + test + build)
  - [x] `Dockerfile` multistage por linguagem (python, node, go)
  - [x] `docker-compose.yml` com serviço app + dependências opcionais (postgres, redis)
  - [x] Runbook template gerado em `docs/RUNBOOK.md`

---

### 🔵 P2 — IMPORTANTE (sprint +2)

- [x] **[IMP-22]** ✅ **CONCLUÍDO 2026-03-07** — Layer 3 — Perfil `k8s-helm` (plataforma)
  - [x] Prompt domain: `.github/prompts/domain/layer3-k8s-helm.prompt.md`
  - [x] Templates: `helm/Chart.yaml`, `helm/values.yaml`, `helm/values-staging.yaml`, `helm/values-prod.yaml`, `helm/templates/` (8 arquivos), `.helmignore`, `Makefile.helm`
  - [x] Compatível com: `python-fastapi`, `python-flask`, `typescript-next` (field `combines_with`)
  - [x] Profile descriptor: `profile-descriptors/k8s-helm.yaml` (layer: 3, Schema A)
  - [x] Testes: `tests/test_smoke_k8s_helm.py` — 13 testes (97 → 110 passed)
- [x] **[IMP-23]** ✅ **CONCLUÍDO 2026-03-07** — Layer 3 — Perfil `terraform-aws` (plataforma)
  - [x] Prompt domain: `.github/prompts/domain/layer3-terraform-aws.prompt.md`
  - [x] Templates: módulos Terraform VPC, ECS Fargate e RDS PostgreSQL (16 arquivos)
  - [x] Security: IAM least privilege (ARN específico), RDS sem public access, passwords via random_password + SSM
  - [x] Profile descriptor: `profile-descriptors/terraform-aws.yaml` (layer: 3, Schema A)
  - [x] Testes: `tests/test_smoke_terraform_aws.py` — 16 testes (110 → 126 passed)
- [x] **[IMP-24]** Motor de Composição de Perfis
  - [x] Resolver conflitos entre perfis (`excludes_with`)
  - [x] Ordem de aplicação de patches
  - [x] Rollback em caso de erro parcial
  - [x] Teste de todas as combinações válidas
- [x] **[IMP-25]** Governança — CHANGELOG, versionamento semântico, matriz de compatibilidade
  - [x] `TEMPLATE-VERSIONS.md`: versionamento por perfil
  - [x] `COMPATIBILITY-MATRIX.md`: perfis × perfis
  - [x] `CHANGELOG.md` com histórico desde v0.1.0
  - [x] Política de depreciação documentada
- [x] **[IMP-10]** ✅ **CONCLUÍDO 2026-03-07** — Documentação humana dos domínios: `docs/copilot/DOMAIN-PROGRAMMING.md`, `DOMAIN-INFRASTRUCTURE.md`, `DOMAIN-ANALYSIS.md`

---

### ⚪ P3 — FUTURO (backlog)

- [x] **[IMP-26]** Layer 3 — Data/Analytics: `data-pipeline-airflow`, `data-warehouse-dbt`
- [x] **[IMP-27]** Layer 4 — Compliance: `lgpd-baseline`, `soc2-baseline`
- [x] **[IMP-28]** Modo upgrade/re-apply: `scaffold.py upgrade` para projetos já gerados — **CONCLUÍDO 2026-03-07** — `--upgrade` lê `.scaffold-state.yaml`, re-aplica todos os passos de geração (idempotente), suporte a `--json` e `--force`. 30 testes.
- [x] **[IMP-29]** ✅ **CONCLUÍDO 2026-03-08** — Documentação gerada por perfil ativo (guia específico por combinação)
  - [x] `generate_profile_guide(cfg, profiles_applied, descriptors)` em `scripts/lib/templates.py`
  - [x] 5 seções: Combinação de Perfis, Arquivos Gerados, Segurança, Quick Start, Referências por Stack
  - [x] Slug derivado dos perfis layer2+ (exclui core e transversal)
  - [x] Integrado em `flow_compose_profiles()` e `flow_upgrade()` em `scaffold.py`
  - [x] Idempotente — skipa se `docs/PROFILE-GUIDE-{slug}.md` já existe
  - [x] 33 testes PASSED → total: **307 tests**
- [x] **[IMP-30]** ✅ **CONCLUÍDO 2026-03-08** — `scaffold.py --publish` — tarball de release do template
  - [x] `scripts/lib/publish.py` — `publish_template(output_dir, project_root)` gera `enterprise-template-v{version}-{date}.tar.gz`
  - [x] Inclui: scripts/lib, profile-descriptors, .github/templates, .github/prompts, Makefile, README, CHANGELOG, testes
  - [x] Exclui: __pycache__, .venv, .git, .secrets, dist, *.pyc
  - [x] Manifesto JSON (`release-manifest-v*.json`) com versão, file_count, size_bytes, lista de arquivos
  - [x] `--output-dir PATH` — diretório de saída configurável (default: `dist/`)
  - [x] Suporte a `--json` para CI/automação
  - [x] 35 testes PASSED → total: **342 tests**
- [x] **[IMP-31]** ✅ **CONCLUÍDO 2026-03-08** — CI/CD do template — GitHub Actions pytest matrix + cli-smoke + lint
  - [x] `.github/workflows/ci-template.yml` — 3 jobs: **test** (matrix 3.10/3.11/3.12), **cli-smoke**, **lint**
  - [x] Disparo em `pull_request` + `push` (paths: scripts/**, tests/**, profile-descriptors/**)
  - [x] `concurrency` com `cancel-in-progress: true` para PRs
  - [x] Job **lint**: `py_compile` em todos `scripts/lib/*.py` + `yaml.safe_load` em `profile-descriptors/*.yaml`
  - [x] `tests/test_smoke_imp31.py` — 26 testes PASSED → total: **368 tests**
- [x] **[IMP-32]** ✅ **CONCLUÍDO 2026-03-08** — `scaffold.py --validate` — validação de profile-descriptors
  - [x] `scripts/lib/validate.py` — módulo de validação: `ValidationIssue`, `ProfileResult`, `ValidationReport`, `validate_descriptors()`
  - [x] 6 regras por descriptor: name, description, version (semver), last_tested, layer, sintaxe YAML
  - [x] Validação cruzada: nomes duplicados + `combines_with`/`excludes_with` referenciando perfis inexistentes
  - [x] Aceita schema antigo (VERSION/LAST_TESTED_DATE) e novo (version/last_tested)
  - [x] Aceita `combines_with` como lista de strings ou lista de objetos `{name, notes}`
  - [x] `flow_validate()` + flag `--validate` em `scaffold.py`; suporte a `--json`
  - [x] Exit code 0 se valid (apenas warnings ok); exit code 1 se erros
  - [x] `tests/test_smoke_imp32.py` — 42 testes PASSED → total: **410 tests**
- [x] **[IMP-17]** ✅ **CONCLUÍDO** — Issue Templates + Script `load-mcp.sh` + VS Code `tasks.json`/`launch.json`/perfil

---

### 📜 Backlog Original (mantido para referência)

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
- [x] **[IMP-18]** ✅ **CONCLUÍDO 2026-03-07** — Criar `.github/copilot-instructions.md` — auto-injeção de regras P0/P1 em toda conversa Copilot
  - [x] `.github/copilot-instructions.md` criado para `a-default-project` (regras P0/P1 compactas, `applyTo: "**"`)
  - [x] `scripts/lib/templates.py`: `generate_copilot_instructions()` adicionada (template com placeholders)
  - [x] `scripts/scaffold.py`: passo 3 atualizado (wired `generate_copilot_instructions(cfg)`)
  - [x] Zero erros de compilação verificados
- [x] **[IMP-09]** ✅ **CONCLUÍDO 2026-03-07** — Enriquecer template `.copilot-rules-[projeto].md` gerado pelo `scaffold.py`
  - [x] Regras P0/P1 pré-preenchidas por domínio (`programming`, `infrastructure`, `analysis`)
  - [x] Convenções de linguagem com tabela detalhada (`python`, `typescript`, `go`, `other`)
  - [x] Estrutura de pastas dinâmica por domínio + linguagem (8 combinações)
  - [x] Tabela de perfis ativos (domínio + segurança transversal + extras)
  - [x] Seção de decisões técnicas pré-populada
  - [x] Smoke-test: 5 combos domain/language ✅ — zero erros
- [x] **[IMP-10]** ✅ **CONCLUÍDO 2026-03-07** — Criar documentação humana dos 3 domínios em `docs/copilot/DOMAIN-PROGRAMMING.md`, `DOMAIN-INFRASTRUCTURE.md`, `DOMAIN-ANALYSIS.md`
- [x] **[IMP-14]** ✅ **FASE A CONCLUÍDA 2026-03-05** — SpecKit instalado no projeto filho + Novos Domain Profiles + Perfis Profissionais
  - Debate: `docs/SESSIONS/2026-03-05/IMP-14-DEBATE.md`
  - Decisões: D-20..D-25 todas respondidas 🟢 (2026-03-05)
  - **Fase A (P0) ✅**: A.1 `SPECKIT_SYNC_DATE` em config.py • A.2 `copy_speckit()` • A.3 `generate_constitution()` • A.4 questão `[8]` em ui.py • A.5 integrar em scaffold.py • A.6 `devops-security.prompt.md` • A.7 extensões Review/Runbook nos 3 perfis • A.8 `constitution.md` v1.0.0
  - **Fase B (P1)** 🔵: `devops-cicd.prompt.md` + testes scaffold + docs de uso
  - **Fase C (P2)** 🔵: melhorias UX `ui.py`
- [ ] **[IMP-15]** (futuro) Geração de `Dockerfile`, `docker-compose.yml`, workflows CI/CD pelo scaffold
- [x] **[IMP-16]** ✅ **CONCLUÍDO 2026-03-07** — Testes para `scaffold.py` e `scripts/lib/`
  - 54 smoke tests PASSED (9 combos × 3 asserts × 2 funções)
  - 4 snapshot tests PASSED (modo CI, comparação contra baseline)
  - Trigger: `.github/workflows/test-scaffold.yml`
- [x] **[IMP-17]** ✅ **CONCLUÍDO** — Issue Templates + Script `load-mcp.sh` + VS Code `tasks.json`/`launch.json`/perfil
  - Debate: `docs/SESSIONS/2026-03-05/IMP-17-DEBATE.md`
  - Decisões: D-26=Markdown • D-27=3 templates+config • D-28=copy_speckit • D-29=Standard • D-30=scripts/+make mcp • D-31=dinâmico • D-32=Standard • D-33=por linguagem • D-34=skip
  - ✅ `.github/ISSUE_TEMPLATE/` — bug_report.md + feature_request.md + improvement.md + config.yml
  - ✅ `generate_load_mcp(cfg)` em `project.py` — scripts/load-mcp.sh dinâmico por domínio (chmod +x)
  - ✅ `generate_tasks(cfg)` em `vscode.py` — .vscode/tasks.json com 7 targets Makefile
  - ✅ `generate_launch(cfg)` em `vscode.py` — .vscode/launch.json por linguagem (Python/TS/Go/other)
  - ✅ `copy_speckit()` atualizado para copiar ISSUE_TEMPLATE/*
  - ✅ `scaffold.py` integrado (passos 4+7)
  - ✅ 27 smoke tests PASSED → total: **153 tests**
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

#### 2026-03-07 (Sessão atual)
- [x] Carregar regras Copilot na memória (`.copilot-rules.md` — único arquivo ativo desde IMP-13)
- [x] Iniciar sessão MCP — servidores `memory` + `sequential-thinking` ativos
- [x] Recuperar dados da sessão anterior (2026-03-05)
- [x] Scan de credenciais/arquivos sensíveis → 🟢 LIMPO
- [x] Verificar `.secrets/` no `.gitignore` (confirmado)
- [x] Verificar organização da raiz → LIMPA (root: 11 itens válidos)
- [x] Renomear `docs/GitHub Copilot Recursos de Agents etc.md` → `GITHUB-COPILOT-AGENTS-RESOURCES.md` (convenção de nomenclatura)
- [x] Criar `docs/SESSIONS/2026-03-07/SESSION_RECOVERY_2026-03-07.md`
- [x] Criar `docs/SESSIONS/2026-03-07/DAILY_ACTIVITIES_2026-03-07.md`
- [x] Atualizar `docs/TODO.md` e `docs/INDEX.md`
- [x] **[IMP-18]** Criar `.github/copilot-instructions.md` + `generate_copilot_instructions()` em `templates.py` + wiring em `scaffold.py`
- [x] **[IMP-09]** Enriquecer template `.copilot-rules-[projeto].md` — smoke-test: 5 combos ✅
- [x] **[IMP-19 — Debate]** Analisar `Default Project Template Skills.md` → criar agente `template-architect.agent.md` + debate IMP-19 + roadmap P0→P3

#### 2026-03-05 (Sessão encerrada)
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
