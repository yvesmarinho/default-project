#!/usr/bin/env python3
"""
session-time-tracker.py — Session Time Tracking with Breaks

Rastreia tempo de trabalho de sessões com suporte a pausas (café, almoço, etc.)
Gera CSV com estatísticas de tempo por sessão.

Uso:
    # Iniciar sessão
    python scripts/session-time-tracker.py start

    # Pausar (café, almoço, etc.)
    python scripts/session-time-tracker.py pause "café"

    # Retomar após pausa
    python scripts/session-time-tracker.py resume

    # Finalizar sessão
    python scripts/session-time-tracker.py stop

    # Visualizar estatísticas
    python scripts/session-time-tracker.py stats [--date YYYY-MM-DD]

    # Exportar CSV
    python scripts/session-time-tracker.py export [--output PATH]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("⚠️  Install 'rich' for better output: pip install rich", file=sys.stderr)

# Arquivo de estado da sessão atual
STATE_FILE = Path(__file__).parent.parent / ".session-time" / "current.json"
# Arquivo CSV com histórico de sessões
HISTORY_CSV = Path(__file__).parent.parent / ".session-time" / "history.csv"


def _ensure_dirs():
    """Garante que diretórios necessários existem."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def _iso_now() -> str:
    """Retorna timestamp ISO 8601 UTC."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _format_duration(seconds: float) -> str:
    """Formata duração em formato legível (HH:MM:SS)."""
    td = timedelta(seconds=int(seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def cmd_start():
    """Inicia nova sessão de trabalho."""
    _ensure_dirs()

    if STATE_FILE.exists():
        print("❌ Sessão já em andamento. Use 'stop' para finalizar antes de iniciar nova.", file=sys.stderr)
        return 1

    now = _iso_now()
    date = datetime.utcnow().strftime("%Y-%m-%d")

    state = {
        "session_date": date,
        "start_time": now,
        "pauses": [],
        "current_pause": None,
        "status": "active"
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"✅ Sessão iniciada: {now}")
    print(f"📅 Data: {date}")
    return 0


def cmd_pause(reason: str = "break"):
    """Pausa a sessão atual (café, almoço, etc.)."""
    if not STATE_FILE.exists():
        print("❌ Nenhuma sessão ativa. Use 'start' primeiro.", file=sys.stderr)
        return 1

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)

    if state.get("current_pause"):
        print("❌ Sessão já pausada. Use 'resume' para retomar.", file=sys.stderr)
        return 1

    now = _iso_now()
    state["current_pause"] = {
        "start": now,
        "reason": reason
    }
    state["status"] = "paused"

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"⏸️  Sessão pausada: {now}")
    print(f"   Motivo: {reason}")
    return 0


def cmd_resume():
    """Retoma sessão após pausa."""
    if not STATE_FILE.exists():
        print("❌ Nenhuma sessão ativa.", file=sys.stderr)
        return 1

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)

    if not state.get("current_pause"):
        print("❌ Sessão não está pausada.", file=sys.stderr)
        return 1

    now = _iso_now()
    pause = state["current_pause"]
    pause["end"] = now

    # Calcular duração da pausa
    start = datetime.fromisoformat(pause["start"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(now.replace("Z", "+00:00"))
    pause["duration_seconds"] = (end - start).total_seconds()

    state["pauses"].append(pause)
    state["current_pause"] = None
    state["status"] = "active"

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    duration = _format_duration(pause["duration_seconds"])
    print(f"▶️  Sessão retomada: {now}")
    print(f"   Pausa: {duration} ({pause['reason']})")
    return 0


def cmd_stop():
    """Finaliza sessão atual e salva no histórico."""
    if not STATE_FILE.exists():
        print("❌ Nenhuma sessão ativa.", file=sys.stderr)
        return 1

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)

    if state.get("current_pause"):
        print("⚠️  Sessão ainda pausada. Retomando automaticamente antes de finalizar.")
        cmd_resume()
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

    now = _iso_now()
    state["end_time"] = now
    state["status"] = "completed"

    # Calcular duração total e líquida
    start = datetime.fromisoformat(state["start_time"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(now.replace("Z", "+00:00"))
    total_seconds = (end - start).total_seconds()

    pause_seconds = sum(p.get("duration_seconds", 0) for p in state["pauses"])
    net_seconds = total_seconds - pause_seconds

    state["total_duration_seconds"] = total_seconds
    state["pause_duration_seconds"] = pause_seconds
    state["net_duration_seconds"] = net_seconds

    # Salvar no CSV
    _save_to_csv(state)

    # Remover arquivo de estado
    STATE_FILE.unlink()

    print(f"🏁 Sessão finalizada: {now}")
    print(f"   Duração total: {_format_duration(total_seconds)}")
    print(
        f"   Pausas: {_format_duration(pause_seconds)} ({len(state['pauses'])} pausa(s))")
    print(f"   Tempo líquido: {_format_duration(net_seconds)}")
    return 0


def _save_to_csv(state: dict[str, Any]):
    """Salva sessão no histórico CSV."""
    _ensure_dirs()

    # Criar CSV se não existir
    file_exists = HISTORY_CSV.exists()

    with open(HISTORY_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "session_date", "start_time", "end_time",
            "total_duration", "pause_duration", "net_duration",
            "num_pauses", "pause_details"
        ])

        if not file_exists:
            writer.writeheader()

        pause_details = "; ".join(
            f"{p['reason']}:{_format_duration(p.get('duration_seconds', 0))}"
            for p in state.get("pauses", [])
        ) or "none"

        writer.writerow({
            "session_date": state["session_date"],
            "start_time": state["start_time"],
            "end_time": state["end_time"],
            "total_duration": _format_duration(state["total_duration_seconds"]),
            "pause_duration": _format_duration(state["pause_duration_seconds"]),
            "net_duration": _format_duration(state["net_duration_seconds"]),
            "num_pauses": len(state.get("pauses", [])),
            "pause_details": pause_details
        })


def cmd_stats(date: str | None = None):
    """Exibe estatísticas de sessões."""
    if not HISTORY_CSV.exists():
        print("❌ Nenhum histórico encontrado.", file=sys.stderr)
        return 1

    sessions = []
    with open(HISTORY_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if date is None or row["session_date"] == date:
                sessions.append(row)

    if not sessions:
        print(
            f"❌ Nenhuma sessão encontrada{f' para {date}' if date else ''}.", file=sys.stderr)
        return 1

    if HAS_RICH:
        _print_stats_rich(sessions, date)
    else:
        _print_stats_plain(sessions, date)

    return 0


def _print_stats_rich(sessions: list[dict], date_filter: str | None):
    """Exibe estatísticas com Rich."""
    console = Console()

    title = "📊 Estatísticas de Sessões"
    if date_filter:
        title += f" — {date_filter}"

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Data", style="cyan")
    table.add_column("Início", style="green")
    table.add_column("Fim", style="green")
    table.add_column("Total", justify="right")
    table.add_column("Pausas", justify="right")
    table.add_column("Líquido", justify="right", style="bold yellow")
    table.add_column("# Pausas", justify="center")

    for s in sessions:
        table.add_row(
            s["session_date"],
            s["start_time"].split("T")[1].replace("Z", ""),
            s["end_time"].split("T")[1].replace("Z", ""),
            s["total_duration"],
            s["pause_duration"],
            s["net_duration"],
            s["num_pauses"]
        )

    console.print(table)


def _print_stats_plain(sessions: list[dict], date_filter: str | None):
    """Exibe estatísticas em texto simples."""
    header = "📊 Estatísticas de Sessões"
    if date_filter:
        header += f" — {date_filter}"
    print(f"\n{header}\n{'=' * len(header)}\n")

    for s in sessions:
        print(f"Data: {s['session_date']}")
        print(f"  Início: {s['start_time']}")
        print(f"  Fim:    {s['end_time']}")
        print(f"  Total:  {s['total_duration']}")
        print(f"  Pausas: {s['pause_duration']} ({s['num_pauses']} pausa(s))")
        print(f"  Líquido: {s['net_duration']}")
        print()


def cmd_export(output: str | None = None):
    """Exporta histórico para CSV."""
    if not HISTORY_CSV.exists():
        print("❌ Nenhum histórico encontrado.", file=sys.stderr)
        return 1

    dest = Path(output) if output else Path.cwd() / "session-time-history.csv"

    import shutil
    shutil.copy(HISTORY_CSV, dest)

    print(f"✅ Histórico exportado: {dest}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Session Time Tracker — Rastreamento de tempo com pausas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando")

    # start
    subparsers.add_parser("start", help="Iniciar nova sessão")

    # pause
    pause_parser = subparsers.add_parser("pause", help="Pausar sessão")
    pause_parser.add_argument(
        "reason", nargs="?", default="break", help="Motivo da pausa")

    # resume
    subparsers.add_parser("resume", help="Retomar sessão")

    # stop
    subparsers.add_parser("stop", help="Finalizar sessão")

    # stats
    stats_parser = subparsers.add_parser("stats", help="Exibir estatísticas")
    stats_parser.add_argument("--date", help="Filtrar por data (YYYY-MM-DD)")

    # export
    export_parser = subparsers.add_parser("export", help="Exportar CSV")
    export_parser.add_argument("--output", help="Caminho do arquivo de saída")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "start":
        return cmd_start()
    elif args.command == "pause":
        return cmd_pause(args.reason)
    elif args.command == "resume":
        return cmd_resume()
    elif args.command == "stop":
        return cmd_stop()
    elif args.command == "stats":
        return cmd_stats(args.date)
    elif args.command == "export":
        return cmd_export(args.output)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
