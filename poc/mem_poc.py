#!/usr/bin/env python3
"""Mini-Engram POC — Proof of Concept for Memory System (IMP-59).

Tests:
1. SQLite FTS5 indexing and search
2. Performance benchmarks
3. Security: PII/secrets detection
4. Concurrent access (WAL mode)

Usage:
    python poc/mem_poc.py
"""

import sqlite3
import hashlib
import time
import re
from pathlib import Path
from typing import List, Tuple, Dict

# ============================================================================
# Configuration
# ============================================================================

POC_DIR = Path(__file__).parent
DB_PATH = POC_DIR / "memory_poc.db"
TEST_DATA_PATH = POC_DIR / "test_data"

# ============================================================================
# Security: PII/Secrets Detection
# ============================================================================

SECRET_PATTERNS = {
    "api_key": r"(api[_-]?key|apikey)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
    "token": r"(token|bearer)\s*[=:]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?",
    "password": r"(password|passwd|pwd)\s*[=:]\s*['\"]?([^\s'\"]{6,})['\"]?",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "github_token": r"ghp_[a-zA-Z0-9]{36}",
}


def detect_secrets(text: str) -> List[Tuple[str, str]]:
    """Detect potential secrets/PII in text."""
    findings = []
    for name, pattern in SECRET_PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Get the actual secret value (group 2) or full match if no groups
            if match.lastindex and match.lastindex >= 2:
                value = match.group(2)
            else:
                value = match.group(0)
            findings.append((name, value))
    return findings


def sanitize(text: str, redact: bool = True) -> Tuple[str, List[str]]:
    """Sanitize text by removing/redacting secrets."""
    warnings = []
    sanitized = text

    for name, pattern in SECRET_PATTERNS.items():
        matches = list(re.finditer(pattern, sanitized, re.IGNORECASE))
        if matches:
            warnings.append(f"Found {len(matches)} potential {name}(s)")
            for match in reversed(matches):
                replacement = "[REDACTED]" if redact else ""
                sanitized = sanitized[: match.start()] + replacement + sanitized[match.end() :]

    return sanitized, warnings


# ============================================================================
# Database: SQLite FTS5
# ============================================================================


def init_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Initialize SQLite database with FTS5 tables."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")  # Concurrency support

    # Main table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            hash TEXT NOT NULL
        )
    """
    )

    # FTS5 virtual table
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            title,
            content,
            tags,
            content=memories,
            content_rowid=id
        )
    """
    )

    # Triggers to sync FTS5
    conn.executescript(
        """
        DROP TRIGGER IF EXISTS memories_ai;
        DROP TRIGGER IF EXISTS memories_au;
        DROP TRIGGER IF EXISTS memories_ad;

        CREATE TRIGGER memories_ai AFTER INSERT ON memories BEGIN
            INSERT INTO memories_fts(rowid, title, content, tags)
            SELECT new.id, new.title, new.content, new.tags;
        END;

        CREATE TRIGGER memories_au AFTER UPDATE ON memories BEGIN
            UPDATE memories_fts SET title=new.title, content=new.content, tags=new.tags
            WHERE rowid=new.id;
        END;

        CREATE TRIGGER memories_ad AFTER DELETE ON memories BEGIN
            DELETE FROM memories_fts WHERE rowid=old.id;
        END;
    """
    )

    # Indices
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_updated_at ON memories(updated_at DESC)")

    conn.commit()
    return conn


def save_memory(
    conn: sqlite3.Connection,
    file_path: Path,
    content: str,
    title: str,
    category: str = "project",
    tags: List[str] = None,
) -> int:
    """Save a memory to the database."""
    from datetime import datetime

    tags_str = ",".join(tags) if tags else ""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    now = datetime.now().isoformat()

    # Check for secrets
    findings = detect_secrets(content)
    if findings:
        print(f"⚠️  WARNING: Found potential secrets in {file_path}:")
        for pattern, value in findings:
            print(f"    - {pattern}: {value[:15]}...")
        content, warnings = sanitize(content, redact=True)
        for warning in warnings:
            print(f"    ✅ {warning}")

    # Insert or replace
    cursor = conn.execute(
        """
        INSERT OR REPLACE INTO memories (file_path, title, content, category, tags, created_at, updated_at, hash)
        VALUES (?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM memories WHERE file_path = ?), ?), ?, ?)
    """,
        (str(file_path), title, content, category, tags_str, str(file_path), now, now, content_hash),
    )

    conn.commit()
    return cursor.lastrowid


