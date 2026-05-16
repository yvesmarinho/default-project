"""flow_generate_rules — gera o arquivo .copilot-rules-[projeto].md."""

from __future__ import annotations

import argparse

from .. import templates
from ..ui import collect_project_info, console, print_final_summary


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
