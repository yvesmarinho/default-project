"""
tests/conftest.py — Fixtures compartilhadas para os testes do scaffold.

IMP-16: Setup de pytest com fixtures de config para todos os combos
        domínio × linguagem.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Garante que scripts/ está no sys.path para importar lib/
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.config import ProjectConfig  # noqa: E402  (import after sys.path)

# ---------------------------------------------------------------------------
# Diretório de snapshots
# ---------------------------------------------------------------------------
SNAPSHOT_DIR = Path(__file__).parent / "snapshots"

# ---------------------------------------------------------------------------
# Opção CLI  --update-snapshots
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Regenera os arquivos de snapshot baseline (sobrescreve os existentes)",
    )


@pytest.fixture
def update_snapshots(request: pytest.FixtureRequest) -> bool:
    return request.config.getoption("--update-snapshots")


# ---------------------------------------------------------------------------
# Fixture factory: ProjectConfig
# ---------------------------------------------------------------------------


@pytest.fixture
def make_project_config(tmp_path: Path):
    """
    Factory fixture que constrói um ProjectConfig isolado em tmp_path.

    Uso:
        def test_foo(make_project_config):
            cfg = make_project_config("programming", "python")
    """

    def _factory(
        domain: str,
        language: str,
        project_name: str = "test-project",
        extra_profiles: list[str] | None = None,
    ) -> ProjectConfig:
        target = tmp_path / project_name
        target.mkdir(parents=True, exist_ok=True)
        return ProjectConfig(
            project_name=project_name,
            project_title="Test Project",
            description="A test project for smoke testing",
            domain=domain,
            language=language,
            github_repo=None,
            shared_dir=tmp_path / "shared",
            target_dir=target,
            created_at="2026-03-07T00:00:00",
            extra_profiles=extra_profiles or [],
        )

    return _factory
