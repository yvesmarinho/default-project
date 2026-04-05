# IMP-59 — Mini-Engram Python: Design & Arquitetura

**Status**: 🟡 Design em andamento (trabalho paralelo com IMP-58)  
**Criado**: 2026-04-05  
**Decisão final**: Aguarda IMP-58 (2026-05-10)

---

## 🎯 Contexto e Motivação

### Por que este documento existe?

**Trabalho em paralelo**: Enquanto IMP-58 coleta dados (2-4 semanas), estamos preparando a arquitetura de IMP-59 para acelerar a implementação **SE** o decision gate der GO.

**Decision Gate** (2026-05-10):
- ✅ **GO**: Continuar implementação completa (40h)
- ❌ **MANTER**: Descartar este trabalho, manter apenas IMP-51 v2.0

### Objetivo do IMP-59

Implementar **memória ativa** (RAG-like) em Python puro, sem dependências externas complexas, reutilizando a infraestrutura de IMP-51 (SQLite + FTS5).

**Diferença para IMP-51**:
- **IMP-51** (memória passiva): Busca manual via `session-search`
- **IMP-59** (memória ativa): Sugestões proativas, injeção automática de contexto

---

## 📐 Arquitetura Proposta

### Estrutura de Diretórios

```
.memory/
├── memories/                    # Fonte versionável (commitável)
│   ├── project/                 # Memórias sobre o projeto
│   │   ├── architecture.md
│   │   ├── conventions.md
│   │   └── troubleshooting.md
│   ├── team/                    # Preferências da equipe
│   │   ├── coding-style.md
│   │   └── workflows.md
│   ├── sessions/                # Insights de sessões
│   │   ├── 2026-04-05_imp57.md
│   │   └── 2026-04-05_imp58.md
│   └── .templates/              # Templates de memória
│       ├── architecture.md
│       └── troubleshooting.md
├── index/                       # Cache não-versionável (gitignored)
│   ├── memory.db                # SQLite com FTS5
│   └── .gitignore               # Ignora *.db
├── MEMORY_POLICY.md             # Políticas de uso
└── README.md                    # Quickstart

scripts/
├── mem_save.py                  # CLI: salvar memória
├── mem_search.py                # CLI: buscar memória
├── mem_context.py               # CLI: contexto proativo
├── mem_mcp_server.py            # MCP server (integração VS Code)
└── lib/
    ├── memory.py                # Core: save/search/context
    └── sanitize.py              # Security: PII/secrets detection

tests/
├── test_memory_save.py          # 5 tests
├── test_memory_search.py        # 5 tests
├── test_memory_security.py      # 5 tests
└── test_memory_integration.py   # 5 tests
```

---

## 🗄️ Schema de Dados

### SQLite Schema (FTS5)

```sql
-- Tabela principal: metadados de memórias
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL UNIQUE,      -- .memory/memories/project/architecture.md
    title TEXT NOT NULL,                  -- Extraído do # heading
    category TEXT NOT NULL,               -- project|team|sessions|custom
    tags TEXT,                            -- JSON array: ["architecture", "design"]
    created_at TEXT NOT NULL,             -- ISO 8601
    updated_at TEXT NOT NULL,             -- ISO 8601
    size_bytes INTEGER,                   -- Tamanho do arquivo
    hash TEXT                             -- SHA256 (detect changes)
);

-- Índice FTS5: busca full-text
CREATE VIRTUAL TABLE memories_fts USING fts5(
    title,
    content,                              -- Conteúdo completo do .md
    tags,
    content=memories,                     -- Vinculado à tabela principal
    content_rowid=id
);

-- Triggers: sincronizar FTS5 com tabela principal
CREATE TRIGGER memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, title, content, tags)
    VALUES (new.id, new.title, (SELECT content FROM read_file(new.file_path)), new.tags);
END;

CREATE TRIGGER memories_au AFTER UPDATE ON memories BEGIN
    UPDATE memories_fts SET title=new.title, content=(SELECT content FROM read_file(new.file_path)), tags=new.tags
    WHERE rowid=new.id;
END;

CREATE TRIGGER memories_ad AFTER DELETE ON memories BEGIN
    DELETE FROM memories_fts WHERE rowid=old.id;
END;

-- Índices adicionais
CREATE INDEX idx_category ON memories(category);
CREATE INDEX idx_updated_at ON memories(updated_at DESC);
```

