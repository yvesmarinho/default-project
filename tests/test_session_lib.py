"""
tests/test_session_lib.py — Testes para scripts/lib/session.py

Suite de testes para o módulo de auto-documentação incremental de sessões.

Cobertura:
- sanitize_text(): redact patterns para dados sensíveis
- ActivityBlock: dataclass e conversão para Markdown
- generate_activity_block(): factory com validações
- append_to_daily_activities(): append idempotente com sanitização
- validate_daily_activities_format(): validação de schema
- sanitize_block(): sanitização de ActivityBlock completo
- get_session_dir_for_date(): cálculo de diretório de sessão
"""

from __future__ import annotations

import re
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

# Importar módulo a ser testado
from scripts.lib.session import (
    ActivityBlock,
    ActivityStatus,
    append_to_daily_activities,
    generate_activity_block,
    get_session_dir_for_date,
    sanitize_block,
    sanitize_text,
    validate_daily_activities_format,
)


# ==============================================================================
# Testes de Sanitização — sanitize_text()
# ==============================================================================


def test_sanitize_github_token():
    """Sanitizar token GitHub (ghp_...)."""
    text = "export GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuv1234"


def test_sanitize_github_pat():
    """Sanitizar Personal Access Token GitHub (github_pat_...)."""
    text = "token=github_pat_" + "1234567890" * 8 + "AB"  # 93 chars total
    result = sanitize_text(text)
    assert "[GITHUB_PAT_REDACTED]" in result
    assert "github_pat_" not in result


def test_sanitize_aws_access_key():
    """Sanitizar AWS Access Key (AKIA...)."""
    text = "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"
    expected = "AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_REDACTED]"
    assert sanitize_text(text) == expected


def test_sanitize_aws_secret_key():
    """Sanitizar AWS Secret Key."""
    text = "aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    result = sanitize_text(text)
    assert "[AWS_SECRET_KEY_REDACTED]" in result
    assert "wJalrXUtnFEMI" not in result


def test_sanitize_jwt_token():
    """Sanitizar JWT token."""
    text = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    result = sanitize_text(text)
    assert "[JWT_TOKEN_REDACTED]" in result
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in result


def test_sanitize_password_in_url():
    """Sanitizar senha em URL."""
    text = "postgres://user:secretpassword@localhost:5432/db"
    result = sanitize_text(text)
    assert "[PASSWORD_REDACTED]" in result
    assert "secretpassword" not in result


def test_sanitize_private_ip():
    """Sanitizar IPs privados."""
    text_1 = "Server: 192.168.1.100"
    text_2 = "DB: 10.0.0.5"
    text_3 = "API: 172.16.0.10"
    
    assert "[PRIVATE_IP_REDACTED]" in sanitize_text(text_1)
    assert "[PRIVATE_IP_REDACTED]" in sanitize_text(text_2)
    assert "[PRIVATE_IP_REDACTED]" in sanitize_text(text_3)


def test_sanitize_email():
    """Sanitizar endereços de email."""
    text = "Contact: admin@company.com"
    result = sanitize_text(text)
    assert "[EMAIL_REDACTED]" in result
    assert "admin@company.com" not in result


def test_sanitize_generic_password():
    """Sanitizar padrões genéricos de password=..."""
    text = "password=mySecret123"
    result = sanitize_text(text)
    assert "password=[PASSWORD_REDACTED]" in result
    assert "mySecret123" not in result


def test_sanitize_api_key():
    """Sanitizar api_key=..."""
    text = "api_key=sk-1234567890abcdef"
    result = sanitize_text(text)
    assert "api_key=[API_KEY_REDACTED]" in result
    assert "sk-1234567890abcdef" not in result


def test_sanitize_multiple_patterns():
    """Sanitizar múltiplos padrões no mesmo texto."""
    text = """
    AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
    AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    DB_HOST=192.168.1.100
    ADMIN_EMAIL=admin@company.com
    """
    result = sanitize_text(text)
    
    assert "[AWS_ACCESS_KEY_REDACTED]" in result
    assert "[AWS_SECRET_KEY_REDACTED]" in result
    assert "[PRIVATE_IP_REDACTED]" in result
    assert "[EMAIL_REDACTED]" in result