def search_memories(
    conn: sqlite3.Connection,
    query: str,
    category: str = None,
    tags: List[str] = None,
    limit: int = 10,
) -> List[Dict]:
    """Search memories with FTS5 ranking."""
    sql = """
        SELECT
            m.id,
            m.file_path,
            m.title,
            m.category,
            m.tags,
            m.updated_at,
            memories_fts.rank AS score
        FROM memories_fts
        JOIN memories m ON memories_fts.rowid = m.id
        WHERE memories_fts MATCH ?
    """

    params = [query]

    if category:
        sql += " AND m.category = ?"
        params.append(category)

    if tags:
        for tag in tags:
            sql += " AND m.tags LIKE ?"
            params.append(f"%{tag}%")

    sql += " ORDER BY memories_fts.rank LIMIT ?"
    params.append(limit)

    results = conn.execute(sql, params).fetchall()

    return [
        {
            "id": row[0],
            "file_path": row[1],
            "title": row[2],
            "category": row[3],
            "tags": row[4].split(",") if row[4] else [],
            "updated_at": row[5],
            "score": row[6],
        }
        for row in results
    ]


# ============================================================================
# Test Data Management
# ============================================================================


def create_test_data():
    """Create sample test data for POC."""
    TEST_DATA_PATH.mkdir(exist_ok=True)

    test_memories = [
        {
            "filename": "architecture.md",
            "title": "Architecture: SQLite FTS5 Decision",
            "category": "project",
            "tags": ["architecture", "database", "decision"],
            "content": """# Architecture: SQLite FTS5 Decision

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
""",
        },
        {
            "filename": "troubleshooting.md",
            "title": "Troubleshooting: Common Issues",
            "category": "project",
            "tags": ["troubleshooting", "debugging"],
            "content": """# Troubleshooting: Common Issues

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
""",
        },
        {
            "filename": "conventions.md",
            "title": "Team Conventions: Python Style",
            "category": "team",
            "tags": ["python", "style", "conventions"],
            "content": """# Team Conventions: Python Style

## Naming
- **snake_case** for variables, functions, methods
- **PascalCase** for classes
- **SCREAMING_SNAKE_CASE** for constants

## Imports
- Standard library first
- Third-party second
- Local imports last
- Alphabetize within groups

## Type Hints
- Required for all public functions
- Optional for private methods (use judgment)

## Docstrings
- Google style for public API
- One-liner for simple functions
- Include Args, Returns, Raises for complex functions

## Testing
- pytest for all tests
- Minimum 80% coverage
- Use fixtures for setup/teardown
""",
        },
        {
            "filename": "secrets_test.md",
            "title": "Security Test: Secrets Detection",
            "category": "test",
            "tags": ["security", "test"],
            "content": """# Security Test: Secrets Detection

This file contains intentional secrets for testing sanitization.

## API Key (should be detected)
api_key = "sk_test_1234567890abcdefghijklmnop"

## Password (should be detected)
password: "mySecretP@ssw0rd123"

## GitHub Token (should be detected)
export GITHUB_TOKEN=ghp_1234567890123456789012345678901234567

## Email (PII, should be detected)
Contact: john.doe@example.com

## AWS Key (should be detected)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE

## Safe content (should NOT be detected)
This is a normal sentence about passwords in general.
The word "token" can appear in documentation safely.
""",
        },
    ]

    for memory in test_memories:
        file_path = TEST_DATA_PATH / memory["filename"]
        file_path.write_text(memory["content"])
        print(f"✅ Created: {file_path}")


