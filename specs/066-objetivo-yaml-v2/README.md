# Feature 066: objetivo.yaml v2.0 — Human-Readable Format

**Status**: 📋 Spec Ready → ⏳ Implementation Pending
**Branch**: `066-objetivo-yaml-v2`
**Created**: 2026-04-27
**Owner**: yves_marinho

---

## 🎯 Quick Summary

Redesenha o formato objetivo.yaml para ser legível e fácil de preencher por desenvolvedores de todos os níveis (iniciante → avançado), reduzindo tempo de preenchimento em 75% e taxa de erro em 89%.

**Formato**: Markdown Híbrido (YAML frontmatter + Markdown body)
**Arquitetura**: Two-file (objetivo.yaml humano + objetivo-spec.yaml máquina)
**Progressive Disclosure**: 3 níveis (P0: 3 campos, P1: 2 campos, P2: 4 campos)

---

## 📊 Impact Metrics

| Métrica | v1.0 (antes) | v2.0 (meta) | Δ |
|---------|--------------|-------------|---|
| **Tempo de preenchimento** (iniciante) | 45-60 min | 10-15 min | **-75%** |
| **Taxa de erro** (campos obrigatórios) | 38% | <5% | **-89%** |
| **Campos obrigatórios P0** | 18 | 3 | **-83%** |
| **Exemplos inline** | 0 | 17+ | **+∞** |
| **NPS** (satisfação) | 28 | >70 | **+150%** |
| **Taxa de abandono** (1ª tentativa) | 42% | <10% | **-76%** |

---

## 📂 Documentation

### Core Spec Files
- **[spec.md](./spec.md)** — Feature specification completa (5 user stories, critérios de aceitação)
- **[plan.md](./plan.md)** — Implementation plan + 6 ADRs (decisões arquiteturais)
- **[tasks.md](./tasks.md)** — Task list detalhada (39 tasks, 10-12 dias úteis)
- **[objetivo.yaml](./objetivo.yaml)** — Meta-exemplo (este projeto usando formato v2.0)

### Research & Design
- **[research/formato-debate.md](./research/formato-debate.md)** — Research summary + links para debate completo

### Related Documents
- [DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md](../../docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md) (~5.4k linhas)
- [COMPARACAO-OBJETIVO-V1-V2.md](../../docs/debates/COMPARACAO-OBJETIVO-V1-V2.md) (~1.2k linhas)
- [RESUMO-REDESIGN-OBJETIVO-YAML.md](../../docs/debates/RESUMO-REDESIGN-OBJETIVO-YAML.md) (~200 linhas)
- [objetivo-v2-example-chatwoot.md](../../poc/objetivo-v2-example-chatwoot.md) (~350 linhas)

---

## 🚀 Implementation Plan

### Fase 1: Validação (2 dias) ⏳

**Goal**: Validar formato v2.0 em cenários diversos

**Tasks**:
- [ ] T001-T003 Converter 3 projetos template para v2.0 (python-fastapi, k8s-helm, terraform-aws)
- [ ] T004 Documentar edge cases encontrados
- [ ] T005 Validar com 2-3 usuários teste

**Deliverables**:
- `poc/objetivo-v2-python-fastapi.md` (~300 linhas)
- `poc/objetivo-v2-k8s-helm.md` (~280 linhas)
- `poc/objetivo-v2-terraform-aws.md` (~320 linhas)
- `docs/debates/VALIDACAO-FASE1-EDGE-CASES.md`

---

### Fase 2: Parser & Validador (1 semana) ⏳

**Goal**: Implementar parser robusto e validador com mensagens claras

**Tasks**:
- [ ] T006-T010 Implementar `objetivo_parser.py` + 8 testes
- [ ] T011-T015 Implementar `objetivo_validator.py` + 5 testes
- [ ] T016-T020 Implementar `objetivo_migrator.py` + 4 testes (v1.0 → v2.0)
- [ ] T021-T024 Integrar com `scaffold.py` (comandos validate/generate/migrate) + 4 testes

**Deliverables**:
- `scripts/lib/objetivo_parser.py` (~500 linhas)
- `scripts/lib/objetivo_validator.py` (~300 linhas)
- `scripts/lib/objetivo_migrator.py` (~200 linhas)
- Integração `scripts/scaffold.py` (+240 linhas)
- `tests/test_objetivo_*.py` (~620 linhas, 21 testes)

---

### Fase 3: Wizard Interativo (3-4 dias) ⏳

**Goal**: Wizard acessível para iniciantes criarem objetivo.yaml sem editar arquivo

