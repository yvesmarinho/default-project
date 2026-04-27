"""
lib/vscode.py — Geração de arquivos VS Code personalizados por domínio/linguagem.

Parte do scripts/scaffold.py — Enterprise Default Project Template.

Gera:
  .vscode/settings.json   — configurações do editor por linguagem
  .vscode/mcp.json        — servidores MCP pré-selecionados por domínio
  .vscode/extensions.json — extensões recomendadas (BASE + DOMAIN + LANGUAGE)
"""

from __future__ import annotations

import json
from pathlib import Path

from .config import CreatedItem, DomainType, LanguageType, ProjectConfig

# ---------------------------------------------------------------------------
# Extensões — 3 camadas: BASE + DOMAIN + LANGUAGE
# ---------------------------------------------------------------------------

BASE_EXTENSIONS: list[str] = [
    "github.copilot",
    "github.copilot-chat",
    "eamodio.gitlens",
    "mhutchie.git-graph",
    "usernamehw.errorlens",
    "EditorConfig.EditorConfig",
    "streetsidesoftware.code-spell-checker",
    "yzhang.markdown-all-in-one",
    "christian-kohler.path-intellisense",
    "donjayamanne.githistory",
    "ms-vscode.live-server",
]

DOMAIN_EXTENSIONS: dict[str, list[str]] = {
    "programming": [],  # linguagem define os extras
    "infrastructure": [
        "ms-azuretools.vscode-docker",
        "p1c2u.docker-compose",
        "exiasr.hadolint",
        "ms-vscode-remote.remote-containers",
        "ms-vscode-remote.remote-ssh",
        "HashiCorp.terraform",
        "redhat.vscode-yaml",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "tim-koehler.helm-intellisense",
        "redhat.ansible",
        "signageos.signageos-vscode-sops",
    ],
    "analysis": [
        "ms-toolsai.jupyter",
        "ms-toolsai.vscode-jupyter-slideshow",
        "ms-toolsai.jupyter-keymap",
        "mechatroner.rainbow-csv",
        "GrapeCity.gc-excelviewer",
    ],
}

LANGUAGE_EXTENSIONS: dict[str, list[str]] = {
    "python": [
        "ms-python.python",
        "ms-python.pylance",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "ms-python.debugpy",
        "njpwerner.autodocstring",
        "ms-python.isort",
        "KevinRose.vsc-python-indent",
    ],
    "typescript": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next",
        "orta.vscode-jest",
        "bradlc.vscode-tailwindcss",
        "ms-vscode.js-debug",
    ],
    "go": [
        "golang.go",
    ],
    "other": [],
}

# ---------------------------------------------------------------------------
# Settings por linguagem
# ---------------------------------------------------------------------------

_SETTINGS_BY_LANGUAGE: dict[str, dict] = {
    "python": {
        "python.defaultInterpreterPath": ".venv/bin/python",
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": True,
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "python.linting.mypyEnabled": True,
        "python.analysis.typeCheckingMode": "basic",
        "editor.rulers": [88],
        "isort.args": ["--profile", "black"],
    },
    "typescript": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {"source.fixAll.eslint": True},
        "typescript.preferences.importModuleSpecifier": "relative",
        "editor.rulers": [100],
    },
    "go": {
        "go.useLanguageServer": True,
        "editor.formatOnSave": True,
        "editor.rulers": [120],
    },
    "other": {
        "editor.formatOnSave": True,
        "editor.rulers": [120],
    },
}

_SETTINGS_BY_DOMAIN: dict[str, dict] = {
    "infrastructure": {
        "editor.defaultFormatter": "redhat.vscode-yaml",
        "editor.formatOnSave": True,
        "yaml.schemas": {
            "https://raw.githubusercontent.com/compose-spec/compose-spec/master/schema/compose-spec.json": "docker-compose*.yml",
        },
        "docker.showStartPage": False,
        "editor.rulers": [120],
    },
    "programming": {},
    "analysis": {
        "editor.formatOnSave": True,
        "editor.rulers": [100],
    },
}

# ---------------------------------------------------------------------------
# Servidores MCP por domínio
# ---------------------------------------------------------------------------

_ALL_MCP_SERVERS: dict[str, dict] = {
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "type": "stdio",
    },
    "sequential-thinking": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        "type": "stdio",
    },
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
        "type": "stdio",
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "type": "stdio",
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}",
        },
    },
    "sqlite": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", ".data/db.sqlite"],
        "type": "stdio",
    },
    "brave-search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "type": "stdio",
        "env": {
            "BRAVE_API_KEY": "${env:BRAVE_API_KEY}",
        },
    },
}

