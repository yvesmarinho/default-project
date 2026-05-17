"""flow_publish — cria tarball de release do template."""

from __future__ import annotations

import argparse
import json as _json
from pathlib import Path

from .. import publish as _publish_module
from ..config import SCAFFOLD_VERSION
from ..ui import console

_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def flow_publish(args: argparse.Namespace) -> int:
    """Cria tarball de release do template em dist/ (ou --output-dir)."""
    use_json: bool = getattr(args, "json_output", False)
    output_dir_arg: str | None = getattr(args, "output_dir", None)

    output_dir = Path(output_dir_arg) if output_dir_arg else _PROJECT_ROOT / "dist"

    if not use_json:
        console.print(
            f"\n  [bold cyan]📦 Publicando template v{SCAFFOLD_VERSION}...[/bold cyan]\n"
            f"  [dim]Destino: {output_dir}[/dim]\n"
        )

    try:
        result = _publish_module.publish_template(
            output_dir=output_dir,
            project_root=_PROJECT_ROOT,
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
