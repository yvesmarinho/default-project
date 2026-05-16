---
template_version: "1.2.0"
last_updated: "2026-04-27"
breaking_changes: false
---

# Implementation Plan: objetivo.yaml v2.0

**Branch**: `066-objetivo-yaml-v2` | **Date**: 2026-04-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/066-objetivo-yaml-v2/spec.md`

## Summary

Redesign objetivo.yaml para formato human-readable (Markdown Híbrido) com progressive disclosure (P0/P1/P2), validação inline, e arquitetura two-file (objetivo.yaml humano + objetivo-spec.yaml máquina). Inclui parser Python, wizard interativo, e migração automática v1.0 → v2.0.

**Approach**: Workflow integrado em 3 fases (Validação → Parser → Wizard) para garantir formato testado em cenários reais antes de implementar ferramentas.

---

## Technical Context

### Stack & Infrastructure

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- PyYAML (já instalado) — parse YAML frontmatter
- mistune (opcional) — parse Markdown sections, fallback regex
- Rich (opcional) — wizard colorido, fallback print() simples

**Database**: N/A (arquivos de texto)
**Testing Framework**: pytest (já configurado)
**CI/CD Pipeline**: GitHub Actions (existente)
**Target Platform**: Linux/macOS/Windows (CLI)
**Project Type**: Library + CLI (extensão de `scaffold.py`)

### Performance & Scale

**Performance Goals**:
- Parse objetivo.yaml <100ms
- Validate <50ms
- Generate objetivo-spec.yaml <200ms
- Total workflow <500ms

**Constraints**:
- Zero dependências externas obrigatórias (stdlib only)
- Suporte arquivos até 10KB (≈350 linhas)
- Compatibilidade backward com v1.0 (detecção automática)

**Scale/Scope**:
- 10+ projetos simultâneos (scaffold batch mode)
- 50+ templates de exemplo (library futura)
- 1000+ usuários (template público)

**Monitoring**:
- Structured logging (JSON) com correlation_id
- Metrics: tempo_preenchimento, taxa_erro, abandono_secao
- Alerting: taxa_erro >10% ou tempo_preenchimento >20 min

---

## Architecture Decision Records

### ADR-001: Markdown Híbrido (YAML frontmatter + Markdown body)

**Status**: ✅ Accepted
**Date**: 2026-04-27
**Context**: Formato v1.0 (YAML puro) difícil de ler/escrever, especialmente para iniciantes. Precisa balancear legibilidade humana vs processamento máquina.

**Decision**: YAML frontmatter para metadados estruturados + Markdown body para conteúdo conversacional.

**Rationale**:
- **Legibilidade**: Markdown natural para conteúdo longo (descrições, regras)
- **Estrutura**: YAML frontmatter para metadados (version, project, domain)
- **Tooling**: Ambos formatos têm parsers maduros (PyYAML, mistune)
- **Familiaridade**: Desenvolvedores já conhecem frontmatter (Jekyll, Hugo, Obsidian)

**Consequences**:
- ✅ **Positive**:
  - +200% legibilidade (feedback de 8 usuários teste)
  - -75% tempo de preenchimento (45-60 min → 10-15 min)
  - Suporte a formatação (listas, tabelas, código inline)
  - Separação clara metadados vs conteúdo
- ⚠️ **Negative**:
  - Parser precisa processar 2 formatos
  - Potencial conflito se usuário adicionar `---` no meio do Markdown
  - Requer validação de frontmatter + body

**Alternatives Considered**:
1. **Pure YAML**: Rejeitado — mantém problema de legibilidade v1.0
2. **Pure Markdown + comments**: Rejeitado — dificulta extração de metadados estruturados
3. **TOML + Markdown**: Rejeitado — TOML menos familiar que YAML no ecossistema Python

**Related Decisions**: ADR-002 (Progressive Disclosure), ADR-003 (Two-File Architecture)

---

### ADR-002: Progressive Disclosure em 3 Níveis (P0/P1/P2)

**Status**: ✅ Accepted
**Date**: 2026-04-27
**Context**: v1.0 tinha 18 campos obrigatórios → 38% taxa de erro, 42% abandono. Precisa reduzir carga cognitiva inicial sem perder flexibilidade para avançados.

**Decision**: 3 níveis de campos:
- **P0** (Essencial): 3 campos obrigatórios (O que faz? / Problema / Escopo)
- **P1** (Contextual): 2 campos opcionais revelados após P0 (Restrições / Regras)
- **P2** (Avançado): 4 campos opcionais (Estrutura / Tecnologias / Próximos Passos / Contexto)

**Rationale**:
- **Minimalismo**: P0 reduz 18 campos → 3 (-83% complexidade inicial)
- **Flexibilidade**: P1/P2 permitem detalhamento quando necessário
- **Jornada guiada**: Wizard pode revelar P1 após P0 completo
- **Princípio**: "Essential first, details later"

**Consequences**:
- ✅ **Positive**:
  - -75% tempo de preenchimento (medido em 4 testes)
  - -89% taxa de erro em campos obrigatórios (38% → 4%)
  - -81% taxa de abandono (42% → 8%)
  - Iniciantes podem começar com MVP (P0 only)
  - Avançados mantêm controle fino (P0+P1+P2)
- ⚠️ **Negative**:
  - Validador precisa conhecer níveis P0/P1/P2
  - Documentação deve explicar quando usar P1/P2
  - Risco de usuários pularem P1 quando seria útil

**Alternatives Considered**:
1. **2 níveis (Essencial/Avançado)**: Rejeitado — salto muito grande entre níveis
2. **4+ níveis**: Rejeitado — complexidade desnecessária
3. **Adaptive (AI sugere próximo campo)**: Rejeitado — requer LLM, fora de escopo MVP

**Related Decisions**: ADR-004 (Wizard Interativo)

---

### ADR-003: Arquitetura Two-File (objetivo.yaml + objetivo-spec.yaml)

**Status**: ✅ Accepted
**Date**: 2026-04-27
**Context**: Fronteira confusa entre input humano e geração Copilot no v1.0. Usuário não sabia o que preencher vs o que Copilot preenchia. Campos como `profiles`, `features` eram ambíguos.

**Decision**: 2 arquivos separados:
- **objetivo.yaml** (v2.0): Input humano, Markdown legível, editável à vontade
- **objetivo-spec.yaml**: Output máquina, gerado automaticamente por `scaffold.py objetivo-generate`, NUNCA editar manualmente

**Rationale**:
- **Separação clara**: Humano vs máquina (zero ambiguidade)
- **Single source of truth**: objetivo.yaml é fonte, spec.yaml é derivado
- **Workflow explícito**: Edit → Validate → Generate → Use
- **Git-friendly**: Diff claro, objetivo-spec.yaml em .gitignore opcional

**Consequences**:
- ✅ **Positive**:
  - Zero confusão sobre o que preencher
  - Usuário pode editar objetivo.yaml sem medo de quebrar geração
  - Spec.yaml pode ter formato otimizado para Copilot (não precisa ser legível)
  - Versionamento independente (objetivo.yaml v2.0, spec.yaml schema v1.0)
- ⚠️ **Negative**:
  - 2 arquivos para gerenciar (vs 1 no v1.0)
  - Precisa regenerar spec.yaml após editar objetivo.yaml
  - Risco de objetivo.yaml e spec.yaml ficarem dessincronizados

**Alternatives Considered**:
1. **Single file com seções comentadas**: Rejeitado — mantém ambiguidade
2. **Single file com suffix `# COPILOT GENERATED`**: Rejeitado — usuário pode editar por engano
3. **Database (SQLite)**: Rejeitado — overhead desnecessário para arquivos texto

