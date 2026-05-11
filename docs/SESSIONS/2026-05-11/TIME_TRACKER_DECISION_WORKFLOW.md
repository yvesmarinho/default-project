# 🔄 Time Tracker Decision Workflow

**Data**: 2026-05-11  
**Arquivo**: `scripts/session-time-tracker.py`  
**Objetivo**: Documentar lógica de decisão para análise de estado e atualização de arquivos

---

## 📋 Visão Geral

O session-time-tracker implementa uma **máquina de estados** que decide quando e como atualizar arquivos de estado (JSON) e histórico (CSV) baseado em verificações de pré-condições.

### Arquivos Gerenciados
- **State File**: `.session-time/current.json` (estado transitório)
- **History CSV**: `.session-time/history.csv` (histórico persistente)

### Estados Possíveis
1. **Sem sessão** — Nenhum arquivo de estado existe
2. **Active** — Sessão em andamento (working)
3. **Paused** — Sessão pausada temporariamente
4. **Completed** — Sessão finalizada (transitório antes de cleanup)

---

## 🔀 Diagrama de Estados

```mermaid
stateDiagram-v2
    [*] --> NoSession: Sistema inicializado
    
    NoSession --> Active: cmd_start()
    
    Active --> Paused: cmd_pause(reason)
    Paused --> Active: cmd_resume()
    
    Active --> Completed: cmd_stop()
    Paused --> Completed: cmd_stop() + auto-resume
    
    Completed --> [*]: CSV salvo + state cleanup
    
    note right of NoSession
        State file não existe
        ❌ Pause/Resume/Stop bloqueados
    end note
    
    note right of Active
        current_pause = None
        ✅ Pause/Stop permitidos
        ❌ Resume bloqueado
    end note
    
    note right of Paused
        current_pause = {...}
        ✅ Resume/Stop permitidos
        ❌ Pause bloqueado
    end note
    
    note right of Completed
        Estado transitório
        Persiste CSV
        Remove state file
    end note
```

---

## 🧠 Lógica de Decisão por Comando

### 1️⃣ START — Iniciar Sessão

```mermaid
flowchart TD
    A[cmd_start chamado] --> B{State file existe?}
    B -->|SIM| C[❌ ERRO: Sessão já ativa]
    B -->|NÃO| D[Criar diretório .session-time/]
    D --> E[Gerar timestamp UTC]
    E --> F[Criar state JSON]
    F --> G[Campos iniciais:<br/>session_date<br/>start_time<br/>pauses=[]<br/>current_pause=null<br/>status=active]
    G --> H[Salvar state file]
    H --> I[✅ SUCESSO: Sessão iniciada]
    
    C --> J[returncode = 1]
    I --> K[returncode = 0]
    
    style C fill:#ff6b6b
    style I fill:#51cf66
```

**Lógica de Atualização**:
- ❌ **NÃO atualiza** se arquivo já existe (proteção duplo start)
- ✅ **CRIA novo** arquivo apenas se não existir

---

### 2️⃣ PAUSE — Pausar Sessão

```mermaid
flowchart TD
    A[cmd_pause chamado] --> B{State file existe?}
    B -->|NÃO| C[❌ ERRO: Sem sessão ativa]
    B -->|SIM| D[Ler state JSON]
    D --> E{current_pause é null?}
    E -->|NÃO| F[❌ ERRO: Já pausado]
    E -->|SIM| G[Gerar timestamp UTC]
    G --> H[Criar objeto pause:<br/>start=timestamp<br/>reason=motivo]
    H --> I[Atualizar state:<br/>current_pause=pause<br/>status=paused]
    I --> J[Salvar state file]
    J --> K[✅ SUCESSO: Pausado]
    
    C --> L[returncode = 1]
    F --> L
    K --> M[returncode = 0]
    
    style C fill:#ff6b6b
    style F fill:#ff6b6b
    style K fill:#51cf66
```

**Lógica de Atualização**:
- ❌ **NÃO atualiza** se não há sessão
- ❌ **NÃO atualiza** se já está pausado
- ✅ **ATUALIZA** apenas se estado é `active`

