"""
Unit tests for Session Search and Indexing

Tests for IMP-51 — MCP Search Integration for Session History
Created: 2026-04-05

Tests cover:
- ActivityBlock parsing (canonical and legacy formats)
- Session indexing (single file, multiple files, rebuild)
- Search functionality (keywords, phrases, boolean, date filters)
- Error handling (missing index, invalid queries)
- Database operations (schema, metadata, stats)
"""

import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from scripts.lib.search import ActivityBlock, SearchResult, SessionIndexer, SessionSearcher


class TestActivityBlock:
    """Test ActivityBlock dataclass and methods."""
    
    def test_searchable_text_combines_fields(self):
        """Test that searchable_text concatenates all relevant fields."""
        block = ActivityBlock(
            session_date="2026-04-05",
            timestamp="14:30",
            title="Test Activity",
            objective="Test objective",
            context="Test context",
            result="Test result",
        )
        
        searchable = block.searchable_text
        assert "Test Activity" in searchable
        assert "Test objective" in searchable
        assert "Test context" in searchable
        assert "Test result" in searchable
    
    def test_searchable_text_handles_none_fields(self):
        """Test that searchable_text handles None fields gracefully."""
        block = ActivityBlock(
            session_date="2026-04-05",
            timestamp="14:30",
            title="Test Activity",
            objective=None,
            context=None,
        )
        
        searchable = block.searchable_text
        assert "Test Activity" in searchable
        assert searchable.strip()  # Not empty
    
    def test_day_of_week_calculation(self):
        """Test day of week calculation from session_date."""
        block = ActivityBlock(
            session_date="2026-04-05",  # Sunday
            timestamp="14:30",
            title="Test",
        )
        
        assert block.day_of_week == "Sunday"
    
    def test_day_of_week_invalid_date(self):
        """Test day of week with invalid date."""
        block = ActivityBlock(
            session_date="invalid",
            timestamp="14:30",
            title="Test",
        )
        
        assert block.day_of_week == "unknown"


