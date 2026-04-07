# Architecture: SQLite FTS5 Decision

## Context
We need a full-text search system for the memory feature (IMP-59).

## Decision
Use SQLite FTS5 for the following reasons:
- Built-in (no external dependencies)
- Fast (BM25 ranking algorithm)
- Offline-first (no network required)
- Deterministic (same query = same results)

## Trade-offs
**Pros:**
- Zero setup complexity
- Predictable behavior
- Works on all platforms

**Cons:**
- Less precise than embeddings (no semantic similarity)
- Doesn't understand synonyms ("car" ≠ "automobile")

## Alternatives Considered
1. **Vector embeddings** (ChromaDB, pgvector): More precise but adds complexity
2. **Elasticsearch**: Overkill for this use case
3. **grep**: Too slow and no ranking

## Conclusion
FTS5 is sufficient for MVP. Can add embeddings later if needed.
