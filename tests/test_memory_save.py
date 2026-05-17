#!/usr/bin/env python3
"""Unit tests for mem_save.py CLI tool (IMP-59 Phase 2).

Tests:
1. Basic save with title and content
2. Save from file
3. Save with tags
4. Auto-generate title from content
5. Append to existing memory
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
MEMORY_DIR = PROJECT_ROOT / ".memory" / "memories"
MEM_SAVE = PROJECT_ROOT / "scripts" / "mem_save.py"


@pytest.fixture
def temp_memory_file(tmp_path):
    """Create temporary memory file for testing."""
    test_file = tmp_path / "test_content.md"
    test_file.write_text("# Test Content\n\nThis is test content from a file.")
    return test_file


def run_mem_save(*args, check=True):
    """Helper to run mem_save.py CLI."""
    cmd = [sys.executable, str(MEM_SAVE)] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
    )
    return result


def test_basic_save():
    """Test 1: Basic save with title and content."""
    result = run_mem_save(
        "--title",
        "Test Basic Save",
        "--content",
        "This is a test memory.",
        "--tags",
        "test,unittest",
    )

    assert result.returncode == 0
    output = result.stdout + result.stderr  # Check both
    assert "✅ Memory saved successfully!" in output
    assert "Test Basic Save" in output
    assert "project" in output  # Default category
    assert "test, unittest" in output


def test_save_from_file(temp_memory_file):
    """Test 2: Save from file."""
    result = run_mem_save(
        "--title",
        "Test File Save",
        "--file",
        str(temp_memory_file),
        "--category",
        "project",
    )

    assert result.returncode == 0
    output = result.stdout + result.stderr
    assert "✅ Memory saved successfully!" in output
    assert "Test File Save" in output

    # Verify file was read
    # (content should be indexed, though we don't check that here)


def test_save_with_custom_category():
    """Test 3: Save with custom category and tags."""
    result = run_mem_save(
        "--title",
        "Test Team Memory",
        "--content",
        "Team process documentation.",
        "--category",
        "team",
        "--tags",
        "process,documentation",
    )

    assert result.returncode == 0
    output = result.stdout + result.stderr
    assert "Test Team Memory" in output
    assert "team" in output
    assert "process, documentation" in output


def test_auto_generate_title():
    """Test 4: Auto-generate title from content."""
    content = "# Auto-Generated Title\n\nThis content has a heading as first line."

    result = run_mem_save(
        "--content",
        content,
        "--auto",
        "--tags",
        "test,auto",
    )

    assert result.returncode == 0
    output = result.stdout + result.stderr
    assert "✅ Memory saved successfully!" in output
    assert "Auto-Generated Title" in output


def test_json_output():
    """Test 5: JSON output mode."""
    result = run_mem_save(
        "--title",
        "Test JSON Output",
        "--content",
        "JSON output test.",
        "--json",
    )

    assert result.returncode == 0

    # Parse JSON
    output = json.loads(result.stdout)
    assert output["success"] is True
    assert output["title"] == "Test JSON Output"
    assert output["category"] == "project"
    assert "id" in output
    assert "file" in output


def test_error_no_title():
    """Test error handling: no title provided."""
    result = run_mem_save(
        "--content",
        "Content without title",
        check=False,  # Expect failure
    )

    assert result.returncode != 0
    assert "ERROR" in result.stderr or "ERROR" in result.stdout


def test_error_no_content():
    """Test error handling: no content provided."""
    result = run_mem_save(
        "--title",
        "Title Without Content",
        check=False,  # Expect failure (no --content or --file)
    )

    assert result.returncode != 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
