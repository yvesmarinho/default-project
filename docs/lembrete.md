# Alterações necessárias

---
## ✅ Processado em 2026-04-05 — Spec Driven Development

Os itens abaixo foram analisados, debatidos e **validados contra metodologias de mercado (Score: 78% — BOM)**.

**Informações adquiridas para futuro debate:**
- ✅ Buscar melhores práticas em Engenharia de Especificação orientada a Engenharia de Software
- ✅ 4 Camadas do desenvolvimento: Negócio → Produto → Arquitetura → Implementação
- ✅ Decisões de Arquitetura (ADRs)
- ✅ Requisitos Funcionais
- ✅ Critérios de Aceite

**Debate gerado**: [`docs/debates/DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md`](debates/DEBATE_SPEC_DRIVEN_DEVELOPMENT_2026-04-05.md)
**Validação de mercado**: [`docs/debates/ANALISE_4_CAMADAS_VS_MERCADO_2026-04-05.md`](debates/ANALISE_4_CAMADAS_VS_MERCADO_2026-04-05.md)

**Resultado da validação**:
- ✅ **Alinhamento com DDD** (Domain-Driven Design): 90%
- ✅ **Alinhamento com ADRs** (Architecture Decision Records): 100% — PERFEITO!
- ✅ **Alinhamento com BDD** (Behavior-Driven Development): 70%
- ✅ **Alinhamento com TDD** (Test-Driven Development): 85%
- ⚠️ **Gap identificado**: C4 Model (40%) — adicionar diagramas opcionais
- ⚠️ **Gap identificado**: DORA Metrics (50%) — adicionar métricas de entrega

**Empresas que usam práticas similares**: Amazon (AWS), Google, ThoughtWorks, Spotify, Netflix

**Veredicto**: ✅ **APROVADO para implementação** com ajustes P1 (bounded_contexts em objetivo.yaml, explicitar TDD em quality gates)

**Issues criadas**:
1. ✅ **[IMP-53]** Implementar objetivo.yaml e speckit.clarify (Camada 1: Negócio)
   - Tipo: Improvement (SpecKit evolution)
   - Prioridade: P1
   - Estimativa: 1 semana (Fase 1)

2. ✅ **[IMP-54]** Integrar ADRs no plan-template.md (Camada 3: Arquitetura)
   - Tipo: Improvement (SpecKit template)
   - Prioridade: P1
   - Estimativa: 3 dias

3. ✅ **[IMP-55]** Sistema de captura de conversas (CHAT-*.md)
   - Tipo: Improvement (memória/documentation)
   - Prioridade: P2
   - Estimativa: 1 semana (Fase 3)

4. ✅ **[IMP-56]** Agent speckit.validate para quality gates
   - Tipo: Improvement (SpecKit validation)
   - Prioridade: P1
   - Estimativa: 1 semana (Fase 2)

**Novas demandas** (originais mantidas para referência):

1. ✅ Criar modelo `objetivo.yaml` → **IMP-53**
2. ✅ Atualizar `mcp-questions.yaml` → Integrado no **IMP-53** (speckit.clarify)
3. ✅ Sistema de captura de conversas → **IMP-55**

---
## ✅ Processado em 2026-04-05 — Integração Engram MCP

**Debate gerado**: [`docs/debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md`](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md)

**Decisão consensual**: ✅ **APROVADO COM CONDIÇÕES** — Implementação Faseada (Cenário 3)

**Veredicto**:
- 7 perspectivas profissionais debateram (template-architect, session-manager, constitution, Platform Tooling, DevEx, AppSec, SRE)
- **Consenso**: Engram tem valor, mas timing incerto (IMP-51 muito recente)
- **Approach**: Incrementar capacidades antes de adicionar complexidade

**Fases aprovadas**:
1. **Fase 1** (imediato, 16h): Estender IMP-51 para indexar mais docs (README, TODO, specs)
2. **Fase 2** (2-4 semanas, 16h): Avaliar necessidade real com dados de uso
3. **Fase 3a** (condicional, 40h): Mini-Engram Python puro SE necessário
4. **Fase 3b** (fallback, 80h): Engram oficial SE Python inadequado

**Issues criadas**:
- **[IMP-57]** Estender IMP-51: indexação de documentos além de DAILY_ACTIVITIES (Fase 1)
- **[IMP-58]** Avaliar necessidade de memória ativa (Fase 2)
- **[IMP-59]** Mini-Engram Python (Fase 3a — condicional)
- **[IMP-45]** Engram oficial (renomeado para Fase 3b — fallback)

