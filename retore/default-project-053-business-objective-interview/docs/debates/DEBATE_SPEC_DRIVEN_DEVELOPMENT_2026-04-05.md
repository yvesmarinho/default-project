# Debate: Spec Driven Development e as 4 Camadas de Desenvolvimento

**Data**: 2026-04-05
**Contexto**: Evolução do SpecKit para suportar Spec Driven Development
**Referência**: [Spec Driven Development é o Caminho?](https://www.youtube.com/watch?v=DJE0LL0CuUQ)
**Status**: ✅ **VALIDADO** (alinhamento com mercado: 78% — Score BOM)
**Análise de mercado**: [ANALISE_4_CAMADAS_VS_MERCADO_2026-04-05.md](ANALISE_4_CAMADAS_VS_MERCADO_2026-04-05.md)
**Participantes**: template-architect, speckit.specify, speckit.plan, speckit.constitution

---

## 📋 Sumário Executivo

Este debate analisa a adoção de **Spec Driven Development (SDD)** e as **4 Camadas de Desenvolvimento** (Negócio → Produto → Arquitetura → Implementação) no contexto do SpecKit, propondo evoluções nos templates e workflows para suportar especificação rigorosa antes da implementação.

**Objetivos**:
1. Definir como as 4 camadas se integram ao SpecKit atual
2. Propor modelo `objetivo.yaml` como contrato inicial
3. Definir integração de ADRs (Architecture Decision Records)
4. Atualizar fluxo SpecKit para suportar camadas de especificação
5. Propor sistema de captura de conversas (CHAT-*.md) como memória

---

## 🎯 Contexto: As 4 Camadas de Desenvolvimento

### Camada 1️⃣: Negócio
- **O quê**: Problema de negócio a resolver
- **Por quê**: Valor entregue, ROI, objetivos estratégicos
- **Artefato**: Objetivo de negócio, casos de uso de alto nível

### Camada 2️⃣: Produto
- **O quê**: Requisitos funcionais, user stories, jornadas de usuário
- **Por quê**: Como os usuários vão interagir, que valor percebem
- **Artefato**: `spec.md` (user scenarios, functional requirements, acceptance criteria)

### Camada 3️⃣: Arquitetura
- **O quê**: Decisões técnicas estruturais (ADRs)
- **Por quê**: Trade-offs, constraints, escolhas de tecnologia
- **Artefato**: `plan.md` (architecture decisions, component design, implementation strategy)

### Camada 4️⃣: Implementação
- **O quê**: Código executável, testes
- **Por quê**: Materialização das decisões anteriores
- **Artefato**: `tasks.md` → código → testes

---

## 🔍 Análise: SpecKit Atual vs 4 Camadas

### Estado Atual do SpecKit

**Templates existentes**:
1. `constitution-template.md`: Princípios do projeto (meta-camada)
2. `spec-template.md`: User scenarios + requirements (Camada 2: Produto)
3. `plan-template.md`: Architecture + implementation strategy (Camada 3: Arquitetura)
4. `tasks-template.md`: Tarefas implementáveis (Camada 4: Implementação)
5. `checklist-template.md`: Quality gates

**O que falta**:
- ✅ **Camada 1 (Negócio)**: Não existe artefato estruturado
- ⚠️ **Camada 2 (Produto)**: Existe (`spec.md`), mas sem priorização P1/P2/P3 sistemática
- ⚠️ **Camada 3 (Arquitetura)**: Existe (`plan.md`), mas sem ADRs formais
- ✅ **Camada 4 (Implementação)**: Existe (`tasks.md`)

---

## 💡 Proposta 1: Introduzir `objetivo.yaml` (Camada 1: Negócio)

### Objetivo

Criar artefato estruturado que captura o **contexto de negócio** antes de qualquer especificação técnica. Este arquivo serve como:
- Entrada para debate entre agentes
- Base para constitution inicial
- Contexto para geração de `spec.md`

### Estrutura Proposta: `objetivo.yaml`

```yaml
# .specify/specs/<feature>/objetivo.yaml
---
feature:
  id: "IMP-XX"
  name: "Nome da Feature"
  branch: "XXX-feature-name"
  created: "YYYY-MM-DD"

negocio:
  problema:
    descricao: "Qual problema de negócio estamos resolvendo?"
    impacto_atual: "O que acontece se não resolvermos?"
    stakeholders:
      - "Cliente/Usuário tipo 1"
      - "Cliente/Usuário tipo 2"

  valor:
    objetivos_estrategicos:
      - "Aumentar eficiência operacional em X%"
      - "Reduzir tempo de resposta de Y para Z"
    metricas_sucesso:
      - metric: "Taxa de adoção"
        target: "80% em 3 meses"
      - metric: "NPS"
        target: ">= 8"

  contexto:
    restricoes_negocio:
      - "Orçamento limitado: R$ X mil"
      - "Deadline regulatório: YYYY-MM-DD"
    premissas:
      - "Usuários têm acesso à internet"
      - "Integração com sistema legado X disponível"

produto:
  visao_alto_nivel: "Em uma frase, o que entregamos?"
  personas:
    - name: "DevOps Engineer"
      needs: "Automatizar deploys sem configuração manual"
      pain_points: "Configuração atual é propensa a erros"

  jornadas_criticas:
    - journey: "Deploy de nova feature"
      priority: "P1"
      value: "Reduz tempo de 2h para 15min"
    - journey: "Rollback em caso de falha"
      priority: "P1"
      value: "Reduz downtime de 30min para 2min"

decisoes_iniciais:
  - id: "D-01"
    question: "Construir ou comprar solução?"
    decision: "Construir (justificativa: requisitos específicos não atendidos por SaaS)"
  - id: "D-02"
    question: "Cloud provider?"
    decision: "AWS (justificativa: equipe tem expertise, integração existente)"

perguntas_abertas:
  - question: "Como lidar com multi-tenancy?"
    impact: "Alto - afeta arquitetura de dados"
  - question: "Suporte a quais idiomas?"
    impact: "Médio - afeta UI e validações"

metadata:
  owner: "Nome do Product Owner"
  tech_lead: "Nome do Tech Lead"
  team: "Nome do Time"
  tags: ["automation", "devops", "deployment"]
```

### Workflow com `objetivo.yaml`

```
1. Usuário cria objetivo.yaml (ou agent faz entrevista e gera)
2. Agent speckit.constitution analisa objetivo.yaml → gera/atualiza constitution.md
3. Agent speckit.clarify identifica perguntas_abertas → entrevista usuário → atualiza objetivo.yaml
4. Agent speckit.specify usa objetivo.yaml + contexto → gera spec.md (Camada 2)
5. Agent speckit.plan usa spec.md + decisoes_iniciais → gera plan.md + ADRs (Camada 3)
6. Agent speckit.tasks usa plan.md → gera tasks.md (Camada 4)
```

---

## 💡 Proposta 2: Integrar ADRs no `plan.md` (Camada 3: Arquitetura)

### Contexto

**Architecture Decision Records (ADRs)** capturam *por que* escolhemos determinada arquitetura, não apenas *o que* escolhemos. São essenciais para:
- Onboarding de novos membros
- Revisão de decisões passadas
- Evitar re-debates de decisões já tomadas

### Estrutura Proposta: Seção ADRs em `plan.md`

```markdown
## Architecture Decision Records

### ADR-001: Escolha de SQLite FTS5 para Busca de Sessões

**Status**: ✅ Accepted
**Date**: 2026-04-05
**Context**: Sistema de busca em histórico de sessões (IMP-51)

**Decision**: Usar SQLite FTS5 em vez de embedding-based search (sentence-transformers)

**Rationale**:
- **Pragmatismo**: Zero dependências externas pesadas (sentence-transformers = 500MB+ de modelos)
- **Performance**: FTS5 atende requisitos (<0.1s para queries complexas)
- **Simplicidade**: Tokenização Porter + Unicode61 suficiente para português/inglês
- **Custo**: SQLite FTS5 é built-in, sem custo de infraestrutura

**Consequences**:
- ✅ Positivas:
  - Indexação rápida (~1s para 100 blocos)
  - Bundle pequeno (~100KB para 100 blocos)
  - Fácil debug (SQL queries legíveis)
- ⚠️ Negativas:
  - Busca semântica limitada (keyword-based, não similarity-based)
  - Queries com hífen requerem aspas (ex: `"IMP-50"`)

**Alternatives Considered**:
1. **sentence-transformers + FAISS**: Descartado por overhead (500MB+ modelos)
2. **Elasticsearch**: Descartado por complexidade de infra
3. **PostgreSQL pg_trgm**: Descartado por não ser embutido

**Related Decisions**: None
**Supersedes**: None
**Superseded by**: None (pode ser revisitado se embedding search for necessário)

---

### ADR-002: [Próxima decisão arquitetural]

[Template igual...]
```

### Atualização do `plan-template.md`

Adicionar seção obrigatória:

```markdown
## Architecture Decision Records *(mandatory for architectural features)*

<!--
  DOCUMENT KEY ARCHITECTURAL DECISIONS using the ADR format:
  - Status (Proposed, Accepted, Deprecated, Superseded)
  - Context (why this decision is needed)
  - Decision (what we chose)
  - Rationale (why we chose it - trade-offs, constraints)
  - Consequences (positive/negative impacts)
  - Alternatives Considered (what we rejected and why)
-->

### ADR-[NUMBER]: [Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Date**: [YYYY-MM-DD]
**Context**: [What problem/question triggered this decision?]

**Decision**: [What did we decide?]

**Rationale**: [Why did we decide this? What trade-offs?]

**Consequences**:
- ✅ Positive: [List positive impacts]
- ⚠️ Negative: [List negative impacts/limitations]

**Alternatives Considered**:
1. **[Option A]**: [Why rejected]
2. **[Option B]**: [Why rejected]

**Related Decisions**: [ADR-XXX, ADR-YYY]
**Supersedes**: [ADR-XXX if applicable]
**Superseded by**: [ADR-XXX if applicable]
```

---

## 💡 Proposta 3: Sistema de Captura de Conversas (CHAT-*.md)

### Contexto

Conversas com o Copilot contêm decisões, clarificações e contexto valioso que se perde se não forem capturadas. Precisamos de:
- Registro automático de conversas importantes
- Integração com sistema de memória
- Vinculação a features/sessions

### Estrutura Proposta: `CHAT-YYYYMMDD-HHMMSS.md`

```markdown
# Chat Session: [Título/Contexto]

**Date**: YYYY-MM-DD HH:MM:SS
**Feature**: [IMP-XX ou session date]
**Participants**: User + GitHub Copilot
**Tags**: [#clarification, #decision, #architecture, etc.]

---

## Context

[Por que essa conversa aconteceu? Qual pergunta/problema estava sendo resolvido?]

---

## Conversation

### User (YYYY-MM-DD HH:MM)
> [Pergunta ou comando do usuário]

### Copilot (YYYY-MM-DD HH:MM)
> [Resposta do Copilot]
>
> [Pode incluir código, explicações, propostas]

### User (YYYY-MM-DD HH:MM)
> [Continuação...]

[...]

---

## Decisions Made

- ✅ **[D-XX]**: [Decisão tomada durante a conversa]
- ⚠️ **[Q-XX]**: [Pergunta que ficou em aberto]

---

## Artifacts Generated

- `path/to/file.md` (created/modified)
- `path/to/code.py` (created/modified)

---

## Next Steps

- [ ] [Ação pendente 1]
- [ ] [Ação pendente 2]

---

**Related**:
- Feature: [link to spec.md]
- Session: [link to DAILY_ACTIVITIES_*.md]
- Previous chat: [link to CHAT-*.md if continuation]
```

### Estratégias de Captura

**Opção 1: Manual (current state)**
- Usuário cria arquivo ao final de conversas importantes
- Pro: Controle total, sem overhead
- Con: Pode ser esquecido

**Opção 2: Engram Integration**
- Usar Engram para captura automática
- Pro: Zero esforço do usuário
- Con: Requer configuração, pode capturar conversas triviais

**Opção 3: Copilot Prompt Enhancement**
- Adicionar instrução em `.github/copilot-instructions.md`:
  ```markdown
  ## Chat Session Capture

  For significant conversations (>5 interactions OR involving architectural decisions):
  1. At conversation end, offer to create CHAT-YYYYMMDD-HHMMSS.md
  2. Summarize: context, key decisions, artifacts, next steps
  3. Save to: docs/SESSIONS/YYYY-MM-DD/CHAT-*.md (session-scoped)
               OR .specify/specs/<feature>/CHAT-*.md (feature-scoped)
  ```

**Recomendação inicial**: Opção 3 (Copilot Prompt) + manual trigger
- Adicionar comando ao `manage.py`: `python scripts/manage.py chat capture [--feature IMP-XX]`
- Copilot oferece criar arquivo, usuário confirma ou executa manualmente

---

## 💡 Proposta 4: Atualização do Fluxo SpecKit

### Fluxo Atual

```
speckit.specify → spec.md
speckit.plan → plan.md
speckit.tasks → tasks.md
speckit.implement → código
```

### Fluxo Proposto (com 4 Camadas)

```
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 1: NEGÓCIO                                           │
├─────────────────────────────────────────────────────────────┤
│ Entrada: Descrição de alto nível do usuário                │
│ Agent: speckit.clarify (entrevista) + speckit.constitution │
│ Artefato: objetivo.yaml + constitution.md                   │
│ Validação: Usuario aprova objetivo e princípios            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 2: PRODUTO                                           │
├─────────────────────────────────────────────────────────────┤
│ Entrada: objetivo.yaml                                       │
│ Agent: speckit.specify                                       │
│ Artefato: spec.md (user scenarios P1/P2/P3, requirements)  │
│ Validação: speckit.analyze (consistency check)             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 3: ARQUITETURA                                       │
├─────────────────────────────────────────────────────────────┤
│ Entrada: spec.md + objetivo.yaml decisoes_iniciais         │
│ Agent: speckit.plan                                         │
│ Artefato: plan.md (architecture + ADRs)                     │
│ Validação: speckit.analyze (ADR completeness)              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ CAMADA 4: IMPLEMENTAÇÃO                                     │
├─────────────────────────────────────────────────────────────┤
│ Entrada: plan.md                                            │
│ Agent: speckit.tasks → speckit.implement                    │
│ Artefato: tasks.md → código → testes                        │
│ Validação: speckit.checklist (quality gates)               │
└─────────────────────────────────────────────────────────────┘
```

### Novo Agent: `speckit.clarify`

**Propósito**: Camada 1 - Elicitar requisitos de negócio

**Workflow**:
1. Recebe descrição de alto nível do usuário
2. Gera até 5 perguntas focadas para preencher `objetivo.yaml`:
   - Problema de negócio e stakeholders
   - Valor e métricas de sucesso
   - Constraints e premissas
   - Personas e jornadas críticas
   - Decisões iniciais conhecidas
3. Processa respostas → gera `objetivo.yaml`
4. Identifica perguntas em aberto (seção `perguntas_abertas:`)

**Agent file**: `.github/agents/speckit.clarify.agent.md`

---

## 💡 Proposta 5: Templates Atualizados

### 5.1. Novo Template: `objetivo-template.yaml`

```yaml
# .specify/templates/objetivo-template.yaml
---
feature:
  id: "[FEATURE_ID]"
  name: "[FEATURE_NAME]"
  branch: "[BRANCH_NAME]"
  created: "[CREATION_DATE]"

negocio:
  problema:
    descricao: "[BUSINESS_PROBLEM_DESCRIPTION]"
    impacto_atual: "[CURRENT_IMPACT]"
    stakeholders:
      - "[STAKEHOLDER_1]"
      - "[STAKEHOLDER_2]"

  valor:
    objetivos_estrategicos:
      - "[STRATEGIC_OBJECTIVE_1]"
      - "[STRATEGIC_OBJECTIVE_2]"
    metricas_sucesso:
      - metric: "[METRIC_NAME]"
        target: "[TARGET_VALUE]"

  contexto:
    restricoes_negocio:
      - "[CONSTRAINT_1]"
    premissas:
      - "[ASSUMPTION_1]"

produto:
  visao_alto_nivel: "[HIGH_LEVEL_VISION]"
  personas:
    - name: "[PERSONA_NAME]"
      needs: "[USER_NEEDS]"
      pain_points: "[PAIN_POINTS]"

  jornadas_criticas:
    - journey: "[USER_JOURNEY]"
      priority: "[P1|P2|P3]"
      value: "[VALUE_PROPOSITION]"

decisoes_iniciais:
  - id: "D-01"
    question: "[DECISION_QUESTION]"
    decision: "[DECISION_MADE]"

perguntas_abertas:
  - question: "[OPEN_QUESTION]"
    impact: "[Alto|Médio|Baixo]"

metadata:
  owner: "[PRODUCT_OWNER]"
  tech_lead: "[TECH_LEAD]"
  team: "[TEAM_NAME]"
  tags: ["[TAG1]", "[TAG2]"]
```

### 5.2. Atualizar `spec-template.md`

Adicionar referência a `objetivo.yaml` no cabeçalho:

```markdown
# Feature Specification: [FEATURE NAME]

**Feature ID**: [FEATURE_ID]
**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Business Objective**: See [objetivo.yaml](./objetivo.yaml)

---

## Business Context (from objetivo.yaml)

**Problem**: [Pulled from objetivo.yaml → negocio.problema.descricao]
**Value**: [Pulled from objetivo.yaml → negocio.valor.objetivos_estrategicos]
**Success Metrics**: [Pulled from objetivo.yaml → negocio.valor.metricas_sucesso]

---

[Rest of spec-template.md...]
```

### 5.3. Atualizar `plan-template.md`

Adicionar seção ADRs obrigatória:

```markdown
## Architecture Decision Records *(mandatory)*

<!--
  IMPORTANT: Document ALL significant architectural decisions using ADR format.
  Reference decisions made in objetivo.yaml → decisoes_iniciais.
-->

### ADR-001: [First Architectural Decision]

**Status**: [Proposed | Accepted]
**Date**: [YYYY-MM-DD]
**Context**: [What triggered this decision?]

**Decision**: [What we chose]

**Rationale**:
- [Why this choice? What trade-offs?]
- [Reference to objetivo.yaml decisoes_iniciais if applicable]

**Consequences**:
- ✅ Positive: [Benefits]
- ⚠️ Negative: [Limitations/costs]

**Alternatives Considered**:
1. **[Option A]**: [Why rejected]

**Related**: [ADR-XXX, spec.md section Y, tasks.md task Z]

---

[Additional ADRs as needed...]
```

---

## 📊 Proposta 6: Governance e Quality Gates

### Quality Gates por Camada

**Camada 1 (Negócio) → Camada 2 (Produto):**
- ✅ `objetivo.yaml` completo (sem `[BRACKET]` tokens)
- ✅ Pelo menos 1 métrica de sucesso definida
- ✅ Pelo menos 1 persona identificada
- ✅ Decisões iniciais documentadas (ou explicitamente marcadas como "não aplicável")

**Camada 2 (Produto) → Camada 3 (Arquitetura):**
- ✅ `spec.md` com pelo menos 1 user story P1
- ✅ Todos user stories têm acceptance criteria (Given/When/Then)
- ✅ Functional requirements numerados (FR-001, FR-002, ...)
- ✅ `speckit.analyze` passou sem erros críticos

**Camada 3 (Arquitetura) → Camada 4 (Implementação):**
- ✅ `plan.md` completo com pelo menos 1 ADR
- ✅ Todos ADRs têm "Alternatives Considered"
- ✅ Component design definido
- ✅ Implementation strategy clara (steps, order, dependencies)

**Camada 4 (Implementação) → Done:**
- ✅ Todos tasks em `tasks.md` marcados ✅
- ✅ Testes passando (coverage >= threshold definido em constitution)
- ✅ `speckit.checklist` aprovado
- ✅ ADRs atualizados se decisões mudaram durante implementação

### Agent de Validação: `speckit.validate`

**Propósito**: Verificar quality gates antes de avançar camadas

**Workflow**:
```bash
# Valida se objetivo.yaml está pronto para gerar spec.md
python scripts/manage.py speckit validate --layer business

# Valida se spec.md está pronto para gerar plan.md
python scripts/manage.py speckit validate --layer product

# Valida se plan.md está pronto para gerar tasks.md
python scripts/manage.py speckit validate --layer architecture

# Valida se implementação está pronta (done)
python scripts/manage.py speckit validate --layer implementation
```

---

## 🔄 Integração com `manage.py`

### Novos Comandos Propostos

```bash
# Camada 1: Negócio
python scripts/manage.py speckit clarify [FEATURE_NAME]
# → Entrevista interativa, gera objetivo.yaml

python scripts/manage.py speckit constitution --from-objetivo
# → Lê objetivo.yaml, atualiza constitution.md

# Camada 2: Produto
python scripts/manage.py speckit specify [FEATURE_NAME] --from-objetivo
# → Lê objetivo.yaml, gera spec.md

# Camada 3: Arquitetura
python scripts/manage.py speckit plan [FEATURE_NAME]
# → Lê spec.md + objetivo.yaml, gera plan.md + ADRs

python scripts/manage.py speckit adr add --title "Decisão X" --feature [FEATURE_NAME]
# → Adiciona ADR ao plan.md existente

# Camada 4: Implementação
python scripts/manage.py speckit tasks [FEATURE_NAME]
# → Lê plan.md, gera tasks.md

# Validação
python scripts/manage.py speckit validate --layer [business|product|architecture|implementation]

# Chat capture
python scripts/manage.py chat capture --feature [FEATURE_NAME]
# → Cria CHAT-YYYYMMDD-HHMMSS.md a partir da conversa atual
```

---

## 📝 Decisões e Recomendações

### Decisões Propostas

**D-01: Adotar modelo objetivo.yaml para Camada 1 (Negócio)**
- ✅ **Aprovado**: Fundamental para capturar contexto de negócio antes de especificação técnica
- Implementar: `.specify/templates/objetivo-template.yaml`
- Agent responsável: `speckit.clarify` (novo)

**D-02: Integrar ADRs formalmente no plan.md (Camada 3)**
- ✅ **Aprovado**: ADRs são essenciais para documentar "por quê" de decisões arquiteturais
- Atualizar: `plan-template.md` com seção ADRs obrigatória
- Adicionar comando: `manage.py speckit adr add`

**D-03: Sistema de captura de conversas (CHAT-*.md)**
- 🟡 **Aprovado com ressalvas**: Implementar Opção 3 (Copilot Prompt + manual trigger)
- Fase 1: Adicionar instrução em `.github/copilot-instructions.md`
- Fase 2: Comando `manage.py chat capture`
- Fase 3 (futuro): Integração Engram automática

**D-04: Quality Gates por camada**
- ✅ **Aprovado**: Criar agent `speckit.validate` para verificar gates
- Implementar: Validações progressivas (business → product → architecture → implementation)
- Bloquear avanço se gates não passarem

**D-05: Priorização P1/P2/P3 obrigatória em user stories**
- ✅ **Aprovado**: Atualizar `spec-template.md` para exigir prioridade em cada user story
- Benefício: Delivery incremental, MVP identificável

### Recomendações de Implementação

**Fase 1: Fundação (1-2 semanas)**
1. Criar `objetivo-template.yaml`
2. Criar agent `speckit.clarify`
3. Atualizar `spec-template.md` para referenciar objetivo.yaml
4. Atualizar `plan-template.md` para incluir seção ADRs

**Fase 2: Validação (1 semana)**
1. Criar agent `speckit.validate`
2. Implementar quality gates
3. Adicionar comandos ao `manage.py`

**Fase 3: Captura de Conversas (1 semana)**
1. Atualizar `.github/copilot-instructions.md` com Chat Session Capture
2. Implementar `manage.py chat capture`
3. Criar template `CHAT-template.md`

**Fase 4: Refinamento (ongoing)**
1. Feedback de uso real
2. Ajustes nos templates baseados em experiência
3. Automação adicional

---

## 🎯 Próximos Passos

### Imediatos (esta sessão)

- [ ] Criar issue **[IMP-53]**: Implementar objetivo.yaml e speckit.clarify (Fase 1)
- [ ] Criar issue **[IMP-54]**: Integrar ADRs no plan-template.md (Fase 1)
- [ ] Atualizar `.specify/templates/` com novos templates
- [ ] Atualizar `docs/TODO.md` com IMPs

### Curto Prazo (próxima sessão)

- [ ] Criar agent `.github/agents/speckit.clarify.agent.md`
- [ ] Criar template `.specify/templates/objetivo-template.yaml`
- [ ] Atualizar `spec-template.md` com referência a objetivo.yaml
- [ ] Atualizar `plan-template.md` com seção ADRs

### Médio Prazo (2-3 sessões)

- [ ] Implementar `speckit.validate` agent
- [ ] Adicionar comandos ao `manage.py`
- [ ] Testar fluxo completo em feature real (usar próprio IMP-53 como dogfooding)

---

## 📚 Referências

1. **Spec Driven Development é o Caminho?** (YouTube): https://www.youtube.com/watch?v=DJE0LL0CuUQ
2. **ADR (Architecture Decision Records)**: https://adr.github.io/
3. **SpecKit documentation**: `.specify/` (internal)
4. **Constitution**: `.specify/memory/constitution.md`
5. **Debate anterior**: `docs/debates/DEBATE_INCREMENTAL_DOCUMENTATION_2026-03-29.md`

---

**Status**: 🔵 Debate concluído, aguardando aprovação para implementação
**Data de conclusão**: 2026-04-05
**Próxima ação**: Criar IMPs e iniciar Fase 1