**Decisão de design**: Usar FTS5 nativo do SQLite (sem dependências externas) em vez de embeddings/vetores (simplicidade vs precisão).

---

## 🔧 Interface CLI

### 1. `mem_save.py` — Salvar memória

```bash
# Uso básico
python scripts/mem_save.py "Architecture decision: use SQLite FTS5" \
    --category project \
    --tags architecture,database,decision \
    --file .memory/memories/project/architecture.md

# Auto-categorização (inferir de contexto)
python scripts/mem_save.py "Preferimos snake_case em Python" --auto

# Append a arquivo existente
python scripts/mem_save.py "New ADR: avoid circular imports" \
    --file .memory/memories/project/architecture.md \
    --append

# Flags
  --category: project|team|sessions|custom
  --tags: comma-separated
  --file: path relativo a .memory/memories/
  --append: adicionar a arquivo existente (vs criar novo)
  --auto: auto-categorização via LLM ou keywords
```

**Output**:
```
✅ Memory saved
File: .memory/memories/project/architecture.md
Category: project
Tags: architecture, database, decision
Size: 342 bytes
Indexed: Yes
```

---

### 2. `mem_search.py` — Buscar memória

```bash
# Busca simples
python scripts/mem_search.py "como usar SQLite FTS5"

# Filtros
python scripts/mem_search.py "architecture" --category project
python scripts/mem_search.py "conventions" --tags python,style
python scripts/mem_search.py "IMP-57" --after 2026-04-01

# Flags
  --category: filtrar por categoria
  --tags: filtrar por tags (AND lógico)
  --after: memórias criadas após data
  --limit: número de resultados (padrão: 10)
  --json: output em JSON
```

**Output**:
```
Search Results
────────────────────────────────────────────────────────────
Query: "como usar SQLite FTS5"
Found: 3 result(s)
────────────────────────────────────────────────────────────

[1] Architecture Decision: SQLite FTS5 ⭐⭐⭐⭐⭐
    Category: project | Tags: architecture, database, decision
    Updated: 2026-04-05
    File: .memory/memories/project/architecture.md

    Preview:
    > We chose SQLite FTS5 for full-text search because it's built-in,
    > fast, and requires zero external dependencies. Unlike vector
    > embeddings (pgvector, ChromaDB), FTS5 works offline and has
    > predictable behavior.

────────────────────────────────────────────────────────────

[2] Troubleshooting: FTS5 queries
    Category: project | Tags: troubleshooting, sqlite
    Updated: 2026-04-03
    File: .memory/memories/project/troubleshooting.md

    Preview:
    > Common issue: FTS5 doesn't support wildcards at beginning (e.g., *term).
    > Solution: Use LIKE for prefix matching or create custom tokenizer.

────────────────────────────────────────────────────────────
```

---

### 3. `mem_context.py` — Contexto proativo

**Uso automático** (integrado em session-start):

```bash
# Analisar contexto da sessão atual e sugerir memórias relevantes
python scripts/mem_context.py --auto

# Manual: fornecer contexto explícito
python scripts/mem_context.py --query "implementar feature X" --task IMP-60
```

**Output**:
```
💡 Suggested Context for Current Session
────────────────────────────────────────────────────────────
Based on: Branch (018-copilot-instructions), Recent commits, Open files

📌 Relevant Memories:

[1] Copilot Instructions Best Practices (90% relevance)
    File: .memory/memories/team/copilot-guidelines.md
    Why: You're working on copilot-instructions; this contains team conventions

[2] Architecture: Session Docs (75% relevance)
    File: .memory/memories/project/architecture.md
    Why: Recent commits mention session-search and IMP-51

[3] Troubleshooting: Git commit issues (60% relevance)
    File: .memory/memories/project/troubleshooting.md
    Why: Pattern detected: git-commit-with-file.sh in recent commands

────────────────────────────────────────────────────────────
💬 Auto-inject these into Copilot context? (y/n):
```