**Campos Modificados**:
- `current_pause` ← novo objeto com start/reason
- `status` ← "paused"

---

### 3️⃣ RESUME — Retomar Sessão

```mermaid
flowchart TD
    A[cmd_resume chamado] --> B{State file existe?}
    B -->|NÃO| C[❌ ERRO: Sem sessão ativa]
    B -->|SIM| D[Ler state JSON]
    D --> E{current_pause existe?}
    E -->|NÃO| F[❌ ERRO: Não está pausado]
    E -->|SIM| G[Gerar timestamp UTC]
    G --> H[Adicionar end ao pause:<br/>end=timestamp]
    H --> I[Calcular duração:<br/>duration_seconds]
    I --> J[Mover pause para array:<br/>pauses.append pause]
    J --> K[Limpar current_pause:<br/>current_pause=null]
    K --> L[Atualizar status:<br/>status=active]
    L --> M[Salvar state file]
    M --> N[✅ SUCESSO: Retomado]
    
    C --> O[returncode = 1]
    F --> O
    N --> P[returncode = 0]
    
    style C fill:#ff6b6b
    style F fill:#ff6b6b
    style N fill:#51cf66
```

**Lógica de Atualização**:
- ❌ **NÃO atualiza** se não há sessão
- ❌ **NÃO atualiza** se não está pausado
- ✅ **ATUALIZA** apenas se estado é `paused`

**Campos Modificados**:
- `current_pause["end"]` ← timestamp
- `current_pause["duration_seconds"]` ← calculado
- `pauses[]` ← append(current_pause)
- `current_pause` ← null
- `status` ← "active"

---

### 4️⃣ STOP — Finalizar Sessão

```mermaid
flowchart TD
    A[cmd_stop chamado] --> B{State file existe?}
    B -->|NÃO| C[❌ ERRO: Sem sessão ativa]
    B -->|SIM| D[Ler state JSON]
    D --> E{current_pause existe?}
    E -->|SIM| F[⚠️ Auto-resume:<br/>chamar cmd_resume]
    E -->|NÃO| G[Continuar]
    F --> G
    G --> H[Gerar timestamp UTC]
    H --> I[Adicionar end_time]
    I --> J[Calcular durações:<br/>total_duration_seconds<br/>pause_duration_seconds<br/>net_duration_seconds]
    J --> K[Atualizar status:<br/>status=completed]
    K --> L[Salvar no CSV:<br/>_save_to_csv]
    L --> M[Remover state file:<br/>STATE_FILE.unlink]
    M --> N[✅ SUCESSO: Finalizado]
    
    C --> O[returncode = 1]
    N --> P[returncode = 0]
    
    style C fill:#ff6b6b
    style F fill:#ffd43b
    style N fill:#51cf66
```

**Lógica de Atualização**:
- ❌ **NÃO atualiza** se não há sessão
- ⚠️ **AUTO-RESUME** se está pausado (recuperação automática)
- ✅ **ATUALIZA state** temporariamente (status=completed)
- ✅ **PERSISTE CSV** com histórico completo
- ✅ **REMOVE state** após persistir

**Campos Modificados (State)**:
- `end_time` ← timestamp
- `total_duration_seconds` ← calculado
- `pause_duration_seconds` ← sum(pauses)
- `net_duration_seconds` ← total - pause
- `status` ← "completed"

**Campos Salvos (CSV)**:
- `session_date`, `start_time`, `end_time`
- `total_duration` (HH:MM:SS)
- `pause_duration` (HH:MM:SS)
- `net_duration` (HH:MM:SS)
- `num_pauses` (count)
- `pause_details` (reason:duration; ...)

---

## 📊 Matriz de Decisão de Atualização

