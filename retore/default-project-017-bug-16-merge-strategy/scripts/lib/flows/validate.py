"""flow_validate — valida todos os profile-descriptors."""

from __future__ import annotations

import argparse
import json as _json
from pathlib import Path

from .. import validate as _validate_module
from ..ui import console

_PROFILE_DESCRIPTORS_DIR = Path(__file__).parent.parent.parent.parent / "profile-descriptors"


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