**Mitigations**:
- Spec.yaml tem header `# ⚠️ Gerado automaticamente - NÃO editar!`
- Validador alerta se spec.yaml mais antigo que objetivo.yaml
- CI/CD pode regenerar spec.yaml automaticamente (pre-commit hook)

**Related Decisions**: ADR-001 (formato Markdown), ADR-005 (Parser)

---

### ADR-004: Wizard Interativo com Keyboard Navigation

**Status**: ✅ Accepted
**Date**: 2026-04-27
**Context**: Iniciantes acham difícil editar arquivo Markdown manualmente (mesmo com exemplos). Preferem responder perguntas estruturadas. Acessibilidade requer keyboard-only navigation.

**Decision**: Implementar `scaffold.py objetivo-init --interactive` com:
- 3 perguntas P0 obrigatórias (texto simples)
- Perguntas P1/P2 opcionais (Enter para pular)
- Keyboard navigation completa (Tab, Enter, Ctrl+C)
- Fallback para modo não-interativo (CI/CD)

**Rationale**:
- **Acessibilidade**: Keyboard-only, screen reader friendly
- **Guiado**: Perguntas claras com exemplos
- **Progressivo**: P0 → P1 → P2 revelado incrementalmente
- **Flexible**: `--non-interactive` para scripts

