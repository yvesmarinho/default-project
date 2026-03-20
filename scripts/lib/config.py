"""
lib/config.py — ProjectConfig dataclass, constantes e paths.

Parte do scripts/scaffold.py — Enterprise Default Project Template.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# ---------------------------------------------------------------------------
# Versão do scaffold e data de sincronização do SpecKit
# ---------------------------------------------------------------------------
SCAFFOLD_VERSION = "1.0.0"

# Data da última atualização dos assets SpecKit neste template.
# Atualizar manualmente sempre que agents/prompts forem modificados.
SPECKIT_SYNC_DATE = "2026-03-05"

# ---------------------------------------------------------------------------
# Caminhos padrão
# ---------------------------------------------------------------------------
DEFAULT_SHARED_DIR = Path.home() / "Documentos" / "DevOps" / ".copilot-shared"

# Pós-IMP-13: apenas um arquivo copilot ativo (consolidado de 5 → 1)
SHARED_COPILOT_FILES: list[str] = [
    ".copilot-rules.md",
]

# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------
DomainType = Literal["programming", "infrastructure", "analysis"]
LanguageType = Literal["python", "typescript", "go", "other"]
ExtraProfilesMode = Literal["domain-only", "all", "custom"]

# ---------------------------------------------------------------------------
# Perfis de domínio
# ---------------------------------------------------------------------------

# Perfil principal por domínio (copiado sempre)
DOMAIN_DEFAULT_PROFILES: dict[str, str] = {
    "programming":    "devops-programming",
    "infrastructure": "devops-infrastructure",
    "analysis":       "devops-analysis",
}

# Todos os perfis selecionáveis (excluindo o transversal de segurança)
ALL_SELECTABLE_PROFILES: list[str] = [
    "devops-programming",
    "devops-infrastructure",
    "devops-analysis",
]

# Perfil transversal — copiado silenciosamente em todos os projetos (D-20)
SPECKIT_TRANSVERSAL_PROFILES: list[str] = ["devops-security"]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ProjectConfig:
    """Configuração completa de um projeto scaffold."""

    project_name: str                   # slug kebab-case, ex: my-api-v2
    project_title: str                  # legível, ex: My API v2
    description: str                    # 1 frase
    domain: DomainType                  # programming | infrastructure | analysis
    language: LanguageType              # python | typescript | go | other
    github_repo: str | None             # URL GitHub ou None
    shared_dir: Path                    # caminho para .copilot-shared
    target_dir: Path                    # onde o projeto será criado
    created_at: str                     # ISO8601 timestamp
    extra_profiles: list[str] = field(default_factory=list)  # perfis extras além do domínio (D-21)


@dataclass
class CreatedItem:
    """Resultado de uma operação de criação (pasta, arquivo, symlink, git)."""

    path: Path
    kind: Literal["dir", "file", "symlink", "git"]
    status: Literal["created", "skipped", "error"]
    message: str = ""


@dataclass
class LinkStatus:
    """Resultado da verificação de um symlink .copilot-*."""

    name: str
    target: Path | None
    status: Literal["ok", "broken", "missing"]


# ---------------------------------------------------------------------------
# Domínios válidos e linguagens válidas
# ---------------------------------------------------------------------------
VALID_DOMAINS: list[str] = ["programming", "infrastructure", "analysis"]
VALID_LANGUAGES: list[str] = ["python", "typescript", "go", "other"]
