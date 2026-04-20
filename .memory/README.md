# Mini-Engram Memory System

**Status**: ✅ Active (IMP-59)
**Purpose**: Persistent memory for GitHub Copilot context retention
**Architecture**: Text-first (markdown source + SQLite FTS5 cache)

---

## 🎯 Quick Start (5 minutes)

### 1. Save a Memory

```bash
# Save a decision/learning/pattern
python scripts/mem_save.py \
  --title "API Authentication Pattern" \
  --content "Use JWT tokens with 1h expiration, refresh tokens stored in httpOnly cookies" \
  --category project \
  --tags "api,security,jwt"
```

### 2. Search Memories

```bash
# Find relevant memories
python scripts/mem_search.py "JWT authentication"

# With filters
python scripts/mem_search.py \
  --query "database migration" \
  --category project \
  --limit 5
```

### 3. Get Context (Proactive)

```bash
# Auto-suggest relevant memories based on current work
python scripts/mem_context.py --auto
```

---

## 📁 Directory Structure

```
.memory/
├── memories/                  # Source of truth (versionable, committa
ble)
│   ├── project/               # Project-level memories (architecture, patterns)
│   │   ├── 2026-04-20__api-authentication-pattern.md
│   │   └── 2026-04-15__database-migration-strategy.md
│   ├── team/                  # Team-level memories (onboarding, processes)
│   │   └── 2026-04-01__deployment-checklist.md
│   ├── sessions/              # Session-specific learnings
│   │   └── 2026-04-20__imp-59-implementation-notes.md
│   └── .templates/            # Example templates
│       └── example_decision.md
├── index/                     # SQLite cache (gitignored, rebuildable)
│   ├── memory.db              # FTS5 index
│   └── .gitignore             # Ignores *.db files
├── README.md                  # This file
└── MEMORY_POLICY.md           # Security and usage policies

```

---

## 💡 Core Concepts

### Source of Truth: Markdown Files

All memories are stored as **markdown files** in `.memory/memories/`:

```markdown
---
title: API Authentication Pattern
category: project
tags: api, security, jwt
created: 2026-04-20T14:30:00
updated: 2026-04-20T14:30:00
---

# API Authentication Pattern

## Decision
Use JWT tokens with 1h expiration for API authentication.

## Rationale
- Stateless (no server-side session storage)
- Short expiration minimizes risk if token is compromised
- Refresh tokens (httpOnly cookies) allow seamless renewal

## Implementation
```python
# Generate JWT
token = jwt.encode({"user_id": 123, "exp": datetime.now() + timedelta(hours=1)}, SECRET_KEY)
```

## Consequences
- Requires HTTPS for secure transmission
- Token revocation requires blacklist (add to Redis)
```

**Why markdown?**
- ✅ **Versionable**: Commit to Git like any other code
- ✅ **Human-readable**: No proprietary formats
- ✅ **Searchable**: Grep, ripgrep, VS Code search all work
- ✅ **Portable**: Works without database

### Index: SQLite FTS5 Cache

The `.memory/index/memory.db` database is a **cache** for fast full-text search:

- **Gitignored**: Not committed (listed in `.memory/index/.gitignore`)
- **Rebuildable**: Run `python scripts/mem_rebuild.py` to recreate from markdown files
- **FTS5**: Porter stemming + Unicode61 tokenization for multilingual search

**Why SQLite?**
- ✅ **Fast**: <100ms search across 1000s of memories
- ✅ **Zero config**: Single file, no server required
- ✅ **FTS5**: Built-in full-text search with BM25 ranking
- ✅ **Concurrent**: WAL mode supports multiple readers

---

## 🔍 Search Capabilities

### Basic Search

```bash
# Simple keyword search
python scripts/mem_search.py "database migration"
```

Output:
```
🔍 Found 3 results for query: database migration

1. Database Migration Strategy (score: -2.45)
   Category: project | Tags: database, migration
   Updated: 2026-04-15
   Snippet: Use Alembic for database migrations with rollback support...
   File: .memory/memories/project/2026-04-15__database-migration-strategy.md

2. Zero-Downtime Deployment (score: -3.12)
   Category: project | Tags: deployment, database
   Updated: 2026-04-10
   Snippet: For database schema changes, use blue-green deployment...
   File: .memory/memories/project/2026-04-10__zero-downtime-deployment.md
```

### Advanced Search (FTS5 Syntax)

