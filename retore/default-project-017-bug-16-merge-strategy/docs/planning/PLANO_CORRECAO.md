# Plano de Correção — Session Start (First Time)

**Projeto**: test-workspace-fix
**Data**: 2026-05-13
**Status**: ✅ Scaffold upgrade executado, ⚠️ Inicialização pendente

---

## 📋 Resumo Executivo

**Situação atual**:
- ✅ Scaffold upgrade executado com sucesso (2026-05-13 13:56)
- ✅ Scripts de rastreamento copiados (BUG-11/BUG-12 resolvidos)
- ⚠️ Sistemas NÃO inicializados (comandos não executados)
- ⚠️ Ritual parcialmente completo (58% de conformidade)

**Objetivo**: Atingir 100% de conformidade com o checklist do `session-start-first.prompt.md`

---

## 🚀 Execução — 4 Passos Simples

### Passo 1 — Inicializar Todos os Sistemas (P0 — CRÍTICO)

**Script automático criado**: `scripts/tmp/init_all_systems.py`

```bash
cd /caminho/para/test-workspace-fix
python scripts/tmp/init_all_systems.py
```

**O que faz**:
1. ✅ Inicializa Session Index (`.session-index/index.db`)
2. ✅ Inicializa Session Time (`.session-time/history.csv`)
3. ✅ Inicializa Memory System (`.memory/memories/`)

**Resultado esperado**:
```
🚀 Inicializando sistemas de rastreamento...
   Projeto: test-workspace-fix

1️⃣  Session Index...
   ✅ Criado: index.db (50.0 KB)

2️⃣  Session Time Tracker...
   ▶️  Iniciando sessão...
   ⏹️  Parando sessão...
   ✅ Criado: history.csv

3️⃣  Memory System...
   ✅ Criadas 4 pastas: project, team, sessions, .templates

============================================================
✅ TODOS OS SISTEMAS INICIALIZADOS COM SUCESSO!
============================================================
```

---

### Passo 2 — Verificar Symlinks (P1 — ALTO)

```bash
cd /caminho/para/test-workspace-fix
uv run scripts/scaffold.py --check
```

**Resultado esperado**:
```
✅ Symlinks verificados
```

---

### Passo 3 — Atualizar docs/TODO.md (P1 — ALTO)

**Ação manual**: Editar `docs/TODO.md` com os primeiros objetivos do projeto.

**Template**:
```markdown
# TODO — test-workspace-fix

## 🎯 Objetivos Imediatos

- [ ] Completar inicialização do projeto
- [ ] Definir escopo e requisitos iniciais
- [ ] Configurar CI/CD básico

## 📋 Backlog

(adicionar itens conforme necessário)
```

---

### Passo 4 — Declarar Domínio e Carregar Profile (P1 — ALTO)

**Adicionar ao** `SESSION_RECOVERY_2026-05-13.md`:

```markdown
---

## 🎯 Domínio e Objetivo

**Modo**: PROGRAMMING
**Projeto**: test-workspace-fix
**Linguagem**: python
**Objetivo desta primeira sessão**: Inicializar projeto e configurar sistemas de rastreamento

**Domain Profile carregado**: `.github/prompts/domain/devops-programming.prompt.md`

**Regras ativas**:
- `.copilot-rules.md` (genérico — Layer 1)
- `.copilot-rules-test-workspace-fix.md` (específico — Layer 3)

---
```

---

## ✅ Verificação de Conformidade

**Script de verificação criado**: `scripts/tmp/verify_first_session.py`

```bash
cd /caminho/para/test-workspace-fix
python scripts/tmp/verify_first_session.py
```

**Resultado esperado após correções**:
```
📊 Verificando conformidade: test-workspace-fix

1️⃣  Infraestrutura
  ✅ Ambiente virtual: pyvenv.cfg
  ✅ MCP config: mcp.json
  ✅ .gitignore: .gitignore
  ✅ .copilot-rules.md: .copilot-rules.md

2️⃣  Sistemas de Rastreamento
  ✅ Session Index DB: index.db
  ✅ Session Time CSV: history.csv
  ✅ Memory System

3️⃣  Scripts de Rastreamento
  ✅ Script: session-index.py
  ✅ Script: session-time-tracker.py
  ✅ Script: create_memory_structure.py

4️⃣  Documentação de Sessão
  ✅ docs/SESSIONS/2026-05-13/
  ✅ SESSION_RECOVERY
  ✅ DAILY_ACTIVITIES

5️⃣  Segurança
  ✅ .secrets/
  ✅ Git hook de segurança: pre-commit.secrets

============================================================
📊 Score: 16/16 (100%)
============================================================
✅ CONFORMIDADE TOTAL — Session Start (First Time) completo!
```

---

## 📝 Ação Manual Necessária — MCP Servers

**IMPORTANTE**: MCP servers não podem ser iniciados programaticamente.

**Instruir usuário**:
```
⚠️  Ação manual necessária:

1. Abra VS Code Command Palette (Ctrl+Shift+P ou Cmd+Shift+P)
2. Digite "MCP: Refresh Servers"
3. Aguarde inicialização (~10 segundos)
4. Verifique com "MCP: List Servers"

Esperado: 4 servidores ativos
  - memory
  - sequential-thinking
  - filesystem
  - github
```

---

## 📊 Checklist Final

Após executar os 4 passos acima:

- [x] Pré-requisitos: `uv`, `git`, `python3 ≥3.10`
- [x] Ambiente virtual criado: `.venv/`
- [x] MCP verificado
- [x] Scaffold executado + upgrade
- [x] Estrutura de diretórios
- [x] `.secrets/` protegido
- [ ] **Symlinks verificados** → **EXECUTAR PASSO 2**
- [x] Git inicializado
- [x] `.copilot-rules.md` lido
- [x] Scan de segurança LIMPO
- [ ] **Session-index inicializado** → **EXECUTAR PASSO 1**
- [ ] **Session-time inicializado** → **EXECUTAR PASSO 1**
- [ ] **Memory system inicializado** → **EXECUTAR PASSO 1**
- [ ] **MCP servers iniciados** → **AÇÃO MANUAL**
- [x] `docs/SESSIONS/[data]/` criada
- [ ] **`docs/TODO.md` atualizado** → **EXECUTAR PASSO 3**
- [ ] **Domínio declarado + Profile carregado** → **EXECUTAR PASSO 4**

---

## 🎯 Ordem de Execução Recomendada

```bash
# 1. Navegar para o projeto
cd /caminho/para/test-workspace-fix

# 2. Inicializar sistemas (P0)
python scripts/tmp/init_all_systems.py

# 3. Verificar symlinks (P1)
uv run scripts/scaffold.py --check

# 4. Verificar conformidade
python scripts/tmp/verify_first_session.py

# 5. Editar manualmente:
#    - docs/TODO.md (adicionar objetivos)
#    - SESSION_RECOVERY_2026-05-13.md (adicionar seção Domínio)

# 6. Instruir usuário para MCP: Refresh Servers
```

---

## 📚 Referências

- **Ritual completo**: `.github/prompts/session-start-first.prompt.md`
- **Regras P0**: `.copilot-rules.md` (seções 1-3)
- **Correções aplicadas**:
  - BUG-11: Session systems não inicializados
  - BUG-12: Memory system não inicializado
  - BUG-13: Copilot instructions not persisted
- **Análise detalhada**: `tmp/ANALISE_SESSION_START_FIRST.md`

---

**Criado em**: 2026-05-13
**Seguindo**: `.copilot-rules.md` P0 (ferramentas nativas, Python stdlib)
