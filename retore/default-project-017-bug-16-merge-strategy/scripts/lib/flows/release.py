"""flow_release — processo completo de release: CHANGELOG → bump → tarball → git tag."""

from __future__ import annotations

import argparse
import json as _json
from pathlib import Path

from ..release import run_release as _run_release
from ..ui import console

_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def flow_release(args: argparse.Namespace) -> int:
    """Executa o processo completo de release: CHANGELOG → bump → tarball → git tag."""
    use_json: bool = getattr(args, "json_output", False)
    version: str = getattr(args, "release_version", "") or ""
    dry_run: bool = getattr(args, "dry_run", False)
    output_dir_arg: str | None = getattr(args, "output_dir", None)

    if not version:
        if use_json:
            print(_json.dumps({"error": "VERSION obrigatório para --release"}, ensure_ascii=False))
        else:
            console.print("\n  [bold red]❌ --release requer VERSION (ex: --release 1.1.0)[/bold red]\n")
        return 1

    output_dir = Path(output_dir_arg) if output_dir_arg else _PROJECT_ROOT / "dist"

    if not use_json:
        mode_label = "[bold yellow]DRY-RUN[/bold yellow] " if dry_run else ""
        console.print(
            f"\n  [bold cyan]🚀 {mode_label}Iniciando release v{version}...[/bold cyan]\n"
        )

    result = _run_release(
        version=version,
        project_root=_PROJECT_ROOT,
        output_dir=output_dir,
        dry_run=dry_run,
    )

    if use_json:
        print(_json.dumps({
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