**Blockers de segurança identificados** (AppSec + constitution):
- 🚨 Principle IV (Zero-Trust on Secrets) pode ser violado se Engram salvar outputs com credenciais
- ✅ Controles obrigatórios: `.gitignore` patterns, `.gitleaks-engram.toml`, sanitização de PII/secrets, pre-commit hooks
- ✅ Policy: `.engram/AGENT_MEMORY_POLICY.md` com seções "Secrets Management" + "Data Privacy"

**Próximo passo**: Implementar IMP-57 (Fase 1) — extensão do IMP-51

---
## Informações adquiridas para futuro debate

- Buscar melhores práticas em Engenharia de Especificação orientada a Engenharia de Software.
- 4 Camadas do desenvolvimento: Negócio -> Produto -> Arquitetura -> Implementação.
- Decisões de Arquitetura (ADRs)
- Requisitos Funcionais
- Critérios de Aceite

---

## Novas demandas para adicionar a lista de tarefas/issues/melhorias.

1. Criar um modelo ser utilizado no inicio do projeto [objetivo.yaml](../docs/modelo_docs/objetivo.yaml)
    - Esse modelo conterá informações e instruções que serão utilizados como base para o contrato/constitution.
    - Conterá informações iniciais para o debate entre os agents mencionados no documento.
    - O debate analisará o conteúdo fornecido pelo usuário para aprimorar as especificações ou indicar informações ausente, gerando um questionário.
    - Informações obtidas em um video do Youtube [Spec Driven Development é o Caminho?](https://www.youtube.com/watch?v=DJE0LL0CuUQ).
    - Fluxo de especificação:

2. Após a conclusão da analise e aprimoramento do "objetivo.yaml" atualizar o [mc-questions.yaml](../docs/modelo_docs/mcp-questions.yaml).

3. Incluir no workflow instruções para gerar arquivo com o resultado do chat [CHAT-YYYYMMDD-000000.md](../docs/modelo_docs/CHAT-20260401-000000.md).
    Toda resposta do Copilot no chat deve gerar um arquivo desse. Esse arquivo pode ser usado como memória.
    Aceito sugestão de um fluxo que atenda essa demanda para torná-la mais agil.
    Um posssíbilidade seria o Engram, que já temos como melhoria.
    Avalie as opções e informe uma boa opção para essa demanda


---

## ✅ Processado em 2026-04-03

Os itens abaixo foram analisados e convertidos em issues estruturadas no `docs/TODO.md`:

1. ✅ **[IMP-52]** Adicionar instruções para usar as ferramentas jsonschema e yamllint já disponíveis.
   - Tipo: Improvement (documentação)
   - Prioridade: P1
   - Adicionado em: docs/TODO.md (seção "Itens Recentes")
   - Estimativa: 2h

2. ✅ **[BUG-03]** Não foi gerado o .github/copilot-instructions.md com as instruções básicas existentes.
   - Tipo: Bug (geração de arquivo do scaffold)
   - Prioridade: P0
   - Adicionado em: docs/TODO.md (seção "Itens Recentes")
   - Requer investigação em: scripts/lib/templates.py, scripts/lib/flows/new_project.py

3. (vazio - descartado)

---

## 📚 Referência

Para entender como gerenciar bugs e features no projeto, consulte:
- **Guia completo**: [docs/ISSUE_MANAGEMENT_GUIDE.md](../docs/ISSUE_MANAGEMENT_GUIDE.md)
- **TODO principal**: [docs/TODO.md](../docs/TODO.md)
- **Templates de issues**: `.github/ISSUE_TEMPLATE/`

---

## 💡 Próximos Passos

1. **Investigar BUG-03** (P0):
   ```bash
   # Verificar se generate_copilot_instructions() é chamado
   grep -r "generate_copilot_instructions" scripts/lib/

   # Criar projeto teste e verificar
   python scripts/scaffold.py new --ci --name test-bug03 \
     --domain programming --language python --target-dir ./tmp

   ls -la ./tmp/test-bug03/.github/copilot-instructions.md
   ```

2. **Implementar IMP-52** (P1):
   - Adicionar seção no README.md sobre validação de YAML/JSON
   - Criar targets `make lint-yaml` e `make lint-json`
   - Documentar em docs/DEVELOPMENT_GUIDE.md (criar se necessário)

---

**Status**: Items triaged and documented ✅