---

## 🔐 Segurança — Sanitização PII/Secrets

### `scripts/lib/sanitize.py`

```python
import re
from typing import List, Tuple

# Patterns de detecção
PATTERNS = {
    "api_key": r"(api[_-]?key|apikey)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
    "token": r"(token|bearer)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
    "password": r"(password|passwd|pwd)\s*[=:]\s*['\"]?([^\s'\"]+)['\"]?",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "github_token": r"ghp_[a-zA-Z0-9]{36}",
}

def detect_secrets(text: str) -> List[Tuple[str, str]]:
    """Detect potential secrets/PII in text.
    
    Returns: List of (pattern_name, matched_value) tuples
    """
    findings = []
    for name, pattern in PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            value = match.group(2) if match.lastindex >= 2 else match.group(0)
            findings.append((name, value))
    return findings

def sanitize(text: str, redact: bool = True) -> Tuple[str, List[str]]:
    """Sanitize text by removing/redacting secrets.
    
    Args:
        text: Input text
        redact: If True, replace with [REDACTED]; if False, remove entirely
    
    Returns:
        (sanitized_text, list_of_warnings)
    """
    warnings = []
    sanitized = text
    
    for name, pattern in PATTERNS.items():
        matches = list(re.finditer(pattern, sanitized, re.IGNORECASE))
        if matches:
            warnings.append(f"Found {len(matches)} potential {name}(s)")
            for match in reversed(matches):  # Reverse to preserve indices
                replacement = "[REDACTED]" if redact else ""
                sanitized = sanitized[:match.start()] + replacement + sanitized[match.end():]
    
    return sanitized, warnings
```

**Uso em `mem_save.py`**:

```python
from lib.sanitize import detect_secrets, sanitize

content = read_user_input()

# 1. Detectar secrets
findings = detect_secrets(content)
if findings:
    print("⚠️  Warning: Potential secrets detected:")
    for pattern, value in findings:
        print(f"  - {pattern}: {value[:10]}...")
    
    if not confirm("Continue saving with redaction?"):
        sys.exit(1)
    
    # 2. Sanitizar
    content, warnings = sanitize(content, redact=True)
    for warning in warnings:
        print(f"  ✅ {warning}")

# 3. Salvar
save_memory(content)
```

---

## 🔍 Algoritmo de Busca (FTS5)

### Ranking de Relevância

```python
def search_memories(query: str, category: str = None, tags: List[str] = None, limit: int = 10):
    """Search memories with ranking.
    
    Ranking factors:
    1. FTS5 BM25 score (built-in)
    2. Tag match bonus (+10 per tag)
    3. Recency bonus (updated in last 7 days: +5)
    4. Title match bonus (query in title: +15)
    """
    
    sql = """
    SELECT 
        m.id,
        m.file_path,
        m.title,
        m.category,
        m.tags,
        m.updated_at,
        fts.rank AS bm25_score,
        -- Calcular score final
        (
            fts.rank * 100 +                                    -- BM25 base
            CASE WHEN m.title LIKE ? THEN 15 ELSE 0 END +       -- Title match
            CASE WHEN julianday('now') - julianday(m.updated_at) <= 7 THEN 5 ELSE 0 END +  -- Recency
            (LENGTH(m.tags) - LENGTH(REPLACE(m.tags, ?, ''))) * 10  -- Tag matches
        ) AS final_score
    FROM memories m
    JOIN memories_fts fts ON m.id = fts.rowid
    WHERE fts MATCH ?
    """
    
    filters = []
    params = [f"%{query}%", query, query]
    
    if category:
        filters.append("m.category = ?")
        params.append(category)
    
    if tags:
        for tag in tags:
            filters.append("m.tags LIKE ?")
            params.append(f"%{tag}%")
    
    if filters:
        sql += " AND " + " AND ".join(filters)
    
    sql += " ORDER BY final_score DESC LIMIT ?"
    params.append(limit)
    
    return db.execute(sql, params).fetchall()
```