_MCP_BY_DOMAIN: dict[str, list[str]] = {
    "programming":    ["memory", "sequential-thinking", "filesystem", "github"],
    "infrastructure": ["memory", "sequential-thinking", "filesystem", "github", "sqlite"],
    "analysis":       ["memory", "sequential-thinking", "filesystem", "sqlite", "brave-search"],
}


# ---------------------------------------------------------------------------
# Funções públicas
# ---------------------------------------------------------------------------

def generate_settings(config: ProjectConfig) -> CreatedItem:
    """
    Gera `.vscode/settings.json` personalizado pela linguagem e domínio.
    Não sobrescreve se já existe.
    """
    dest = config.project_path / ".vscode" / "settings.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")

    settings: dict = {}
    # Aplica settings do domínio primeiro
    settings.update(_SETTINGS_BY_DOMAIN.get(config.domain, {}))
    # Depois os da linguagem (mais específicos sobrescrevem)
    settings.update(_SETTINGS_BY_LANGUAGE.get(config.language, {}))

    return _write_json(dest, settings)


def generate_mcp(config: ProjectConfig) -> CreatedItem:
    """
    Gera `.vscode/mcp.json` com servidores pré-selecionados pelo domínio.
    Não sobrescreve se já existe.
    """
    dest = config.project_path / ".vscode" / "mcp.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")

    server_names = _MCP_BY_DOMAIN.get(config.domain, ["memory", "sequential-thinking"])
    servers = {name: _ALL_MCP_SERVERS[name] for name in server_names if name in _ALL_MCP_SERVERS}

    return _write_json(dest, {"servers": servers})


def generate_extensions(config: ProjectConfig) -> CreatedItem:
    """
    Gera `.vscode/extensions.json` com extensões recomendadas.

    Combina em 3 camadas:
      1. BASE_EXTENSIONS      → sempre incluídas
      2. DOMAIN_EXTENSIONS    → por domínio
      3. LANGUAGE_EXTENSIONS  → por linguagem

    Lista final deduplicada e ordenada. Não sobrescreve se já existe.
    """
    dest = config.project_path / ".vscode" / "extensions.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")

    combined: list[str] = list(BASE_EXTENSIONS)  # cópia
    combined.extend(DOMAIN_EXTENSIONS.get(config.domain, []))
    combined.extend(LANGUAGE_EXTENSIONS.get(config.language, []))

    # Deduplica preservando ordem de inserção
    seen: set[str] = set()
    unique: list[str] = []
    for ext in combined:
        if ext not in seen:
            seen.add(ext)
            unique.append(ext)

    payload = {"recommendations": sorted(unique)}
    return _write_json(dest, payload)


# ---------------------------------------------------------------------------
# Auxiliar interno
# ---------------------------------------------------------------------------

def generate_tasks(config: ProjectConfig) -> CreatedItem:
    """
    Gera `.vscode/tasks.json` com os targets padrão do Makefile como tasks VS Code.

    Tasks: install-deps, dev, build, test (isDefault), lint, format, clean.
    Não sobrescreve se já existe.
    """
    dest = config.project_path / ".vscode" / "tasks.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")

    tasks = [
        {
            "label": "make: install-deps",
            "type": "shell",
            "command": "make install-deps",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "make: dev",
            "type": "shell",
            "command": "make dev",
            "group": {"kind": "build", "isDefault": True},
            "problemMatcher": [],
        },
        {
            "label": "make: build",
            "type": "shell",
            "command": "make build",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "make: test",
            "type": "shell",
            "command": "make test",
            "group": {"kind": "test", "isDefault": True},
            "problemMatcher": [],
        },
        {
            "label": "make: lint",
            "type": "shell",
            "command": "make lint",
            "group": "test",
            "problemMatcher": [],
        },
        {
            "label": "make: format",
            "type": "shell",
            "command": "make format",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "make: clean",
            "type": "shell",
            "command": "make clean",
            "group": "build",
            "problemMatcher": [],
        },
    ]

    return _write_json(dest, {"version": "2.0.0", "tasks": tasks})


def generate_launch(config: ProjectConfig) -> CreatedItem:
    """
    Gera `.vscode/launch.json` com configurações de debug por linguagem.

    Python: debugpy (módulo atual + pytest)
    TypeScript: js-debug (arquivo atual + jest)
    Go: dlv (teste + execução direta)
    other: generic shell run

    Não sobrescreve se já existe.
    """
    dest = config.project_path / ".vscode" / "launch.json"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")

    configurations: list[dict] = _LAUNCH_BY_LANGUAGE.get(
        config.language, _LAUNCH_BY_LANGUAGE["other"]
    )

    return _write_json(dest, {"version": "0.2.0", "configurations": configurations})


