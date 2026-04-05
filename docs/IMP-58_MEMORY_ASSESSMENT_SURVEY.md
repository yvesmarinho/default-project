# IMP-58 — Survey de Avaliação de Necessidade de Memória Ativa

**Criado**: 2026-04-05  
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
- [ ] **Constantemente** — ≥5x por dia ⭐ (necessidade alta)

**Comentários adicionais**:
```
[Espaço para comentários livres]
```

---

### 2. Perda de Contexto

**Pergunta**: Com que frequência você **não consegue encontrar** informações que sabe que existem nas sessões, mesmo usando o sistema de busca?

- [ ] **Nunca** — sempre encontro o que procuro
- [ ] **Raramente** — <1x por semana
- [ ] **Ocasionalmente** — 1-2x por semana
- [ ] **Frequentemente** — ≥3x por semana ⭐ (necessidade alta)
- [ ] **Muito frequentemente** — diariamente

**Exemplos de contexto perdido** (se aplicável):
```
[Descreva situações onde não encontrou informações]
Exemplo: "Não consegui encontrar a decisão sobre qual biblioteca usar para X"
```

---

### 3. Tempo de Onboarding

**Pergunta**: Quando você precisa entender uma funcionalidade ou decisão passada do projeto, quanto tempo leva para encontrar todas as informações necessárias?

- [ ] **Muito rápido** — <15 minutos
- [ ] **Rápido** — 15-30 minutos
- [ ] **Moderado** — 30-60 minutos
- [ ] **Lento** — 1-2 horas
- [ ] **Muito lento** — >2 horas ⭐ (necessidade alta)

**Exemplo recente** (se aplicável):
```
[Descreva uma situação recente de onboarding]
Exemplo: "Levei 3h para entender todas as decisões do IMP-48 lendo 4 sessões diferentes"
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
- [ ] **Definitivamente sim** — economizaria muito tempo ⭐ (necessidade alta)

**Cenário de uso ideal** (se sim):
```
[Descreva como você usaria memória ativa]
Exemplo: "Quando pergunto ao Copilot sobre validação, ele deveria lembrar automaticamente 
que já implementamos validador semver no IMP-XX"
```

---

### 5. Principais Dores com Sistema Atual

**Pergunta**: Quais são suas **3 maiores dificuldades** com o sistema de busca/memória atual?

1. ```
   [Primeira dificuldade]
   ```

2. ```
   [Segunda dificuldade]
   ```

3. ```
   [Terceira dificuldade]
   ```

**Sugestões de melhoria**:
```
[Ideias para melhorar o sistema atual, mesmo sem memória ativa]
```

---

## 📊 Seção de Análise (preenchida pelo avaliador)

### Scoring Individual

| Critério | Resposta | Score | Peso | Pontos Ponderados |
|----------|----------|-------|------|-------------------|
| Frequência de busca | [resposta] | 0-5 | 2x | [score × 2] |
| Perda de contexto | [resposta] | 0-5 | 3x | [score × 3] |
| Tempo de onboarding | [resposta] | 0-5 | 2x | [score × 2] |
| Interesse em memória ativa | [resposta] | 0-5 | 1x | [score × 1] |

**Total de Pontos**: [soma] / 40 pontos possíveis  
**Percentual**: [% do total]

**Necessidade Alta**: ≥60% pontuação (≥24/40 pontos)  
**Necessidade Moderada**: 40-59% pontuação (16-23/40 pontos)  
**Necessidade Baixa**: <40% pontuação (<16/40 pontos)

### Observações Qualitativas

```
[Insights adicionais do avaliador sobre este respondente]
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

## 📝 Instruções de Aplicação

### Para Respondentes

1. Clone este arquivo: `cp docs/IMP-58_MEMORY_ASSESSMENT_SURVEY.md docs/IMP-58_SURVEY_[seu_nome].md`
2. Preencha as 5 perguntas marcando checkboxes e adicionando comentários
3. Salve o arquivo preenchido em `docs/IMP-58_SURVEY_[seu_nome].md`
4. Adicione ao git: `git add docs/IMP-58_SURVEY_[seu_nome].md`
5. Commit: `git commit -m "docs: IMP-58 survey response - [seu_nome]"`

### Para Avaliador

1. Após 2-4 semanas, coletar todos os arquivos `docs/IMP-58_SURVEY_*.md`
2. Preencher seção de análise em cada survey
3. Consolidar resultados em `docs/IMP-58_MEMORY_ASSESSMENT_REPORT.md`
4. Aplicar decision gate criteria
5. Documentar decisão em TODO.md

---

## 📅 Timeline

- **Início**: 2026-04-05 (após conclusão IMP-57)
- **Distribuição do survey**: 2026-04-05 a 2026-04-07
- **Período de coleta**: 2-4 semanas (até 2026-04-26 a 2026-05-03)
- **Análise**: 1 semana (até 2026-05-10)
- **Decisão**: 2026-05-10

---

## 🔗 Referências

- [DEBATE_ENGRAM_INTEGRATION_2026-04-05.md](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md) — Debate estratégico
- [TODO.md](TODO.md) — IMP-58, IMP-59, IMP-45
- [SESSION_SEARCH_GUIDE.md](SESSION_SEARCH_GUIDE.md) — Sistema atual de busca

---

**Status**: 🟡 Coleta em andamento  
**Última atualização**: 2026-04-05