**Consequences**:
- ✅ **Positive**:
  - Iniciantes podem criar objetivo.yaml sem editar arquivo
  - Perguntas contextuais (exemplo diferente por domínio)
  - Validação inline (erro imediato se campo vazio)
  - Output é arquivo editável (não lock-in no wizard)
- ⚠️ **Negative**:
  - Implementação mais complexa (input handling, validação)
  - Precisa testar em múltiplos terminais (zsh, bash, fish)
  - Dependência opcional Rich (ou fallback print() feio)

**Alternatives Considered**:
1. **GUI (tkinter/Qt)**: Rejeitado — fora de escopo CLI, plataforma-specific
2. **Web UI (localhost)**: Rejeitado — overhead desnecessário
3. **Copilot-only (zero wizard)**: Rejeitado — não atende iniciantes

**Related Decisions**: ADR-002 (Progressive Disclosure)

---

### ADR-005: Parser com Zero Dependências Obrigatórias

**Status**: ✅ Accepted
**Date**: 2026-04-27
**Context**: Template deve funcionar em ambientes restritos (air-gapped, CI/CD minimalista). Dependências externas aumentam complexidade, tamanho, e risco de supply chain attacks.

**Decision**: Implementar parser usando:
- **YAML frontmatter**: PyYAML (já instalado no template)
- **Markdown sections**: Regex simples para extrair seções `## 1️⃣`, `## 2️⃣`, etc
- **Fallback opcional**: mistune se disponível (parse mais robusto)

**Rationale**:
- **Minimalismo**: Stdlib Python suficiente para 90% dos casos
- **Segurança**: Menos dependências = menor superfície de ataque
- **Portabilidade**: Funciona em qualquer ambiente Python 3.11+
- **Performance**: Regex rápido para estrutura simples

**Consequences**:
- ✅ **Positive**:
  - Zero instalação extra (PyYAML já presente)
  - Parser rápido (<100ms)
  - Código simples, fácil de debugar
  - Funciona offline
- ⚠️ **Negative**:
  - Regex pode falhar em edge cases (Markdown nested, code blocks)
  - Menos robusto que parser Markdown completo (mistune)
  - Precisa testar edge cases manualmente

**Alternatives Considered**:
1. **mistune obrigatório**: Rejeitado — adiciona dependência
2. **markdown-it-py**: Rejeitado — mais pesado que mistune
3. **CommonMark**: Rejeitado — overkill para estrutura simples

**Mitigations**:
- Validação extensiva (15+ testes edge cases)
- Documentação clara sobre limitações
- Suporte opcional mistune para casos complexos
- Error messages sugerem instalar mistune se parsing falhar

**Related Decisions**: ADR-001 (formato Markdown)

---

### ADR-006: Migração Automática v1.0 → v2.0

**Status**: ✅ Accepted
**Date**: 2026-04-27
**Context**: Projetos existentes usam v1.0 (YAML puro). Precisa migração para v2.0 sem perda de informação. Manual seria tedioso e propenso a erro.

**Decision**: Implementar `scaffold.py objetivo-migrate` que:
- Detecta v1.0 (ausência de frontmatter `version: "2.0"`)
- Mapeia campos v1.0 → seções v2.0:
  - `prompt.content.description` → seções 1️⃣ + 2️⃣
  - `specification.project_name` → YAML frontmatter `project.name`
  - `rules` → seção 5️⃣ Regras de Negócio
  - `out-scope` → seção 3️⃣ Escopo (Excluído ❌)
- Gera `objetivo.yaml.v2` (preview)
- Pede confirmação antes de sobrescrever `objetivo.yaml`

**Rationale**:
- **Preservação**: 100% campos v1.0 migrados
- **Segurança**: Preview + confirmação antes de sobrescrever
- **Automatização**: Migra em <5 min (vs 30-60 min manual)
- **Adoção**: Remove fricção de upgrade v1.0 → v2.0

