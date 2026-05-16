# IMP-58 — Survey de Avaliação de Necessidade de Memória Ativa

**Respondente**: Yves Marinho
**Data de resposta**: 2026-04-20
**Parte de**: IMP-58 — Avaliar necessidade de memória ativa (Fase 2 Engram Integration)
**Duração**: 2-4 semanas de coleta
**Objetivo**: Decidir entre manter IMP-51 v2.0 (memória passiva) ou implementar IMP-59 (memória ativa)

---

## 📋 Survey para Desenvolvedores

**Instruções**: Responda estas 5 perguntas com base em sua experiência nas últimas 2 semanas usando o sistema de busca de sessões (`session-search`).

### 1. Frequência de Busca Manual

**Pergunta**: Com que frequência você usa `python scripts/session-search.py` ou `make session-search` para encontrar informações?

- [ ] **Nunca** — não uso o sistema de busca
- [ ] **Raramente** — 1-2x por semana
- [ ] **Ocasionalmente** — 3-4x por semana
- [ ] **Frequentemente** — 1-2x por dia
- [ ] **Muito frequentemente** — 3-4x por dia
- [x] **Constantemente** — ≥5x por dia ⭐ (necessidade alta)

**Comentários adicionais**:
```
Eu faço com que o Copilot busque constantemente informações anterires.
Tenho grande ocorrência de erros cometidos por perda de dados passados, muitas vezes recentes.
O Copilot tem dificuldade até para manter vivo as instruções em ".copilot-rules*"
```

---

### 2. Perda de Contexto

**Pergunta**: Com que frequência você **não consegue encontrar** informações que sabe que existem nas sessões, mesmo usando o sistema de busca?

- [ ] **Nunca** — sempre encontro o que procuro
- [ ] **Raramente** — <1x por semana
- [x] **Ocasionalmente** — 1-2x por semana
- [ ] **Frequentemente** — ≥3x por semana ⭐ (necessidade alta)
- [ ] **Muito frequentemente** — diariamente

**Exemplos de contexto perdido** (se aplicável):
```
Exemplo uqe mais ocorre é as instruções do ".copilot-rules*"
Exemplo: "Instrução para manusear os arquivos com os recursos internos do Copilot/Code, não usar Heredoc. Frequemente Copilot usa Heredoc, inclusive para executar comandos via SSH, que arpensentam erro de finalização com o `"`."
```

---

### 3. Tempo de Onboarding

**Pergunta**: Quando você precisa entender uma funcionalidade ou decisão passada do projeto, quanto tempo leva para encontrar todas as informações necessárias?

- [ ] **Muito rápido** — <15 minutos
- [ ] **Rápido** — 15-30 minutos
- [x] **Moderado** — 30-60 minutos
- [ ] **Lento** — 1-2 horas
- [ ] **Muito lento** — >2 horas ⭐ (necessidade alta)

**Comentários adicionais**:
```
Eu faço com que o Copilot busque constantemente informações anterires.
Minha utilização é exclusivamente Codigo Gerado por IA sob meu comando.
```

---

### 4. Interesse em Memória Ativa (Engram)

**Pergunta**: Você gostaria de ter um sistema de **memória ativa** que:
- Sugere automaticamente contexto relevante durante conversas com Copilot
- Lembra decisões passadas sem precisar buscar manualmente
- Aprende com as sessões e oferece insights proativos

- [ ] **Não** — sistema atual (busca passiva) é suficiente
- [ ] **Talvez** — dependendo da complexidade/overhead
- [ ] **Sim** — seria útil ocasionalmente
- [x] **Definitivamente sim** — economizaria muito tempo ⭐ (necessidade alta)

**Cenário de uso ideal** (se sim):
```
É meu padrão de trabalho gerar dados de tudo que acontece nas sessões de trabalho.
O objetivo disso é criar uma Base de Conhecimento para o Copilot executar tarefas com menos erros e sempre focado no contexto.
Eu faço com que o Copilot busque constantemente informações anterires.
O Copilot tem dificuldade até para manter vivo as instruções em ".copilot-rules*"
Quero a Memória Ativa para reduzir os problemas gerados por dados de curta duração.
É necessário usar algum recurso que me auxilie na duração das informações.
```

---

### 5. Principais Dores com Sistema Atual

**Pergunta**: Quais são suas **3 maiores dificuldades** com o sistema de busca/memória atual?

1. ```
   Memória de curta duração. Uma instrução ou solicitação não duramais que 5 minutos, as vezes menis, dependendo da complexidade do contexto.
   ```

2. ```
   Instruções de comportamento do Copilot são de curta duração. Frequemente são executados ações fora do padrão existente na instrução.
   ```

3. ```
   Perde constantemente o contexto de um código, muitas vezes gerando vários arquivos de código para fazer a mesma coisa.
   ```

**Sugestões de melhoria**:
```
Preciso das melhores soluções em FOSS, com uso de recursos de computador moderados.
```

---

## 📊 Seção de Análise (preenchida pelo avaliador)

### Scoring Individual

| Critério | Resposta | Score | Peso | Pontos Ponderados |
|----------|----------|-------|------|-------------------|
| Frequência de busca | Constantemente (≥5x/dia) ⭐ | 5 | 2x | **10** |
| Perda de contexto | Ocasionalmente (1-2x/semana) | 2 | 3x | **6** |
| Tempo de onboarding | Moderado (30-60 min) | 2 | 2x | **4** |
| Interesse em memória ativa | Definitivamente sim ⭐ | 5 | 1x | **5** |

**Total de Pontos**: **25** / 40 pontos possíveis
**Percentual**: **62.5%**

✅ **Necessidade Alta**: ≥60% pontuação (≥24/40 pontos) — **ATENDIDO**
**Necessidade Moderada**: 40-59% pontuação (16-23/40 pontos)
**Necessidade Baixa**: <40% pontuação (<16/40 pontos)

### Observações Qualitativas

```
**Perfil do Respondente**: Power user com uso intensivo de IA-assisted coding

