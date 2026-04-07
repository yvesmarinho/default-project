# Troubleshooting: Common Issues

## FTS5 Queries
**Issue**: FTS5 doesn't support leading wildcards (e.g., `*term`)
**Solution**: Use `LIKE` for prefix matching or create custom tokenizer

## Database Locks
**Issue**: "database is locked" error
**Solution**: Enable WAL mode: `PRAGMA journal_mode=WAL`

## Performance
**Issue**: Search is slow (>1s)
**Solution**:
- Build proper indices (category, updated_at)
- Limit result set (LIMIT 10)
- Use phrase queries ("exact match") instead of OR queries

## Secrets Detection
**Issue**: False positives (e.g., "password" in documentation)
**Solution**: Context-aware patterns (only match assignment: `password=...`)
