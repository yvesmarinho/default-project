"""
lib/project.py — Criação de estrutura de pastas e arquivos base.

Parte do scripts/scaffold.py — Enterprise Default Project Template.
"""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

from .config import (
    DOMAIN_DEFAULT_PROFILES,
    SPECKIT_SYNC_DATE,
    SPECKIT_TRANSVERSAL_PROFILES,
    CreatedItem,
    ProjectConfig,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Raiz do template (a-default-project/) deduzida a partir da localização deste módulo
_TEMPLATE_ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Placeholders e substituição
# ---------------------------------------------------------------------------

PLACEHOLDERS = {
    "{{PROJECT_NAME}}",
    "{{PROJECT_TITLE}}",
    "{{PROJECT_DESCRIPTION}}",
    "{{CREATED_AT}}",
    "{{DOMAIN}}",
    "{{LANGUAGE}}",
    "{{GITHUB_REPO}}",
}


def _apply_placeholders(text: str, config: ProjectConfig) -> str:
    """Substitui todos os placeholders pelo valor real da config."""
    replacements = {
        "{{PROJECT_NAME}}":        config.project_name,
        "{{PROJECT_TITLE}}":       config.project_title,
        "{{PROJECT_DESCRIPTION}}": config.description,
        "{{CREATED_AT}}":          config.created_at,
        "{{DOMAIN}}":              config.domain,
        "{{LANGUAGE}}":            config.language,
        "{{GITHUB_REPO}}":         config.github_repo or "",
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


# ---------------------------------------------------------------------------
# Templates internos
# ---------------------------------------------------------------------------

_README_MD = """\
# {{PROJECT_TITLE}}

> {{PROJECT_DESCRIPTION}}

**Domínio**: {{DOMAIN}} | **Linguagem**: {{LANGUAGE}}
**Criado em**: {{CREATED_AT}}
{github_section}

---

## 🚀 Início Rápido

```bash
# Instalar dependências
make install-deps

# Iniciar desenvolvimento
make dev
```

## 📚 Documentação

- [Índice](docs/INDEX.md)
- [Tarefas](docs/TODO.md)

## 🏗️ Estrutura

Consulte os [documentos de arquitetura](docs/) para detalhes.
"""

_DOCS_INDEX_MD = """\
# 📚 Índice — {{PROJECT_TITLE}}

**Projeto**: `{{PROJECT_NAME}}`
**Criado em**: {{CREATED_AT}}
**Last Updated**: {{CREATED_AT}}
**Last Session**: N/A

---

## Documentação Principal

| Arquivo | Descrição |
|---------|-----------|
| [README.md](../README.md) | Documentação pública |
| [TODO.md](TODO.md) | Tarefas pendentes |
| [TODAY_ACTIVITIES.md](TODAY_ACTIVITIES.md) | Atividades do dia |

## Sessões de Trabalho

```
SESSIONS/
└── YYYY-MM-DD/
    ├── SESSION_RECOVERY_YYYY-MM-DD.md
    ├── DAILY_ACTIVITIES_YYYY-MM-DD.md
    ├── SESSION_REPORT_YYYY-MM-DD.md
    └── FINAL_STATUS_YYYY-MM-DD.md
```

---

*Gerado por scaffold.py em {{CREATED_AT}}*
"""

_DOCS_TODO_MD = """\
# 📝 TODO — {{PROJECT_TITLE}}

**Last Updated**: {{CREATED_AT}}
**Status**: 🟢 Em andamento

---

## 🟠 Em Progresso

*(nenhum)*

## 🔵 Pendente

- [ ] Configurar estrutura inicial do projeto
- [ ] Adicionar testes unitários
- [ ] Documentar APIs

## ✅ Concluído

- [x] Scaffold inicial gerado ({{CREATED_AT}})
"""

_DOCS_TODAY_ACTIVITIES_MD = """\
# 📅 Atividades — {{PROJECT_TITLE}}

**Data**: {{CREATED_AT}}
**Projeto**: `{{PROJECT_NAME}}`

---

## ⏰ Atividades do Dia

### ✅ Scaffold Inicial Criado

- Projeto `{{PROJECT_NAME}}` inicializado via `uv run scripts/scaffold.py`
- Domínio: {{DOMAIN}} | Linguagem: {{LANGUAGE}}
- Estrutura de pastas criada
- Regras Copilot geradas

---

*Gerado por scaffold.py*
"""

_GITIGNORE = """\
# Segredos e credenciais
.secrets/
*.key
*.pem
*.crt
*.p12
*.pfx
*.jks
*.keystore
secrets/
credentials/
*.credentials
.env
.env.*
!.env.example

# Python
.venv/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage

# Node.js
node_modules/
npm-debug.log*
.npm

# VS Code
.vscode/*
!.vscode/settings.json
!.vscode/mcp.json
!.vscode/extensions.json

# OS
.DS_Store
Thumbs.db
*.swp
*.swo

# Logs
*.log
logs/
!scripts/logs/.gitkeep
"""

_SECRETS_README = """\
# 🔒 .secrets/ — Arquivos Sensíveis

**NUNCA commitar este diretório.**

Este diretório é ignorado pelo `.gitignore`.

## O que armazenar aqui

| Tipo | Exemplos |
|------|---------|
| Variáveis de ambiente | `.env`, `.env.production` |
| Chaves SSH | `id_rsa`, `*.pem` |
| Tokens de API | `api-tokens.txt` |
| Credenciais cloud | `aws-credentials` |
| Segredos Kubernetes | `kubeconfig` |

## Uso com MCP

Para servidores MCP que precisam de tokens:

```json
"env": {
  "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}"
}
```

Configure em `.secrets/.env` e carregue no shell antes de iniciar o VS Code.
"""

_VSCODE_MCP_JSON = """\
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "type": "stdio"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "type": "stdio"
    }
  }
}
"""

_VSCODE_SETTINGS_JSON = """\
{
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/.mypy_cache": true
  }
}
"""

_MAKEFILE = """\
# Makefile — {{PROJECT_TITLE}}
# Gerado por scaffold.py em {{CREATED_AT}}

.PHONY: help init dev build test lint format clean

## Mostra esta ajuda
help:
\t@grep -E '^## ' Makefile | sed 's/## //'

## [DEPRECATED] — use: uv run scripts/scaffold.py
init:
\t@echo ""
\t@echo " ⚠️  Para criar/configurar o projeto, use diretamente:"
\t@echo "      uv run scripts/scaffold.py"
\t@echo "      python scripts/scaffold.py"
\t@echo ""

## Instala dependências
install-deps:
\t@echo "Instalando dependências..."

## Inicia servidor de desenvolvimento
dev:
\t@echo "Iniciando desenvolvimento..."

## Build de produção
build:
\t@echo "Buildando..."

## Executa testes
test:
\t@echo "Executando testes..."

## Lint do código
lint:
\t@echo "Linting..."

## Formata código
format:
\t@echo "Formatando..."

## Remove arquivos gerados
clean:
\t@rm -rf dist/ build/ __pycache__/ .pytest_cache/ *.egg-info/ .coverage htmlcov/
## Carrega variáveis MCP do .secrets/.env e orienta a abrir o VS Code
mcp:
	@bash scripts/load-mcp.sh"""

_CODE_WORKSPACE = """\
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true
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
        "group": { "kind": "build", "isDefault": true },
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
        "group": { "kind": "test", "isDefault": true },
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
"""

# ---------------------------------------------------------------------------
# Pastas a criar
# ---------------------------------------------------------------------------

DIRS_TO_CREATE = [
    "docs",
    "docs/SESSIONS",
    "docs/copilot",
    ".github",
    ".github/agents",
    ".github/prompts",
    ".github/prompts/domain",
    ".secrets",
    ".vscode",
    "scripts/lib",
    "scripts/logs",
    "src",
]

# ---------------------------------------------------------------------------
# Arquivos a criar: (caminho relativo, conteúdo_template)
# ---------------------------------------------------------------------------

FILES_TO_CREATE: list[tuple[str, str]] = [
    ("README.md",                  _README_MD),
    ("docs/INDEX.md",              _DOCS_INDEX_MD),
    ("docs/TODO.md",               _DOCS_TODO_MD),
    ("docs/TODAY_ACTIVITIES.md",   _DOCS_TODAY_ACTIVITIES_MD),
    (".gitignore",                 _GITIGNORE),
    (".secrets/README.md",         _SECRETS_README),
    (".vscode/mcp.json",           _VSCODE_MCP_JSON),
    (".vscode/settings.json",      _VSCODE_SETTINGS_JSON),
    ("Makefile",                   _MAKEFILE),
    ("scripts/logs/.gitkeep",      ""),
]


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------

def create_structure(config: ProjectConfig) -> list[CreatedItem]:
    """
    Cria a estrutura de pastas e arquivos base do projeto em config.project_path.

    - Pastas já existentes → skipped (sem erro)
    - Arquivos já existentes → skipped (não sobrescreve)
    - Retorna lista de CreatedItem com status de cada operação
    """
    results: list[CreatedItem] = []
    base = config.project_path
    base.mkdir(parents=True, exist_ok=True)

    # 1. Pastas
    for dir_rel in DIRS_TO_CREATE:
        dir_path = base / dir_rel
        if dir_path.exists():
            results.append(CreatedItem(
                path=dir_path, kind="dir", status="skipped",
            ))
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                results.append(CreatedItem(
                    path=dir_path, kind="dir", status="created",
                ))
            except OSError as e:
                results.append(CreatedItem(
                    path=dir_path, kind="dir", status="error", message=str(e),
                ))

    # 2. Arquivos
    for file_rel, template in FILES_TO_CREATE:
        file_path = base / file_rel
        if file_path.exists():
            results.append(CreatedItem(
                path=file_path, kind="file", status="skipped",
            ))
            continue
        try:
            # Substitui {{PROJECT_*}} antes de escrever
            content = _prepare_content(template, file_rel, config)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            results.append(CreatedItem(
                path=file_path, kind="file", status="created",
            ))
        except OSError as e:
            results.append(CreatedItem(
                path=file_path, kind="file", status="error", message=str(e),
            ))

    # 3. [nome].code-workspace (nome dinâmico)
    ws_path = base / f"{config.project_name}.code-workspace"
    if ws_path.exists():
        results.append(CreatedItem(path=ws_path, kind="file", status="skipped"))
    else:
        try:
            ws_path.write_text(_CODE_WORKSPACE, encoding="utf-8")
            results.append(CreatedItem(path=ws_path, kind="file", status="created"))
        except OSError as e:
            results.append(CreatedItem(path=ws_path, kind="file", status="error", message=str(e)))

    return results


def _prepare_content(template: str, file_rel: str, config: ProjectConfig) -> str:
    """Aplica placeholders e ajustes especiais (ex: README github section)."""
    if file_rel == "README.md":
        github_section = (
            f"**Repositório**: [{config.github_repo}]({config.github_repo})"
            if config.github_repo
            else ""
        )
        template = template.replace("{github_section}", github_section)
    return _apply_placeholders(template, config)


# ---------------------------------------------------------------------------
# SpecKit — cópia de agents, prompts e perfis de domínio
# ---------------------------------------------------------------------------

def copy_speckit(config: ProjectConfig) -> list[CreatedItem]:
    """
    Copia assets SpecKit do template para o projeto gerado.

    Copia (de _TEMPLATE_ROOT → config.target_dir):
      - .github/agents/speckit.*.agent.md
      - .github/prompts/speckit.*.prompt.md
      - .github/prompts/session-*.prompt.md
      - .specify/templates/ (diretório completo)
      - .specify/config.json (se existir)
      - Perfil de domínio principal (DOMAIN_DEFAULT_PROFILES[cfg.domain])
      - Perfis extras selecionados (cfg.extra_profiles)
      - Sempre: SPECKIT_TRANSVERSAL_PROFILES (ex: devops-security)

    Arquivos já existentes no destino são saltados (idempotente).
    """
    results: list[CreatedItem] = []
    errors: list[str] = []
    base = config.target_dir
    src_root = _TEMPLATE_ROOT

    # --- Padrões glob de arquivos SpecKit a copiar ---
    speckit_globs = [
        (".github/agents",                "*.agent.md"),
        (".github/prompts",               "speckit.*.prompt.md"),
        (".github/prompts",               "session-*.prompt.md"),
        (".github/ISSUE_TEMPLATE",        "*.md"),
        (".github/ISSUE_TEMPLATE",        "*.yml"),
    ]

    for rel_dir, pattern in speckit_globs:
        src_dir = src_root / rel_dir
        if not src_dir.is_dir():
            log.warning("⚠️  Diretório de origem não encontrado: %s", src_dir)
            continue
        for src_file in sorted(src_dir.glob(pattern)):
            dst_file = base / rel_dir / src_file.name
            result = _copy_file(src_file, dst_file)
            if result.status == "error":
                errors.append(str(src_file))
            results.append(result)

    # --- .specify/templates/ (diretório completo) ---
    src_specify = src_root / ".specify" / "templates"
    if src_specify.is_dir():
        for src_file in sorted(src_specify.rglob("*")):
            if src_file.is_file():
                rel = src_file.relative_to(src_root)
                dst_file = base / rel
                result = _copy_file(src_file, dst_file)
                if result.status == "error":
                    errors.append(str(src_file))
                results.append(result)
    else:
        log.warning("⚠️  .specify/templates/ não encontrado em %s", src_root)

    # --- .specify/config.json ---
    src_cfg = src_root / ".specify" / "config.json"
    if src_cfg.is_file():
        dst_cfg = base / ".specify" / "config.json"
        result = _copy_file(src_cfg, dst_cfg)
        if result.status == "error":
            errors.append(str(src_cfg))
        results.append(result)

    # --- Perfis de domínio ---
    # 1) principal (pelo domínio)
    domain_profile = DOMAIN_DEFAULT_PROFILES.get(config.domain)
    if domain_profile:
        result = _copy_domain_profile(src_root, base, domain_profile, errors)
        results.append(result)

    # 2) extras selecionados pelo utilizador (D-21)
    for profile_name in config.extra_profiles:
        if profile_name != domain_profile:  # evita duplicata
            result = _copy_domain_profile(src_root, base, profile_name, errors)
            results.append(result)

    # 3) transversais — sempre copiados (D-20)
    for profile_name in SPECKIT_TRANSVERSAL_PROFILES:
        result = _copy_domain_profile(src_root, base, profile_name, errors)
        results.append(result)

    if errors:
        log.warning("⚠️  %d erro(s) ao copiar SpecKit: %s", len(errors), errors)

    return results


def _copy_domain_profile(
    src_root: Path,
    base: Path,
    profile_name: str,
    errors: list[str],
) -> CreatedItem:
    """Copia um perfil de domínio individual."""
    src_file = src_root / ".github" / "prompts" / "domain" / f"{profile_name}.prompt.md"
    dst_file = base / ".github" / "prompts" / "domain" / f"{profile_name}.prompt.md"
    result = _copy_file(src_file, dst_file)
    if result.status == "error":
        errors.append(str(src_file))
    return result


def _copy_file(src: Path, dst: Path) -> CreatedItem:
    """Copia src → dst com logging. Salta se dst já existe."""
    if dst.exists():
        log.info("⏭️  skipped (já existe): %s", dst)
        return CreatedItem(path=dst, kind="file", status="skipped")
    if not src.exists():
        msg = f"origem não encontrada: {src}"
        log.warning("⚠️  %s", msg)
        return CreatedItem(path=dst, kind="file", status="error", message=msg)
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        log.info("✅ copiado: %s → %s", src.name, dst)
        return CreatedItem(path=dst, kind="file", status="created")
    except OSError as exc:
        log.warning("⚠️  erro ao copiar %s: %s", src, exc)
        return CreatedItem(path=dst, kind="file", status="error", message=str(exc))


# ---------------------------------------------------------------------------
# Constitution — geração do arquivo .specify/memory/constitution.md
# ---------------------------------------------------------------------------

def generate_constitution(config: ProjectConfig) -> CreatedItem:
    """
    Gera .specify/memory/constitution.md no projeto destino.

    Copia o constitution-template.md do template, resolve os placeholders
    padrão e adiciona metadados do projeto no cabeçalho.
    Se o arquivo já existir no destino, salta (idempotente).
    """
    src = _TEMPLATE_ROOT / ".specify" / "templates" / "constitution-template.md"
    dst = config.project_path / ".specify" / "memory" / "constitution.md"

    if dst.exists():
        log.info("⏭️  skipped (já existe): %s", dst)
        return CreatedItem(path=dst, kind="file", status="skipped")

    if not src.exists():
        msg = f"constitution-template.md não encontrado em {src}"
        log.warning("⚠️  %s", msg)
        return CreatedItem(path=dst, kind="file", status="error", message=msg)

    try:
        template_content = src.read_text(encoding="utf-8")

        # Substitui os marcadores de template do SpecKit
        content = template_content.replace("[PROJECT_NAME]", config.project_title)
        content = content.replace("[RATIFICATION_DATE]", config.created_at[:10])
        content = content.replace("[LAST_AMENDED_DATE]", config.created_at[:10])
        content = content.replace("[CONSTITUTION_VERSION]", "1.0.0")

        # Cabeçalho com metadados do scaffold
        header = (
            f"<!-- Gerado por scaffold.py {SPECKIT_SYNC_DATE} | "
            f"Domínio: {config.domain} | Linguagem: {config.language} -->\n"
        )
        content = header + content

        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content, encoding="utf-8")
        log.info("✅ constitution.md gerado: %s", dst)
        return CreatedItem(path=dst, kind="file", status="created")
    except OSError as exc:
        log.warning("⚠️  erro ao gerar constitution.md: %s", exc)
        return CreatedItem(path=dst, kind="file", status="error", message=str(exc))


# ---------------------------------------------------------------------------
# MCP env vars required per domain (mirrors vscode._MCP_BY_DOMAIN "env" fields)
# ---------------------------------------------------------------------------

_MCP_ENV_VARS_BY_DOMAIN: dict[str, list[str]] = {
    "programming":    ["GITHUB_PERSONAL_ACCESS_TOKEN"],
    "infrastructure": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
    "analysis":       ["BRAVE_API_KEY"],
}


# ---------------------------------------------------------------------------
# load-mcp.sh — geração dinâmica por domínio
# ---------------------------------------------------------------------------

def generate_load_mcp(config: ProjectConfig) -> CreatedItem:
    """
    Gera scripts/load-mcp.sh com as variáveis de ambiente obrigatórias para o domínio.

    - Verifica .secrets/.env; orienta o usuário se ausente
    - Carrega as variáveis (set -a; source; set +a)
    - Valida variáveis obrigatórias pelo domínio
    - Verifica presença de npx e node
    - Imprime instrução para abrir o VS Code
    - Idempotente — skip se scripts/load-mcp.sh já existe
    """
    dest = config.project_path / "scripts" / "load-mcp.sh"
    if dest.exists():
        return CreatedItem(path=dest, kind="file", status="skipped", message="já existe")

    required_vars = _MCP_ENV_VARS_BY_DOMAIN.get(config.domain, [])

    # Bloco de exemplo para .secrets/.env
    example_lines = "\n".join(
        f"   {var}=your-value-here" for var in required_vars
    ) or "   (nenhuma variável requerida para este domínio)"

    # Bloco de validação de variáveis
    validation_lines = "\n".join(
        f'  [[ -z "${{{var}:-}}" ]] && MISSING+=("{var}")'
        for var in required_vars
    ) or "  # nenhuma variável requerida para este domínio"

    script = (
        "#!/usr/bin/env bash\n"
        "# load-mcp.sh — Carrega variáveis de ambiente para MCP Servers\n"
        f"# Domínio: {config.domain}\n"
        "# Gerado por scaffold.py — NÃO commitar este script com tokens reais\n"
        "#\n"
        "# Uso:\n"
        "#   bash scripts/load-mcp.sh\n"
        "#   make mcp\n"
        "set -euo pipefail\n"
        "\n"
        'SECRETS_ENV=".secrets/.env"\n'
        "\n"
        'if [[ ! -f "$SECRETS_ENV" ]]; then\n'
        '  echo "⚠️  .secrets/.env não encontrado."\n'
        '  echo "   Crie o arquivo com os tokens necessários:"\n'
        '  echo ""\n'
        '  echo "   # .secrets/.env"\n'
        f'  echo "{example_lines}"\n'
        '  echo ""\n'
        '  exit 1\n'
        "fi\n"
        "\n"
        "# Carrega sem poluir o histórico do shell\n"
        "set -a; source \"$SECRETS_ENV\"; set +a\n"
        "\n"
        "# Valida variáveis obrigatórias\n"
        "MISSING=()\n"
        + validation_lines + "\n"
        "\n"
        "if [[ ${#MISSING[@]} -gt 0 ]]; then\n"
        '  echo "❌ Variáveis obrigatórias ausentes em $SECRETS_ENV:"\n'
        "  printf '   %s\\n' \"${MISSING[@]}\"\n"
        "  exit 1\n"
        "fi\n"
        "\n"
        "# Verifica dependências de runtime\n"
        "for cmd in npx node; do\n"
        '  if ! command -v "$cmd" &>/dev/null; then\n'
        '    echo "❌ Dependência ausente: $cmd"\n'
        '    echo "   Instale o Node.js: https://nodejs.org/"\n'
        "    exit 1\n"
        "  fi\n"
        "done\n"
        "\n"
        'echo "✅ Ambiente MCP carregado com sucesso."\n'
        'echo ""\n'
        'echo "   Abra o VS Code com:"\n'
        'echo "   code ."\n'
    )

    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(script, encoding="utf-8")
        # Torna executável: rwxr-xr-x (0o755)
        os.chmod(dest, 0o755)
        log.info("✅ load-mcp.sh gerado: %s", dest)
        return CreatedItem(path=dest, kind="file", status="created")
    except OSError as exc:
        log.warning("⚠️  erro ao gerar load-mcp.sh: %s", exc)
        return CreatedItem(path=dest, kind="file", status="error", message=str(exc))


# ---------------------------------------------------------------------------
# Scaffold state — persiste e recupera configuração do projeto gerado
# ---------------------------------------------------------------------------

_STATE_FILENAME = ".scaffold-state.yaml"


def write_scaffold_state(
    config: ProjectConfig,
    profiles_applied: list[str] | None = None,
) -> CreatedItem:
    """
    Persiste o estado do projeto em <target_dir>/.scaffold-state.yaml.

    Chamado ao final de flow_new_project e de flow_compose_profiles para que
    o fluxo de upgrade saiba quais perfis foram aplicados e com qual config
    o projeto foi criado.

    O arquivo é SEMPRE sobrescrito (não é idempotente como os demais).
    """
    from datetime import datetime, timezone

    state_path = config.project_path / _STATE_FILENAME

    # Carrega estado anterior (se existir) para preservar created_at e profiles
    existing_profiles: list[str] = []
    original_created_at: str = config.created_at
    if state_path.exists():
        try:
            import yaml
            with state_path.open(encoding="utf-8") as f:
                old = yaml.safe_load(f) or {}
            existing_profiles = old.get("profiles_applied", [])
            original_created_at = old.get("created_at", config.created_at)
        except Exception:
            pass

    # Merge: adiciona novos perfis sem duplicar
    merged_profiles = list(existing_profiles)
    for p in (profiles_applied or []):
        if p not in merged_profiles:
            merged_profiles.append(p)

    state: dict = {
        "scaffold_version": "1.0.0",
        "created_at": original_created_at,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "project": {
            "name":        config.project_name,
            "title":       config.project_title,
            "description": config.description,
            "domain":      config.domain,
            "language":    config.language,
            "github_repo": config.github_repo or "",
        },
        "paths": {
            "target_dir": str(config.target_dir),
            "shared_dir": str(config.shared_dir),
        },
        "profiles_applied": merged_profiles,
    }

    try:
        import yaml
        state_path.write_text(
            yaml.dump(state, allow_unicode=True, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )
        log.info("✅ scaffold state gravado: %s", state_path)
        return CreatedItem(path=state_path, kind="file", status="created")
    except Exception as exc:
        log.warning("⚠️  erro ao gravar scaffold state: %s", exc)
        return CreatedItem(path=state_path, kind="file", status="error", message=str(exc))


def read_scaffold_state(target_dir: Path) -> dict | None:
    """
    Lê <target_dir>/.scaffold-state.yaml e retorna o dict com o estado.
    Retorna None se o arquivo não existe ou está corrompido.
    """
    state_path = target_dir / _STATE_FILENAME
    if not state_path.exists():
        return None
    try:
        import yaml
        with state_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else None
    except Exception as exc:
        log.warning("⚠️  erro ao ler scaffold state: %s", exc)
        return None


def config_from_state(state: dict, override_target: Path | None = None) -> ProjectConfig:
    """
    Reconstrói um ProjectConfig a partir do estado salvo.

    Args:
        state:           dict retornado por read_scaffold_state()
        override_target: se fornecido, sobrescreve paths.target_dir do state
                        No modo upgrade, override_target é o próprio projeto.
    """
    from datetime import datetime, timezone

    proj = state.get("project", {})
    paths = state.get("paths", {})
    project_name = proj.get("name", "unknown")

    # Correção IMP-47: detectar se override_target é o próprio projeto
    if override_target:
        # Se override_target termina com o nome do projeto,
        # então está apontando para o projeto, não para o diretório pai
        if override_target.name == project_name:
            target = override_target.parent
        else:
            # Fallback: assume que override_target é o diretório pai
            target = override_target
    else:
        # Modo normal: usa target_dir do state
        target = Path(paths.get("target_dir", "."))

    shared = Path(paths.get("shared_dir", str(
        Path.home() / "Documentos" / "DevOps" / ".copilot-shared"
    )))

    return ProjectConfig(
        project_name=project_name,
        project_title=proj.get("title", proj.get("name", "Unknown")),
        description=proj.get("description", ""),
        domain=proj.get("domain", "programming"),
        language=proj.get("language", "python"),
        github_repo=proj.get("github_repo") or None,
        shared_dir=shared,
        target_dir=target,
        created_at=state.get("created_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
        extra_profiles=state.get("profiles_applied", []),
    )
