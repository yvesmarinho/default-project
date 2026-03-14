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

import json as _json

from lib import composer as _composer_module
from lib import config as _config_module
from lib import git, infra, links, project, templates, vscode
from lib import publish as _publish_module
from lib import validate as _validate_module
from lib.config import SCAFFOLD_VERSION
from lib.project import config_from_state, read_scaffold_state, write_scaffold_state
from lib.ui import (
    collect_project_info,
    confirm_summary,
    console,
    print_final_summary,
    show_banner,
    show_menu,
)

# Diretório dos profile descriptors (raiz do projeto)
_PROFILE_DESCRIPTORS_DIR = Path(__file__).parent.parent / "profile-descriptors"

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
    console.print(f"  [dim]Diretório: {cfg.target_dir}[/dim]\n")
    return 0


def flow_compose_profiles(args: argparse.Namespace) -> int:
    """Aplica um ou mais perfis copiando templates para o diretório de destino."""
    use_json: bool = getattr(args, "json_output", False)
    ci_mode = args.ci

    profiles_raw: str = getattr(args, "compose", "") or ""
    profile_names = [p.strip() for p in profiles_raw.split(",") if p.strip()]
    if not profile_names:
        console.print("\n  [bold red]\u274c --compose requer ao menos um perfil (ex: --compose typescript-next)[/bold red]\n")
        return 1

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
        console.print(f"\n  [bold red]\u274c Erro:[/bold red] {e}\n")
        return 1

    composer = _composer_module.ProfileComposer(
        descriptors_dir=_PROFILE_DESCRIPTORS_DIR,
        project_root=Path(__file__).parent.parent,
    )

    result = composer.compose(profile_names, cfg)

    if use_json:
        output = {
            "success":      result.success,
            "applied":      result.applied,
            "created":      result.created_count,
            "skipped":      result.skipped_count,
            "errors":       result.errors,
            "rolled_back":  [str(p) for p in result.rolled_back],
        }
        print(_json.dumps(output, indent=2, ensure_ascii=False))
        return 0 if result.success else 1

    if result.errors:
        for err in result.errors:
            console.print(f"  [bold red]\u274c {err}[/bold red]")
        if result.rolled_back:
            console.print(f"  [yellow]\u21a9 Rollback: {len(result.rolled_back)} arquivo(s) removido(s)[/yellow]")
        return 1

    # Persiste perfis aplicados no state file
    write_scaffold_state(cfg, profiles_applied=result.applied)

    # IMP-29: Gera guia de documentação para a combinação de perfis
    guide_item = templates.generate_profile_guide(cfg, result.applied, composer.descriptors)
    if guide_item.status == "created":
        console.print(f"  [dim]📖 Guia de perfis gerado: docs/{guide_item.path.name}[/dim]")

    from rich.table import Table
    table = Table(show_lines=False, expand=False, show_header=False)
    table.add_column(style="dim", no_wrap=True)
    table.add_column()

    for item in result.items:
        icon = "\u2705" if item.status == "created" else ("\u23ed" if item.status == "skipped" else "\u274c")
        table.add_row(icon, str(item.path.relative_to(cfg.target_dir)) if cfg.target_dir in item.path.parents else str(item.path))

    console.print(f"\n  [bold]Composição:[/bold] {', '.join(result.applied)}")
    console.print(f"  [dim]Destino: {cfg.target_dir}[/dim]\n")
    console.print(table)
    console.print(f"\n  [bold green]\u2705 {result.created_count} arquivo(s) criado(s), {result.skipped_count} pulado(s).[/bold green]\n")
    return 0


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
            console.print(f"  [dim]Perfis aplicados anteriormente: {', '.join(profiles_applied)}[/dim]")
        if force:
            console.print("  [yellow]⚠  --force: arquivos existentes serão sobrescritos.[/yellow]")
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
    results.extend(project.copy_speckit(cfg))

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
            project_root=Path(__file__).parent.parent,
        )
        if not use_json:
            console.print(f"  [blue]🧩 Re-aplicando {len(profiles_applied)} perfil(is)...[/blue]")
        compose_result = composer.compose(profiles_applied, cfg)
        # Converte CompositionItem → CreatedItem para o resumo
        for item in getattr(compose_result, "items", []):
            results.append(item)
        # IMP-29: Gera/verifica guia de combinação de perfis
        guide_item = templates.generate_profile_guide(cfg, profiles_applied, composer.descriptors)
        results.append(guide_item)

    # Atualiza state file com updated_at
    write_scaffold_state(cfg, profiles_applied=profiles_applied)

    if use_json:
        created  = [r for r in results if hasattr(r, "status") and r.status == "created"]
        skipped  = [r for r in results if hasattr(r, "status") and r.status == "skipped"]
        errors   = [r for r in results if hasattr(r, "status") and r.status == "error"]
        output = {
            "project": cfg.project_name,
            "upgrade": True,
            "created": len(created),
            "skipped": len(skipped),
            "errors":  len(errors),
            "profiles_applied": profiles_applied,
        }
        print(_json.dumps(output, indent=2, ensure_ascii=False))
        return 0 if not errors else 1

    print_final_summary(results)

    created = [r for r in results if hasattr(r, "status") and r.status == "created"]
    errs    = [r for r in results if hasattr(r, "status") and r.status == "error"]

    if errs:
        console.print(f"  [bold red]❌ {len(errs)} erro(s) durante o upgrade.[/bold red]\n")
        return 1

    if created:
        console.print(
            f"  [bold green]✅ Upgrade concluído: {len(created)} arquivo(s) novo(s) ou atualizado(s).[/bold green]\n"
        )
    else:
        console.print(
            "  [bold green]✅ Projeto já está atualizado — nenhuma mudança necessária.[/bold green]\n"
        )
    return 0