**Trade-off**: FTS5 BM25 é menos preciso que embeddings, mas:
- ✅ Zero dependência externa (offline-first)
- ✅ Determinístico (mesma query = mesmo resultado)
- ✅ Rápido (<50ms para 1000 memórias)
- ❌ Não captura similaridade semântica ("carro" ≠ "automóvel")

**Decisão**: Para MVP, FTS5 suficiente. Se IMP-58 mostrar necessidade, avaliar embeddings lightweight (sentence-transformers).

---

## 🔗 Integração com Session System

### Atualizar `session-start.prompt.md`

```markdown
## Step 4: Load Relevant Context (Memory)

**BEFORE** starting work, search for relevant memories:

1. Run memory context suggestion:
   ```bash
   python scripts/mem_context.py --auto
   ```

2. Review suggested memories (top 3-5 most relevant)

3. If helpful, ask user:
   "💡 I found these relevant memories:
   - [Memory 1 title]
   - [Memory 2 title]
   
   Would you like me to load them into context?"

4. If yes, read the memory files and incorporate context into planning
```

### Atualizar `session-end.prompt.md`

```markdown
## Step 5: Save Session Insights (Memory)

**AFTER** completing work, save important insights:

1. Identify saveable insights:
   - Architecture decisions made
   - Problems solved (and how)
   - Patterns discovered
   - Mistakes avoided

2. Ask user:
   "Would you like to save any insights from this session to memory?"
   
   Examples:
   - "Learned: SQLite FTS5 doesn't support leading wildcards"
   - "Decision: Use Python stdlib only for memory system"
   - "Troubleshooting: Fixed deadlock by using WAL mode"

3. If yes, use `mem_save.py`:
   ```bash
   python scripts/mem_save.py "Insight text" \
       --category sessions \
       --tags IMP-59,memory,sqlite \
       --file .memory/memories/sessions/2026-04-05_imp59.md
   ```
```

---

## 🧪 Estratégia de Testes

### Test Coverage (20 tests)

**`test_memory_save.py`** (5 tests):
1. `test_save_simple_memory` - salvar memória básica
2. `test_save_with_tags` - tags e categorização
3. `test_save_append` - append a arquivo existente
4. `test_save_duplicate` - evitar duplicatas (mesmo file_path)
5. `test_save_index_update` - verificar FTS5 atualizado

**`test_memory_search.py`** (5 tests):
1. `test_search_simple` - busca básica
2. `test_search_with_filters` - category + tags
3. `test_search_ranking` - verificar ordem de relevância
4. `test_search_empty_db` - DB vazio retorna gracefully
5. `test_search_special_chars` - query com caracteres especiais

**`test_memory_security.py`** (5 tests):
1. `test_detect_api_key` - detectar API keys
2. `test_detect_password` - detectar passwords
3. `test_sanitize_redact` - redação de secrets
4. `test_sanitize_email` - PII (emails)
5. `test_save_with_secrets_blocked` - bloquear save se secrets detectados

**`test_memory_integration.py`** (5 tests):
1. `test_end_to_end_save_search` - salvar → buscar
2. `test_context_suggestion` - mem_context.py sugestões
3. `test_session_integration` - integração com session-start/end
4. `test_rebuild_index` - recriar DB de .md files
5. `test_concurrent_access` - SQLite WAL mode (múltiplos processos)

---

## 📊 POC — Proof of Concept

### Objetivo do POC

Validar viabilidade técnica **ANTES** de implementação completa:
1. ✅ FTS5 funciona para busca de memórias?
2. ✅ Performance aceitável (<100ms para 1000 memórias)?
3. ✅ Sanitização de secrets é confiável?
4. ✅ Integração com SQLite é estável?