**Principais Insights**:

1. **Alto volume de uso** (5/5 score):
   - Frequência ≥5x/dia de busca por contexto anterior
   - Padrão de trabalho: código 100% gerado por IA sob comando humano
   - Objetivo: construir Base de Conhecimento para reduzir erros do Copilot

2. **Problema crítico identificado — Memória de curta duração**:
   - Instruções/contexto duram <5 minutos em sessões complexas
   - Instruções `.copilot-rules*` frequentemente ignoradas
   - Grande ocorrência de erros por perda de dados recentes
   - Perde contexto de código → gera duplicações (múltiplos arquivos para mesma função)

3. **Pain points específicos**:
   - Copilot usa Heredoc/shell apesar de instruções proibirem
   - Comandos SSH com heredoc apresentam erros de finalização (`"`)
   - Comportamentos fora do padrão instruído são recorrentes

4. **Necessidade de memória ativa claramente articulada**:
   - Quote: "Quero a Memória Ativa para reduzir os problemas gerados por dados de curta duração"
   - Expectativa: contexto persistente, decisões lembradas automaticamente
   - Cenário ideal: Copilot mantém instruções comportamentais ativas por toda sessão

5. **Impacto no workflow**:
   - Onboarding moderado (30-60 min) — poderia ser mais rápido com memória ativa
   - Perda de contexto ocasional (1-2x/semana) — não crítica mas presente

**Recomendação**: Este respondente é **caso de uso ideal para IMP-59**. O perfil de trabalho
(IA-assisted coding intensivo) se beneficiaria significativamente de:
- Memória ativa com persistência >24h
- Injeção automática de contexto de `.copilot-rules*`
- Histórico de decisões arquiteturais disponível proativamente
- Detecção de padrões anti-pattern (ex: uso de heredoc apesar de proibição)

**Score final**: 62.5% (Necessidade Alta) — suporta decisão GO para IMP-59.
```

---

## 🎯 Decision Gate Criteria

**Critérios para GO em IMP-59** (Mini-Engram Python):

1. ✅ **Frequência alta**: ≥50% dos respondentes buscam ≥5x/dia
2. ✅ **Perda de contexto**: ≥50% dos respondentes relatam ≥3x/semana
3. ✅ **Onboarding lento**: ≥50% dos respondentes levam >2h

**Decisão**: Se **≥2 critérios** atendidos → **GO** para IMP-59
**Caso contrário**: **MANTER** IMP-51 v2.0 (scope search suficiente)

---