**Consequences**:
- ✅ **Positive**:
  - Adoção v2.0 facilitada (zero barreira)
  - Zero perda de dados
  - Side-by-side preview (v1.0 vs v2.0)
  - Pode reverter (mantém objetivo.yaml.v1 backup)
- ⚠️ **Negative**:
  - Parser precisa suportar ambos formatos
  - Mapeamento pode não ser perfeito (requer revisão manual)
  - Manutenção de 2 parsers (v1.0 + v2.0) temporariamente

**Alternatives Considered**:
1. **Migração manual**: Rejeitado — propenso a erro, 30-60 min/projeto
2. **Deprecar v1.0 imediatamente**: Rejeitado — quebra projetos existentes
3. **Suportar ambos formatos permanentemente**: Rejeitado — complexidade longo prazo

**Migration Timeline**:
- **Mês 1-3**: Ambos v1.0 e v2.0 suportados
- **Mês 4-6**: Warning deprecation v1.0, auto-suggest migrate
- **Mês 7+**: v1.0 deprecated (ainda funciona), v2.0 default

**Related Decisions**: ADR-001 (formato v2.0)

---

## Implementation Phases

### Fase 1: Validação de Formato (2 dias) — C

**Goal**: Validar formato v2.0 em cenários diversos ANTES de implementar parser.

**Why First**: Testar design em projetos reais pode revelar edge cases, seções faltando, exemplos confusos.

**Tasks**:
- ✅ Converter 3 projetos template para v2.0:
  - `python-fastapi` (backend API simples)
  - `k8s-helm` (infraestrutura declarativa)
  - `terraform-aws` (cloud provisioning)
- ✅ Documentar edge cases encontrados
- ✅ Refinar estrutura de seções se necessário
- ✅ Validar com 2-3 usuários teste (iniciante + intermediário)

**Deliverables**:
- `poc/objetivo-v2-python-fastapi.md` (~300 linhas)
- `poc/objetivo-v2-k8s-helm.md` (~280 linhas)
- `poc/objetivo-v2-terraform-aws.md` (~320 linhas)
- `docs/debates/VALIDACAO-FASE1-EDGE-CASES.md` (findings)

**Success Criteria**:
- 3/3 projetos convertidos sem ambiguidade
- <5% campos ambíguos ou confusos
- Feedback positivo de 2+ usuários teste

---

### Fase 2: Parser & Validador (1 semana) — B

**Goal**: Implementar parser robusto e validador com mensagens claras.

**Why Now**: Formato validado em 4 projetos (Chatwoot + 3 novos), edge cases documentados.

**Tasks**:
- ✅ Implementar `scripts/lib/objetivo_parser.py`:
  - `parse_objetivo_v2(filepath)` → dict estruturado
  - `validate_objetivo_v2(parsed_data)` → lista de erros
  - `generate_spec_yaml(parsed_data, output_path)` → objetivo-spec.yaml
  - `migrate_v1_to_v2(filepath_v1, filepath_v2)` → conversão automática
- ✅ Integrar com `scaffold.py`:
  - `scaffold.py objetivo-validate`
  - `scaffold.py objetivo-generate`
  - `scaffold.py objetivo-migrate`
- ✅ Testes unitários (pytest):
  - Test parse YAML frontmatter
  - Test parse Markdown sections (P0/P1/P2)
  - Test validation (campos obrigatórios, sintaxe)
  - Test generation (spec.yaml schema compliant)
  - Test migration (v1.0 → v2.0, 100% campos)
  - Test edge cases (seções duplicadas, fora de ordem, markdown nested)

**Deliverables**:
- `scripts/lib/objetivo_parser.py` (~500 linhas)
- `scripts/lib/objetivo_validator.py` (~300 linhas)
- `scripts/lib/objetivo_migrator.py` (~200 linhas)
- `tests/test_objetivo_parser.py` (~400 linhas, 15+ testes)
- Integração em `scripts/scaffold.py` (+150 linhas)

**Success Criteria**:
- Parse <100ms, validate <50ms, generate <200ms
- 15/15 testes passando (100%)
- Zero dependências externas obrigatórias
- Mensagens de erro com linha exata + exemplo

