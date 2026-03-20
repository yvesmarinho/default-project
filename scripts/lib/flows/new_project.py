"""flow_new_project — criação completa de novo projeto."""

from __future__ import annotations

import argparse

from .. import git, links, project, templates, vscode
from ..project import write_scaffold_state
from ..ui import collect_project_info, confirm_summary, console, print_final_summary


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
    results.append(templates.generate_copilot_instructions(cfg))

    # 4. VS Code: settings, mcp, extensions, tasks, launch
    console.print("  [blue]🔧 Gerando configuração VS Code...[/blue]")
    results.append(vscode.generate_settings(cfg))
    results.append(vscode.generate_mcp(cfg))
    results.append(vscode.generate_extensions(cfg))
    results.append(vscode.generate_tasks(cfg))
    results.append(vscode.generate_launch(cfg))

    # 5. SpecKit: agents, prompts e perfis de domínio
    console.print("  [blue]🤖 Copiando assets SpecKit...[/blue]")
    results.extend(project.copy_speckit(cfg))

    # 6. Constitution: .specify/memory/constitution.md
    console.print("  [blue]📜 Gerando constitution.md...[/blue]")
    results.append(project.generate_constitution(cfg))

    # 7. MCP script: scripts/load-mcp.sh
    console.print("  [blue]🔑 Gerando load-mcp.sh...[/blue]")
    results.append(project.generate_load_mcp(cfg))

    # 8. Git
    console.print("  [blue]🗃️  Inicializando repositório Git...[/blue]")
    results.append(git.init_repository(cfg))

    # Resumo final
    print_final_summary(results)

    errors = [r for r in results if hasattr(r, "status") and r.status == "error"]
    if errors:
        console.print(f"  [bold red]❌ {len(errors)} erro(s) durante a criação.[/bold red]\n")
        return 1

    # 9. Persiste estado do projeto para uso futuro pelo modo upgrade
    write_scaffold_state(cfg, profiles_applied=[])

    console.print(f"  [bold green]✅ Projeto '{cfg.project_name}' criado com sucesso![/bold green]\n")
    console.print(f"  [dim]Diretório: {cfg.project_path}[/dim]\n")
    return 0