### Estrutura do POC

```
poc/
├── mem_poc.py               # Script standalone (200 linhas)
├── test_data/               # Memórias de exemplo
│   ├── architecture.md
│   ├── troubleshooting.md
│   └── conventions.md
└── README.md                # Instruções de teste
```

**`mem_poc.py`** (simplificado):
```python
#!/usr/bin/env python3
"""Mini-Engram POC — Test FTS5 search and sanitization."""

import sqlite3
import hashlib
from pathlib import Path

DB_PATH = "poc/memory.db"
MEMORIES_PATH = "poc/test_data"

def init_db():
    """Create SQLite DB with FTS5."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY,
            file_path TEXT UNIQUE,
            title TEXT,
            content TEXT
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts 
        USING fts5(title, content, content=memories, content_rowid=id)
    """)
    return conn

def index_memory(conn, file_path: Path):
    """Index a markdown file."""
    content = file_path.read_text()
    title = content.split('\n')[0].strip('# ')
    
    conn.execute(
        "INSERT OR REPLACE INTO memories (file_path, title, content) VALUES (?, ?, ?)",
        (str(file_path), title, content)
    )
    conn.execute(
        "INSERT INTO memories_fts (rowid, title, content) VALUES ((SELECT id FROM memories WHERE file_path = ?), ?, ?)",
        (str(file_path), title, content)
    )
    conn.commit()

def search(conn, query: str, limit: int = 5):
    """Search memories."""
    results = conn.execute("""
        SELECT m.title, m.file_path, fts.rank
        FROM memories m
        JOIN memories_fts fts ON m.id = fts.rowid
        WHERE fts MATCH ?
        ORDER BY fts.rank
        LIMIT ?
    """, (query, limit)).fetchall()
    return results

# Main
conn = init_db()

# Index all .md files
for md_file in Path(MEMORIES_PATH).glob("*.md"):
    print(f"Indexing: {md_file}")
    index_memory(conn, md_file)

# Test search
query = input("Search query: ")
results = search(conn, query)

print(f"\nResults for '{query}':")
for title, path, rank in results:
    print(f"  [{rank:.2f}] {title} ({path})")
```

**Critérios de Sucesso do POC**:
- ✅ Índice criado sem erros
- ✅ Busca retorna resultados relevantes
- ✅ Performance <100ms (medir com `time`)
- ✅ Sanitização bloqueia API keys/passwords

---

## 🚧 Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| FTS5 não suficiente (vs embeddings) | Média | Alto | POC antes; se insuficiente, avaliar sentence-transformers |
| Performance ruim (>1s para 10k memórias) | Baixa | Médio | Benchmark POC; otimizar índices; limitar a 5k memórias |
| Secrets vazados em commits | Baixa | **CRÍTICO** | Pre-commit hook obrigatório; testes de segurança |
| Conflitos de schema (múltiplos devs) | Média | Baixo | Migration scripts; versionar schema |
| SQLite corrupção de DB | Baixa | Médio | WAL mode; backups automáticos; rebuild de .md files |

---

## 📈 Roadmap de Implementação (SE GO)

### Fase 1: Core (16h)
- [ ] Estrutura de pastas `.memory/`
- [ ] `scripts/lib/memory.py` (save/search)
- [ ] `scripts/mem_save.py` CLI
- [ ] `scripts/mem_search.py` CLI
- [ ] Schema SQLite + migrations
- [ ] Tests básicos (10 tests)

### Fase 2: Security (8h)
- [ ] `scripts/lib/sanitize.py`
- [ ] Pre-commit hook `.git/hooks/pre-commit`
- [ ] `.gitleaks-memory.toml`
- [ ] `MEMORY_POLICY.md`
- [ ] Tests de segurança (5 tests)

### Fase 3: Integration (8h)
- [ ] `scripts/mem_context.py`
- [ ] Atualizar `session-start.prompt.md`
- [ ] Atualizar `session-end.prompt.md`
- [ ] MCP server `scripts/mem_mcp_server.py` (opcional)
- [ ] Tests de integração (5 tests)