**Tasks**:
- [ ] T025-T031 Implementar `objetivo_wizard.py` (perguntas P0/P1/P2, keyboard navigation)
- [ ] T032-T033 Fallback graceful (sem Rich)
- [ ] T034-T036 Integrar com `scaffold.py objetivo-init --interactive` + 6 testes E2E
- [ ] T037-T039 Documentação (`OBJETIVO_WIZARD_GUIDE.md`, README.md, JSON schema)

**Deliverables**:
- `scripts/lib/objetivo_wizard.py` (~400 linhas)
- `tests/test_objetivo_wizard.py` (~200 linhas, 6 testes)
- `docs/guides/OBJETIVO_WIZARD_GUIDE.md` (~150 linhas)
- `.specify/schemas/objetivo-spec-v1.0.json` (~120 linhas)

---

## 🎯 User Stories

### 🎯 US1 (P1 - MVP): Criar objetivo.yaml v2.0 para projeto simples
**Persona**: DevOps Iniciante  
**Goal**: Criar primeiro objetivo.yaml sem erros em <15 min  
**Acceptance**: Template com exemplos inline, validação com mensagens claras, <5% taxa erro

### 🎯 US2 (P1 - MVP): Converter objetivo.yaml v1.0 → v2.0
**Persona**: Programador Intermediário  
**Goal**: Migrar projeto existente sem perda de informação  
**Acceptance**: 100% campos migrados, preview side-by-side, backup automático

### 🎯 US3 (P1 - MVP): Gerar objetivo-spec.yaml a partir de objetivo.yaml v2.0
**Persona**: Tech Lead Avançado  
**Goal**: Gerar arquivo máquina para Copilot processar  
**Acceptance**: YAML técnico válido, perfis/features/personas extraídos automaticamente

### 🎯 US4 (P2): Wizard interativo para criar objetivo.yaml v2.0
**Persona**: DevOps Iniciante  
**Goal**: Criar objetivo.yaml respondendo perguntas (sem editar arquivo)  
**Acceptance**: 3 perguntas P0, keyboard navigation completa, <5 min

### 🎯 US5 (P2): Validar objetivo.yaml v2.0 com mensagens claras
**Persona**: Programador Intermediário  
**Goal**: Corrigir erros de validação rapidamente  
**Acceptance**: Linha exata do erro, diff colorido, exemplo de correção sugerido

---

## 🏗️ Architecture Decisions (ADRs)

### ADR-001: Markdown Híbrido (YAML frontmatter + Markdown body)
**Status**: ✅ Accepted  
**Rationale**: Legibilidade +200%, suporte formatação (listas/tabelas/código), parsers maduros disponíveis

### ADR-002: Progressive Disclosure em 3 Níveis (P0/P1/P2)
**Status**: ✅ Accepted  
**Rationale**: -75% tempo preenchimento, -89% taxa erro, minimalismo (3 campos P0 vs 18 v1.0)

### ADR-003: Arquitetura Two-File (objetivo.yaml + objetivo-spec.yaml)
**Status**: ✅ Accepted  
**Rationale**: Separação clara humano/máquina, zero ambiguidade, Git-friendly

### ADR-004: Wizard Interativo com Keyboard Navigation
**Status**: ✅ Accepted  
**Rationale**: Acessibilidade (keyboard-only), guiado (perguntas claras), progressivo (P0→P1→P2)

### ADR-005: Parser com Zero Dependências Obrigatórias
**Status**: ✅ Accepted  
**Rationale**: Minimalismo (stdlib Python suficiente), segurança (menos dependências), portabilidade

### ADR-006: Migração Automática v1.0 → v2.0
**Status**: ✅ Accepted  
**Rationale**: Preservação (100% campos migrados), segurança (preview + confirmação), adoção facilitada

Ver [plan.md](./plan.md) para detalhes completos de cada ADR.

---

## 📋 Task Summary

| Fase | Tasks | Estimate | Status |
|------|-------|----------|--------|
| **Fase 1: Validação** | T001-T005 (5 tasks) | 2 dias | ⏳ Pending |
| **Fase 2: Parser** | T006-T024 (19 tasks) | 1 semana | ⏳ Pending |
| **Fase 3: Wizard** | T025-T039 (15 tasks) | 3-4 dias | ⏳ Pending |
| **TOTAL** | **39 tasks** | **10-12 dias úteis** | ⏳ Pending |

Ver [tasks.md](./tasks.md) para task list completa.

---

## 🧪 Testing Strategy

