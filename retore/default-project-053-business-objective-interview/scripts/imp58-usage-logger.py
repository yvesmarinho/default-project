#!/usr/bin/env python3
"""
IMP-58 Usage Logger — Session Search Analytics

Captura estatísticas de uso do session-search para análise de necessidade
de memória ativa (Engram Integration Phase 2).

Usage:
    # Wrap session-search calls
    python scripts/imp58-usage-logger.py "query text" [--scope sessions]

    # Or via alias (add to ~/.zshrc):
    alias session-search='python scripts/imp58-usage-logger.py'

Log location: .imp58-usage/usage.log
Created: 2026-04-05
Part of: IMP-58 — Memory Active Needs Assessment
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Log directory
LOG_DIR = Path(".imp58-usage")
LOG_FILE = LOG_DIR / "usage.log"


def ensure_log_dir():
    """Create log directory if it doesn't exist."""
    LOG_DIR.mkdir(exist_ok=True)

    # Create .gitignore to exclude logs from version control
    gitignore = LOG_DIR / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("*.log\n*.json\n")


def log_usage(query: str, scope: str = None, results_count: int = None,
              execution_time: float = None, found_what_looking_for: bool = None):
    """Log a session-search usage event."""
    ensure_log_dir()

    event = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "scope": scope,
        "results_count": results_count,
        "execution_time_ms": round(execution_time * 1000, 2) if execution_time else None,
        "found_what_looking_for": found_what_looking_for,
    }

    # Append to log file (JSONL format)
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(event) + "\n")


def run_session_search(args):
    """Execute session-search.py and capture output."""
    import time

    # Build command
    cmd = ["python", "scripts/session-search.py", args.query]

    if args.scope:
        cmd.extend(["--scope", args.scope])

    if args.limit:
        cmd.extend(["--limit", str(args.limit)])

    if args.date_from:
        cmd.extend(["--from", args.date_from])

    if args.date_to:
        cmd.extend(["--to", args.date_to])

    if args.context:
        cmd.append("--context")

    # Execute and time
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    execution_time = time.time() - start_time

    # Parse results count from output
    results_count = None
    for line in result.stdout.split("\n"):
        if "Found:" in line and "result" in line:
            # Extract number from "Found: N result(s)"
            try:
                results_count = int(line.split(":")[1].split()[0])
            except:
                pass
            break

    # Print output
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Ask user if they found what they were looking for
    if results_count is not None and results_count > 0:
        try:
            response = input("\n🔍 Did you find what you were looking for? (y/n/skip): ").lower()
            found = True if response == 'y' else (False if response == 'n' else None)
        except (EOFError, KeyboardInterrupt):
            found = None
            print()
    else:
        found = False  # No results = didn't find

    # Log usage
    log_usage(
        query=args.query,
        scope=args.scope,
        results_count=results_count,
        execution_time=execution_time,
        found_what_looking_for=found
    )

    return result.returncode


def generate_stats():
    """Generate usage statistics from logs."""
    if not LOG_FILE.exists():
        print("No usage logs found. Start using session-search to generate data.")
        return

    events = []
    with LOG_FILE.open() as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except:
                pass

    if not events:
        print("No valid log entries found.")
        return

    # Calculate statistics
    total_searches = len(events)
    successful_searches = sum(1 for e in events if e.get("found_what_looking_for") is True)
    failed_searches = sum(1 for e in events if e.get("found_what_looking_for") is False)
    avg_results = sum(e.get("results_count", 0) for e in events if e.get("results_count")) / total_searches
    avg_time = sum(e.get("execution_time_ms", 0) for e in events if e.get("execution_time_ms")) / total_searches

    # Scope distribution
    scope_dist = {}
    for e in events:
        scope = e.get("scope", "all")
        scope_dist[scope] = scope_dist.get(scope, 0) + 1

    # Date range
    dates = [datetime.fromisoformat(e["timestamp"]).date() for e in events]
    first_date = min(dates)
    last_date = max(dates)
    days_active = (last_date - first_date).days + 1

    # Print statistics
    print("\n" + "="*60)
    print("IMP-58 Usage Statistics — Session Search Analytics")
    print("="*60)
    print(f"\n📊 Overall Statistics")
    print(f"  Total searches:       {total_searches}")
    print(f"  Successful:           {successful_searches} ({successful_searches/total_searches*100:.1f}%)")
    print(f"  Failed:               {failed_searches} ({failed_searches/total_searches*100:.1f}%)")
    print(f"  Unknown:              {total_searches - successful_searches - failed_searches}")
    print(f"  Avg results per query: {avg_results:.1f}")
    print(f"  Avg execution time:    {avg_time:.0f}ms")

    print(f"\n📅 Time Period")
    print(f"  First search:         {first_date}")
    print(f"  Last search:          {last_date}")
    print(f"  Days active:          {days_active}")
    print(f"  Searches per day:     {total_searches/days_active:.1f}")

    print(f"\n🎯 Scope Distribution")
    for scope, count in sorted(scope_dist.items(), key=lambda x: -x[1]):
        print(f"  {scope:15s} {count:4d} ({count/total_searches*100:5.1f}%)")

    print(f"\n💡 Insights")
    if total_searches / days_active >= 5:
        print("  ⚠️  HIGH FREQUENCY: ≥5 searches/day → necessidade alta detectada")
    else:
        print(f"  ✅ Normal frequency: {total_searches/days_active:.1f} searches/day")

    if failed_searches / total_searches >= 0.3:
        print(f"  ⚠️  HIGH FAILURE RATE: {failed_searches/total_searches*100:.1f}% → perda de contexto detectada")
    else:
        print(f"  ✅ Low failure rate: {failed_searches/total_searches*100:.1f}%")

    print("\n" + "="*60)
    print(f"Log file: {LOG_FILE.absolute()}")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="IMP-58 Usage Logger — Track session-search usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Stats mode
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show usage statistics"
    )

    # Search arguments (pass-through to session-search.py)
    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Search query"
    )

    parser.add_argument(
        "--scope",
        type=str,
        choices=["sessions", "docs", "specs", "all"],
        help="Filter by document type"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum results (default: 20)"
    )

    parser.add_argument(
        "--from",
        dest="date_from",
        type=str,
        help="Filter by start date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--to",
        dest="date_to",
        type=str,
        help="Filter by end date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--context",
        action="store_true",
        help="Show full activity context"
    )

    args = parser.parse_args()

    # Stats mode
    if args.stats:
        generate_stats()
        return 0

    # Search mode
    if not args.query:
        parser.error("query is required (unless using --stats)")

    return run_session_search(args)


if __name__ == "__main__":
    sys.exit(main())