| Comando | State Existe? | Estado Atual | Current Pause? | Ação | Atualiza State? | Atualiza CSV? |
|---------|---------------|--------------|----------------|------|-----------------|---------------|
| **START** | ❌ Não | - | - | ✅ Cria novo | ✅ SIM (create) | ❌ NÃO |
| **START** | ✅ Sim | Qualquer | Qualquer | ❌ Erro | ❌ NÃO | ❌ NÃO |
| **PAUSE** | ❌ Não | - | - | ❌ Erro | ❌ NÃO | ❌ NÃO |
| **PAUSE** | ✅ Sim | Active | ❌ Não | ✅ Pausa | ✅ SIM (update) | ❌ NÃO |
| **PAUSE** | ✅ Sim | Paused | ✅ Sim | ❌ Erro | ❌ NÃO | ❌ NÃO |
| **RESUME** | ❌ Não | - | - | ❌ Erro | ❌ NÃO | ❌ NÃO |
| **RESUME** | ✅ Sim | Active | ❌ Não | ❌ Erro | ❌ NÃO | ❌ NÃO |
| **RESUME** | ✅ Sim | Paused | ✅ Sim | ✅ Retoma | ✅ SIM (update) | ❌ NÃO |
| **STOP** | ❌ Não | - | - | ❌ Erro | ❌ NÃO | ❌ NÃO |
| **STOP** | ✅ Sim | Active | ❌ Não | ✅ Finaliza | ✅ SIM (temp) | ✅ SIM (persist) |
| **STOP** | ✅ Sim | Paused | ✅ Sim | ⚠️ Auto-resume → Finaliza | ✅ SIM (temp) | ✅ SIM (persist) |

---

## 🔐 Proteções Implementadas

### 1. Proteção contra Duplo Start
```python
if STATE_FILE.exists():
    print("❌ Sessão já em andamento. Use 'stop' para finalizar antes de iniciar nova.")
    return 1
```
**Decisão**: ❌ NÃO cria novo arquivo

---

### 2. Proteção contra Comandos sem Sessão
```python
if not STATE_FILE.exists():
    print("❌ Nenhuma sessão ativa. Use 'start' primeiro.")
    return 1
```
**Decisão**: ❌ NÃO atualiza nada

---

### 3. Proteção contra Duplo Pause
```python
if state.get("current_pause"):
    print("❌ Sessão já pausada. Use 'resume' para retomar.")
    return 1
```
**Decisão**: ❌ NÃO atualiza state

---

### 4. Proteção contra Resume sem Pause
```python
if not state.get("current_pause"):
    print("❌ Sessão não está pausada.")
    return 1
```
**Decisão**: ❌ NÃO atualiza state

---

### 5. Auto-Recovery em Stop
```python
if state.get("current_pause"):
    print("⚠️  Sessão ainda pausada. Retomando automaticamente antes de finalizar.")
    cmd_resume()
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
```
**Decisão**: ⚠️ ATUALIZA com auto-resume → depois finaliza

---

## 📂 Operações de Arquivo

### State File (.session-time/current.json)

```mermaid
flowchart LR
    A[Estado em Memória] --> B{Operação?}
    B -->|CREATE| C[json.dump]
    B -->|READ| D[json.load]
    B -->|UPDATE| E[json.load → modify → json.dump]
    B -->|DELETE| F[STATE_FILE.unlink]
    
    C --> G[Disco]
    D --> H[Memória]
    E --> G
    F --> I[Removed]
    
    style C fill:#51cf66
    style D fill:#339af0
    style E fill:#ffd43b
    style F fill:#ff6b6b
```

### History CSV (.session-time/history.csv)

```mermaid
flowchart LR
    A[Estado Completed] --> B[_save_to_csv]
    B --> C{CSV existe?}
    C -->|NÃO| D[Criar + Header]
    C -->|SIM| E[Append mode]
    D --> F[writer.writeheader]
    E --> G[writer.writerow]
    F --> G
    G --> H[Nova linha persistida]
    
    style D fill:#51cf66
    style E fill:#339af0
    style H fill:#51cf66
```

**Modo de Escrita**: `append` (preserva histórico completo)

---

## 🎯 Fluxo Completo de Uma Sessão