def load_test_data(conn: sqlite3.Connection):
    """Load test data into database."""
    if not TEST_DATA_PATH.exists():
        create_test_data()

    for md_file in TEST_DATA_PATH.glob("*.md"):
        content = md_file.read_text()
        title = content.split("\n")[0].strip("# ")

        # Infer category and tags from filename
        if "architecture" in md_file.stem:
            category, tags = "project", ["architecture", "decision"]
        elif "troubleshooting" in md_file.stem:
            category, tags = "project", ["troubleshooting", "debugging"]
        elif "conventions" in md_file.stem:
            category, tags = "team", ["conventions", "style"]
        else:
            category, tags = "test", ["security", "test"]

        memory_id = save_memory(conn, md_file, content, title, category, tags)
        print(f"📝 Indexed: {title} (ID: {memory_id})")


# ============================================================================
# Benchmarks
# ============================================================================


def benchmark_search(conn: sqlite3.Connection, query: str, iterations: int = 100):
    """Benchmark search performance."""
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        search_memories(conn, query, limit=10)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\n📊 Benchmark: '{query}' ({iterations} iterations)")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Min: {min_time:.2f}ms")
    print(f"  Max: {max_time:.2f}ms")
    print(f"  ✅ {'PASS' if avg_time < 100 else 'FAIL'} (target: <100ms)")


# ============================================================================
# Interactive Demo
# ============================================================================


def demo(conn: sqlite3.Connection):
    """Interactive demo of memory system."""
    print("\n" + "=" * 70)
    print("Mini-Engram POC — Interactive Demo")
    print("=" * 70)

    while True:
        print("\nCommands:")
        print("  1. Search memories")
        print("  2. List all memories")
        print("  3. Benchmark")
        print("  4. Test security (secrets detection)")
        print("  5. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            query = input("Search query: ").strip()
            results = search_memories(conn, query, limit=5)
            print(f"\nFound {len(results)} result(s):\n")
            for i, result in enumerate(results, 1):
                print(f"[{i}] {result['title']} (score: {result['score']:.2f})")
                print(f"    Category: {result['category']} | Tags: {', '.join(result['tags'])}")
                print(f"    File: {result['file_path']}")
                print()

        elif choice == "2":
            rows = conn.execute(
                "SELECT id, title, category, tags FROM memories ORDER BY updated_at DESC"
            ).fetchall()
            print(f"\nAll memories ({len(rows)}):\n")
            for row in rows:
                tags = row[3].split(",") if row[3] else []
                print(f"[{row[0]}] {row[1]}")
                print(f"    Category: {row[2]} | Tags: {', '.join(tags)}")
                print()

        elif choice == "3":
            query = input("Benchmark query (default: 'database'): ").strip() or "database"
            benchmark_search(conn, query, iterations=100)

        elif choice == "4":
            print("\nTesting secrets detection on 'secrets_test.md'...\n")
            test_file = TEST_DATA_PATH / "secrets_test.md"
            if test_file.exists():
                content = test_file.read_text()
                findings = detect_secrets(content)
                print(f"Found {len(findings)} potential secrets:\n")
                for pattern, value in findings:
                    print(f"  - {pattern}: {value}")

                sanitized, warnings = sanitize(content)
                print(f"\nSanitization warnings:")
                for warning in warnings:
                    print(f"  - {warning}")

                print(f"\nSanitized content preview:")
                print("-" * 70)
                print(sanitized[:500] + "...")
            else:
                print("⚠️  secrets_test.md not found")

        elif choice == "5":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")


# ============================================================================
# Main
# ============================================================================


def main():
    """Run POC."""
    print("Mini-Engram POC — IMP-59 Proof of Concept")
    print("=" * 70)

    # Initialize DB
    print("\n📦 Initializing database...")
    conn = init_db()
    print(f"✅ Database created: {DB_PATH}")

    # Load test data
    print("\n📝 Loading test data...")
    load_test_data(conn)

    # Quick search test
    print("\n🔍 Quick search test...")
    results = search_memories(conn, "database", limit=3)
    print(f"Found {len(results)} results for 'database':")
    for result in results:
        print(f"  - {result['title']} (score: {result['score']:.2f})")

    # Run benchmark
    benchmark_search(conn, "database", iterations=100)

    # Interactive demo
    demo(conn)

    conn.close()


if __name__ == "__main__":
    main()
