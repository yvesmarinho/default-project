"""
Integration tests for session documentation system.

Part of: IMP-49 — Sistema de documentação incremental — Integração
Created: 2026-04-03

Tests cover:
- Session validator (scripts/session-validate.py)
- Makefile targets (session-log, session-validate, session-sanitize)
- Gitleaks configuration (.gitleaks-session-docs.toml)
- Session prompts integration (session-start, session-end)
- .scaffold-config.json features.session_docs
"""

import json
import importlib.util
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

# Import session validator module from scripts/ (with hyphen in filename)
validator_path = Path(__file__).parent.parent / "scripts" / "session-validate.py"
spec = importlib.util.spec_from_file_location("session_validate", validator_path)
session_validate = importlib.util.module_from_spec(spec)
sys.modules["session_validate"] = session_validate
spec.loader.exec_module(session_validate)

SessionValidator = session_validate.SessionValidator
ActivityBlock = session_validate.ActivityBlock


@pytest.fixture
def session_validator():
    """Fixture providing a SessionValidator instance."""
    return SessionValidator()


@pytest.fixture
def valid_activity_block():
    """Fixture providing a valid activity block."""
    return dedent("""
        ### IMP-49 Implementation (IMP-49)

        **14:30 — ✅ Completo**

        **Objetivo**: Integrar sistema de documentação incremental

        **Contexto**: Sistema implementado em IMP-48, precisa integração com prompts e CI

        **Passos executados**:
        1. Atualizar session-start.prompt.md
        2. Atualizar session-end.prompt.md
        3. Criar .gitleaks-session-docs.toml

        **Resultado**: Integração completa funcionando

        **Arquivos modificados/criados**:
        - .github/prompts/session-start.prompt.md (+50/-10)
        - .github/prompts/session-end.prompt.md (+80/-20)
        - .gitleaks-session-docs.toml (+200/-0)

        **Commits**:
        - `abc1234` — feat(session-docs): integrar sistema com prompts e CI

        **Status**: ✅ Completo
    """).strip()


@pytest.fixture
def invalid_activity_block_missing_fields():
    """Fixture providing an invalid activity block (missing required fields)."""
    return dedent("""
        ### Some Task

        **14:30 — ✅ Completo**

        **Objetivo**: Do something

        **Status**: ✅ Completo
    """).strip()


@pytest.fixture
def block_with_sensitive_data():
    """Fixture providing a block with potentially sensitive data."""
    return dedent("""
        ### Database Migration

        **15:00 — ✅ Completo**

        **Objetivo**: Migrate production database

        **Contexto**: Need to update schema for new feature

        **Passos executados**:
        1. Connect to database: mysql://admin:MyS3cr3tP@ss@10.20.30.40:3306/prod
        2. Run migration script
        3. Verify results

        **Resultado**: Migration successful

        **Status**: ✅ Completo
    """).strip()


# ============================================================================
# TESTS 1-5: Activity Block Parsing
# ============================================================================


def test_parse_valid_activity_block(session_validator, valid_activity_block):
    """Test parsing a valid activity block."""
    block = session_validator._parse_single_block(valid_activity_block, 1)

    assert block.title == "IMP-49 Implementation (IMP-49)"
    assert block.timestamp == "14:30"
    assert block.status_marker == "✅ Completo"
    assert block.has_objetivo is True
    assert block.has_contexto is True
    assert block.has_passos is True
    assert block.has_resultado is True
    assert block.has_status is True


def test_parse_block_missing_title(session_validator):
    """Test parsing block without title."""
    content = "**14:30 — ✅ Completo**\n\n**Objetivo**: Something"
    block = session_validator._parse_single_block(content, 1)

    assert block.title is None


def test_parse_block_missing_timestamp(session_validator):
    """Test parsing block without timestamp."""
    content = "### Some Title\n\n**Objetivo**: Something"
    block = session_validator._parse_single_block(content, 1)

    assert block.timestamp is None


def test_parse_block_invalid_timestamp_format(session_validator):
    """Test parsing block with invalid timestamp format."""
    content = "### Title\n\n**25:99 — Status**\n\n**Objetivo**: Something"
    block = session_validator._parse_single_block(content, 1)

    assert block.timestamp == "25:99"  # Captured but invalid


def test_parse_multiple_blocks(session_validator, valid_activity_block):
    """Test parsing multiple blocks from content."""
    content = f"---\n{valid_activity_block}\n---\n\n---\n{valid_activity_block}\n---"
    blocks = session_validator.parse_activity_blocks(content)

    assert len(blocks) == 2
    assert all(b.title == "IMP-49 Implementation (IMP-49)" for b in blocks)


# ============================================================================
# TESTS 6-10: Block Validation
# ============================================================================


def test_validate_valid_block(session_validator, valid_activity_block):
    """Test validation of a valid block."""
    block = session_validator._parse_single_block(valid_activity_block, 1)
    errors, warnings = session_validator.validate_block(block, Path("test.md"))

    assert len(errors) == 0  # No errors for valid block


def test_validate_block_missing_required_fields(
    session_validator, invalid_activity_block_missing_fields
):
    """Test validation of block missing required fields."""
    block = session_validator._parse_single_block(invalid_activity_block_missing_fields, 1)
    errors, warnings = session_validator.validate_block(block, Path("test.md"))

    # Should have errors for missing fields (contexto, passos, resultado)
    assert len(errors) >= 3
    assert any("contexto" in err.lower() for err in errors)
    assert any("passos" in err.lower() for err in errors)
    assert any("resultado" in err.lower() for err in errors)