# ==============================================================================
# Testes de ActivityBlock — dataclass e to_markdown()
# ==============================================================================


def test_activity_block_to_markdown_minimal():
    """Converter ActivityBlock mínimo para Markdown."""
    block = ActivityBlock(
        title="Test Activity",
        timestamp="14:30",
        objective="Test objective",
        context="Test context",
        steps=["Step 1", "Step 2"],
        result="Success",
        status=ActivityStatus.COMPLETE,
    )
    
    markdown = block.to_markdown(sanitize=False)
    
    assert "### Test Activity" in markdown
    assert "**14:30 — ✅ Completo**" in markdown
    assert "**Objetivo**: Test objective" in markdown
    assert "**Contexto**: Test context" in markdown
    assert "1. Step 1" in markdown
    assert "2. Step 2" in markdown
    assert "**Resultado**: Success" in markdown
    assert "**Status**: ✅ Completo" in markdown


def test_activity_block_to_markdown_with_todo_id():
    """Converter ActivityBlock com TODO ID."""
    block = ActivityBlock(
        title="Fix Bug",
        todo_id="IMP-47",
        timestamp="10:00",
        objective="Fix nested folder bug",
        context="Bug found in previous session",
        steps=["Analyze code"],
        result="Bug fixed",
        status=ActivityStatus.COMPLETE,
    )
    
    markdown = block.to_markdown(sanitize=False)
    
    assert "### Fix Bug (IMP-47)" in markdown


def test_activity_block_to_markdown_with_decisions():
    """Converter ActivityBlock com decisões técnicas."""
    block = ActivityBlock(
        title="Architecture Decision",
        timestamp="11:00",
        objective="Choose approach",
        context="Multiple options available",
        steps=["Evaluate options"],
        result="Option A selected",
        status=ActivityStatus.COMPLETE,
        decisions="Chose Option A over B due to better compatibility",
    )
    
    markdown = block.to_markdown(sanitize=False)
    
    assert "**Decisões técnicas**: Chose Option A over B" in markdown


def test_activity_block_to_markdown_with_files_and_commits():
    """Converter ActivityBlock com arquivos e commits."""
    block = ActivityBlock(
        title="Implementation",
        timestamp="15:00",
        objective="Implement feature",
        context="Required by IMP-48",
        steps=["Write code", "Write tests"],
        result="Feature complete",
        status=ActivityStatus.COMPLETE,
        files_modified=[
            "scripts/lib/session.py (+100/-10)",
            "tests/test_session.py (+200/-0)",
        ],
        commits=[
            "abc1234 — feat: implement session docs",
            "def5678 — test: add session tests",
        ],
    )
    
    markdown = block.to_markdown(sanitize=False)
    
    assert "scripts/lib/session.py (+100/-10)" in markdown
    assert "tests/test_session.py (+200/-0)" in markdown
    assert "`abc1234 — feat: implement session docs`" in markdown


def test_activity_block_to_markdown_with_sanitization():
    """Converter ActivityBlock aplicando sanitização."""
    block = ActivityBlock(
        title="Deploy",
        timestamp="16:00",
        objective="Deploy to prod",
        context="Required deployment",
        steps=["Configure with AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"],
        result="Deployed to 192.168.1.100",
        status=ActivityStatus.COMPLETE,
    )
    
    markdown = block.to_markdown(sanitize=True)
    
    assert "AKIAIOSFODNN7EXAMPLE" not in markdown
    assert "[AWS_ACCESS_KEY_REDACTED]" in markdown
    assert "192.168.1.100" not in markdown
    assert "[PRIVATE_IP_REDACTED]" in markdown


def test_activity_block_status_variations():
    """Testar diferentes status no ActivityBlock."""
    statuses = [
        (ActivityStatus.COMPLETE, "✅ Completo"),
        (ActivityStatus.IN_PROGRESS, "🔵 Em progresso"),
        (ActivityStatus.BLOCKED, "❌ Bloqueado"),
        (ActivityStatus.ON_HOLD, "⏸️ On hold"),
    ]
    
    for status, expected_text in statuses:
        block = ActivityBlock(
            title="Test",
            timestamp="12:00",
            objective="Test",
            context="Test",
            steps=["Test"],
            result="Test",
            status=status,
        )
        markdown = block.to_markdown(sanitize=False)
        assert expected_text in markdown