class TestSessionIndexer:
    """Test SessionIndexer class."""
    
    @pytest.fixture
    def temp_index(self, tmp_path):
        """Create temporary index database."""
        index_path = tmp_path / "test_index.db"
        indexer = SessionIndexer(index_path=index_path)
        yield indexer
        indexer.close()
    
    @pytest.fixture
    def sample_canonical_file(self, tmp_path):
        """Create sample canonical format activity file."""
        content = """# DAILY_ACTIVITIES — 2026-04-05 (Sunday)

---

### Test Activity 1

**14:30** | Status: ✅ CONCLUÍDO

**Objetivo**: Implementar feature X

**Contexto**: Requisito do projeto Y

**Passos executados**:
1. Criar arquivo test.py
2. Implementar função
3. Executar testes

**Resultado**: Feature implementada com sucesso

**Decisões técnicas**: Usar SQLite FTS5

**Arquivos modificados/criados**:
- scripts/test.py

**Commits**:
- feat(test): implement feature X

**Status**: ✅ Completo

---

### Test Activity 2

**15:00** | Status: 🔵 EM PROGRESSO

**Objetivo**: Revisar documentação

**Resultado**: Documentação atualizada
"""
        file_path = tmp_path / "DAILY_ACTIVITIES_2026-04-05.md"
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    @pytest.fixture
    def sample_legacy_file(self, tmp_path):
        """Create sample legacy format activity file."""
        content = """# TODAY_ACTIVITIES — 2026-04-03

- **12:00** — Started session

### Legacy Activity 1

Did some work at 13:00 on implementing feature

### Legacy Activity 2

Fixed bug at 14:00 related to validation
"""
        file_path = tmp_path / "TODAY_ACTIVITIES_2026-04-03.md"
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    def test_database_schema_creation(self, temp_index):
        """Test that database schema is created correctly."""
        cursor = temp_index.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "activities" in tables
        assert "metadata" in tables
    
    def test_parse_canonical_format(self, temp_index, sample_canonical_file):
        """Test parsing canonical format DAILY_ACTIVITIES file."""
        blocks = temp_index.parse_daily_activities(sample_canonical_file)
        
        assert len(blocks) == 2
        
        # First block
        assert blocks[0].session_date == "2026-04-05"
        assert blocks[0].timestamp == "14:30"
        assert blocks[0].title == "Test Activity 1"
        assert blocks[0].objective == "Implementar feature X"
        assert blocks[0].result == "Feature implementada com sucesso"
        assert "feat(test): implement feature X" in blocks[0].commits
        
        # Second block
        assert blocks[1].title == "Test Activity 2"
        assert blocks[1].timestamp == "15:00"
    
    def test_parse_legacy_format(self, temp_index, sample_legacy_file):
        """Test parsing legacy format TODAY_ACTIVITIES file."""
        blocks = temp_index.parse_daily_activities(sample_legacy_file)
        
        assert len(blocks) == 2
        assert blocks[0].session_date == "2026-04-03"
        assert blocks[0].title == "Legacy Activity 1"
        assert blocks[1].title == "Legacy Activity 2"
    
    def test_index_single_file(self, temp_index, sample_canonical_file):
        """Test indexing a single file."""
        blocks_count = temp_index.index_file(sample_canonical_file)
        
        assert blocks_count == 2
        
        # Verify data in database
        cursor = temp_index.conn.execute("SELECT COUNT(*) FROM activities")
        assert cursor.fetchone()[0] == 2
    
    def test_index_all_sessions(self, temp_index, tmp_path, sample_canonical_file, sample_legacy_file):
        """Test indexing all sessions."""
        # Create sessions directory structure
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir()
        
        # Create session subdirectories
        session1 = sessions_dir / "2026-04-05"
        session1.mkdir()
        (session1 / "DAILY_ACTIVITIES_2026-04-05.md").write_text(
            sample_canonical_file.read_text(), encoding="utf-8"
        )
        
        session2 = sessions_dir / "2026-04-03"
        session2.mkdir()
        (session2 / "TODAY_ACTIVITIES_2026-04-03.md").write_text(
            sample_legacy_file.read_text(), encoding="utf-8"
        )
        
        # Index all
        files_indexed, blocks_indexed = temp_index.index_all_sessions(sessions_dir)
        
        assert files_indexed == 2
        assert blocks_indexed == 4  # 2 from canonical + 2 from legacy
        
        # Verify metadata
        stats = temp_index.get_stats()
        assert stats["total_blocks"] == 4
        assert stats["total_sessions"] == 2  # 2 different dates
    
    def test_rebuild_clears_existing_data(self, temp_index, tmp_path, sample_canonical_file):
        """Test that rebuild clears existing data."""
        # Create sessions directory
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir()
        session = sessions_dir / "2026-04-05"
        session.mkdir()
        (session / "DAILY_ACTIVITIES_2026-04-05.md").write_text(
            sample_canonical_file.read_text(), encoding="utf-8"
        )
        
        # Index once
        temp_index.index_all_sessions(sessions_dir)
        stats1 = temp_index.get_stats()
        
        # Index again with rebuild
        temp_index.index_all_sessions(sessions_dir, force_rebuild=True)
        stats2 = temp_index.get_stats()
        
        # Should have same count, not double
        assert stats1["total_blocks"] == stats2["total_blocks"]
    
    def test_get_stats(self, temp_index, tmp_path, sample_canonical_file):
        """Test get_stats method."""
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir()
        session = sessions_dir / "2026-04-05"
        session.mkdir()
        (session / "DAILY_ACTIVITIES_2026-04-05.md").write_text(
            sample_canonical_file.read_text(), encoding="utf-8"
        )
        
        temp_index.index_all_sessions(sessions_dir)
        stats = temp_index.get_stats()
        
        assert "total_blocks" in stats
        assert "total_sessions" in stats
        assert "last_indexed" in stats
        assert stats["total_blocks"] > 0
        assert stats["last_indexed"] != "never"


