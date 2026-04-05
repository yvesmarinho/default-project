#!/usr/bin/env python3
"""
Tests for IMP-57 — Search Scope Functionality

Test scope-based indexing and searching for sessions, docs, and specs.

Created: 2026-04-05
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.lib.search import SessionIndexer, SessionSearcher


@pytest.fixture
def temp_index_db():
    """Create a temporary index database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    
    yield db_path
    
    # Cleanup
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def temp_docs_dir(tmp_path):
    """Create temporary docs directory with sample files."""
    # Create sessions
    sessions_dir = tmp_path / "docs" / "SESSIONS"
    session1 = sessions_dir / "2026-04-01"
    session1.mkdir(parents=True)
    
    (session1 / "DAILY_ACTIVITIES_2026-04-01.md").write_text("""---

### 14:00 — Session Start

**Objetivo**: Iniciar sessão de teste de busca.

**Contexto**:
- Implementando IMP-57
- Testando funcionalidade de scope

**Passos**:
1. Criar estrutura de teste
2. Validar indexação

**Resultado**: Sessão iniciada com sucesso.

**Status**: ✅ COMPLETO

---

### 15:00 — Test Activity

**Objetivo**: Implementar teste de busca por scope sessions.

**Contexto**:
- Validando search scope
- Testando FTS5

**Passos**:
1. Criar casos de teste
2. Executar validação

**Resultado**: Testes implementados.

**Status**: ✅ COMPLETO
""")
    
    # Create docs
    docs_dir = tmp_path / "docs"
    (docs_dir / "README.md").write_text("""# Project Documentation

This is the main README file.

## Architecture

The system uses Python and FastAPI.
""")
    
    (docs_dir / "TODO.md").write_text("""# TODO List

## 🔥 P0 — Critical

- [ ] IMP-57: Extend search to all documents
- [x] IMP-51: Session search implementation
""")
    
    # Create specs
    specify_dir = tmp_path / ".specify" / "specs" / "feature-001"
    specify_dir.mkdir(parents=True)
    
    (specify_dir / "spec.md").write_text("""# Feature 001 — Search Enhancement

## Specification

Extend search to index all markdown documents.

## Requirements

- Index sessions
- Index docs
- Index specs
""")
    
    return tmp_path


def test_index_markdown_document(temp_index_db, temp_docs_dir):
    """Test indexing generic markdown document."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    readme_path = temp_docs_dir / "docs" / "README.md"
    sections_count = indexer.index_markdown_document(readme_path, document_type="docs")
    
    # README has 1 ## header (Architecture)
    assert sections_count == 1
    
    # Verify indexed with correct document_type
    cursor = indexer.conn.execute(
        "SELECT document_type, title FROM activities WHERE file_path LIKE '%README.md%'"
    )
    row = cursor.fetchone()
    assert row is not None
    assert row["document_type"] == "docs"
    assert row["title"] == "Architecture"
    
    indexer.close()


def test_split_into_sections(temp_index_db, temp_docs_dir):
    """Test _split_into_sections method."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    content = """# Main Title

This is intro.

## Section 1

Content 1.

## Section 2

Content 2.
"""
    
    sections = indexer._split_into_sections(content, "test.md")
    
    # Should extract 2 sections
    assert len(sections) == 2
    assert sections[0]["title"] == "Section 1"
    assert "Content 1" in sections[0]["content"]
    assert sections[1]["title"] == "Section 2"
    assert "Content 2" in sections[1]["content"]
    
    indexer.close()


def test_split_into_sections_no_headers(temp_index_db):
    """Test _split_into_sections with document without ## headers."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    content = """# Single Title