# ==============================================================================
# Testes de generate_activity_block() — Factory
# ==============================================================================


def test_generate_activity_block_success():
    """Gerar ActivityBlock com todos os campos válidos."""
    block = generate_activity_block(
        title="Test Activity",
        objective="Test objective",
        context="Test context",
        steps=["Step 1", "Step 2"],
        result="Success",
        status=ActivityStatus.COMPLETE,
        todo_id="IMP-01",
        timestamp="14:30",
    )
    
    assert block.title == "Test Activity"
    assert block.todo_id == "IMP-01"
    assert block.timestamp == "14:30"
    assert block.objective == "Test objective"
    assert len(block.steps) == 2
    assert block.status == ActivityStatus.COMPLETE


def test_generate_activity_block_auto_timestamp():
    """Gerar ActivityBlock com timestamp automático (HH:MM)."""
    block = generate_activity_block(
        title="Test",
        objective="Test",
        context="Test",
        steps=["Test"],
        result="Test",
    )
    
    # Verificar que timestamp tem formato HH:MM
    assert re.match(r"\d{2}:\d{2}", block.timestamp)


def test_generate_activity_block_validation_empty_title():
    """Validar que título vazio levanta ValueError."""
    with pytest.raises(ValueError, match="'title' não pode estar vazio"):
        generate_activity_block(
            title="",
            objective="Test",
            context="Test",
            steps=["Test"],
            result="Test",
        )


def test_generate_activity_block_validation_empty_objective():
    """Validar que objetivo vazio levanta ValueError."""
    with pytest.raises(ValueError, match="'objective' não pode estar vazio"):
        generate_activity_block(
            title="Test",
            objective="",
            context="Test",
            steps=["Test"],
            result="Test",
        )


def test_generate_activity_block_validation_empty_steps():
    """Validar que steps vazio levanta ValueError."""
    with pytest.raises(ValueError, match="'steps' não pode estar vazio"):
        generate_activity_block(
            title="Test",
            objective="Test",
            context="Test",
            steps=[],
            result="Test",
        )


def test_generate_activity_block_validation_empty_result():
    """Validar que resultado vazio levanta ValueError."""
    with pytest.raises(ValueError, match="'result' não pode estar vazio"):
        generate_activity_block(
            title="Test",
            objective="Test",
            context="Test",
            steps=["Test"],
            result="",
        )


# ==============================================================================
# Testes de append_to_daily_activities() — Append com idempotência
# ==============================================================================


def test_append_to_daily_activities_success(tmp_path):
    """Adicionar bloco a DAILY_ACTIVITIES com sucesso."""
    # Criar estrutura de sessão temporária
    session_dir = tmp_path / "2026-03-29"
    session_dir.mkdir(parents=True)
    
    daily_activities = session_dir / "DAILY_ACTIVITIES_2026-03-29.md"
    daily_activities.write_text("# 📅 Daily Activities — 2026-03-29\n\n---\n")
    
    # Criar bloco
    block = ActivityBlock(
        title="Test Activity",
        timestamp="14:30",
        objective="Test",
        context="Test",
        steps=["Test"],
        result="Success",
        status=ActivityStatus.COMPLETE,
    )
    
    # Adicionar bloco
    success = append_to_daily_activities(block, session_dir, sanitize=False)
    
    assert success is True
    
    # Verificar conteúdo
    content = daily_activities.read_text()
    assert "### Test Activity" in content
    assert "**14:30 — ✅ Completo**" in content


def test_append_to_daily_activities_idempotent(tmp_path):
    """Verificar idempotência: não adicionar bloco duplicado."""
    # Criar estrutura de sessão
    session_dir = tmp_path / "2026-03-29"
    session_dir.mkdir(parents=True)
    
    daily_activities = session_dir / "DAILY_ACTIVITIES_2026-03-29.md"
    daily_activities.write_text("# 📅 Daily Activities\n\n---\n\n### Test Activity\n")
    
    # Criar bloco com mesmo título
    block = ActivityBlock(
        title="Test Activity",
        timestamp="14:30",
        objective="Test",
        context="Test",
        steps=["Test"],
        result="Success",
        status=ActivityStatus.COMPLETE,
    )
    
    # Tentar adicionar (deve detectar duplicação)
    success = append_to_daily_activities(block, session_dir, sanitize=False)
    
    assert success is False  # Não foi adicionado (já existe)


