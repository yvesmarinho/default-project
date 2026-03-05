#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "rich>=13.7",
# ]
# ///
"""
scaffold.py — Enterprise Project Scaffold — Entry Point

Uso:
  uv run scripts/scaffold.py          # modo interativo (recomendado)
  python scripts/scaffold.py          # alternativa (deps já instaladas)

  scaffold.py --new                   # pula menu, vai direto para Novo Projeto
  scaffold.py --check                 # verifica symlinks e sai
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

from lib import config as _config_module
from lib import git, links, project, templates, vscode
from lib.config import SCAFFOLD_VERSION
from lib.ui import (
    collect_project_info,
    confirm_summary,
    console,
    print_final_summary,
    show_banner,
    show_menu,
)

# ---------------------------------------------------------------------------
# Fluxos
# ---------------------------------------------------------------------------

def flow_new_project(args: argparse.Namespace) -> int:
    """Fluxo completo de criação de novo projeto."""
    ci_mode = args.ci

    overrides = {
        "name":           args.name,
        "title":          args.title,
        "description":    args.description,
        "domain":         args.domain,
        "language":       args.language,
        "repo":           args.repo,
        "shared_dir":     args.shared_dir,
        "target_dir":     args.target_dir,
        "extra_profiles": getattr(args, "extra_profiles", None),
    }
    # Remove chaves None para não substituir defaults
    overrides = {k: v for k, v in overrides.items() if v is not None}

    try:
        cfg = collect_project_info(ci_mode=ci_mode, **overrides)
    except ValueError as e:
        console.print(f"\n  [bold red]❌ Erro:[/bold red] {e}\n")
        return 1

    if not ci_mode:
        if not confirm_summary(cfg):
            console.print("\n  [yellow]Operação cancelada.[/yellow]\n")
            return 0

    results = []

    # 1. Estrutura de pastas e arquivos base
    console.print("\n  [blue]📁 Criando estrutura...[/blue]")
    results.extend(project.create_structure(cfg))

    # 2. Symlinks .copilot-*
    console.print("  [blue]🔗 Configurando symlinks...[/blue]")
    results.extend(links.setup_symlinks(cfg))

    # 3. Regras Copilot específicas do projeto
    console.print("  [blue]📝 Gerando regras Copilot...[/blue]")
    results.append(templates.generate_copilot_rules(cfg))

    # 4. VS Code: settings, mcp, extensions
    console.print("  [blue]🔧 Gerando configuração VS Code...[/blue]")
    results.append(vscode.generate_settings(cfg))
    results.append(vscode.generate_mcp(cfg))
    results.append(vscode.generate_extensions(cfg))

    # 5. SpecKit: agents, prompts e perfis de domínio
    console.print("  [blue]🤖 Copiando assets SpecKit...[/blue]")
    results.extend(project.copy_speckit(cfg))

    # 6. Constitution: .specify/memory/constitution.md
    console.print("  [blue]📜 Gerando constitution.md...[/blue]")
    results.append(project.generate_constitution(cfg))

    # 7. Git
    console.print("  [blue]🗃️  Inicializando repositório Git...[/blue]")
    results.append(git.init_repository(cfg))

    # Resumo final
    print_final_summary(results)

    errors = [r for r in results if hasattr(r, "status") and r.status == "error"]
    if errors:
        console.print(f"  [bold red]❌ {len(errors)} erro(s) durante a criação.[/bold red]\n")
        return 1

    console.print(f"  [bold green]✅ Projeto '{cfg.project_name}' criado com sucesso![/bold green]\n")
    console.print(f"  [dim]Diretório: {cfg.target_dir}[/dim]\n")
    return 0


def flow_check_links(args: argparse.Namespace) -> int:
    """Verifica status dos symlinks .copilot-* no diretório atual."""
    from lib.config import DEFAULT_SHARED_DIR

    target = Path(args.target_dir) if args.target_dir else Path.cwd()
    shared = Path(args.shared_dir) if args.shared_dir else DEFAULT_SHARED_DIR

    statuses = links.check_symlinks(target, shared)
    print_final_summary(statuses)

    broken_or_missing = [s for s in statuses if s.status in ("broken", "missing")]
    return 1 if broken_or_missing else 0


def flow_generate_rules(args: argparse.Namespace) -> int:
    """Gera apenas o arquivo .copilot-rules-[projeto].md."""
    ci_mode = args.ci
    overrides = {
        "name":        args.name,
        "title":       args.title,
        "description": args.description,
        "domain":      args.domain,
        "language":    args.language,
        "repo":        args.repo,
        "shared_dir":  args.shared_dir,
        "target_dir":  args.target_dir,
    }
    overrides = {k: v for k, v in overrides.items() if v is not None}

    try:
        cfg = collect_project_info(ci_mode=ci_mode, **overrides)
    except ValueError as e:
        console.print(f"\n  [bold red]❌ Erro:[/bold red] {e}\n")
        return 1

    result = templates.generate_copilot_rules(cfg)
    print_final_summary([result])
    return 0 if result.status != "error" else 1


# ---------------------------------------------------------------------------
# CLI — argparse
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
        elif choice == "4":
            console.print("\n  [dim]Até mais.[/dim]\n")
            return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n  Cancelado.\n")
        sys.exit(130)