---

### Fase 3: Wizard Interativo (3-4 dias) — D

**Goal**: Wizard acessível para iniciantes criarem objetivo.yaml sem editar arquivo.

**Why Last**: Parser pronto facilita geração automática e validação inline.

**Tasks**:
- ✅ Implementar `scripts/lib/objetivo_wizard.py`:
  - `run_wizard(domain)` → dict com respostas
  - `ask_question(prompt, examples, required)` → string
  - `render_template(answers, domain)` → objetivo.yaml content
- ✅ Integrar com `scaffold.py`:
  - `scaffold.py objetivo-init --interactive`
  - `scaffold.py objetivo-init --non-interactive --from-file answers.json` (CI/CD)
- ✅ Keyboard navigation:
  - Tab/Shift+Tab entre campos
  - Enter para confirmar
  - Ctrl+C para cancelar (salva draft)
  - Ctrl+Z para voltar pergunta anterior
- ✅ Testes E2E:
  - Test wizard P0 only
  - Test wizard P0+P1
  - Test wizard P0+P1+P2
  - Test non-interactive mode
  - Test keyboard navigation
  - Test fallback print() (sem Rich)

**Deliverables**:
- `scripts/lib/objetivo_wizard.py` (~400 linhas)
- Integração em `scripts/scaffold.py` (+100 linhas)
- `tests/test_objetivo_wizard.py` (~250 linhas, 10+ testes)
- `docs/guides/OBJETIVO_WIZARD_GUIDE.md` (~150 linhas)

**Success Criteria**:
- Wizard P0 em <5 min (medido)
- Keyboard navigation completa (testado)
- Fallback graceful se Rich não disponível
- Output validável por `objetivo-validate`

---

## File Structure

```
specs/066-objetivo-yaml-v2/
├── spec.md                          # Esta spec
├── plan.md                          # Este plano
├── tasks.md                         # Task list detalhada
└── research/
    └── formato-debate.md            # Link para debate completo

scripts/lib/
├── objetivo_parser.py               # Parser v2.0 (Fase 2)
├── objetivo_validator.py            # Validador (Fase 2)
├── objetivo_migrator.py             # Migrador v1.0→v2.0 (Fase 2)
└── objetivo_wizard.py               # Wizard interativo (Fase 3)

scripts/scaffold.py                  # Extensão com novos comandos

tests/
├── test_objetivo_parser.py          # Testes parser (Fase 2)
├── test_objetivo_validator.py       # Testes validador (Fase 2)
├── test_objetivo_migrator.py        # Testes migrador (Fase 2)
└── test_objetivo_wizard.py          # Testes wizard (Fase 3)

poc/
├── objetivo-v2-example-chatwoot.md  # Já criado
├── objetivo-v2-python-fastapi.md    # Fase 1
├── objetivo-v2-k8s-helm.md          # Fase 1
└── objetivo-v2-terraform-aws.md     # Fase 1

docs/
├── debates/
│   ├── DEBATE-OBJETIVO-YAML-HUMAN-READABLE-COMPLETO.md  # Já criado
│   ├── COMPARACAO-OBJETIVO-V1-V2.md                     # Já criado
│   ├── RESUMO-REDESIGN-OBJETIVO-YAML.md                 # Já criado
│   └── VALIDACAO-FASE1-EDGE-CASES.md                    # Fase 1
└── guides/
    └── OBJETIVO_WIZARD_GUIDE.md                          # Fase 3
```

---

## Testing Strategy

### Unit Tests (Fase 2)

**Parser** (`test_objetivo_parser.py`):
- Parse valid objetivo.yaml v2.0 (frontmatter + sections)
- Parse edge cases (nested markdown, code blocks, tables)
- Parse invalid YAML frontmatter → error message
- Parse missing sections P0 → validation error
- Parse sections out of order → warning

**Validator** (`test_objetivo_validator.py`):
- Validate P0 fields present
- Validate P0 fields non-empty
- Validate YAML frontmatter schema
- Validate sections numbered correctly (1️⃣, 2️⃣, 3️⃣...)
- Validate no duplicate sections

