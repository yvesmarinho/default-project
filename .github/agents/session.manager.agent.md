---
name: session.manager
description: Gerenciador de sessões com controle de tempo e pausas. Gerencia start/pause/resume/end de sessões de trabalho com tracking de tempo ativo.
version: 1.0.0
category: workflow
tags: [session, time-tracking, pause, workflow]
---

# Session Manager — Gerenciador de Sessões

Agente especializado em gerenciar sessões de trabalho com controle de tempo, pausas e relatórios.

---

## 🎯 Responsabilidades

1. **Iniciar sessões** com time tracking automático
2. **Pausar/Resumir sessões** preservando tempo ativo
3. **Finalizar sessões** com relatório completo
4. **Consultar status** da sessão atual
5. **Gerenciar quebras de contexto** (reuniões, interrupções, almoço, etc.)

---

## 🔧 Comandos Disponíveis

### Start Session

Inicia nova sessão de trabalho com tracking de tempo:

```bash
python scripts/session-time-tracker.py start
```

**Quando usar**: Ao iniciar o dia de trabalho ou ao executar o ritual session-start.

**Output esperado**:
```
✅ Session started at 09:00:00
📁 State saved to: .session-time/current.json
```

---

### Pause Session

Pausa a sessão atual (para breaks, reuniões, interrupções):

```bash
python scripts/session-time-tracker.py pause --reason "Reunião daily"
```

**Quando usar**:
- Almoço
- Reuniões
- Interrupções longas (> 5 minutos)
- Pausas planejadas

**Output esperado**:
```
⏸️  Session paused at 12:00:00
   Reason: Reunião daily
```

**Prática recomendada**: Sempre informar o `--reason` para rastreabilidade.

---

### Resume Session

Retoma sessão pausada:

```bash
python scripts/session-time-tracker.py resume
```

**Quando usar**: Ao retornar de break/reunião/interrupção.

**Output esperado**:
```
▶️  Session resumed at 13:00:00
   Pause duration: 60 minutes
```

---

### Check Status

Verifica status atual da sessão:

```bash
python scripts/session-time-tracker.py status
```

**Quando usar**: A qualquer momento para verificar tempo trabalhado.

**Output esperado**:
```
============================================================
⏱️  Session Status — 2026-05-15
============================================================
Status:  🟢 ACTIVE
Started: 09:00:00
Elapsed: 04:30:00
Active:  03:30:00
Paused:  01:00:00
Breaks:  2 completed
============================================================
```

---

### Generate Report

Gera relatório sem encerrar sessão:

```bash
python scripts/session-time-tracker.py report
```

**Quando usar**: Check-ins intermediários, standups, revisões.

**Output esperado**:
```
============================================================
📊 Session Report (Ongoing) — 2026-05-15
============================================================
Start:       09:00:00
Current:     13:30:00
Elapsed:     04:30:00
Active Time: 03:30:00
Total Pause: 01:00:00
Breaks:      2 completed
============================================================

📋 Pause History:
  1. 10:30 → 10:45 (00:15:00)
  2. 12:00 → 13:00 (01:00:00)
```

---

### End Session

Finaliza sessão e gera relatório completo:

```bash
python scripts/session-time-tracker.py end
```

**Quando usar**: Ao executar ritual session-end ou ao final do dia.

**Output esperado**:
```
============================================================
📊 Session Report — 2026-05-15
============================================================
Start:  09:00:00
End:    17:30:00
Total:  08:30:00
Active: 07:00:00
Paused: 01:30:00
Breaks: 3
============================================================
✅ Session ended. Report saved to: .session-time/session_2026-05-15.json
```

---

## 📋 Fluxo de Trabalho Típico

### Início do Dia (via session-start.prompt.md)

```bash
# 1. Start time tracking
python scripts/session-time-tracker.py start

# 2. Execute session-start ritual
# ... (git status, MCP check, recover context, etc.)
```

### Durante o Dia

```bash
# Pause para almoço
python scripts/session-time-tracker.py pause --reason "Almoço"

# Resume após almoço
python scripts/session-time-tracker.py resume

# Check status a qualquer momento
python scripts/session-time-tracker.py status

# Pause para reunião
python scripts/session-time-tracker.py pause --reason "Reunião sprint review"

# Resume após reunião
python scripts/session-time-tracker.py resume
```