def test_append_to_daily_activities_with_sanitization(tmp_path):
    """Verificar que sanitização é aplicada ao adicionar bloco."""
    # Criar estrutura de sessão
    session_dir = tmp_path / "2026-03-29"
    session_dir.mkdir(parents=True)
    
    daily_activities = session_dir / "DAILY_ACTIVITIES_2026-03-29.md"
    daily_activities.write_text("# 📅 Daily Activities\n\n---\n")
    
    # Criar bloco com dados sensíveis
    block = ActivityBlock(
        title="Deploy",
        timestamp="16:00",
        objective="Deploy with AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE",
        context="Production deployment",
        steps=["Deploy to 192.168.1.100"],
        result="Success",
        status=ActivityStatus.COMPLETE,
    )
    
    # Adicionar com sanitização
    append_to_daily_activities(block, session_dir, sanitize=True)
    
    # Verificar que dados foram sanitizados
    content = daily_activities.read_text()
    assert "AKIAIOSFODNN7EXAMPLE" not in content
    assert "[AWS_ACCESS_KEY_REDACTED]" in content
    assert "192.168.1.100" not in content
    assert "[PRIVATE_IP_REDACTED]" in content


def test_append_to_daily_activities_dry_run(tmp_path):
    """Verificar modo dry-run (não persiste)."""
    # Criar estrutura de sessão
    session_dir = tmp_path / "2026-03-29"
    session_dir.mkdir(parents=True)
    
    daily_activities = session_dir / "DAILY_ACTIVITIES_2026-03-29.md"
    initial_content = "# 📅 Daily Activities\n\n---\n"
    daily_activities.write_text(initial_content)
    
    # Criar bloco
    block = ActivityBlock(
        title="Test",
        timestamp="14:30",
        objective="Test",
        context="Test",
        steps=["Test"],
        result="Test",
        status=ActivityStatus.COMPLETE,
    )
    
    # Dry run
    success = append_to_daily_activities(block, session_dir, dry_run=True)
    
    assert success is True
    
    # Verificar que arquivo NÃO foi modificado
    content = daily_activities.read_text()
    assert content == initial_content


def test_append_to_daily_activities_missing_dir():
    """Verificar erro quando diretório de sessão não existe."""
    nonexistent_dir = Path("/tmp/nonexistent-session-dir-xyz")
    
    block = ActivityBlock(
        title="Test",
        timestamp="14:30",
        objective="Test",
        context="Test",
        steps=["Test"],
        result="Test",
        status=ActivityStatus.COMPLETE,
    )
    
    with pytest.raises(FileNotFoundError):
        append_to_daily_activities(block, nonexistent_dir)


# ==============================================================================
# Testes de validate_daily_activities_format() — Validação de schema
# ==============================================================================


def test_validate_daily_activities_valid(tmp_path):
    """Validar arquivo DAILY_ACTIVITIES válido."""
    valid_content = """# 📅 Daily Activities — 2026-03-29

---

### Test Activity

**14:30 — ✅ Completo**

**Objetivo**: Test objective

**Contexto**: Test context

**Resultado**: Success

**Status**: ✅ Completo

---
"""
    
    file_path = tmp_path / "DAILY_ACTIVITIES_2026-03-29.md"
    file_path.write_text(valid_content)
    
    is_valid, errors = validate_daily_activities_format(file_path)
    
    assert is_valid is True
    assert len(errors) == 0


def test_validate_daily_activities_missing_header(tmp_path):
    """Validar erro quando cabeçalho principal está ausente."""
    invalid_content = """
### Activity

**14:30**

**Objetivo**: Test
"""
    
    file_path = tmp_path / "DAILY_ACTIVITIES_2026-03-29.md"
    file_path.write_text(invalid_content)
    
    is_valid, errors = validate_daily_activities_format(file_path)
    
    assert is_valid is False
    assert any("Cabeçalho principal ausente" in err for err in errors)