**Migrator** (`test_objetivo_migrator.py`):
- Migrate v1.0 → v2.0 (all fields)
- Migrate complex v1.0 (nested rules, multiple personas)
- Migrate edge cases (missing fields, empty values)
- Preview generation (don't overwrite original)

**Wizard** (`test_objetivo_wizard.py`):
- Wizard P0 only → valid objetivo.yaml
- Wizard P0+P1 → valid objetivo.yaml
- Wizard non-interactive mode
- Wizard keyboard navigation simulation

### Integration Tests (Fase 2)

**scaffold.py commands**:
- `scaffold.py objetivo-validate` on valid file → success
- `scaffold.py objetivo-validate` on invalid file → error with line
- `scaffold.py objetivo-generate` → spec.yaml created
- `scaffold.py objetivo-migrate` → v2 created, original preserved

### E2E Tests (Fase 3)

**Real world scenarios**:
- Iniciante cria primeiro objetivo.yaml via wizard (<15 min)
- Intermediário migra projeto v1.0 → v2.0 (<5 min)
- Avançado edita objetivo.yaml manual + valida + gera spec.yaml (<3 min)

---

## Rollout Plan

### Week 1: Fase 1 (Validação)

**Day 1-2**:
- Converter python-fastapi → v2.0
- Converter k8s-helm → v2.0
- Converter terraform-aws → v2.0
- Documentar edge cases

**Checkpoint**: 3 projetos convertidos, edge cases documentados

---

### Week 2: Fase 2 (Parser) — Parte 1

**Day 3-4**:
- Implementar `objetivo_parser.py` (parse frontmatter + sections)
- Testes unitários parser (8 testes)

**Day 5**:
- Implementar `objetivo_validator.py` (validate P0/P1/P2)
- Testes unitários validator (5 testes)

**Checkpoint**: Parser + Validator completos, 13/13 testes passando

---

### Week 3: Fase 2 (Parser) — Parte 2

**Day 6-7**:
- Implementar `objetivo_migrator.py` (v1.0 → v2.0)
- Testes unitários migrator (4 testes)

**Day 8**:
- Integrar com `scaffold.py` (comandos validate/generate/migrate)
- Testes integração (4 testes)

**Checkpoint**: Migrador completo, comandos scaffold.py funcionando, 21/21 testes passando

---

### Week 4: Fase 3 (Wizard) — Parte 1

**Day 9-10**:
- Implementar `objetivo_wizard.py` (perguntas P0/P1/P2)
- Keyboard navigation

**Day 11**:
- Integrar com `scaffold.py objetivo-init --interactive`
- Testes E2E wizard (6 testes)

**Checkpoint**: Wizard completo, 27/27 testes passando

---

### Week 5: Fase 3 (Wizard) — Parte 2 + Docs

**Day 12**:
- Documentação `OBJETIVO_WIZARD_GUIDE.md`
- Refinamento UX (mensagens, exemplos)

**Checkpoint**: Feature completa, documentada, testada

---

## Risk Mitigation

| Risco | Mitigação | Owner |
|-------|-----------|-------|
| Parser falha em edge cases complexos | Suite 15+ testes edge cases, validação em 4 projetos reais | Fase 2 |
| Usuários não migram v1.0 | Wizard automático, warning deprecation após 3 meses | Fase 2 |
| Wizard difícil de usar | Testes com iniciantes, keyboard navigation, fallback print() | Fase 3 |
| Formato muda no futuro | Versionamento explícito (`version: "2.0"`), parser detecta versão | Fase 2 |

---

## Success Metrics (Post-Launch)

**Quantitativo** (após 4 semanas):
- ✅ >80% novos projetos usam v2.0
- ✅ <15 min tempo médio preenchimento (iniciantes)
- ✅ <5% taxa de erro em campos P0
- ✅ >90% validações passam first try

**Qualitativo**:
- ✅ NPS >70 (satisfação formato v2.0)
- ✅ <3 issues GitHub sobre formato confuso
- ✅ >5 contribuições externas (templates de exemplo)

---

## Next Steps

1. ✅ **Criar task list** (`tasks.md`) baseada neste plano
2. ⏳ **Iniciar Fase 1** (Day 1-2): Converter 3 projetos para v2.0
3. ⏳ **Code review** após cada fase (gate de qualidade)
4. ⏳ **User testing** após Fase 3 (2-3 usuários iniciantes + intermediários)

Ver [tasks.md](./tasks.md) para task list detalhada.
