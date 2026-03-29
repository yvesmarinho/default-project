"""
tests/test_smoke_imp47.py — IMP-47: Correção do bug de pasta aninhada em scaffold upgrade.

Cobertura:
  config_from_state():
    - Modo new: target_dir é o diretório pai, project_path = target_dir / name ✅
    - Modo upgrade com override apontando para o projeto:
      * override_target.name == project_name → extrai diretório pai
      * project_path = parent / name (sem duplicação) ✅
    - Modo upgrade com override apontando para o pai:
      * override_target.name != project_name → usa como está
      * project_path = target_dir / name ✅
    - Modo normal sem override:
      * Usa target_dir do state
      * project_path = target_dir / name ✅

Bug original (IMP-47):
  - upgrade --target-dir /path/to/my-project criava /path/to/my-project/my-project/
  - Causa: config_from_state não detectava que override era o próprio projeto
  - Correção: detectar se override_target.name == project_name e extrair pai
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.project import config_from_state  # noqa: E402

# ---------------------------------------------------------------------------
# Testes unitários para config_from_state
# ---------------------------------------------------------------------------


def test_config_from_state_mode_new_no_override():
    """Modo new: sem override, usa target_dir do state (diretório pai)."""
    state = {
        "project": {
            "name": "my-api",
            "title": "My API",
            "description": "Test project",
            "domain": "software",
            "language": "python",
        },
        "paths": {
            "target_dir": "/home/user/projects",
            "shared_dir": "/home/user/.copilot-shared",
        },
    }

    config = config_from_state(state, override_target=None)

    assert config.project_name == "my-api"
    assert config.target_dir == Path("/home/user/projects")
    # project_path deve ser target_dir / project_name
    assert config.project_path == Path("/home/user/projects/my-api")


def test_config_from_state_upgrade_override_is_project():
    """
    Modo upgrade (IMP-47): override_target É O PRÓPRIO PROJETO.
    
    Comportamento esperado:
      - override_target = /home/user/projects/my-api
      - project_name = my-api
      - override_target.name == project_name → extrai diretório pai
      - target_dir = /home/user/projects (pai)
      - project_path = /home/user/projects/my-api ✅ (sem duplicação)
    """
    state = {
        "project": {
            "name": "my-api",
            "title": "My API",
            "description": "Test project",
            "domain": "software",
            "language": "python",
        },
        "paths": {
            "target_dir": "/home/user/projects",  # Histórico da criação
            "shared_dir": "/home/user/.copilot-shared",
        },
    }

    # Simula: scaffold.py upgrade --target-dir /home/user/projects/my-api
    override_target = Path("/home/user/projects/my-api")

    config = config_from_state(state, override_target=override_target)

    assert config.project_name == "my-api"
    # Correção IMP-47: deve extrair o diretório pai
    assert config.target_dir == Path("/home/user/projects")
    # project_path NÃO deve criar pasta aninhada
    assert config.project_path == Path("/home/user/projects/my-api")
    # NÃO deve ser /home/user/projects/my-api/my-api ❌


def test_config_from_state_upgrade_override_is_parent():
    """
    Modo upgrade: override_target aponta para o diretório pai (uso raro).
    
    Comportamento esperado:
      - override_target = /home/user/projects
      - project_name = my-api
      - override_target.name != project_name → usa como está
      - target_dir = /home/user/projects
      - project_path = /home/user/projects/my-api ✅
    """
    state = {
        "project": {
            "name": "my-api",
            "title": "My API",
            "description": "Test project",
            "domain": "software",
            "language": "python",
        },
        "paths": {
            "target_dir": "/home/user/projects",
            "shared_dir": "/home/user/.copilot-shared",
        },
    }

    # Simula: scaffold.py upgrade --target-dir /home/user/projects
    override_target = Path("/home/user/projects")

    config = config_from_state(state, override_target=override_target)

    assert config.project_name == "my-api"
    assert config.target_dir == Path("/home/user/projects")
    assert config.project_path == Path("/home/user/projects/my-api")


def test_config_from_state_nested_folder_bug_scenario():
    """
    Cenário real do bug IMP-47 (enterprise-python-analysis).
    
    Setup:
      - Projeto: enterprise-python-analysis
      - State: target_dir = /home/user/Vya-Jobs (diretório pai)
      - Comando: cd enterprise-python-analysis && scaffold.py upgrade
      - override_target = /home/user/Vya-Jobs/enterprise-python-analysis
    
    Bug original:
      - target_dir ficava = /home/user/Vya-Jobs/enterprise-python-analysis
      - project_path = target_dir / name
                      = /home/user/Vya-Jobs/enterprise-python-analysis/enterprise-python-analysis ❌
    
    Após correção:
      - Detecta override_target.name == "enterprise-python-analysis"
      - Extrai pai: target_dir = /home/user/Vya-Jobs
      - project_path = /home/user/Vya-Jobs/enterprise-python-analysis ✅
    """
    state = {
        "project": {
            "name": "enterprise-python-analysis",
            "title": "Enterprise Python Analysis",
            "description": "Python analysis project",
            "domain": "software",
            "language": "python",
        },
        "paths": {
            "target_dir": "/home/user/Vya-Jobs",
            "shared_dir": "/home/user/.copilot-shared",
        },
    }

    # Comando executado do diretório do projeto
    override_target = Path("/home/user/Vya-Jobs/enterprise-python-analysis")

    config = config_from_state(state, override_target=override_target)

    assert config.project_name == "enterprise-python-analysis"
    # Correção: extrai diretório pai
    assert config.target_dir == Path("/home/user/Vya-Jobs")
    # NÃO deve criar pasta aninhada
    assert config.project_path == Path("/home/user/Vya-Jobs/enterprise-python-analysis")
    # Verifica que NÃO é a pasta aninhada
    assert str(config.project_path) != "/home/user/Vya-Jobs/enterprise-python-analysis/enterprise-python-analysis"


def test_config_from_state_preserves_other_fields():
    """Verificar que a correção não quebra outros campos do ProjectConfig."""
    state = {
        "project": {
            "name": "test-project",
            "title": "Test Project",
            "description": "Test description",
            "domain": "infrastructure",
            "language": "python",
            "github_repo": "user/test-project",
        },
        "paths": {
            "target_dir": "/projects",
            "shared_dir": "/shared",
        },
        "profiles_applied": ["python-fastapi", "devops-infrastructure"],
        "created_at": "2026-01-01T00:00:00Z",
    }

    override_target = Path("/projects/test-project")
    config = config_from_state(state, override_target=override_target)

    # Campos do projeto preservados
    assert config.project_name == "test-project"
    assert config.project_title == "Test Project"
    assert config.description == "Test description"
    assert config.domain == "infrastructure"
    assert config.language == "python"
    assert config.github_repo == "user/test-project"

    # Paths corretos
    assert config.target_dir == Path("/projects")
    assert config.shared_dir == Path("/shared")
    assert config.project_path == Path("/projects/test-project")

    # Metadata preservado
    assert config.extra_profiles == ["python-fastapi", "devops-infrastructure"]
    assert config.created_at == "2026-01-01T00:00:00Z"


# ---------------------------------------------------------------------------
# Testes de edge cases
# ---------------------------------------------------------------------------


def test_config_from_state_project_name_with_special_chars():
    """Garantir que nomes com caracteres especiais não quebram a detecção."""
    state = {
        "project": {
            "name": "my-api-v2",
            "title": "My API v2",
            "domain": "software",
            "language": "typescript",
        },
        "paths": {
            "target_dir": "/projects",
            "shared_dir": "/shared",
        },
    }

    # override termina com o nome do projeto
    override_target = Path("/projects/my-api-v2")
    config = config_from_state(state, override_target=override_target)

    assert config.project_name == "my-api-v2"
    assert config.target_dir == Path("/projects")
    assert config.project_path == Path("/projects/my-api-v2")


def test_config_from_state_deeply_nested_path():
    """Verificar que paths profundos funcionam corretamente."""
    state = {
        "project": {
            "name": "deep-project",
            "domain": "software",
            "language": "python",
        },
        "paths": {
            "target_dir": "/home/user/workspace/subdir1/subdir2",
            "shared_dir": "/shared",
        },
    }

    override_target = Path("/home/user/workspace/subdir1/subdir2/deep-project")
    config = config_from_state(state, override_target=override_target)

    assert config.target_dir == Path("/home/user/workspace/subdir1/subdir2")
    assert config.project_path == Path("/home/user/workspace/subdir1/subdir2/deep-project")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