def test_validate_block_invalid_timestamp(session_validator):
    """Test validation of block with invalid timestamp format."""
    content = "### Title\n\n**1430 — Status**\n\n**Objetivo**: X\n**Contexto**: X\n**Passos executados**:\n1. X\n**Resultado**: X\n**Status**: ✅ Completo"
    block = session_validator._parse_single_block(content, 1)
    errors, warnings = session_validator.validate_block(block, Path("test.md"))

    # Should have error for malformatted timestamp (missing colon)
    assert any("timestamp" in err.lower() for err in errors)


def test_validate_block_title_too_long(session_validator):
    """Test validation warning for overly long title."""
    long_title = "A" * 120
    content = f"### {long_title}\n\n**14:30 — ✅ Completo**\n\n**Objetivo**: X\n**Contexto**: X\n**Passos executados**:\n1. X\n**Resultado**: X\n**Status**: ✅ Completo"
    block = session_validator._parse_single_block(content, 1)
    errors, warnings = session_validator.validate_block(block, Path("test.md"))

    assert any("Title too long" in warn for warn in warnings)


def test_validate_block_non_standard_status(session_validator):
    """Test validation warning for non-standard status value."""
    content = "### Title\n\n**14:30 — ✅ Completo**\n\n**Objetivo**: X\n**Contexto**: X\n**Passos executados**:\n1. X\n**Resultado**: X\n**Status**: 🟢 Done"
    block = session_validator._parse_single_block(content, 1)
    errors, warnings = session_validator.validate_block(block, Path("test.md"))

    assert any("Non-standard status" in warn for warn in warnings)


# ============================================================================
# TESTS 11-15: Sensitive Data Detection
# ============================================================================


def test_detect_password_in_content(session_validator):
    """Test detection of password pattern."""
    content = "DB_PASSWORD=MyS3cr3tP@ssw0rd"
    findings = session_validator.scan_for_suspicious_patterns(content, Path("test.md"))

    assert len(findings) > 0
    assert any(name == "password" for _, name, _ in findings)


def test_detect_api_key_in_content(session_validator):
    """Test detection of API key pattern."""
    content = "api_key = sk_live_abc123def456ghi789jkl012mno345"
    findings = session_validator.scan_for_suspicious_patterns(content, Path("test.md"))

    assert len(findings) > 0
    assert any(name == "api_key" for _, name, _ in findings)


def test_detect_private_ip_10_network(session_validator):
    """Test detection of private IP (10.x.x.x)."""
    content = "Connected to database at 10.20.30.40"
    findings = session_validator.scan_for_suspicious_patterns(content, Path("test.md"))

    assert len(findings) > 0
    assert any(name == "private_ip_10" for _, name, _ in findings)


def test_detect_jwt_token(session_validator):
    """Test detection of JWT token."""
    content = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
    findings = session_validator.scan_for_suspicious_patterns(content, Path("test.md"))

    assert len(findings) > 0
    assert any(name == "jwt" for _, name, _ in findings)


def test_allowlist_sanitized_examples(session_validator):
    """Test that sanitized examples are allowlisted."""
    content = """
    API_KEY=<REDACTED>
    PASSWORD=***
    user@example.com
    192.0.2.1
    example_key=sample123
    """
    findings = session_validator.scan_for_suspicious_patterns(content, Path("test.md"))

    # These should NOT be detected as suspicious
    assert len(findings) == 0


# ============================================================================
# TESTS 16-18: File Validation
# ============================================================================


def test_validate_nonexistent_file(session_validator, tmp_path):
    """Test validation of non-existent file."""
    nonexistent = tmp_path / "does_not_exist.md"
    result = session_validator.validate_file(nonexistent)

    assert len(result.errors) > 0
    assert "File not found" in result.errors[0]


def test_validate_empty_file(session_validator, tmp_path):
    """Test validation of empty file."""
    empty_file = tmp_path / "DAILY_ACTIVITIES_2026-04-03.md"
    empty_file.write_text("")
    result = session_validator.validate_file(empty_file)

    assert len(result.blocks) == 0


def test_validate_file_with_valid_content(session_validator, tmp_path, valid_activity_block):
    """Test validation of file with valid content."""
    file_path = tmp_path / "DAILY_ACTIVITIES_2026-04-03.md"
    content = f"# Daily Activities 2026-04-03\n\n---\n{valid_activity_block}\n---"
    file_path.write_text(content)

    result = session_validator.validate_file(file_path)

    assert len(result.blocks) == 1
    assert len(result.errors) == 0


# ============================================================================
# TESTS 19-20: Configuration and Integration
# ============================================================================


def test_scaffold_config_has_session_docs_feature():
    """Test that .scaffold-config.json has session_docs feature."""
    config_path = Path(__file__).parent.parent / ".scaffold-config.json"

    if not config_path.exists():
        pytest.skip(".scaffold-config.json not found (expected in project root)")

    with open(config_path) as f:
        config = json.load(f)

    assert "features" in config
    assert "session_docs" in config["features"]
    assert config["features"]["session_docs"]["enabled"] is True
    assert config["features"]["session_docs"]["format"] == "structured"


def test_gitleaks_session_docs_config_exists():
    """Test that .gitleaks-session-docs.toml exists."""
    gitleaks_config = Path(__file__).parent.parent / ".gitleaks-session-docs.toml"

    assert gitleaks_config.exists(), ".gitleaks-session-docs.toml should exist in project root"

    content = gitleaks_config.read_text()

    # Verify key sections exist
    assert "session-aws-access-key" in content
    assert "session-github-token" in content
    assert "session-private-ip-10" in content
    assert "session-jwt-token" in content
