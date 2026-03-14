"""flow_check_links — verifica status dos symlinks .copilot-*."""

from __future__ import annotations

import argparse
from pathlib import Path

from .. import links
from ..config import DEFAULT_SHARED_DIR
from ..ui import print_final_summary


def flow_check_links(args: argparse.Namespace) -> int:
    """Verifica status dos symlinks .copilot-* no diretório atual."""
    target = Path(args.target_dir) if args.target_dir else Path.cwd()
    shared = Path(args.shared_dir) if args.shared_dir else DEFAULT_SHARED_DIR

    statuses = links.check_symlinks(target, shared)
    print_final_summary(statuses)

    broken_or_missing = [s for s in statuses if s.status in ("broken", "missing")]
    return 1 if broken_or_missing else 0
