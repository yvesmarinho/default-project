"""
tests/test_smoke_infra.py — IMP-15: Smoke tests para lib/infra.py.

Cobertura: 4 funções × 4 linguagens + 1 teste de idempotência = 17 testes.
IMP-40: testes de seções parametrizadas por perfil no RUNBOOK.md.
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


# ---------------------------------------------------------------------------
# RUNBOOK.md — seções parametrizadas por perfil (IMP-40)
# ---------------------------------------------------------------------------


def test_runbook_no_profile_sections_when_empty(make_project_config) -> None:
    """Sem extra_profiles, RUNBOOK não contém seções de perfil específico."""
    cfg = make_project_config("programming", "python")
    result = generate_runbook(cfg)

    content = result.path.read_text()
    assert "helm status" not in content
    assert "terraform plan" not in content
    assert "uv run pytest" not in content


def test_runbook_contains_k8s_helm_section(make_project_config) -> None:
    """Com k8s-helm em extra_profiles, RUNBOOK contém comandos Helm/kubectl."""
    cfg = make_project_config("programming", "python", extra_profiles=["k8s-helm"])
    result = generate_runbook(cfg)

    content = result.path.read_text()
    assert "helm status" in content
    assert "helm rollback" in content
    assert "kubectl rollout undo" in content
    assert cfg.project_name in content


def test_runbook_contains_terraform_aws_section(make_project_config) -> None:
    """Com terraform-aws em extra_profiles, RUNBOOK contém comandos Terraform/AWS."""
    cfg = make_project_config("programming", "python", extra_profiles=["terraform-aws"])
    result = generate_runbook(cfg)

    content = result.path.read_text()
    assert "terraform plan" in content
    assert "terraform apply -target" in content
    assert "aws ecs describe-services" in content
    assert cfg.project_name in content


def test_runbook_contains_python_fastapi_section(make_project_config) -> None:
    """Com python-fastapi em extra_profiles, RUNBOOK contém comandos FastAPI."""
    cfg = make_project_config("programming", "python", extra_profiles=["python-fastapi"])
    result = generate_runbook(cfg)

    content = result.path.read_text()
    assert "uv run pytest" in content
    assert "/health" in content
    assert "uvicorn" in content


def test_runbook_multi_profile_injects_all_sections(make_project_config) -> None:
    """Com múltiplos perfis, todas as seções correspondentes são injetadas."""
    cfg = make_project_config(
        "programming",
        "python",
        extra_profiles=["k8s-helm", "terraform-aws", "python-fastapi"],
    )
    result = generate_runbook(cfg)

    content = result.path.read_text()
    assert "helm status" in content
    assert "terraform plan" in content
    assert "uv run pytest" in content


def test_runbook_generic_content_always_present(make_project_config) -> None:
    """Conteúdo genérico (Quick-start, CI/CD, Deploy) está presente com ou sem perfis."""
    cfg_no_profiles = make_project_config("programming", "python")
    cfg_with_profiles = make_project_config(
        "programming",
        "go",
        extra_profiles=["k8s-helm"],
    )

    for cfg in (cfg_no_profiles, cfg_with_profiles):
        content = generate_runbook(cfg).path.read_text()
        assert "Quick-start" in content
        assert "CI/CD" in content
        assert "Deploy" in content
        assert cfg.project_name in content


def test_runbook_unknown_profile_no_extra_sections(make_project_config) -> None:
    """Perfil desconhecido não injeta seções extras (sem crash)."""
    cfg = make_project_config("programming", "python", extra_profiles=["unknown-profile"])
    result = generate_runbook(cfg)

    content = result.path.read_text()
    assert result.status == "created"
    assert "helm status" not in content
    assert "terraform plan" not in content
    assert "uv run pytest" not in content
