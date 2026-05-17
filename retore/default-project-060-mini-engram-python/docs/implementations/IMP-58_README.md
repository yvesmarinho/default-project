# IMP-58 — Memory Needs Assessment System

**Status**: 🟡 Coleta em andamento
**Criado**: 2026-04-05
**Período de coleta**: 2026-04-05 a 2026-05-03 (4 semanas)
**Decisão esperada**: 2026-05-10

---

## 📋 Visão Geral

Sistema de avaliação para determinar se é necessário implementar **memória ativa** (Engram/Mini-Engram Python) ou se a **memória passiva** atual (session-search com scope) é suficiente.

**Parte de**: [DEBATE_ENGRAM_INTEGRATION_2026-04-05.md](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md)

---

## 🎯 Objetivo

**Decision Gate**: Decidir entre:
- **GO para IMP-59**: Implementar Mini-Engram Python (memória ativa) — 40h de trabalho
- **MANTER IMP-51 v2.0**: Memória passiva (scope search) é suficiente — 0h adicional

**Critérios de decisão**: SE **≥2 de 3** critérios atendidos → GO

1. ✅ **Frequência alta**: ≥50% dos participantes buscam ≥5x/dia
2. ✅ **Perda de contexto**: ≥50% relatam falha de busca ≥3x/semana
3. ✅ **Onboarding lento**: ≥50% levam >2h para encontrar informações

---

## 📁 Arquivos do Sistema

```
docs/
├── IMP-58_MEMORY_ASSESSMENT_SURVEY.md       # Template de survey (5 perguntas)
├── IMP-58_INTERVIEW_TEMPLATE.md             # Template de entrevista (30-45 min)
├── IMP-58_MEMORY_ASSESSMENT_REPORT.md       # Report consolidado (preencher após coleta)
└── IMP-58_README.md                         # Este arquivo

scripts/
└── imp58-usage-logger.py                    # Logger automático de uso

.imp58-usage/
├── usage.log                                # Log de buscas (JSONL, gitignored)
└── .gitignore                               # Ignora logs (não commitar dados privados)
```

---

## 🚀 Como Usar

### Para Participantes (Desenvolvedores)

#### 1. Responder Survey (5 min)

```bash
# Copiar template
cp docs/IMP-58_MEMORY_ASSESSMENT_SURVEY.md docs/IMP-58_SURVEY_[seu_nome].md

# Preencher as 5 perguntas
code docs/IMP-58_SURVEY_[seu_nome].md

# Commitar resposta
git add docs/IMP-58_SURVEY_[seu_nome].md
git commit -m "docs: IMP-58 survey response - [seu_nome]"
```

#### 2. Habilitar Usage Logging (opcional, 1 min)

Adicione ao seu `~/.zshrc` ou `~/.bashrc`:

```bash
# Alias para session-search com logging automático
alias session-search='python scripts/imp58-usage-logger.py'
```

Recarregue:
```bash
source ~/.zshrc  # ou source ~/.bashrc
```

Agora, toda vez que usar `session-search`, será logado automaticamente!

**Uso normal**:
```bash
# Funciona exatamente como antes
session-search "IMP-57"
session-search "architecture" --scope docs
```

**Ver suas estatísticas**:
```bash
python scripts/imp58-usage-logger.py --stats
```

#### 3. Participar de Entrevista (30-45 min)

Se convidado, agendar com o avaliador. A entrevista seguirá o template em [IMP-58_INTERVIEW_TEMPLATE.md](IMP-58_INTERVIEW_TEMPLATE.md).

---

### Para Avaliador (Análise)

#### 1. Durante Coleta (2-4 semanas)

- Distribuir survey para 3-5 desenvolvedores
- Agendar e conduzir entrevistas (usar template)
- Monitorar usage logs periodicamente:
  ```bash
  python scripts/imp58-usage-logger.py --stats
  ```

#### 2. Após Coleta (1 semana de análise)

```bash
# Consolidar todos os dados
# - Coletar docs/IMP-58_SURVEY_*.md (N surveys)
# - Coletar docs/IMP-58_INTERVIEW_*.md (N entrevistas)
# - Extrair .imp58-usage/usage.log

# Preencher report
code docs/IMP-58_MEMORY_ASSESSMENT_REPORT.md

# Calcular scores, aplicar decision gate criteria
# Escrever recomendação final (GO ou MANTER)
```

#### 3. Decisão (2026-05-10)

```bash
# Commitar report final
git add docs/IMP-58_MEMORY_ASSESSMENT_REPORT.md
git commit -m "docs: IMP-58 memory assessment complete - decisão: [GO/MANTER]"

# Atualizar TODO.md
# - Se GO: IMP-59 → 🟢 EM ANDAMENTO
# - Se MANTER: IMP-58 → ✅ CONCLUÍDO, IMP-59/IMP-45 → ⚪ ARQUIVADO
```

---

## 📊 Metodologia

### 1. Survey (Quantitativo)

- **5 perguntas fechadas** + comentários qualitativos
- **Scoring**: 0-40 pontos por respondente (ponderado)
- **Meta**: 3-5 respondentes
- **Tempo**: 5 minutos por respondente

### 2. Usage Logging (Quantitativo)