def test_validate_daily_activities_invalid_status(tmp_path):
    """Validar erro quando status inválido é encontrado."""
    invalid_content = """# 📅 Daily Activities — 2026-03-29

---

### Test Activity

**14:30 — ✅ Completo**

**Objetivo**: Test

**Contexto**: Test

**Resultado**: Test

**Status**: ⚠️ Invalid Status

---
"""
    
    file_path = tmp_path / "DAILY_ACTIVITIES_2026-03-29.md"
    file_path.write_text(invalid_content)
    
    is_valid, errors = validate_daily_activities_format(file_path)
    
    assert is_valid is False
    assert any("Status inválido" in err for err in errors)


def test_validate_daily_activities_file_not_found():
    """Validar erro quando arquivo não existe."""
    nonexistent_file = Path("/tmp/nonexistent-daily-activities-xyz.md")
    
    is_valid, errors = validate_daily_activities_format(nonexistent_file)
    
    assert is_valid is False
    assert any("Arquivo não encontrado" in err for err in errors)


# ==============================================================================
# Testes de sanitize_block() — Sanitizar ActivityBlock completo
# ==============================================================================


def test_sanitize_block_all_fields():
    """Sanitizar todos os campos de um ActivityBlock."""
    block = ActivityBlock(
        title="Deploy with token ghp_1234567890abcdefghijklmnopqrstuv1234",
        timestamp="16:00",
        objective="Deploy using AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE",
        context="Contact admin@company.com",
        steps=[
            "Connect to 192.168.1.100",
            "Configure password=secret123",
        ],
        result="Deployed via https://user:pass@api.example.com",
        status=ActivityStatus.COMPLETE,
        decisions="Use token=abc123 for auth",
        files_modified=["config with secret=xyz789"],
        commits=["abc1234 — deploy with api_key=123456"],
    )
    
    sanitized = sanitize_block(block)
    
    # Verificar que dados sensíveis foram removidos
    assert "[GITHUB_TOKEN_REDACTED]" in sanitized.title
    assert "ghp_" not in sanitized.title
    
    assert "[AWS_ACCESS_KEY_REDACTED]" in sanitized.objective
    assert "AKIAIOSFODNN7EXAMPLE" not in sanitized.objective
    
    assert "[EMAIL_REDACTED]" in sanitized.context
    assert "admin@company.com" not in sanitized.context
    
    assert "[PRIVATE_IP_REDACTED]" in sanitized.steps[0]
    assert "192.168.1.100" not in sanitized.steps[0]
    
    assert "[PASSWORD_REDACTED]" in sanitized.steps[1]
    assert "secret123" not in sanitized.steps[1]


def test_sanitize_block_preserves_none_fields():
    """Sanitizar bloco preservando campos None."""
    block = ActivityBlock(
        title="Test",
        timestamp="14:30",
        objective="Test",
        context="Test",
        steps=["Test"],
        result="Test",
        status=ActivityStatus.COMPLETE,
        decisions=None,  # None deve ser preservado
    )
    
    sanitized = sanitize_block(block)
    
    assert sanitized.decisions is None


# ==============================================================================
# Testes de get_session_dir_for_date() — Cálculo de diretório
# ==============================================================================


def test_get_session_dir_for_date_default():
    """Calcular diretório de sessão para hoje (default)."""
    base_dir = Path("docs/SESSIONS")
    session_dir = get_session_dir_for_date(base_dir)
    
    # Verificar formato YYYY-MM-DD
    expected_date = datetime.now().strftime("%Y-%m-%d")
    expected_dir = base_dir / expected_date
    
    assert session_dir == expected_dir


def test_get_session_dir_for_date_specific():
    """Calcular diretório de sessão para data específica."""
    base_dir = Path("docs/SESSIONS")
    date = datetime(2026, 3, 29)
    session_dir = get_session_dir_for_date(base_dir, date)
    
    expected_dir = base_dir / "2026-03-29"
    
    assert session_dir == expected_dir


# ==============================================================================
# Fim dos testes
# ==============================================================================