def flow_generate_infra(args: argparse.Namespace) -> int:
    """Gera .github/workflows/ci.yml, Dockerfile, docker-compose.yml e docs/RUNBOOK.md."""
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
        console.print(f"\n  [bold red]\u274c Erro:[/bold red] {e}\n")
        return 1

    results = [
        infra.generate_ci_workflow(cfg),
        infra.generate_dockerfile(cfg),
        infra.generate_docker_compose(cfg),
        infra.generate_runbook(cfg),
    ]
    print_final_summary(results)

    errors = [r for r in results if hasattr(r, "status") and r.status == "error"]
    if errors:
        console.print(f"  [bold red]\u274c {len(errors)} erro(s) durante a gera\u00e7\u00e3o.[/bold red]\n")
        return 1

    console.print("  [bold green]\u2705 Arquivos de infra gerados com sucesso![/bold green]\n")
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


def flow_publish(args: argparse.Namespace) -> int:
    """Cria tarball de release do template em dist/ (ou --output-dir)."""
    use_json: bool = getattr(args, "json_output", False)
    output_dir_arg: str | None = getattr(args, "output_dir", None)

    project_root = Path(__file__).parent.parent
    output_dir = Path(output_dir_arg) if output_dir_arg else project_root / "dist"

    if not use_json:
        console.print(
            f"\n  [bold cyan]📦 Publicando template v{SCAFFOLD_VERSION}...[/bold cyan]\n"
            f"  [dim]Destino: {output_dir}[/dim]\n"
        )

    try:
        result = _publish_module.publish_template(
            output_dir=output_dir,
            project_root=project_root,
        )
    except Exception as exc:
        if use_json:
            print(_json.dumps({"error": str(exc)}, ensure_ascii=False))
        else:
            console.print(f"  [bold red]\u274c Erro ao publicar: {exc}[/bold red]\n")
        return 1

    if use_json:
        output = {
            "success":    True,
            "version":    result.version,
            "tarball":    str(result.tarball_path),
            "manifest":   str(result.manifest_path),
            "file_count": result.file_count,
            "size_bytes": result.size_bytes,
            "created_at": result.created_at,
        }
        print(_json.dumps(output, indent=2, ensure_ascii=False))
        return 0

    size_kb = result.size_bytes / 1024
    console.print("  [bold green]\u2705 Template publicado com sucesso![/bold green]")
    console.print(f"  [dim]Tarball:   {result.tarball_path}[/dim]")
    console.print(f"  [dim]Manifesto: {result.manifest_path}[/dim]")
    console.print(f"  [dim]{result.file_count} arquivo(s) | {size_kb:.1f} KB[/dim]\n")
    return 0


