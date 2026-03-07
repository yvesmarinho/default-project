"""
tests/test_smoke_infra.py — IMP-15: Smoke tests para lib/infra.py.

Cobertura: 4 funções × 4 linguagens + 1 teste de idempotência = 17 testes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.infra import (  # noqa: E402
    generate_ci_workflow,
    generate_docker_compose,
    generate_dockerfile,
    generate_runbook,
)

LANGUAGES = ["python", "typescript", "go", "other"]


# ---------------------------------------------------------------------------
# CI Workflow
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("language", LANGUAGES)
def test_ci_workflow_created(make_project_config, language: str) -> None:
    """ci.yml é criado com status 'created' e conteúdo válido."""
    cfg = make_project_config("programming", language)
    result = generate_ci_workflow(cfg)

    assert result.status == "created", f"[{language}] status={result.status!r}"
    assert result.path.name == "ci.yml"
    content = result.path.read_text()
    assert "CI" in content
    assert "on:" in content
    assert len(content) > 100


@pytest.mark.parametrize("language", LANGUAGES)
def test_ci_workflow_skipped_if_exists(make_project_config, language: str) -> None:
    """Segunda chamada retorna 'skipped' (não sobrescreve)."""
    cfg = make_project_config("programming", language)
    generate_ci_workflow(cfg)
    result2 = generate_ci_workflow(cfg)

    assert result2.status == "skipped", f"[{language}] deveria ser skipped, got={result2.status!r}"


# ---------------------------------------------------------------------------
# Dockerfile
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("language", LANGUAGES)
def test_dockerfile_created(make_project_config, language: str) -> None:
    """Dockerfile é criado com status 'created' e multistage válido."""
    cfg = make_project_config("programming", language)
    result = generate_dockerfile(cfg)

    assert result.status == "created", f"[{language}] status={result.status!r}"
    content = result.path.read_text()
    assert "FROM" in content, f"[{language}] Dockerfile sem instrução FROM"
    assert "AS " in content, f"[{language}] Dockerfile não é multistage"


# ---------------------------------------------------------------------------
# docker-compose.yml
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("language", LANGUAGES)
def test_docker_compose_created(make_project_config, language: str) -> None:
    """docker-compose.yml contém serviço app e placeholders substituídos."""
    cfg = make_project_config("programming", language)
    result = generate_docker_compose(cfg)

    assert result.status == "created", f"[{language}] status={result.status!r}"
    content = result.path.read_text()
    assert "services:" in content
    assert "app:" in content
    assert cfg.project_name in content, f"[{language}] project_name não substituído"
    assert "{project_name}" not in content, f"[{language}] placeholder não resolvido"


# ---------------------------------------------------------------------------
# RUNBOOK.md
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("language", LANGUAGES)
def test_runbook_created(make_project_config, language: str) -> None:
    """RUNBOOK.md contém project_name e project_title substituídos."""
    cfg = make_project_config("programming", language)
    result = generate_runbook(cfg)

    assert result.status == "created", f"[{language}] status={result.status!r}"
    content = result.path.read_text()
    assert "Runbook" in content
    assert cfg.project_name in content, f"[{language}] project_name não substituído"
    assert cfg.project_title in content, f"[{language}] project_title não substituído"
    assert "{project_name}" not in content, f"[{language}] placeholder não resolvido"


# ---------------------------------------------------------------------------
# Idempotência global
# ---------------------------------------------------------------------------


def test_all_infra_skipped_on_second_call(make_project_config) -> None:
    """Todos os 4 geradores retornam 'skipped' na segunda chamada."""
    cfg = make_project_config("programming", "python")
    generate_ci_workflow(cfg)
    generate_dockerfile(cfg)
    generate_docker_compose(cfg)
    generate_runbook(cfg)

    assert generate_ci_workflow(cfg).status == "skipped"
    assert generate_dockerfile(cfg).status == "skipped"
    assert generate_docker_compose(cfg).status == "skipped"
    assert generate_runbook(cfg).status == "skipped"