- **Automático** via wrapper de `session-search`
- **Métricas**:
  - Frequência de buscas por dia
  - Taxa de sucesso (encontrou o que procurava?)
  - Tempo médio de execução
  - Distribuição por scope (sessions/docs/specs)
- **Período**: 2-4 semanas contínuas
- **Formato**: JSONL (JSON Lines) em `.imp58-usage/usage.log`

### 3. Entrevistas (Qualitativo)

- **Estruturadas** com 5 seções:
  1. Uso atual do sistema de busca
  2. Pain points e contexto perdido
  3. Cenários de memória ativa
  4. Trade-offs e preocupações
  5. Priorização e decisão
- **Duração**: 30-45 min por entrevista
- **Meta**: 3-5 entrevistados
- **Scoring**: 1-25 pontos por entrevistado

---

## 📈 Exemplo de Uso do Logger

### Uso Normal

```bash
# Buscar com logging automatico
$ session-search "IMP-57" --scope all

Search Results
────────────────────────────────────────────────────────────
Query: IMP-57
Scope: all
Found: 5 result(s)
────────────────────────────────────────────────────────────
[DOC] 2026-04-05 [doc] — Searching Beyond Sessions (IMP-57)
...

🔍 Did you find what you were looking for? (y/n/skip): y

# Loggado automaticamente:
# - query: "IMP-57"
# - scope: "all"
# - results_count: 5
# - execution_time: 123ms
# - found_what_looking_for: true
```

### Ver Estatísticas

```bash
$ python scripts/imp58-usage-logger.py --stats

============================================================
IMP-58 Usage Statistics — Session Search Analytics
============================================================

📊 Overall Statistics
  Total searches:       47
  Successful:           38 (80.9%)
  Failed:               9 (19.1%)
  Unknown:              0
  Avg results per query: 3.2
  Avg execution time:    95ms

📅 Time Period
  First search:         2026-04-05
  Last search:          2026-04-26
  Days active:          21
  Searches per day:     2.2

🎯 Scope Distribution
  sessions        28 ( 59.6%)
  docs            12 ( 25.5%)
  all              5 ( 10.6%)
  specs            2 (  4.3%)

💡 Insights
  ✅ Normal frequency: 2.2 searches/day
  ✅ Low failure rate: 19.1%

============================================================
Log file: /projeto/.imp58-usage/usage.log
============================================================
```

---

## 🎯 Timeline

| Fase | Datas | Duração | Responsável |
|------|-------|---------|-------------|
| **Preparação** | 2026-04-05 | 1 dia | [avaliador] |
| **Distribuição survey** | 2026-04-05 a 04-07 | 2 dias | [avaliador] |
| **Coleta logs** | 2026-04-05 a 05-03 | 2-4 semanas | [participantes] |
| **Entrevistas** | 2026-04-10 a 04-30 | 3 semanas | [avaliador + participantes] |
| **Análise** | 2026-05-03 a 05-10 | 1 semana | [avaliador] |
| **Decisão** | 2026-05-10 | 1 dia | [tech lead / arquiteto] |

---

## ⚠️ Considerações Importantes

### Privacidade

- Logs são **gitignored** (`.imp58-usage/.gitignore`)
- Surveys individuais **podem ser commitados** (não contêm dados sensíveis)
- Entrevistas **podem ser commitadas** (anonimizar se necessário)
- Report final **deve ser commitado** (dados agregados apenas)

### Participação Voluntária

- Participar do survey é **opcional**
- Usage logging é **opt-in** (requer alias manual)
- Entrevistas são **por convite** (consentimento explícito)

### Confidencialidade

- Respostas individuais são **confidenciais**
- Report final mostra apenas **dados agregados**
- Quotes em entrevistas podem ser **anonimizadas** se solicitado

---

## 🔗 Referências

- [DEBATE_ENGRAM_INTEGRATION_2026-04-05.md](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md) — Debate estratégico original
- [TODO.md](TODO.md) — IMPs 57, 58, 59, 45
- [SESSION_SEARCH_GUIDE.md](SESSION_SEARCH_GUIDE.md) — Sistema atual de busca (IMP-51 v1.1)

---

## ❓ FAQ

**P: Preciso participar de tudo (survey + logs + entrevista)?**
R: Não. Cada método é independente. Quanto mais participar, melhor a qualidade da decisão.

**P: Os logs capturam minhas queries pessoais?**
R: Sim, MAS são gitignored e não versionados. Só análises agregadas vão para o report.

**P: Posso ver meus próprios dados de log?**
R: Sim: `python scripts/imp58-usage-logger.py --stats`

**P: E se eu não quiser logging?**
R: Não adicione o alias. Use `python scripts/session-search.py` diretamente (sem logging).

**P: Quanto tempo leva para preencher o survey?**
R: ~5 minutos (5 perguntas fechadas + comentários opcionais).

**P: O que acontece se nenhum critério for atendido?**
R: **MANTER IMP-51 v2.0** — memória passiva é suficiente, não implementar Engram.

**P: E se TODOS os critérios forem atendidos?**
R: **GO forte para IMP-59** — memória ativa é necessidade crítica.

---

**Status**: 🟡 Coleta em andamento
**Última atualização**: 2026-04-05
**Responsável**: [definir]
**Dúvidas/sugestões**: [canal de comunicação]