def flow_release(args: argparse.Namespace) -> int:
    """Executa o processo completo de release: CHANGELOG → bump → tarball → git tag."""
    import sys as _sys

    use_json: bool = getattr(args, "json_output", False)
    version: str = getattr(args, "release_version", "") or ""
    dry_run: bool = getattr(args, "dry_run", False)
    output_dir_arg: str | None = getattr(args, "output_dir", None)

    project_root = Path(__file__).parent.parent

    if not version:
        if use_json:
            import json as _j
            print(_j.dumps({"error": "VERSION obrigatório para --release"}, ensure_ascii=False))
        else:
            console.print("\n  [bold red]❌ --release requer VERSION (ex: --release 1.1.0)[/bold red]\n")
        return 1

    _sys.path.insert(0, str(project_root / "scripts"))
    try:
        from lib.release import run_release as _run_release  # type: ignore
    except ImportError:
        from scripts.lib.release import run_release as _run_release  # type: ignore

    output_dir = Path(output_dir_arg) if output_dir_arg else project_root / "dist"

    if not use_json:
        mode_label = "[bold yellow]DRY-RUN[/bold yellow] " if dry_run else ""
        console.print(
            f"\n  [bold cyan]🚀 {mode_label}Iniciando release v{version}...[/bold cyan]\n"
        )

    result = _run_release(
        version=version,
        project_root=project_root,
        output_dir=output_dir,
        dry_run=dry_run,
    )

    if use_json:
        import json as _j
        print(_j.dumps({
            "success":     result.success,
            "version":     result.version,
            "dry_run":     dry_run,
            "steps_done":  result.steps_done,
            "errors":      result.errors,
            "tarball":     str(result.tarball) if result.tarball else None,
            "tag_created": result.tag_created,
        }, indent=2, ensure_ascii=False))
        return 0 if result.success else 1

    if result.success:
        console.print("  [bold green]✅ Release concluída com sucesso![/bold green]")
        for step in result.steps_done:
            console.print(f"  [dim]  ✓ {step}[/dim]")
        if result.tarball:
            console.print(f"\n  [cyan]Tarball:[/cyan] {result.tarball}")
        if result.tag_created:
            console.print(f"  [cyan]Tag git:[/cyan] v{result.version}")
        console.print("")
        return 0
    else:
        console.print("  [bold red]❌ Release falhou:[/bold red]")
        for err in result.errors:
            console.print(f"  [red]  • {err}[/red]")
        if result.steps_done:
            console.print("\n  [dim]Passos concluídos antes do erro:[/dim]")
            for step in result.steps_done:
                console.print(f"  [dim]  ✓ {step}[/dim]")
        console.print("")
        return 1


def flow_validate(args: argparse.Namespace) -> int:
    """Valida todos os profile-descriptors e reporta erros/avisos."""
    use_json: bool = getattr(args, "json_output", False)

    report = _validate_module.validate_descriptors(_PROFILE_DESCRIPTORS_DIR)

    if use_json:
        output = {
            "valid":            report.valid,
            "descriptor_dir":   str(report.descriptor_dir),
            "profiles_checked": report.profiles_checked,
            "errors":           report.total_errors,
            "warnings":         report.total_warnings,
            "results": [
                {
                    "name":   r.name,
                    "file":   r.file,
                    "status": r.status,
                    "issues": [
                        {"field": i.field, "severity": i.severity, "message": i.message}
                        for i in r.issues
                    ],
                }
                for r in report.results
            ],
        }
        print(_json.dumps(output, indent=2, ensure_ascii=False))
        return 0 if report.valid else 1

    from rich.table import Table

    table = Table(
        title="[bold]Validação dos Profile Descriptors[/bold]",
        show_lines=True,
        expand=False,
    )
    table.add_column("Perfil",   style="cyan",   no_wrap=True)
    table.add_column("Arquivo",  style="dim",    no_wrap=True)
    table.add_column("Status",   no_wrap=True)
    table.add_column("Issues")

    for r in report.results:
        if r.status == "ok":
            status_cell = "[green]✅ OK[/green]"
        elif r.status == "warning":
            status_cell = "[yellow]⚠  aviso[/yellow]"
        else:
            status_cell = "[red]❌ erro[/red]"

        issues_text = ""
        if r.issues:
            lines = []
            for iss in r.issues:
                color = "red" if iss.severity == "error" else "yellow"
                lines.append(f"[{color}]{iss.field}:[/{color}] {iss.message}")
            issues_text = "\n".join(lines)

        table.add_row(r.name, r.file, status_cell, issues_text)

    console.print()
    console.print(table)
    console.print(
        f"\n  [dim]{report.profiles_checked} perfil(s) verificado(s) | "
        f"[red]{report.total_errors} erro(s)[/red] | "
        f"[yellow]{report.total_warnings} aviso(s)[/yellow][/dim]\n"
    )

    if report.valid:
        console.print("  [bold green]✅ Todos os descriptors são válidos.[/bold green]\n")
    else:
        console.print(
            f"  [bold red]❌ {report.total_errors} erro(s) encontrado(s). "
            f"Corrija os campos acima.[/bold red]\n"
        )
    return 0 if report.valid else 1


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
# Helper — descriptor YAML loader
# ---------------------------------------------------------------------------