### Unit Tests (21 testes)
- Parser: 8 testes (happy path, edge cases, invalid YAML)
- Validator: 5 testes (P0 fields, frontmatter, duplicate sections)
- Migrator: 4 testes (v1.0→v2.0, complex cases, edge cases)
- Integration: 4 testes (scaffold.py commands)

### E2E Tests (6 testes)
- Wizard: P0 only, P0+P1, Ctrl+C/Ctrl+Z, non-interactive, fallback

**Target Coverage**: >90%

---

## 📦 Deliverables

### Code
- `scripts/lib/objetivo_parser.py` (~500 linhas)
- `scripts/lib/objetivo_validator.py` (~300 linhas)
- `scripts/lib/objetivo_migrator.py` (~200 linhas)
- `scripts/lib/objetivo_wizard.py` (~400 linhas)
- Extensão `scripts/scaffold.py` (+240 linhas)
- Testes (`tests/test_objetivo_*.py`) (~820 linhas, 27 testes)

### Documentation
- `docs/guides/OBJETIVO_WIZARD_GUIDE.md` (~150 linhas)
- `docs/debates/VALIDACAO-FASE1-EDGE-CASES.md` (TBD linhas)
- `.specify/schemas/objetivo-spec-v1.0.json` (~120 linhas)
- Atualização README.md (+50 linhas)

### Examples
- `poc/objetivo-v2-python-fastapi.md` (~300 linhas)
- `poc/objetivo-v2-k8s-helm.md` (~280 linhas)
- `poc/objetivo-v2-terraform-aws.md` (~320 linhas)
- `poc/objetivo-v2-template-base.md` (~250 linhas)

---

## 🎓 How to Get Started

### Read the Spec
1. **Start here**: [spec.md](./spec.md) — Compreenda os 5 user stories e critérios de aceitação
2. **Understand design**: [plan.md](./plan.md) — Veja os 6 ADRs e decisões arquiteturais
3. **See example**: [objetivo-v2-example-chatwoot.md](../../poc/objetivo-v2-example-chatwoot.md) — Formato v2.0 real

### Understand the Problem
1. **Read debate**: [DEBATE-COMPLETO.md](../../docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md) — 5 especialistas, 6 horas
2. **See comparison**: [COMPARACAO.md](../../docs/debates/COMPARACAO-OBJETIVO-V1-V2.md) — v1.0 vs v2.0 lado a lado
3. **Review summary**: [RESUMO.md](../../docs/debates/RESUMO-REDESIGN-OBJETIVO-YAML.md) — Executive summary

### Start Implementation
1. **Pick a task**: [tasks.md](./tasks.md) — 39 tasks organizadas por fase
2. **Fase 1 first**: T001-T005 (converter 3 projetos, validar formato)
3. **Then Fase 2**: T006-T024 (parser + validator + migrator)
4. **Finally Fase 3**: T025-T039 (wizard interativo)

---

## ✅ Success Criteria

### Pre-Launch
- ✅ 3 projetos convertidos para v2.0 (python-fastapi, k8s-helm, terraform-aws)
- ✅ Parser funcional (<100ms)
- ✅ Validador com mensagens claras (linha exata + exemplo)
- ✅ Migrador v1.0→v2.0 (100% campos migrados)
- ✅ Wizard interativo (keyboard navigation completa)
- ✅ 27/27 testes passando (>90% cobertura)
- ✅ Documentação completa (OBJETIVO_WIZARD_GUIDE.md)

### Post-Launch (após 4 semanas)
- ✅ >80% novos projetos usam v2.0
- ✅ <15 min tempo médio preenchimento (iniciantes)
- ✅ <5% taxa de erro em campos P0
- ✅ NPS >70
- ✅ <3 issues GitHub sobre formato confuso

---

## 🔗 Quick Links

**Spec Files**:
- [spec.md](./spec.md) | [plan.md](./plan.md) | [tasks.md](./tasks.md) | [objetivo.yaml](./objetivo.yaml)

**Debate Docs**:
- [DEBATE-COMPLETO.md](../../docs/debates/DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md)
- [COMPARACAO.md](../../docs/debates/COMPARACAO-OBJETIVO-V1-V2.md)
- [RESUMO.md](../../docs/debates/RESUMO-REDESIGN-OBJETIVO-YAML.md)

**Examples**:
- [objetivo-v2-example-chatwoot.md](../../poc/objetivo-v2-example-chatwoot.md)

---

**Last Updated**: 2026-04-27  
**Spec Version**: 1.0.0  
**Implementation Status**: 📋 Spec Ready → ⏳ Implementation Pending
