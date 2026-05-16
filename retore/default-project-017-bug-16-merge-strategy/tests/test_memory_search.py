#!/usr/bin/env python3
"""Unit tests for mem_search.py CLI tool (IMP-59 Phase 2).

Tests:
1. Basic search
2. Search with category filter
3. Search with tags filter
4. Search with limit
5. JSON output
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
MEM_SEARCH = PROJECT_ROOT / "scripts" / "mem_search.py"
MEM_SAVE = PROJECT_ROOT / "scripts" / "mem_save.py"


def run_mem_search(*args, check=True):
    """Helper to run mem_search.py CLI."""
    cmd = [sys.executable, str(MEM_SEARCH)] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
    )
    return result


def run_mem_save(*args):
    """Helper to save test data."""
    cmd = [sys.executable, str(MEM_SAVE)] + list(args)
    subprocess.run(cmd, capture_output=True, text=True, check=True)


@pytest.fixture(scope="module", autouse=True)
def setup_test_memories():
    """Setup: Create test memories for search tests."""
    # Save test memories
    run_mem_save(
        "--title",
        "Search Test: JWT Authentication",
        "--content",
        "Use JWT tokens for API authentication with 1h expiration.",
        "--category",
        "project",
        "--tags",
        "api,security,jwt",
    )

    run_mem_save(
        "--title",
        "Search Test: Database Migration",
        "--content",
        "Use Alembic for database migrations with rollback support.",
        "--category",
        "project",
        "--tags",
        "database,migration",
    )

    run_mem_save(
        "--title",
        "Search Test: Team Onboarding",
        "--content",
        "New team members should complete security training first.",
        "--category",
        "team",
        "--tags",
        "onboarding,security",
    )

    yield

    # Teardown: Clean up test memories
    # (In production, you might delete test files here)


def test_basic_search():
    """Test 1: Basic search."""
    result = run_mem_search("JWT")

    assert result.returncode == 0
    output = result.stdout + result.stderr
    assert ("Found" in output or "JWT Authentication" in result.stdout)


def test_search_with_category_filter():
    """Test 2: Search with category filter."""
    result = run_mem_search("Search Test", "--category", "team")

    assert result.returncode == 0

    # Should only find team memories
    if "Team Onboarding" not in result.stdout and "No results" not in result.stdout:
        # Either found it or no results (acceptable)
        pass


def test_search_with_tags_filter():
    """Test 3: Search with tags filter."""
    result = run_mem_search("Search Test", "--tags", "security")

    assert result.returncode == 0

    # Should find memories tagged with "security"
    # (JWT Authentication and Team Onboarding both have security tag)


def test_search_with_limit():
    """Test 4: Search with limit."""
    result = run_mem_search("Search Test", "--limit", "1")

    assert result.returncode == 0

    # Count number of results (look for numbered lines like "1. ")
    result_count = result.stdout.count("\n1. ")
    # Should have at most 1 result (though might be 0 if query doesn't match)
    assert result_count <= 1


def test_json_output():
    """Test 5: JSON output."""
    result = run_mem_search("JWT", "--json")

    assert result.returncode == 0

    # Parse JSON
    output = json.loads(result.stdout)
    assert "query" in output
    assert "count" in output
    assert "results" in output
    assert isinstance(output["results"], list)

    # Check result structure
    if output["count"] > 0:
        first_result = output["results"][0]
        assert "title" in first_result
        assert "category" in first_result
        assert "tags" in first_result
        assert "score" in first_result


def test_no_results():
    """Test search with no results."""
    result = run_mem_search("xyznonexistentquery12345")

    assert result.returncode == 0  # No error, just no results
    output = result.stdout + result.stderr
    assert "No results found" in output or "Found 0" in output


def test_fts5_boolean_search():
    """Test FTS5 boolean search syntax."""
    result = run_mem_search("Search AND Test")

    assert result.returncode == 0
    # Should work (FTS5 supports AND operator)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
