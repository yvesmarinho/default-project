"""
tests/test_smoke_imp31.py — IMP-31: Smoke tests para CI/CD do template.

Cobertura:
  Existência e estrutura do workflow ci-template.yml:
    - arquivo existe em .github/workflows/ci-template.yml
    - é YAML válido
    - tem chave 'on' (trigger)
    - dispara em pull_request
    - dispara em push para main/master
    - contém path trigger para scripts/**
    - contém path trigger para tests/**
    - contém path trigger para profile-descriptors/**
    - job 'test' existe
    - job 'test' usa matrix python-version
    - matrix inclui python 3.10
    - matrix inclui python 3.12
    - job 'test' roda 'pytest tests/'
    - job 'cli-smoke' existe
    - job 'cli-smoke' executa --list-profiles --json
    - job 'cli-smoke' executa --dry-run
    - job 'cli-smoke' executa --publish --json
    - job 'lint' existe
    - job 'lint' compila scaffold.py
    - job 'lint' valida YAMLs dos profile descriptors
    - concurrency com cancel-in-progress
    - job 'cli-smoke' depende de 'test' (needs: test)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_PROJECT_ROOT = Path(__file__).parent.parent
_WORKFLOW_PATH = _PROJECT_ROOT / ".github" / "workflows" / "ci-template.yml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_workflow() -> dict:
    """Carrega o workflow YAML — pula o teste se pyyaml não estiver instalado."""
    if not _HAS_YAML:
        pytest.skip("pyyaml não instalado — pulando testes de estrutura YAML")
    return yaml.safe_load(_WORKFLOW_PATH.read_text(encoding="utf-8")) or {}


def _workflow_text() -> str:
    return _WORKFLOW_PATH.read_text(encoding="utf-8")


# ===========================================================================
# Existência e validade
# ===========================================================================


class TestWorkflowExists:

    def test_file_exists(self) -> None:
        assert _WORKFLOW_PATH.exists(), f"Workflow não encontrado: {_WORKFLOW_PATH}"

    def test_file_is_valid_yaml(self) -> None:
        data = _load_workflow()
        assert isinstance(data, dict), "Workflow YAML não é um dict"

    def test_has_on_trigger(self) -> None:
        data = _load_workflow()
        assert "on" in data or True in data, "Chave 'on' ausente no workflow"

    def test_has_jobs(self) -> None:
        data = _load_workflow()
        assert "jobs" in data, "Chave 'jobs' ausente no workflow"


# ===========================================================================
# Triggers
# ===========================================================================


class TestWorkflowTriggers:

    def test_triggers_on_pull_request(self) -> None:
        text = _workflow_text()
        assert "pull_request" in text

    def test_triggers_on_push(self) -> None:
        text = _workflow_text()
        assert "push" in text

    def test_push_targets_master(self) -> None:
        text = _workflow_text()
        assert "master" in text

    def test_push_targets_main(self) -> None:
        text = _workflow_text()
        assert "main" in text

    def test_path_trigger_scripts(self) -> None:
        text = _workflow_text()
        assert "scripts/**" in text

    def test_path_trigger_tests(self) -> None:
        text = _workflow_text()
        assert "tests/**" in text

    def test_path_trigger_profile_descriptors(self) -> None:
        text = _workflow_text()
        assert "profile-descriptors/**" in text

    def test_has_concurrency_cancel(self) -> None:
        text = _workflow_text()
        assert "cancel-in-progress" in text


# ===========================================================================
# Job: test (matrix)
# ===========================================================================


class TestJobTest:

    def test_job_test_exists(self) -> None:
        data = _load_workflow()
        assert "test" in data["jobs"], "Job 'test' ausente"

    def test_job_test_has_matrix(self) -> None:
        data = _load_workflow()
        strategy = data["jobs"]["test"].get("strategy", {})
        assert "matrix" in strategy, "Job 'test' sem strategy.matrix"

    def test_matrix_includes_python_310(self) -> None:
        text = _workflow_text()
        assert "3.10" in text, "Python 3.10 ausente na matrix"

    def test_matrix_includes_python_312(self) -> None:
        text = _workflow_text()
        assert "3.12" in text, "Python 3.12 ausente na matrix"

    def test_job_test_runs_full_suite(self) -> None:
        text = _workflow_text()
        assert "pytest tests/" in text, "'pytest tests/' ausente nos steps"

    def test_job_test_uses_pip_cache(self) -> None:
        text = _workflow_text()
        assert "actions/cache" in text, "Cache de pip ausente"


# ===========================================================================
# Job: cli-smoke
# ===========================================================================


class TestJobCliSmoke:

    def test_job_cli_smoke_exists(self) -> None:
        data = _load_workflow()
        assert "cli-smoke" in data["jobs"], "Job 'cli-smoke' ausente"

    def test_cli_smoke_needs_test(self) -> None:
        data = _load_workflow()
        needs = data["jobs"]["cli-smoke"].get("needs", [])
        if isinstance(needs, str):
            needs = [needs]
        assert "test" in needs, "cli-smoke não declara needs: test"

    def test_cli_smoke_runs_list_profiles(self) -> None:
        text = _workflow_text()
        assert "--list-profiles --json" in text

    def test_cli_smoke_runs_dry_run(self) -> None:
        text = _workflow_text()
        assert "--dry-run" in text

    def test_cli_smoke_runs_publish(self) -> None:
        text = _workflow_text()
        assert "--publish --json" in text


# ===========================================================================
# Job: lint
# ===========================================================================


class TestJobLint:

    def test_job_lint_exists(self) -> None:
        data = _load_workflow()
        assert "lint" in data["jobs"], "Job 'lint' ausente"

    def test_lint_compiles_scaffold_py(self) -> None:
        text = _workflow_text()
        assert "py_compile" in text and "scaffold.py" in text

    def test_lint_validates_profile_descriptors_yaml(self) -> None:
        text = _workflow_text()
        assert "profile-descriptors" in text and "yaml" in text.lower()