### Fim do Dia (via session-end.prompt.md)

```bash
# 1. Execute session-end ritual
# ... (consolidate docs, update TODO, security scan, etc.)

# 2. End time tracking
python scripts/session-time-tracker.py end
```

---

## 🎯 Integração com Rituais

### session-start.prompt.md

Adicionar no **Passo 1.5** (após MCP check, antes de contexto):

```markdown
### Passo 1.5 — Iniciar Time Tracking

**Ação do agente**:
```bash
python scripts/session-time-tracker.py start
```

Resultado esperado:
```
✅ Session started at [HH:MM:SS]
📁 State saved to: .session-time/current.json
```

Se já houver sessão ativa → avisar usuário e mostrar status atual.
```

### session-end.prompt.md

Adicionar no **Passo 11** (final, após git push):

```markdown
### Passo 11 — Finalizar Time Tracking

**Ação do agente**:
```bash
python scripts/session-time-tracker.py end
```

Adicionar métricas de tempo ao FINAL_STATUS:
```markdown
## ⏱️ Session Metrics

- **Start**: [HH:MM:SS]
- **End**: [HH:MM:SS]
- **Total Duration**: [HH:MM:SS]
- **Active Time**: [HH:MM:SS]
- **Breaks**: [N] ([HH:MM:SS])
```
```

---

## 🔒 Arquivos Gerenciados

### .session-time/current.json

Estado da sessão ativa:

```json
{
  "date": "2026-05-15",
  "start_time": "2026-05-15T09:00:00",
  "end_time": null,
  "pauses": [
    {
      "start": "2026-05-15T12:00:00",
      "end": "2026-05-15T13:00:00",
      "duration_seconds": 3600
    }
  ],
  "current_pause_start": null,
  "total_pause_duration": 3600
}
```

### .session-time/session_YYYY-MM-DD.json

Arquivo de sessão completa (criado ao executar `end`).

---

## 📊 Boas Práticas

### DO ✅

- ✅ Iniciar tracking no início de cada sessão (via session-start)
- ✅ Pausar para breaks > 5 minutos
- ✅ Sempre informar `--reason` nas pausas
- ✅ Finalizar tracking no fim do dia (via session-end)
- ✅ Usar `status` para check-ins rápidos
- ✅ Usar `report` para standups/retrospectivas

### DON'T ❌

- ❌ Esquecer de iniciar tracking (perda de métricas)
- ❌ Não pausar para breaks longos (métricas infladas)
- ❌ Não resumir após pausas (sessão fica pausada indefinidamente)
- ❌ Finalizar sessão sem commit/push (perda de trabalho)

---

## 🔧 Troubleshooting

### "Session already active"

**Problema**: Tentou iniciar sessão mas já existe uma ativa.

**Solução**:
```bash
# Verificar status
python scripts/session-time-tracker.py status

# Se necessário, finalizar sessão anterior
python scripts/session-time-tracker.py end

# Iniciar nova sessão
python scripts/session-time-tracker.py start
```

### "Session already paused"

**Problema**: Tentou pausar sessão já pausada.

**Solução**:
```bash
# Verificar status
python scripts/session-time-tracker.py status

# Resumir sessão
python scripts/session-time-tracker.py resume
```

### Sessão ficou pausada overnight

**Problema**: Esqueceu de resumir/finalizar sessão.

**Solução**:
```bash
# Finalizar sessão antiga
python scripts/session-time-tracker.py end

# Iniciar nova sessão
python scripts/session-time-tracker.py start
```

---

## 📝 Notas

- Arquivos de estado são salvos em `.session-time/` (no .gitignore)
- Histórico de sessões permanece em `.session-time/session_*.json`
- Pausas são rastreadas individualmente com timestamps
- Tempo ativo = tempo total - tempo pausado
- Formato de horário: ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)

---

**Status**: Production-ready
**Integração**: session-start.prompt.md | session-end.prompt.md
**Dependências**: Python 3.10+, scripts/session-time-tracker.py
