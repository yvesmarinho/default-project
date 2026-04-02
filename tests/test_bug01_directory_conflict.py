"""
Test for BUG-01: Directory conflict validation.

Validates that scaffold detects and prevents duplicate directory structures
when project_name matches target_dir name.
"""

from pathlib import Path
import pytest
from scripts.lib.ui import _validate_directory_conflict


def test_directory_conflict_detected():
    """Should detect conflict when project name matches target dir name."""
    project_name = "my-project"
    target_dir = Path("/home/user/projects/my-project")

    is_valid, error_msg = _validate_directory_conflict(project_name, target_dir)

    assert not is_valid, "Should detect conflict"
    assert "Conflito detectado" in error_msg
    assert "my-project" in error_msg


def test_directory_no_conflict():
    """Should pass validation when names differ."""
    project_name = "my-project"
    target_dir = Path("/home/user/projects")

    is_valid, error_msg = _validate_directory_conflict(project_name, target_dir)

    assert is_valid, "Should not detect conflict"
    assert error_msg == ""


def test_directory_conflict_with_parent_paths():
    """Should detect conflict regardless of full path."""
    project_name = "api-service"
    target_dir = Path("/very/long/path/to/api-service")

    is_valid, error_msg = _validate_directory_conflict(project_name, target_dir)

    assert not is_valid, "Should detect conflict with nested paths"


def test_directory_different_case_same_name():
    """Should handle case-sensitive comparison correctly."""
    project_name = "my-project"
    target_dir = Path("/home/user/My-Project")

    is_valid, error_msg = _validate_directory_conflict(project_name, target_dir)

    # Linux is case-sensitive, so these are different
    assert is_valid, "Should not detect conflict with different case"