def _load_descriptor(yaml_path: Path) -> dict:
    """Carrega um profile descriptor YAML retornando um dict com os campos."""
    try:
        import yaml  # pyyaml
        with yaml_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Fallback mínimo: parse de campos escalares simples (sem pyyaml)
        data: dict = {}
        with yaml_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith("#") or line.startswith(" "):
                    continue
                if ": " in line:
                    key, _, val = line.partition(": ")
                    val = val.strip().strip('"').strip("'")
                    if val and val not in ("|", ">", ""):
                        data[key.strip()] = val
        return data


# ---------------------------------------------------------------------------
# flow_list_profiles
# ---------------------------------------------------------------------------

def flow_list_profiles(args: argparse.Namespace) -> int:
    """Lista perfis disponíveis lendo os descriptors YAML em profile-descriptors/."""
    use_json: bool = getattr(args, "json_output", False)
    profiles: list[dict] = []

    if _PROFILE_DESCRIPTORS_DIR.exists():
        for yaml_file in sorted(_PROFILE_DESCRIPTORS_DIR.glob("*.yaml")):
            try:
                data = _load_descriptor(yaml_file)
                desc = (data.get("description") or "").strip().replace("\n", " ")
                profiles.append({
                    "name":        str(data.get("name", yaml_file.stem)),
                    "description": desc,
                    "layer":       str(data.get("layer", "—")),
                    "version":     str(data.get("VERSION") or data.get("version") or "—"),
                    "last_tested": str(data.get("LAST_TESTED_DATE") or data.get("last_tested") or "—"),
                    "tags":        data.get("tags") or [],
                })
            except Exception as exc:
                console.print(f"  [red]⚠ Erro ao ler {yaml_file.name}: {exc}[/red]")
    else:
        msg = f"Diretório não encontrado: {_PROFILE_DESCRIPTORS_DIR}"
        if use_json:
            print(_json.dumps({"error": msg}, ensure_ascii=False))
        else:
            console.print(f"  [yellow]⚠ {msg}[/yellow]\n")
        return 1

    if use_json:
        print(_json.dumps(profiles, indent=2, ensure_ascii=False))
        return 0

    from rich.table import Table
    table = Table(title="[bold]Perfis disponíveis[/bold]", show_lines=True, expand=False)
    table.add_column("Nome",             style="cyan",   no_wrap=True)
    table.add_column("Layer",            style="yellow", no_wrap=True)
    table.add_column("Versão",           no_wrap=True)
    table.add_column("Última validação", no_wrap=True)
    table.add_column("Descrição")

    for p in profiles:
        desc = p["description"]
        if len(desc) > 72:
            desc = desc[:69] + "..."
        table.add_row(p["name"], p["layer"], p["version"], p["last_tested"], desc)

    console.print()
    console.print(table)
    console.print(f"\n  [dim]{len(profiles)} perfil(s) em {_PROFILE_DESCRIPTORS_DIR}[/dim]\n")
    return 0


# ---------------------------------------------------------------------------
# flow_dry_run
# ---------------------------------------------------------------------------

