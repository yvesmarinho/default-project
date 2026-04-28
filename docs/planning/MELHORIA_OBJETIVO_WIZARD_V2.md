# Melhoria: Objetivo Wizard v2.0 — Formato Markdown Híbrido Completo

**Tracking**: Planejamento futuro
**Prioridade**: P1 (Médio prazo)
**Esforço estimado**: 2-3 sprints
**Criado**: 2026-04-28
**Status**: Planejado (não iniciado)

---

## Contexto

Atualmente temos **dois formatos** de objetivo.yaml:

### Formato v1.0 (YAML Puro) — EM USO
- **Arquivo**: `objetivo-init.yaml` (98 linhas)
- **Estrutura**: YAML puro com 13 campos críticos
- **Wizard**: Implementado, funcional
- **Validação**: `scaffold objetivo-validate` ✅
- **Geração**: `scaffold objetivo-generate` ✅
- **Status**: **ESTÁVEL E COMPLETO**

### Formato v2.0 (Markdown Híbrido) — INCOMPLETO
- **Arquivo**: `objetivo.yaml` (335 linhas)
- **Estrutura**: YAML frontmatter + Markdown sections
- **Wizard**: Implementado, mas captura apenas 6/13 campos
- **Validação**: Parcial
- **Geração**: Não implementado
- **Status**: **PROTÓTIPO — 69% DE PERDA DE INFORMAÇÃO**

---

## Problema

O wizard v2.0 atual **não captura campos críticos**:

| Campo | v1.0 (objetivo-init.yaml) | v2.0 wizard | Gap |
|-------|---------------------------|-------------|-----|
| project_name | ✅ | ✅ | OK |
| response (solução técnica) | ✅ | ❌ | **Crítico** |
| docstyle (padrão docs) | ✅ | ❌ | Alto |
| workflow-objetivo | ✅ | ❌ | Médio |
| workflow-specify | ✅ | ❌ | Médio |
| out-scope | ✅ | ❌ | Alto |
| rules (regras negócio) | ✅ | ❌ | **Crítico** |
| folder_structure | ✅ | ❌ | Alto |
| expected_outcome | ✅ | ❌ | **Crítico** |
| infrastructure | ✅ | ❌ | Alto |
| profile (roles) | ✅ | ❌ | **Crítico** |
| features_to_implement | ✅ | Parcial | Médio |
| pending_tasks | ✅ | ❌ | Médio |

**Gap total**: 9/13 campos críticos não capturados (69% de perda)

---

## Solução Proposta: Opção A — Unificar Formatos

### Objetivo

Migrar wizard v2.0 para capturar **todos os campos** do objetivo-init.yaml v1.0, mantendo formato Markdown Híbrido legível.

### Arquitetura

```
objetivo.yaml v3.0 (Markdown Híbrido Completo)
├── YAML Frontmatter (metadados projeto)
│   ├── version: "3.0"
│   ├── project: {name, title, type, domain, language}
│   ├── created_at, created_by
│   ├── generation: {profiles_auto_detect, ...}
│   └── validation: {level, fail_on_warning, ...}
│
├── ## 1️⃣ O que este projeto faz?
│   ├── Descrição (1 frase)
│   ├── Componentes principais
│   └── Stack técnico
│
├── ## 2️⃣ Qual problema resolve? (se update)
│   ├── Problema atual
│   ├── Impacto medido
│   └── Audiência afetada
│
├── ## 3️⃣ Escopo do Projeto
│   ├── ✅ Incluído (features_to_implement)
│   ├── ❌ Excluído (out_of_scope)
│   └── ⚠️ Fora de Escopo
│
├── ## 4️⃣ Solução Técnica (NOVO — do v1.0 response)
│   ├── Tipo de solução (API, CLI, ETL, etc)
│   ├── Padrão de documentação (docstyle)
│   └── Workflows (objetivo → constitution → specify)
│
├── ## 5️⃣ Regras de Negócio (NOVO — do v1.0 rules)
│   ├── Regra #1: Validações
│   ├── Regra #2: Integridade
│   └── Regra #3: Segurança
│
├── ## 6️⃣ Resultados Esperados (NOVO — do v1.0 expected_outcome)
│   ├── Critérios de sucesso mensuráveis
│   ├── KPIs de qualidade
│   └── Acceptance criteria
│
├── ## 7️⃣ Infraestrutura (NOVO — do v1.0 infrastructure)
│   ├── Servidores / containers
│   ├── Bancos de dados
│   └── Dependências externas
│
├── ## 8️⃣ Perfis Necessários (NOVO — do v1.0 profile)
│   ├── Role 1: dba_architect (expert)
│   ├── Role 2: python_developer (senior)
│   └── Role 3: devops_engineer (intermediate)
│
├── ## 9️⃣ Estrutura de Pastas (do v1.0 folder_structure)
│   └── Tree comentado
│
└── ## 🔟 Tarefas Pendentes (NOVO — do v1.0 pending_tasks)
    ├── - [ ] D1: Tarefa com status
    └── - [ ] D2: Outra tarefa
```

