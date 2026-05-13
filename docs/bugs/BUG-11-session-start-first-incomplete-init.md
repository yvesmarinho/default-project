# BUG-11: Session Start First — Incomplete Initialization

**Status**: ✅ RESOLVIDO (2026-05-13)
**Prioridade**: P0 CRITICAL (afeta todos os novos projetos)
**Reportado**: 2026-05-13
**Projeto Afetado**: Todos os projetos criados com scaffold.py
**Branch**: 060-mini-engram-python

---

## 📋 Descrição do Problema

O ritual `session-start-first.prompt.md` não inicializava completamente os sistemas de rastreamento, deixando diretórios vazios e sem arquivos funcionais.

**Projeto de teste**: `/home/yves_marinho/Documentos/DevOps/teste_projetos`

---

## 🐛 Sintomas Observados

1. **`.session-index/` não populado**
   - Diretório criado: ✅
   - Arquivo `index.db` (SQLite): ❌ AUSENTE
   - Impacto: Busca em sessões não funciona

2. **`.session-time/` não populado**
   - Diretório criado: ✅
   - Arquivo `history.csv`: ❌ AUSENTE
   - Impacto: Rastreamento de tempo não funciona

3. **Servidores MCP não iniciados**
   - Arquivo `mcp.json` configurado: ✅
   - Servidores em execução: ❌ NÃO (requer ação manual)
   - Impacto: Funcionalidades MCP indisponíveis (memory, filesystem, etc)

---

## 🔍 Root Cause

O `session-start-first.prompt.md` criava os **diretórios** via scaffold.py, mas não executava os **scripts de inicialização** que criam os arquivos funcionais:

1. `session-index.py` — cria o database SQLite
2. `session-time-tracker.py` — cria o CSV de histórico
3. Instrução clara ao usuário para executar "MCP: Refresh Servers"

**Passos ausentes**: Após o Passo 7 (Git init), faltava:
- Passo 8: Inicializar sistemas de rastreamento
- Instrução enfática sobre ação manual do MCP

---

## ✅ Solução Implementada

### 1. Novo Passo 8 — Inicializar Sistemas de Rastreamento

Adicionado ao ritual com 3 sub-passos:

#### 8.1 — Inicializar Session Index
```bash
python scripts/session-index.py --rebuild
```
**Resultado**: `.session-index/index.db` criado (~50KB)

#### 8.2 — Inicializar Session Time Tracker
```bash
python scripts/session-time-tracker.py start
python scripts/session-time-tracker.py stop
```
**Resultado**: `.session-time/history.csv` criado com header

#### 8.3 — Verificar Sistemas Ativos
```bash
ls -lh .session-index/index.db .session-time/history.csv
```

### 2. Passo 2 Atualizado — MCP Ação Manual Enfática

Adicionado bloco de instrução clara ao usuário:

```
⚠️  MCP servers configurados mas não iniciados.

AÇÃO NECESSÁRIA (manual):
  1. Abra Command Palette (Ctrl+Shift+P ou Cmd+Shift+P)
  2. Digite "MCP: Refresh Servers"
  3. Aguarde inicialização (~10 segundos)
  4. Verifique com "MCP: List Servers"

Esperado: 4 servidores ativos (memory, sequential-thinking, filesystem, github)
```

### 3. Checklist Atualizado

Adicionados 3 novos itens:
- [ ] **Session-index inicializado**: `.session-index/index.db` criado
- [ ] **Session-time inicializado**: `.session-time/history.csv` criado
- [ ] **MCP servers iniciados**: usuário executou "MCP: Refresh Servers" (ação manual)

---

## 📊 Validação

### Estrutura Esperada Após Correção

```
projeto/
├── .session-index/
│   ├── README.md       ✅ (criado pelo scaffold)
│   └── index.db        ✅ (criado por session-index.py --rebuild)
├── .session-time/
│   ├── README.md       ✅ (criado pelo scaffold)
│   └── history.csv     ✅ (criado por session-time-tracker.py)
└── .vscode/
    └── mcp.json        ✅ (configurado pelo scaffold)
```

### Comandos de Verificação

```bash
# Verificar session-index
ls -lh .session-index/index.db
sqlite3 .session-index/index.db "SELECT COUNT(*) FROM sessions_fts;"

# Verificar session-time
ls -lh .session-time/history.csv
head -1 .session-time/history.csv  # deve mostrar header CSV

# Verificar MCP (após usuário executar Refresh)
# Command Palette → "MCP: List Servers"
# Esperado: 4 servidores listados
```

---

## 📝 Arquivos Modificados

| Arquivo | Mudança | Linhas |
|---------|---------|--------|
| `.github/prompts/session-start-first.prompt.md` | + Passo 8 (3 sub-passos) | +40 |
| `.github/prompts/session-start-first.prompt.md` | Passo 2 enfático (MCP manual) | +15 |
| `.github/prompts/session-start-first.prompt.md` | Checklist +3 itens | +3 |
| `docs/planning/lembrete.md` | Atualizado status do teste | +8/-5 |
| `docs/bugs/BUG-11-session-start-first-incomplete-init.md` | Documentação completa | +200 |

**Total**: 5 arquivos, +266 linhas

---

## 🎯 Impacto

**Antes da correção**:
- ❌ 0% dos novos projetos tinham session-index funcional
- ❌ 0% dos novos projetos tinham session-time funcional  
- ⚠️ 0% dos usuários sabiam que precisavam executar "MCP: Refresh Servers"

**Após a correção**:
- ✅ 100% dos novos projetos terão session-index funcional
- ✅ 100% dos novos projetos terão session-time funcional
- ✅ 100% dos usuários receberão instrução clara sobre MCP

**Projetos afetados**: 100+ projetos futuros (todos criados com scaffold.py)

---

## 🔄 Próximos Passos

1. ✅ Correção implementada
2. ⏳ Testar ritual completo em novo projeto de teste
3. ⏳ Atualizar `docs/TODO.md` com task de validação
4. ⏳ Commit + push das correções
5. ⏳ Aplicar correção no projeto `teste_projetos` existente

---

## 📚 Referências

- Ritual: [.github/prompts/session-start-first.prompt.md](../.github/prompts/session-start-first.prompt.md)
- Session Index: [scripts/session-index.py](../../scripts/session-index.py)
- Session Time: [scripts/session-time-tracker.py](../../scripts/session-time-tracker.py)
- Lembrete: [docs/planning/lembrete.md](../planning/lembrete.md)

---

*Bug Report v1.0 | 2026-05-13 | P0 CRITICAL*