```bash
# Boolean operators
python scripts/mem_search.py "database AND migration"
python scripts/mem_search.py "jwt OR oauth"
python scripts/mem_search.py "deployment NOT kubernetes"

# Phrase search
python scripts/mem_search.py '"zero downtime deployment"'

# Proximity search (words within N tokens)
python scripts/mem_search.py "database NEAR/5 migration"
```

### Filters

```bash
# By category
python scripts/mem_search.py --query "authentication" --category project

# By tags
python scripts/mem_search.py --query "API" --tags api,security

# By date
python scripts/mem_search.py --query "refactor" --after 2026-04-01
```

---

## 🚀 Workflows

### Workflow 1: Save Decision After Completing Task

```bash
# After completing IMP-XX
python scripts/mem_save.py \
  --title "IMP-59: Mini-Engram Architecture" \
  --content "$(cat docs/IMP-59_DESIGN.md)" \
  --category project \
  --tags "imp-59,architecture,memory"
```

### Workflow 2: Search Before Starting New Task

```bash
# Before starting new feature
python scripts/mem_search.py "authentication API"

# Read relevant memories
cat .memory/memories/project/2026-04-20__api-authentication-pattern.md
```

### Workflow 3: Proactive Context (Auto-Suggest)

```bash
# At start of session (auto-detect from git)
python scripts/mem_context.py --auto

# Manual query
python scripts/mem_context.py --query "database performance"

# Task-specific context
python scripts/mem_context.py --task IMP-60

# JSON output for automation
python scripts/mem_context.py --auto --json
```

Output example:
```
💡 Suggested Context for Current Session

Based on: Branch: 060-mini-engram-python, Recent commits: IMP-59 Phase 4, mem_context implementation

[1] IMP-59: Mini-Engram Architecture (95% relevance)
    Category: project | Updated: 2026-04-20
    Why: Title matches 2 keyword(s); Tags match: imp-59, architecture; Branch context
    File: .memory/memories/project/2026-04-20__imp-59-architecture.md

[2] SQLite FTS5 Performance Tuning (78% relevance)
    Category: project | Updated: 2026-04-15
    Why: Title matches 1 keyword(s); Snippet context; Recent (6 days)
    File: .memory/memories/project/2026-04-15__sqlite-fts5-tuning.md
```

**How context analysis works**:
- **Auto mode**: Analyzes current git branch + recent commits (top 10 keywords)
- **Query mode**: Uses your explicit search terms
- **Task mode**: Extracts task ID and searches related memories
- **Relevance scoring** (0-100%):
  - BM25 base score (0-30 points)
  - Title match (20 points)
  - Snippet match (15 points)
  - Tag match (15 points)
  - Category bonus (10 for project, 5 for team)
  - Recency bonus (10 for <7 days, 5 for <30 days)
  - Context match (task/branch keywords)

---

## 🔒 Security & Compliance

**See [MEMORY_POLICY.md](MEMORY_POLICY.md) for complete security policies.**

### Key Rules

❌ **NEVER save**:
- Credentials (passwords, tokens, API keys)
- PII (emails, phone numbers, SSNs, CPF)
- Connection strings with embedded passwords
- Output of: `kubectl get secret`, `cat .env`, `printenv`

✅ **DO save**:
- Architectural decisions
- Code patterns and best practices
- Learnings and troubleshooting notes
- Team processes and checklists
- References to where credentials are stored (NOT the credentials themselves)

**Example (WRONG)**:
```markdown
# Database Connection
postgresql://admin:MyP@ssw0rd@db.prod.company.com/app
```

**Example (CORRECT)**:
```markdown
# Database Connection
Database credentials stored in `.secrets/.db_credentials` (gitignored).
Connection string format: `postgresql://user:password@host:port/database`
```

---

## 🛠️ Maintenance

### Rebuild Index

If `.memory/index/memory.db` is corrupted or deleted:

```bash
python scripts/mem_rebuild.py
```

This scans all `.memory/memories/**/*.md` files and recreates the index.

### Statistics

```bash
python scripts/mem_stats.py
```

Output:
```
📊 Memory Statistics

Total memories: 47
Categories:
  - project: 32
  - team: 8
  - sessions: 7

Oldest: 2025-11-03
Newest: 2026-04-20
Tags: terraform (12), kubernetes (8), python (15), debugging (7)

Index size: 450 KB
Memory files: 2.3 MB
```

### Health Check

```bash
make memory-health
```

Checks:
- ✅ `.memory/` structure exists
- ✅ Index DB is valid (PRAGMA integrity_check)
- ✅ No secrets in memory files (gitleaks scan)

---

## 🧪 Testing

Run memory system tests:

```bash
# All tests (46 tests, <2s)
pytest tests/test_memory*.py -v