def _build_manifest(cfg) -> list[dict]:
    """Retorna a sequência de operações que flow_new_project executaria."""
    from lib.config import DOMAIN_DEFAULT_PROFILES
    domain_profile = DOMAIN_DEFAULT_PROFILES.get(cfg.domain, cfg.domain)

    lang_files: list[dict] = []
    if cfg.language == "python":
        lang_files = [{"step": "create_structure", "op": "create", "path": "pyproject.toml", "desc": "Configuração Python PEP 621 + uv"}]
    elif cfg.language == "typescript":
        lang_files = [{"step": "create_structure", "op": "create", "path": "package.json", "desc": "Configuração Node.js"}]
    elif cfg.language == "go":
        lang_files = [{"step": "create_structure", "op": "create", "path": "go.mod", "desc": "Módulo Go"}]

    ops: list[dict] = [
        {"step": "create_structure", "op": "mkdir",   "path": "docs/SESSIONS/",                                           "desc": "Estrutura de pastas padrão"},
        {"step": "create_structure", "op": "create",  "path": "docs/INDEX.md",                                           "desc": "Índice do projeto"},
        {"step": "create_structure", "op": "create",  "path": "docs/TODO.md",                                            "desc": "Lista de tarefas"},
        {"step": "create_structure", "op": "create",  "path": ".gitignore",                                              "desc": "Gitignore padrão"},
        *lang_files,
        {"step": "setup_symlinks",   "op": "symlink", "path": ".copilot-rules.md",                                      "desc": "→ .copilot-shared/.copilot-rules.md"},
        {"step": "generate_rules",   "op": "create",  "path": f".copilot-rules-{cfg.project_name}.md",                  "desc": "Regras Copilot específicas do projeto"},
        {"step": "generate_rules",   "op": "create",  "path": ".github/copilot-instructions.md",                       "desc": "Instruções auto-injetadas em toda sessão"},
        {"step": "vscode",           "op": "create",  "path": ".vscode/settings.json",                                  "desc": "Configurações VS Code"},
        {"step": "vscode",           "op": "create",  "path": ".vscode/mcp.json",                                       "desc": "Servidores MCP"},
        {"step": "vscode",           "op": "create",  "path": ".vscode/extensions.json",                               "desc": "Extensões recomendadas"},
        {"step": "copy_speckit",     "op": "copy",    "path": f".github/prompts/domain/{domain_profile}.prompt.md",    "desc": "Domain profile prompt"},
        {"step": "copy_speckit",     "op": "copy",    "path": ".github/prompts/domain/devops-security.prompt.md",      "desc": "Security profile (transversal)"},
        {"step": "copy_speckit",     "op": "copy",    "path": ".github/prompts/session-start.prompt.md",               "desc": "Ritual de início de sessão"},
        {"step": "copy_speckit",     "op": "copy",    "path": ".github/prompts/session-end.prompt.md",                 "desc": "Ritual de encerramento"},
        {"step": "constitution",     "op": "create",  "path": ".specify/memory/constitution.md",                       "desc": "Constitution SpecKit"},
        {"step": "git",              "op": "git",     "path": ".git/",                                                  "desc": "git init + commit inicial"},
    ]
    return ops


def flow_dry_run(args: argparse.Namespace) -> int:
    """Mostra o que seria gerado sem criar nenhum arquivo."""
    use_json: bool = getattr(args, "json_output", False)
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

    manifest = _build_manifest(cfg)

    if use_json:
        output = {
            "dry_run":     True,
            "project_name": cfg.project_name,
            "domain":      cfg.domain,
            "language":    cfg.language,
            "target_dir":  str(cfg.target_dir),
            "manifest":    manifest,
        }
        print(_json.dumps(output, indent=2, ensure_ascii=False))
        return 0

    from rich.table import Table
    console.print(
        f"\n  [bold yellow]📋 DRY RUN[/bold yellow] — "
        f"Projeto: [cyan]{cfg.project_name}[/cyan] | "
        f"Domínio: [cyan]{cfg.domain}[/cyan] | "
        f"Linguagem: [cyan]{cfg.language}[/cyan]"
    )
    console.print(f"  [dim]Destino: {cfg.target_dir}[/dim]\n")

    table = Table(show_lines=True, expand=False)
    table.add_column("#",      style="dim",    width=3,  no_wrap=True)
    table.add_column("Etapa",  style="yellow", no_wrap=True)
    table.add_column("Op",     style="cyan",   no_wrap=True)
    table.add_column("Arquivo / Destino")
    table.add_column("Descrição")

    for i, entry in enumerate(manifest, 1):
        table.add_row(str(i), entry["step"], entry["op"], entry["path"], entry["desc"])

    console.print(table)
    console.print("\n  [bold yellow]⚠  Modo dry-run: nenhum arquivo foi criado.[/bold yellow]\n")
    return 0


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