---

## Implementação

### Sprint 4.1: Adicionar Campos Críticos ao Wizard

**Tarefas**:
1. Adicionar perguntas ao `_build_questions()`:
   - q4_technical_solution (response, docstyle, workflows)
   - q5_business_rules (regras de validação, integridade)
   - q6_expected_outcome (KPIs, critérios de sucesso)
   - q7_infrastructure (servidores, DBs, containers)
   - q8_profiles (roles necessários com skill level)
   - q9_folder_structure (tree comentado)
   - q10_pending_tasks (tarefas com status)

2. Criar template v3.0 em `poc/objetivo-v3-template-base.md`

3. Atualizar `_render_template()` para substituir placeholders

4. Atualizar testes em `tests/test_objetivo_wizard.py`

**Estimativa**: 1 sprint (5 dias)

---

### Sprint 4.2: Implementar objetivo-validate para v3.0

**Tarefas**:
1. Parser para Markdown Híbrido
2. Validações de schema (YAML frontmatter)
3. Validações de conteúdo (seções P0 preenchidas)
4. Validações de consistência (profiles × features)

**Estimativa**: 0.5 sprint (2-3 dias)

---

### Sprint 4.3: Implementar objetivo-generate para v3.0

**Tarefas**:
1. Converter objetivo.yaml v3.0 → objetivo-spec.yaml
2. Auto-detectar profiles baseado em domain/language/roles
3. Mapear features_to_implement → spec.features
4. Gerar personas baseado em roles
5. Validar output com schema

**Estimativa**: 1 sprint (5 dias)

---

### Sprint 4.4: Deprecar v1.0 e v2.0

**Tarefas**:
1. Migrar projetos existentes v1.0 → v3.0
2. Criar `scaffold objetivo-migrate --from v1.0 --to v3.0`
3. Deprecar `objetivo-init.yaml` (manter compat por 2 sprints)
4. Atualizar documentação

**Estimativa**: 0.5 sprint (2-3 dias)

---

## Benefícios

### Para Usuários
- ✅ **100% das informações capturadas** (vs 31% atual)
- ✅ Formato legível (Markdown) + estruturado (YAML)
- ✅ Validação automática
- ✅ Geração de spec técnico sem edição manual

### Para Desenvolvedores
- ✅ Formato único (sem confusão v1/v2)
- ✅ Pipeline objetivo → validate → generate → new project
- ✅ Menos manutenção (1 template vs 2)

### Para Projeto
- ✅ Onboarding mais rápido (wizard completo)
- ✅ Documentação mais rica
- ✅ Rastreabilidade de requisitos

---

## Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Wizard fica muito longo (>30 min) | Alta | Médio | Modo Quick (P0) vs Complete (P0+P1+P2) |
| Breaking change em projetos existentes | Média | Alto | Migração automática v1→v3 |
| Complexidade de validação aumenta | Baixa | Baixo | Testes unitários robustos |

---

## Métricas de Sucesso

- [ ] 100% dos campos de objetivo-init.yaml capturados
- [ ] Tempo de preenchimento wizard <20 min (modo Complete)
- [ ] Tempo de preenchimento wizard <10 min (modo Quick)
- [ ] Taxa de erro validação <5%
- [ ] 100% dos projetos novos usam v3.0 após 4 semanas

---

## Decisão

**Status**: PLANEJADO (aguardando priorização)
**Owner**: TBD
**Inicio estimado**: Q2 2026
**Conclusão estimada**: Q3 2026

---

## Referências

- Spec v2.0: `specs/066-objetivo-yaml-v2/spec.md`
- Template v2.0: `poc/objetivo-v2-template-base.md`
- Wizard atual: `scripts/lib/objetivo_wizard.py`
- Exemplo real v1.0: `docs/guides/objetivo-init.yaml`
