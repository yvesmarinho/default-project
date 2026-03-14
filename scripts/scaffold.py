#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "rich>=13.7",
#   "pyyaml>=6.0",
# ]
# ///
"""
scaffold.py — Enterprise Project Scaffold — Entry Point

Uso:
  uv run scripts/scaffold.py          # modo interativo (recomendado)
  python scripts/scaffold.py          # alternativa (deps já instaladas)

  scaffold.py --new                   # pula menu, vai direto para Novo Projeto
  scaffold.py --check                 # verifica symlinks e sai
  scaffold.py --list-profiles         # lista perfis disponíveis e sai
  scaffold.py --list-profiles --json  # output JSON (para CI/automação)
  scaffold.py --validate              # valida todos os profile-descriptors
  scaffold.py --validate --json       # validação em JSON (para CI)
  scaffold.py --dry-run --ci --name X --domain Y --language Z  # simula sem criar
  scaffold.py --config config.yaml    # lê config de arquivo YAML (não-interativo)
  scaffold.py --ci --name X --domain Y --language Z  # modo não-interativo

Separação de domínios:
  scaffold.py → scaffolding de projetos (estrutura, links, regras, git)
  Makefile    → build, test, lint, CI/CD (NÃO tem lógica de scaffolding)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Garante que scripts/ está no sys.path para encontrar lib/
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import SCAFFOLD_VERSION
from lib.flows import (
    _load_descriptor,
    flow_check_links,
    flow_compose_profiles,
    flow_dry_run,
    flow_generate_infra,
    flow_generate_rules,
    flow_list_profiles,
    flow_new_project,
    flow_publish,
    flow_release,
    flow_upgrade,
    flow_validate,
)
from lib.ui import console, show_banner, show_menu

# ---------------------------------------------------------------------------
# CLI — argparse
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scaffold.py",
        description="Enterprise Project Scaffold — cria projetos a partir do template padrão.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"scaffold.py {SCAFFOLD_VERSION}"
    )

    # Ações
    action_group = parser.add_argument_group("ações")
    action_group.add_argument(
        "--new",
        action="store_true",
        help="pula menu — inicia fluxo de Novo Projeto diretamente",
    )
    action_group.add_argument(
        "--check",
        action="store_true",
        help="verifica symlinks .copilot-* e sai",
    )
    action_group.add_argument(
        "--list-profiles",
        action="store_true",
        dest="list_profiles",
        help="lista perfis disponíveis com descrição e sai",
    )
    action_group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="mostra o que seria gerado sem criar arquivos",
    )
    action_group.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="output em JSON (usar com --list-profiles ou --dry-run)",
    )
    action_group.add_argument(
        "--compose",
        metavar="PROFILES",
        help=(
            "aplica perfis ao projeto (lista separada por vírgulas)\n"
            "  ex: --compose typescript-next\n"
            "  ex: --compose devops-programming,python-fastapi"
        ),
    )
    action_group.add_argument(
        "--infra",
        action="store_true",
        help="gera .github/workflows/ci.yml, Dockerfile, docker-compose.yml e docs/RUNBOOK.md",
    )
    action_group.add_argument(
        "--upgrade",
        action="store_true",
        help=(
            "re-aplica o template a um projeto já existente\n"
            "  lê .scaffold-state.yaml no diretório alvo (--target-dir ou cwd)\n"
            "  arquivos ausentes são criados; existentes são mantidos"
        ),
    )
    action_group.add_argument(
        "--force",
        action="store_true",
        help="usar com --upgrade: sobrescreve arquivos existentes com divergência",
    )
    action_group.add_argument(
        "--publish",
        action="store_true",
        help="gera tarball de release do template (dist/enterprise-template-v*.tar.gz)",
    )
    action_group.add_argument(
        "--release",
        metavar="VERSION",
        dest="release_version",
        help=(
            "processo completo de release: CHANGELOG → bump SCAFFOLD_VERSION"
            " → tarball → git tag vX.Y.Z\n"
            "  Ex: --release 1.1.0 | --release 1.1.0 --dry-run"
        ),
    )
    action_group.add_argument(
        "--output-dir",
        metavar="PATH",
        dest="output_dir",
        help="diretório de saída para --publish (default: dist/)",
    )
    action_group.add_argument(
        "--validate",
        action="store_true",
        help="valida todos os profile-descriptors (campos, semver, refs cruzadas)",
    )
    action_group.add_argument(
        "--config",
        metavar="FILE",
        help="arquivo YAML com configuração do projeto (força modo não-interativo)",
    )

    # Modo
    mode_group = parser.add_argument_group("modo")
    mode_group.add_argument(
        "--ci",
        action="store_true",
        help="modo não-interativo — usa flags, sem prompts",
    )

    # Campos do projeto
    fields_group = parser.add_argument_group("campos do projeto")
    fields_group.add_argument("--name",        metavar="NAME",  help="nome kebab-case (obrigatório em --ci)")
    fields_group.add_argument("--title",       metavar="TITLE", help="título legível")
    fields_group.add_argument("--description", metavar="DESC",  help="descrição breve")
    fields_group.add_argument(
        "--domain",
        choices=["programming", "infrastructure", "analysis"],
        metavar="DOMAIN",
        help="domínio: programming | infrastructure | analysis",
    )
    fields_group.add_argument(
        "--language",
        choices=["python", "typescript", "go", "other"],
        metavar="LANG",
        help="linguagem: python | typescript | go | other",
    )
    fields_group.add_argument("--repo",       metavar="URL",  help="URL do repositório GitHub")
    fields_group.add_argument("--shared-dir", metavar="PATH", dest="shared_dir", help="caminho para .copilot-shared")
    fields_group.add_argument("--target-dir", metavar="PATH", dest="target_dir", help="onde criar o projeto (default: cwd)")
    fields_group.add_argument(
        "--extra-profiles",
        metavar="PROFILES",
        dest="extra_profiles",
        default="domain-only",
        help=(
            "perfis SpecKit extras além do domínio principal\n"
            "  domain-only  apenas perfil do domínio (default)\n"
            "  all          todos os perfis disponíveis\n"
            "  none         equivalente a domain-only\n"
            "  p1,p2        lista separada por vírgulas"
        ),
    )

    return parser


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # --config: carrega configuração de arquivo YAML e injeta em args
    if getattr(args, "config", None):
        try:
            cfg_data = _load_descriptor(Path(args.config))
            for key in ("name", "title", "description", "domain", "language", "repo"):
                yaml_val = cfg_data.get(key)
                if yaml_val is not None and getattr(args, key, None) is None:
                    setattr(args, key, str(yaml_val))
            if "shared_dir" in cfg_data and args.shared_dir is None:
                args.shared_dir = cfg_data["shared_dir"]
            if "target_dir" in cfg_data and args.target_dir is None:
                args.target_dir = cfg_data["target_dir"]
            args.ci = True  # força modo não-interativo
        except Exception as exc:
            console.print(f"\n  [bold red]❌ Erro ao carregar --config:[/bold red] {exc}\n")
            return 1

    # --validate: valida profile-descriptors e sai
    if getattr(args, "validate", False):
        return flow_validate(args)

    # --publish: gera tarball de release e sai
    if getattr(args, "publish", False):
        return flow_publish(args)

    # --release: processo completo de release (CHANGELOG → bump → tarball → tag)
    if getattr(args, "release_version", None):
        return flow_release(args)

    # --list-profiles: lista perfis e sai
    if getattr(args, "list_profiles", False):
        return flow_list_profiles(args)

    # --upgrade: re-aplica template a projeto existente
    if getattr(args, "upgrade", False):
        if not getattr(args, "json_output", False):
            show_banner()
        return flow_upgrade(args)

    # --dry-run: simula criação sem escrever arquivos
    if getattr(args, "dry_run", False):
        if not getattr(args, "json_output", False):
            show_banner()
        return flow_dry_run(args)

    # --compose: aplica perfis e sai
    if getattr(args, "compose", None):
        if not getattr(args, "json_output", False):
            show_banner()
        return flow_compose_profiles(args)

    # --infra: gera arquivos de infra e sai
    if getattr(args, "infra", False):
        if not getattr(args, "json_output", False):
            show_banner()
        return flow_generate_infra(args)

    # --check: verifica links e sai
    if args.check:
        return flow_check_links(args)

    # --new: pula menu
    if args.new or args.ci:
        show_banner()
        return flow_new_project(args)

    # Modo interativo: exibe banner + menu
    show_banner()
    while True:
        choice = show_menu()
        if choice == "1":
            rc = flow_new_project(args)
            return rc
        elif choice == "2":
            rc = flow_check_links(args)
            # não sai — volta ao menu após check
            continue
        elif choice == "3":
            rc = flow_generate_rules(args)
            continue
        elif choice == "5":
            rc = flow_upgrade(args)
            continue
        elif choice == "4":
            console.print("\n  [dim]Até mais.[/dim]\n")
            return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n  Cancelado.\n")
        sys.exit(130)