# ---------------------------------------------------------------------------
# Launch configurations per language
# ---------------------------------------------------------------------------

_LAUNCH_BY_LANGUAGE: dict[str, list[dict]] = {
    "python": [
        {
            "name": "Python: módulo atual",
            "type": "debugpy",
            "request": "launch",
            "module": "${fileBasenameNoExtension}",
            "justMyCode": True,
        },
        {
            "name": "Python: pytest",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": ["${workspaceFolder}/tests", "-v"],
            "justMyCode": False,
        },
    ],
    "typescript": [
        {
            "name": "TypeScript: arquivo atual",
            "type": "node",
            "request": "launch",
            "program": "${file}",
            "runtimeArgs": ["-r", "ts-node/register"],
            "sourceMaps": True,
            "outFiles": ["${workspaceFolder}/dist/**/*.js"],
        },
        {
            "name": "TypeScript: Jest",
            "type": "node",
            "request": "launch",
            "runtimeExecutable": "npx",
            "runtimeArgs": ["jest", "--runInBand", "--no-coverage"],
            "sourceMaps": True,
            "console": "integratedTerminal",
        },
    ],
    "go": [
        {
            "name": "Go: arquivo atual",
            "type": "go",
            "request": "launch",
            "mode": "debug",
            "program": "${file}",
        },
        {
            "name": "Go: testes do pacote",
            "type": "go",
            "request": "launch",
            "mode": "test",
            "program": "${workspaceFolder}",
            "args": ["-v", "-run", "Test"],
        },
    ],
    "other": [
        {
            "name": "Shell: script atual",
            "type": "node",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
        },
    ],
}


def generate_workspace(config: ProjectConfig) -> CreatedItem:
    """
    Gera `[project-name].code-workspace` com configurações MCP integradas.
    
    Inclui:
    - Folders (path atual)
    - Settings básicos (formatOnSave, rulers, etc)
    - Tasks do Makefile
    - Launch configurations vazias
    - **MCP servers** (dinamicamente por domínio) ⭐ FIX BUG
    
    Não sobrescreve se já existe.
    """
    dest = config.project_path / f"{config.project_name}.code-workspace"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")
    
    # Get MCP servers for this domain
    server_names = _MCP_BY_DOMAIN.get(config.domain, ["memory", "sequential-thinking"])
    mcp_servers = {name: _ALL_MCP_SERVERS[name] for name in server_names if name in _ALL_MCP_SERVERS}
    
    # Get settings for this language/domain
    settings: dict = {}
    settings.update(_SETTINGS_BY_DOMAIN.get(config.domain, {}))
    settings.update(_SETTINGS_BY_LANGUAGE.get(config.language, {}))
    
    # Add base settings
    settings.update({
        "editor.formatOnSave": True,
        "editor.rulers": [88, 120],
        "files.trimTrailingWhitespace": True,
        "files.insertFinalNewline": True,
    })
    
    workspace_config = {
        "folders": [{"path": "."}],
        "settings": settings,
        "mcp": {
            "servers": mcp_servers
        },
        "tasks": {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "make: install-deps",
                    "type": "shell",
                    "command": "make install-deps",
                    "group": "build",
                    "problemMatcher": []
                },
                {
                    "label": "make: dev",
                    "type": "shell",
                    "command": "make dev",
                    "group": {"kind": "build", "isDefault": True},
                    "problemMatcher": []
                },
                {
                    "label": "make: build",
                    "type": "shell",
                    "command": "make build",
                    "group": "build",
                    "problemMatcher": []
                },
                {
                    "label": "make: test",
                    "type": "shell",
                    "command": "make test",
                    "group": {"kind": "test", "isDefault": True},
                    "problemMatcher": []
                },
                {
                    "label": "make: lint",
                    "type": "shell",
                    "command": "make lint",
                    "group": "test",
                    "problemMatcher": []
                },
                {
                    "label": "make: format",
                    "type": "shell",
                    "command": "make format",
                    "group": "build",
                    "problemMatcher": []
                },
                {
                    "label": "make: clean",
                    "type": "shell",
                    "command": "make clean",
                    "group": "build",
                    "problemMatcher": []
                }
            ]
        },
        "launch": {
            "version": "0.2.0",
            "configurations": []
        }
    }
    
    return _write_json(dest, workspace_config)


# ---------------------------------------------------------------------------
# Auxiliar interno
# ---------------------------------------------------------------------------

def _write_json(dest: Path, data: dict) -> CreatedItem:
    """Serializa dict como JSON formatado e grava em dest."""
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return CreatedItem(path=dest, kind="file", status="created")
    except OSError as e:
        return CreatedItem(path=dest, kind="file", status="error", message=str(e))