```mermaid
sequenceDiagram
    participant U as User
    participant CMD as Command
    participant STATE as State File
    participant CSV as History CSV
    
    U->>CMD: start
    CMD->>STATE: CREATE current.json
    STATE-->>CMD: ✅ Created
    CMD-->>U: Sessão iniciada
    
    Note over U,CSV: Trabalhando...
    
    U->>CMD: pause "café"
    CMD->>STATE: READ current.json
    STATE-->>CMD: state (active)
    CMD->>STATE: UPDATE current.json<br/>(add current_pause)
    STATE-->>CMD: ✅ Updated
    CMD-->>U: Sessão pausada
    
    Note over U,CSV: Break...
    
    U->>CMD: resume
    CMD->>STATE: READ current.json
    STATE-->>CMD: state (paused)
    CMD->>STATE: UPDATE current.json<br/>(move to pauses[], clear current_pause)
    STATE-->>CMD: ✅ Updated
    CMD-->>U: Sessão retomada
    
    Note over U,CSV: Mais trabalho...
    
    U->>CMD: stop
    CMD->>STATE: READ current.json
    STATE-->>CMD: state (active)
    CMD->>STATE: UPDATE current.json<br/>(add end_time, calculate)
    STATE-->>CMD: ✅ Updated (completed)
    CMD->>CSV: APPEND history.csv
    CSV-->>CMD: ✅ Persisted
    CMD->>STATE: DELETE current.json
    STATE-->>CMD: ✅ Removed
    CMD-->>U: Sessão finalizada
```

---

## 🧪 Validação de Testes

Todos os cenários de decisão foram testados em `test_session_time_tracker.py`:

| Teste | Cenário | Estado Esperado | Atualização |
|-------|---------|-----------------|-------------|
| test_01 | Start nova sessão | State criado | ✅ CREATE |
| test_02 | Start com sessão ativa | Erro retornado | ❌ BLOCKED |
| test_03 | Pause → Resume | Pause movido para array | ✅ UPDATE |
| test_04 | Múltiplas pausas | 3 pausas no array | ✅ UPDATE × 6 |
| test_05 | Stop com pausa | CSV persistido | ✅ PERSIST + DELETE |
| test_06 | Stop enquanto pausado | Auto-resume → CSV | ⚠️ AUTO + PERSIST |
| test_07 | Pause sem sessão | Erro retornado | ❌ BLOCKED |
| test_08 | Resume sem pause | Erro retornado | ❌ BLOCKED |
| test_09 | Duplo pause | Erro retornado | ❌ BLOCKED |
| test_10 | Stats | Leitura CSV | 🔍 READ-ONLY |
| test_11 | Workflow completo | 3 pausas + CSV | ✅ ALL OPERATIONS |

**Resultado**: ✅ 11/11 passed — Todas decisões validadas

---

## 📌 Resumo da Lógica

### Quando ATUALIZAR State File?
1. ✅ **START**: Criar novo (apenas se não existir)
2. ✅ **PAUSE**: Atualizar existente (apenas se active)
3. ✅ **RESUME**: Atualizar existente (apenas se paused)
4. ✅ **STOP**: Atualizar temporariamente → depois deletar

### Quando ATUALIZAR CSV?
- ✅ **Apenas no STOP**: Append nova linha com sessão completa
- ❌ **Nunca nos outros comandos**: CSV é histórico imutável (append-only)

### Princípios de Decisão
1. **Idempotência**: Comandos inválidos retornam erro sem side effects
2. **Estado Explícito**: Sempre verificar arquivo antes de modificar
3. **Proteção de Dados**: Validar pré-condições antes de atualizar
4. **Recuperação Automática**: Auto-resume no stop se necessário
5. **Persistência Segura**: CSV append-only, state transitório

---

## 🔗 Referências

- **Código**: `scripts/session-time-tracker.py`
- **Testes**: `tests/test_session_time_tracker.py`
- **Test Report**: `docs/SESSIONS/2026-05-11/TIME_TRACKER_TEST_REPORT_2026-05-11.md`
- **Integration**: `.github/agents/session-manager.agent.md`