This is a simple document without sections.
"""
    
    sections = indexer._split_into_sections(content, "simple.md")
    
    # Should return 1 section (whole document)
    assert len(sections) == 1
    assert sections[0]["title"] == "Single Title"
    assert "simple document" in sections[0]["content"]
    
    indexer.close()


def test_index_by_scope_sessions(temp_index_db, temp_docs_dir):
    """Test index_by_scope with sessions scope."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    # Change to temp directory for relative paths
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_docs_dir)
    
    try:
        files, blocks = indexer.index_by_scope(scope="sessions")
        
        # Should index 1 session file with 2 activities
        assert files == 1
        assert blocks == 2
        
        # Verify document_type
        cursor = indexer.conn.execute("SELECT DISTINCT document_type FROM activities")
        doc_types = {row["document_type"] for row in cursor.fetchall()}
        assert doc_types == {"sessions"}
        
    finally:
        os.chdir(original_cwd)
        indexer.close()


def test_index_by_scope_docs(temp_index_db, temp_docs_dir):
    """Test index_by_scope with docs scope."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_docs_dir)
    
    try:
        files, sections = indexer.index_by_scope(scope="docs")
        
        # Should index README.md + TODO.md
        assert files == 2
        assert sections >= 2  # At least 1 section from README + 1 from TODO
        
        # Verify document_type
        cursor = indexer.conn.execute("SELECT DISTINCT document_type FROM activities")
        doc_types = {row["document_type"] for row in cursor.fetchall()}
        assert doc_types == {"docs"}
        
    finally:
        os.chdir(original_cwd)
        indexer.close()


def test_index_by_scope_specs(temp_index_db, temp_docs_dir):
    """Test index_by_scope with specs scope."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_docs_dir)
    
    try:
        files, sections = indexer.index_by_scope(scope="specs")
        
        # Should index spec.md
        assert files == 1
        assert sections >= 1
        
        # Verify document_type
        cursor = indexer.conn.execute("SELECT DISTINCT document_type FROM activities")
        doc_types = {row["document_type"] for row in cursor.fetchall()}
        assert doc_types == {"specs"}
        
    finally:
        os.chdir(original_cwd)
        indexer.close()


def test_index_by_scope_all(temp_index_db, temp_docs_dir):
    """Test index_by_scope with all scopes."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_docs_dir)
    
    try:
        files, blocks = indexer.index_by_scope(scope="all")
        
        # Should index: 1 session + 2 docs + 1 spec = 4 files
        assert files == 4
        assert blocks >= 4
        
        # Verify all document types
        cursor = indexer.conn.execute("SELECT DISTINCT document_type FROM activities ORDER BY document_type")
        doc_types = {row["document_type"] for row in cursor.fetchall()}
        assert doc_types == {"docs", "sessions", "specs"}
        
    finally:
        os.chdir(original_cwd)
        indexer.close()


def test_search_with_scope_filter(temp_index_db, temp_docs_dir):
    """Test search with scope parameter."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_docs_dir)
    
    try:
        # Index all documents
        indexer.index_by_scope(scope="all")
        indexer.close()
        
        # Search with scope filter
        searcher = SessionSearcher(index_path=temp_index_db)
        
        # Search only in sessions
        results = searcher.search("test", scope="sessions")
        assert all(r.document_type == "sessions" for r in results)
        
        # Search only in docs
        results = searcher.search("IMP", scope="docs")
        assert all(r.document_type == "docs" for r in results)
        
        # Search only in specs
        results = searcher.search("search", scope="specs")
        assert all(r.document_type == "specs" for r in results)
        
        # Search in all (no scope filter)
        results = searcher.search("search", scope=None)
        doc_types = {r.document_type for r in results}
        assert len(doc_types) >= 2  # Should find in multiple document types
        
        searcher.close()
        
    finally:
        os.chdir(original_cwd)


def test_document_type_in_search_results(temp_index_db, temp_docs_dir):
    """Test that SearchResult includes document_type field."""
    indexer = SessionIndexer(index_path=temp_index_db)
    
    import os
    original_cwd = os.getcwd()
    os.chdir(temp_docs_dir)
    
    try:
        # Index docs
        indexer.index_by_scope(scope="docs")
        indexer.close()
        
        # Search
        searcher = SessionSearcher(index_path=temp_index_db)
        results = searcher.search("IMP")
        
        # Verify document_type attribute exists
        assert len(results) > 0
        for result in results:
            assert hasattr(result, "document_type")
            assert result.document_type == "docs"
        
        searcher.close()
        
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