# Specific test suite
pytest tests/test_memory_save.py      # CLI save tests (7)
pytest tests/test_memory_search.py    # CLI search tests (7)
pytest tests/test_memory_security.py  # Security tests (14)
pytest tests/test_memory_context.py   # Context tests (18)
```

---

## 🎯 Makefile Integration

For convenience, memory commands are integrated into the project Makefile:

```bash
# Save a memory
make memory-save

# Search memories
make memory-search QUERY="database migration"

# Get context suggestions
make memory-context

# Rebuild index
make memory-rebuild

# Health check
make memory-health

# Run all tests
make memory-test
```

See `Makefile` for complete target definitions.

---

## 📚 Integration with Session System

Mini-Engram integrates with the existing session system (IMP-48/49/51):

| System | Purpose | Storage |
|--------|---------|---------|
| **Session History** (IMP-51) | Chronological log of activities | `docs/SESSIONS/*/DAILY_ACTIVITIES_*.md` |
| **Mini-Engram** (IMP-59) | Curated knowledge (decisions, learnings) | `.memory/memories/**/*.md` |

**Complementary, not redundant**:
- **Session history**: "What did I do?" (passive, comprehensive)
- **Mini-Engram**: "What did I learn?" (active, selective)

**Session integration hooks**:

1. **session-start.prompt.md**:
   ```markdown
   5. Check for relevant memories:
      ```bash
      python scripts/mem_context.py --auto
      ```
   ```

2. **session-end.prompt.md**:
   ```markdown
   7. Save key learnings to memory:
      - If you made an architectural decision → `mem_save --category project`
      - If you discovered a pattern → `mem_save --category project`
      - If you documented a process → `mem_save --category team`
   ```

---

## 🔗 Related Documentation

- [MEMORY_POLICY.md](MEMORY_POLICY.md) — Security and usage policies
- [IMP-59_DESIGN.md](../docs/IMP-59_DESIGN.md) — Architecture and design decisions
- [IMP-59_IMPLEMENTATION_PLAN.md](../docs/IMP-59_IMPLEMENTATION_PLAN.md) — Implementation plan (6 phases)
- [docs/SESSIONS/](../docs/SESSIONS/) — Session history (IMP-48/49/51)

---

## ❓ FAQ

### Q: Should I commit `.memory/memories/` to Git?

**A**: It depends on your use case:

- **YES** if memories are **project-level** (architecture, patterns, team processes) → valuable for team
- **NO** if memories are **personal** (session notes, personal learnings) → not relevant to team

Recommendation: Commit `.memory/memories/project/` and `.memory/memories/team/`, exclude `.memory/memories/sessions/` (add to `.gitignore` if desired).

### Q: What if `.memory/index/memory.db` is deleted?

**A**: No problem! Run `python scripts/mem_rebuild.py` to recreate from markdown files.

### Q: Can I edit markdown files directly?

**A**: Yes! Edit `.memory/memories/**/*.md` files directly, then run `python scripts/mem_rebuild.py` to update the index.

### Q: How is this different from Engram official?

**A**: 

| Feature | Mini-Engram (IMP-59) | Engram Official (IMP-45) |
|---------|---------------------|-------------------------|
| Implementation | Python stdlib | Go binary (external) |
| Dependencies | Zero (Python 3.10+) | Requires binary installation |
| MCP Server | Python (planned) | Go native |
| Performance | Good (<100ms) | Excellent (<50ms) |
| Maintenance | Template-controlled | Upstream-controlled |
| Features | Core (save, search, context) | Core + extras |

**Decision**: Start with Mini-Engram (faster, zero deps), migrate to Engram official if inadequate (see IMP-45).

---

## 📦 Implementation Status

| Phase | Status | Tests | Commit |
|-------|--------|-------|--------|
| 1. Structure | ✅ Complete | 4 smoke | `4845fc7` |
| 2. CLI Tools | ✅ Complete | 14 | `dec06a0` |
| 3. Security | ✅ Complete | 14 | `ca12487` |
| 4. Context | ✅ Complete | 18 | `513fe59` |
| 5. Final Tests | ✅ Complete | 46 total | — |
| 6. Documentation | ✅ Complete | — | TBD |

**Total**: 46/46 tests passing (<2s), zero dependencies, production-ready.

---

**Version**: 1.0.0 (IMP-59 Complete)
**Last updated**: 2026-04-20
**Implementation**: [docs/IMP-59_IMPLEMENTATION.md](../docs/IMP-59_IMPLEMENTATION.md)
