"""flow_upgrade — re-aplica o template a um projeto já existente."""

from __future__ import annotations

import argparse
import json as _json
from pathlib import Path

from .. import composer as _composer_module
from .. import links, project, templates, vscode
from ..project import config_from_state, read_scaffold_state, write_scaffold_state
from ..ui import console, print_final_summary

_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
_PROFILE_DESCRIPTORS_DIR = _PROJECT_ROOT / "profile-descriptors"


def flow_upgrade(args: argparse.Namespace) -> int:
    """
    Modo upgrade: relê .scaffold-state.yaml do projeto alvo e re-aplica
    todos os passos de geração.

    - Arquivos já existentes com conteúdo idêntico → skipped
    - Arquivos já existentes com conteúdo diferente → skipped (use --force para sobrescrever)
    - Arquivos ausentes → criados
    Útil quando o template é atualizado e você quer trazer novidades para
    um projeto existente sem apagar personalizações.
    """
    force: bool = getattr(args, "force", False)
    use_json: bool = getattr(args, "json_output", False)

    # Diretório alvo (default: cwd)
    target = Path(args.target_dir) if args.target_dir else Path.cwd()

    state = read_scaffold_state(target)
    if state is None:
        msg = (
            f".scaffold-state.yaml não encontrado em {target}\n"
            "  Este projeto não foi criado com scaffold.py, ou o arquivo foi removido.\n"
            "  Crie um novo projeto com: scaffold.py --new"
        )
        if use_json:
            print(_json.dumps({"error": msg}, ensure_ascii=False))
        else:
            console.print(f"  [bold red]❌ {msg}[/bold red]\n")
        return 1

    cfg = config_from_state(state, override_target=target)
    profiles_applied: list[str] = state.get("profiles_applied", [])

    if not use_json:
        console.print(
            f"\n  [bold cyan]🔄 Upgrade:[/bold cyan] "
            f"[cyan]{cfg.project_name}[/cyan] | "
            f"domínio: [cyan]{cfg.domain}[/cyan] | "
            f"linguagem: [cyan]{cfg.language}[/cyan]"
        )
        if profiles_applied:
            console.print(
                f"  [dim]Perfis aplicados anteriormente: {', '.join(profiles_applied)}[/dim]")
        if force:
            console.print(
                "  [yellow]⚠  --force: arquivos existentes serão sobrescritos.[/yellow]")
        console.print()

    results = []

    # Em JSON mode, redireciona consoles dos módulos lib para stderr para evitar
    # que warnings de setup (ex: symlink ausente) poluam o output JSON.
    if use_json:
        from rich.console import Console as _RichConsole
        _stderr_console = _RichConsole(stderr=True, highlight=False)
        links.console = _stderr_console  # type: ignore[attr-defined]

    # Re-aplica todos os passos de geração (idempotentes por design)
    if not use_json:
        console.print("  [blue]📁 Verificando estrutura...[/blue]")
    results.extend(project.create_structure(cfg))

    if not use_json:
        console.print("  [blue]🔗 Verificando symlinks...[/blue]")
    results.extend(links.setup_symlinks(cfg))

    if not use_json:
        console.print("  [blue]📝 Verificando regras Copilot...[/blue]")
    results.append(templates.generate_copilot_rules(cfg))
    results.append(templates.generate_copilot_instructions(cfg))

    if not use_json:
        console.print("  [blue]🔧 Verificando configuração VS Code...[/blue]")
    results.append(vscode.generate_settings(cfg))
    results.append(vscode.generate_mcp(cfg))
    results.append(vscode.generate_extensions(cfg))
    results.append(vscode.generate_tasks(cfg))
    results.append(vscode.generate_launch(cfg))

    if not use_json:
        console.print("  [blue]🤖 Verificando assets SpecKit...[/blue]")

    # Opção 3: Detectar drift antes de aplicar force
    if force:
        # Primeiro, detectar drift sem force
        drift_results = project.copy_speckit(cfg, force=False)
        drift_files = [
            r for r in drift_results
            if hasattr(r, "status") and r.status == "drift"
        ]

        if drift_files and not use_json:
            console.print()
            console.print(
                "  [yellow]⚠️  DRIFT DETECTADO EM ARQUIVOS DO TEMPLATE[/yellow]")
            console.print(
                f"  [yellow]{len(drift_files)} arquivo(s) diferem do upstream:[/yellow]")
            console.print()
            for item in drift_files[:10]:  # Mostrar no máximo 10
                console.print(f"    • [dim]{item.path.name}[/dim]")
            if len(drift_files) > 10:
                console.print(
                    f"    ... e mais {len(drift_files) - 10} arquivo(s)")
            console.print()
            console.print("  [yellow]💡 Opções disponíveis:[/yellow]")
            console.print(
                "    1. [cyan]--force ativado[/cyan]: arquivos serão backupados (.backup) e sobrescritos")
            console.print(
                "    2. [cyan]Verificar manualmente[/cyan]: uv run scripts/scaffold.py --check-templates")
            console.print(
                "    3. [cyan]Diff assistido[/cyan]: uv run scripts/scaffold.py --diff-template <arquivo>")
            console.print(
                "    4. [cyan]Merge 3-way[/cyan]: uv run scripts/scaffold.py --merge-template <arquivo>")
            console.print()
            console.print(
                "  [yellow]⚠️  Prosseguindo com --force em 3 segundos...[/yellow]")
            import time
            time.sleep(3)
            console.print()

    # Aplicar copy_speckit com force (se especificado)
    results.extend(project.copy_speckit(cfg, force=force))

    if not use_json:
        console.print("  [blue]📜 Verificando constitution.md...[/blue]")
    results.append(project.generate_constitution(cfg))

    if not use_json:
        console.print("  [blue]🔑 Verificando load-mcp.sh...[/blue]")
    results.append(project.generate_load_mcp(cfg))

    # Re-aplica perfis previamente aplicados (idempotentes)
    if profiles_applied:
        composer = _composer_module.ProfileComposer(
            descriptors_dir=_PROFILE_DESCRIPTORS_DIR,
            project_root=_PROJECT_ROOT,
        )
        if not use_json:
            console.print(
                f"  [blue]🧩 Re-aplicando {len(profiles_applied)} perfil(is)...[/blue]")
        compose_result = composer.compose(profiles_applied, cfg)
        # Converte CompositionItem → CreatedItem para o resumo
        for item in getattr(compose_result, "items", []):
            results.append(item)
        # IMP-29: Gera/verifica guia de combinação de perfis
        guide_item = templates.generate_profile_guide(
            cfg, profiles_applied, composer.descriptors)
        results.append(guide_item)

    # Atualiza state file com updated_at
    write_scaffold_state(cfg, profiles_applied=profiles_applied)

    if use_json:
        created = [r for r in results if hasattr(
            r, "status") and r.status == "created"]
        skipped = [r for r in results if hasattr(
            r, "status") and r.status == "skipped"]
        drift = [r for r in results if hasattr(
            r, "status") and r.status == "drift"]
        errors = [r for r in results if hasattr(
            r, "status") and r.status == "error"]
        output = {
            "project": cfg.project_name,
            "upgrade": True,
            "created": len(created),
            "skipped": len(skipped),
            "drift": len(drift),
            "errors":  len(errors),
            "profiles_applied": profiles_applied,
        }
        if drift:
            output["drift_files"] = [str(r.path) for r in drift[:20]]
        print(_json.dumps(output, indent=2, ensure_ascii=False))
        return 0 if not errors else 1

    print_final_summary(results)

    created = [r for r in results if hasattr(
        r, "status") and r.status == "created"]
    drift = [r for r in results if hasattr(
        r, "status") and r.status == "drift"]
    errs = [r for r in results if hasattr(r, "status") and r.status == "error"]

    if errs:
        console.print(
            f"  [bold red]❌ {len(errs)} erro(s) durante o upgrade.[/bold red]\n")
        return 1

    if drift:
        console.print()
        console.print(
            f"  [bold yellow]📊 DRIFT DETECTADO: {len(drift)} arquivo(s) diferem do template upstream[/bold yellow]")
        console.print()
        console.print("  [yellow]Arquivos com drift:[/yellow]")
        for item in drift[:15]:
            console.print(f"    • {item.path.relative_to(cfg.project_path)}")
        if len(drift) > 15:
            console.print(f"    ... e mais {len(drift) - 15} arquivo(s)")
        console.print()
        console.print("  [cyan]💡 Para atualizar os arquivos:[/cyan]")
        console.print()
        console.print(
            "    [bold cyan]Opção 1 — Sobrescrever tudo (com backup):[/bold cyan]")
        console.print("      uv run scripts/scaffold.py --upgrade --force")
        console.print()
        console.print(
            "    [bold cyan]Opção 2 — Verificar manualmente:[/bold cyan]")
        console.print("      uv run scripts/scaffold.py --check-templates")
        console.print()
        console.print("    [bold cyan]Opção 3 — Diff individual:[/bold cyan]")
        console.print(
            "      uv run scripts/scaffold.py --diff-template .github/agents/session-manager.agent.md")
        console.print()
        console.print(
            "    [bold cyan]Opção 4 — Merge 3-way (preserva customizações):[/bold cyan]")
        console.print(
            "      uv run scripts/scaffold.py --merge-template .github/agents/session-manager.agent.md")
        console.print()
        console.print(
            "  [dim]Nota: Arquivos com drift NÃO foram modificados (use --force ou merge manual)[/dim]")
        console.print()
        return 0

    if created:
        console.print(
            f"  [bold green]✅ Upgrade concluído: {len(created)} arquivo(s) novo(s) ou atualizado(s).[/bold green]\n"
        )
    else:
        console.print(
            "  [bold green]✅ Projeto já está atualizado — nenhuma mudança necessária.[/bold green]\n"
        )
    return 0