### Fase 4: Polish (8h)
- [ ] Documentação (`README.md`)
- [ ] Templates de memória (`.memory/memories/.templates/`)
- [ ] Performance benchmarks
- [ ] Disaster recovery (`make mem-rebuild`)
- [ ] Observability (`make mem-stats`)

---

## ❓ Perguntas em Aberto (para debate)

### 1. Embeddings vs FTS5?

**Opções**:
- **A)** FTS5 puro (decisão atual) - simplicidade, zero deps
- **B)** Hybrid: FTS5 + embeddings lightweight (sentence-transformers)
- **C)** Embeddings only (ChromaDB, pgvector) - melhor semântica

**Decisão pendente**: Aguardar POC e feedback IMP-58

### 2. MCP Server necessário?

**Opções**:
- **A)** CLI apenas (mais simples, suficiente para prompts)
- **B)** MCP server (integração nativa VS Code, requer `mcp` package)

**Decisão pendente**: Ver se IMP-58 mostra necessidade de auto-sugestão

### 3. Limite de memórias?

**Opções**:
- **A)** Ilimitado (confiar em SQLite scaling)
- **B)** Soft limit 5.000 memórias (warning se ultrapassar)
- **C)** Hard limit 10.000 (errors se ultrapassar)

**Decisão pendente**: Benchmark POC com 10k memórias

### 4. Auto-categorização?

**Opções**:
- **A)** Manual apenas (usuário escolhe category + tags)
- **B)** Semi-auto (sugerir tags via keywords, usuário confirma)
- **C)** Full-auto (LLM classifica, usuário pode override)

**Decisão pendente**: Depende de complexidade; começar com A

---

## 📝 Notas de Implementação

### Reutilização de IMP-51

**Código compartilhado**:
- `scripts/lib/search.py` → renomear para `scripts/lib/fts.py` (genérico)
- Funções `create_fts_table()`, `insert_fts()`, `search_fts()` → reutilizar

**Diferenças**:
- IMP-51: índice em `docs/SESSIONS/.search/session_index.db`
- IMP-59: índice em `.memory/index/memory.db`
- Schema diferente (adicionar tags, category, metadata)

### Versionamento de Schema

**Migration Strategy**:
```python
SCHEMA_VERSION = 1

def migrate_schema(conn):
    """Apply migrations if needed."""
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    
    if current < 1:
        # Migration 1: Initial schema
        conn.executescript(INITIAL_SCHEMA)
        conn.execute("PRAGMA user_version = 1")
    
    # Future migrations
    # if current < 2:
    #     conn.executescript(MIGRATION_2)
    #     conn.execute("PRAGMA user_version = 2")
```

---

## 🎯 Critérios de Sucesso (POC)

Para prosseguir com implementação completa (pós-IMP-58 GO), o POC deve demonstrar:

1. ✅ **Funcionalidade**: Save + search funcionam end-to-end
2. ✅ **Performance**: <100ms para search em 1000 memórias
3. ✅ **Segurança**: Sanitização detecta API keys, passwords, emails
4. ✅ **Confiabilidade**: SQLite WAL mode suporta concorrência
5. ✅ **Simplicidade**: Código <500 linhas (core), fácil de entender

**Se POC falhar**: Revisar decisão ou considerar IMP-45 (Engram oficial)

---

## 📚 Referências

- [IMP-58 Decision Gate](IMP-58_README.md) - Processo de avaliação
- [IMP-51 Implementation](../scripts/lib/search.py) - FTS5 existente
- [SQLite FTS5 Docs](https://www.sqlite.org/fts5.html) - Documentação oficial
- [DEBATE_ENGRAM_INTEGRATION](debates/DEBATE_ENGRAM_INTEGRATION_2026-04-05.md) - Contexto estratégico

---

**Status**: 🟡 Design completo, aguardando POC  
**Próximo**: Implementar POC isolado (4h)  
**Decisão final**: 2026-05-10 (pós-IMP-58)
