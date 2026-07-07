"""
tests/test_session_manager_workflow.py — Testes do novo CLI unificado de sessão.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.lib.session_context import SessionPaths, recover_context, validate_mcp_config
from scripts.lib.session_security import scan_session_documents, scan_workspace
from scripts.lib.session_workflow import run_end, run_start, run_status


PROJECT_ROOT = Path(__file__).parent.parent
SESSION_MANAGER = PROJECT_ROOT / "scripts" / "session-manager.py"


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _create_workspace(tmp_path: Path) -> Path:
    root = tmp_path / "workspace"
    _write(
        root / ".vscode" / "mcp.json",
        json.dumps(
            {
                "servers": {
                    "memory": {"command": "npx"},
                    "sequential-thinking": {"command": "npx"},
                }
            },
        ),
    )
    _write(root / ".gitignore", ".secrets/\n")
    _write(root / ".copilot-rules.md", "# rules\n")
    _write(root / "README.md", "# Teste\n")
    _write(
        root / "docs" / "TODO.md",
        "# TODO\n\n- [ ] Primeira pendência\n- [ ] Segunda pendência\n",
    )
    _write(root / "docs" / "INDEX.md", "# INDEX\n")
    _write(
        root / "docs" / "SESSIONS" / "2026-07-06" / "FINAL_STATUS_2026-07-06.md",
        "# Final Status\n",
    )
    _write(
        root / "docs" / "SESSIONS" / "2026-07-06" / "DAILY_ACTIVITIES_2026-07-06.md",
        "# 📅 Daily Activities — 2026-07-06\n\n---\n",
    )
    return root


def test_validate_mcp_config_detects_required_servers(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)
    status = validate_mcp_config(SessionPaths.from_root(root))

    assert status.ok is True
    assert status.missing_servers == ()


def test_recover_context_reads_previous_session_and_todos(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)
    context = recover_context(SessionPaths.from_root(root), today="2026-07-07")

    assert context["latest_session_date"] == "2026-07-06"
    assert context["pending_todos"] == ["Primeira pendência", "Segunda pendência"]


def test_run_start_creates_current_session_files(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)

    result = run_start(root, today="2026-07-07")

    assert result["ready"] is True
    assert result["docs"]["statuses"]["recovery"] == "created"
    assert (root / "docs" / "SESSIONS" / "2026-07-07" / "SESSION_RECOVERY_2026-07-07.md").exists()
    assert (root / "docs" / "SESSIONS" / "2026-07-07" / "DAILY_ACTIVITIES_2026-07-07.md").exists()
    assert (root / "docs" / "SESSIONS" / "2026-07-07" / "SESSION_REPORT_2026-07-07.md").exists()
    assert (root / "docs" / "SESSIONS" / "2026-07-07" / "FINAL_STATUS_2026-07-07.md").exists()


def test_scan_workspace_flags_sensitive_files_outside_secrets(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)
    _write(root / "config" / "prod.key", "secret")

    result = scan_workspace(SessionPaths.from_root(root))

    assert result["clean"] is False
    assert any(item["path"] == "config/prod.key" for item in result["findings"])


def test_scan_session_documents_flags_private_ip(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)
    _write(
        root / "docs" / "SESSIONS" / "2026-07-07" / "SESSION_REPORT_2026-07-07.md",
        "# Report\n\nServidor: 10.20.30.40\n",
    )

    result = scan_session_documents(SessionPaths.from_root(root))

    assert result["clean"] is False
    assert any("10.20.30.40" in item["detail"] for item in result["findings"])


def test_run_end_updates_report_and_final_status(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)
    run_start(root, today="2026-07-07")

    result = run_end(root, today="2026-07-07")

    assert result["ready_for_next_session"] is True
    report_content = (
        root
        / "docs"
        / "SESSIONS"
        / "2026-07-07"
        / "SESSION_REPORT_2026-07-07.md"
    ).read_text(encoding="utf-8")
    final_content = (
        root
        / "docs"
        / "SESSIONS"
        / "2026-07-07"
        / "FINAL_STATUS_2026-07-07.md"
    ).read_text(encoding="utf-8")

    assert "## Resumo automático" in report_content
    assert "## Próximas ações" in final_content
    assert "Primeira pendência" in final_content


def test_run_status_reports_daily_validation(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)
    run_start(root, today="2026-07-07")

    result = run_status(root, today="2026-07-07")

    assert result["daily_validation"]["valid"] is True


def test_session_manager_cli_outputs_json(tmp_path: Path) -> None:
    root = _create_workspace(tmp_path)

    completed = subprocess.run(
        [
            sys.executable,
            str(SESSION_MANAGER),
            "--root",
            str(root),
            "--today",
            "2026-07-07",
            "--json",
            "start",
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        check=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["command"] == "start"
    assert payload["ready"] is True