class TestSessionSearcher:
    """Test SessionSearcher class."""
    
    @pytest.fixture
    def indexed_searcher(self, tmp_path):
        """Create indexed database and searcher."""
        # Create index
        index_path = tmp_path / "search_index.db"
        indexer = SessionIndexer(index_path=index_path)
        
        # Create sample sessions
        sessions_dir = tmp_path / "sessions"
        sessions_dir.mkdir()
        
        # Session 1: 2026-04-05
        session1 = sessions_dir / "2026-04-05"
        session1.mkdir()
        content1 = """# DAILY_ACTIVITIES — 2026-04-05

---

### Implementar validador de semver

**14:30** | Status: ✅ CONCLUÍDO

**Objetivo**: Criar validador de semver para versões Python

**Resultado**: Validador implementado e testado
"""
        (session1 / "DAILY_ACTIVITIES_2026-04-05.md").write_text(content1, encoding="utf-8")
        
        # Session 2: 2026-04-03
        session2 = sessions_dir / "2026-04-03"
        session2.mkdir()
        content2 = """# DAILY_ACTIVITIES — 2026-04-03

---

### Bug fix em Python FastAPI

**10:00** | Status: ✅ CONCLUÍDO

**Objetivo**: Corrigir bug de validação

**Resultado**: Bug corrigido com testes
"""
        (session2 / "DAILY_ACTIVITIES_2026-04-03.md").write_text(content2, encoding="utf-8")
        
        # Index
        indexer.index_all_sessions(sessions_dir)
        indexer.close()
        
        # Return searcher
        searcher = SessionSearcher(index_path=index_path)
        yield searcher
        searcher.close()
    
    def test_search_simple_keyword(self, indexed_searcher):
        """Test simple keyword search."""
        results = indexed_searcher.search("semver")
        
        assert len(results) >= 1
        assert any("semver" in r.title.lower() or "semver" in r.snippet.lower() for r in results)
    
    def test_search_multiple_keywords(self, indexed_searcher):
        """Test search with multiple keywords."""
        results = indexed_searcher.search("python validador")
        
        assert len(results) >= 1
    
    def test_search_phrase(self, indexed_searcher):
        """Test phrase search with quotes."""
        results = indexed_searcher.search('"bug fix"')
        
        assert len(results) >= 1
        assert any("bug" in r.snippet.lower() and "fix" in r.snippet.lower() for r in results)
    
    def test_search_date_filter(self, indexed_searcher):
        """Test search with date filter."""
        results = indexed_searcher.search("python", date_from="2026-04-04")
        
        # Should only return results from 2026-04-05
        assert all(r.session_date >= "2026-04-04" for r in results)
    
    def test_search_limit(self, indexed_searcher):
        """Test result limit."""
        results = indexed_searcher.search("python", limit=1)
        
        assert len(results) <= 1
    
    def test_search_no_results(self, indexed_searcher):
        """Test search with no results."""
        results = indexed_searcher.search("nonexistent_keyword_xyz")
        
        assert len(results) == 0
    
    def test_search_invalid_query(self, indexed_searcher):
        """Test invalid FTS5 query."""
        with pytest.raises(ValueError, match="Invalid FTS5 query"):
            indexed_searcher.search("IMP-50")  # Should fail without quotes
    
    def test_get_activity_context(self, indexed_searcher):
        """Test retrieving full activity context."""
        context = indexed_searcher.get_activity_context(
            session_date="2026-04-05",
            title="Implementar validador de semver"
        )
        
        assert context is not None
        assert "validador de semver" in context.lower()
        assert "14:30" in context
    
    def test_missing_index_error(self, tmp_path):
        """Test error when index doesn't exist."""
        nonexistent_path = tmp_path / "nonexistent.db"
        
        with pytest.raises(FileNotFoundError, match="Index database not found"):
            SessionSearcher(index_path=nonexistent_path)


class TestSearchResult:
    """Test SearchResult dataclass."""
    
    def test_str_representation(self):
        """Test string representation of SearchResult."""
        result = SearchResult(
            session_date="2026-04-05",
            timestamp="14:30",
            title="Test Activity",
            snippet="This is a test snippet",
            rank=-1.5,
            file_path="/path/to/file.md",
        )
        
        result_str = str(result)
        assert "2026-04-05" in result_str
        assert "14:30" in result_str
        assert "Test Activity" in result_str
        assert "This is a test snippet" in result_str
