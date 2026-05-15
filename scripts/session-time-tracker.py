#!/usr/bin/env python3
"""
Session Time Tracker

Tracks session duration, pauses, and generates time reports.
Integrates with session-start and session-end prompts.

Usage:
    # Start session tracking
    python scripts/session-time-tracker.py start

    # Pause session
    python scripts/session-time-tracker.py pause

    # Resume session
    python scripts/session-time-tracker.py resume

    # End session and generate report
    python scripts/session-time-tracker.py end

    # Show current status
    python scripts/session-time-tracker.py status

    # Generate report without ending
    python scripts/session-time-tracker.py report
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class SessionTimeTracker:
    """Tracks session time with pause/resume support."""

    def __init__(self, base_dir: Path = Path(".")):
        """Initialize tracker with base directory."""
        self.base_dir = base_dir
        self.state_dir = base_dir / ".session-time"
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "current.json"

    def start(self) -> dict:
        """Start a new session."""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        if self.state_file.exists():
            print("⚠️  Session already active. End current session first or use 'resume'.")
            return self.get_status()

        state = {
            "date": today,
            "start_time": now.isoformat(),
            "end_time": None,
            "pauses": [],
            "current_pause_start": None,
            "total_pause_duration": 0,
        }

        self._save_state(state)
        print(f"✅ Session started at {now.strftime('%H:%M:%S')}")
        print(f"📁 State saved to: {self.state_file}")
        return state

    def pause(self, reason: Optional[str] = None) -> dict:
        """Pause the current session."""
        state = self._load_state()
        if not state:
            print("❌ No active session. Start a session first.")
            return {}

        if state.get("current_pause_start"):
            print("⚠️  Session already paused.")
            return state

        now = datetime.now()
        state["current_pause_start"] = now.isoformat()

        self._save_state(state)
        print(f"⏸️  Session paused at {now.strftime('%H:%M:%S')}")
        if reason:
            print(f"   Reason: {reason}")
        return state

    def resume(self) -> dict:
        """Resume a paused session."""
        state = self._load_state()
        if not state:
            print("❌ No active session. Start a session first.")
            return {}

        if not state.get("current_pause_start"):
            print("⚠️  Session is not paused.")
            return state

        now = datetime.now()
        pause_start = datetime.fromisoformat(state["current_pause_start"])
        pause_duration = (now - pause_start).total_seconds()

        state["pauses"].append({
            "start": state["current_pause_start"],
            "end": now.isoformat(),
            "duration_seconds": pause_duration,
        })
        state["total_pause_duration"] += pause_duration
        state["current_pause_start"] = None

        self._save_state(state)
        pause_minutes = int(pause_duration // 60)
        print(f"▶️  Session resumed at {now.strftime('%H:%M:%S')}")
        print(f"   Pause duration: {pause_minutes} minutes")
        return state

    def end(self) -> dict:
        """End the current session and generate report."""
        state = self._load_state()
        if not state:
            print("❌ No active session to end.")
            return {}

        # If paused, resume first
        if state.get("current_pause_start"):
            print("⚠️  Session is paused. Resuming before ending...")
            state = self.resume()

        now = datetime.now()
        state["end_time"] = now.isoformat()

        # Calculate durations
        start = datetime.fromisoformat(state["start_time"])
        total_duration = (now - start).total_seconds()
        active_duration = total_duration - state["total_pause_duration"]

        # Save final state to archive
        archive_file = self.state_dir / f"session_{state['date']}.json"
        with open(archive_file, "w") as f:
            json.dump(state, f, indent=2)

        # Remove current state
        self.state_file.unlink()

        # Print report
        print("\n" + "=" * 60)
        print(f"📊 Session Report — {state['date']}")
        print("=" * 60)
        print(f"Start:  {start.strftime('%H:%M:%S')}")
        print(f"End:    {now.strftime('%H:%M:%S')}")
        print(f"Total:  {self._format_duration(total_duration)}")
        print(f"Active: {self._format_duration(active_duration)}")
        print(f"Paused: {self._format_duration(state['total_pause_duration'])}")
        print(f"Breaks: {len(state['pauses'])}")
        print("=" * 60)
        print(f"✅ Session ended. Report saved to: {archive_file}\n")

        return state

    def get_status(self) -> dict:
        """Get current session status."""
        state = self._load_state()
        if not state:
            print("⚪ No active session.")
            return {}

        now = datetime.now()
        start = datetime.fromisoformat(state["start_time"])
        elapsed = (now - start).total_seconds()

        # Calculate current active time
        current_pause_duration = 0
        if state.get("current_pause_start"):
            pause_start = datetime.fromisoformat(state["current_pause_start"])
            current_pause_duration = (now - pause_start).total_seconds()

        total_paused = state["total_pause_duration"] + current_pause_duration
        active_time = elapsed - total_paused

        status = "⏸️  PAUSED" if state.get("current_pause_start") else "🟢 ACTIVE"

        print("\n" + "=" * 60)
        print(f"⏱️  Session Status — {state['date']}")
        print("=" * 60)
        print(f"Status:  {status}")
        print(f"Started: {start.strftime('%H:%M:%S')}")
        print(f"Elapsed: {self._format_duration(elapsed)}")
        print(f"Active:  {self._format_duration(active_time)}")
        print(f"Paused:  {self._format_duration(total_paused)}")
        print(f"Breaks:  {len(state['pauses'])} completed")
        if state.get("current_pause_start"):
            pause_start = datetime.fromisoformat(state["current_pause_start"])
            print(f"Current pause: {self._format_duration(current_pause_duration)} (since {pause_start.strftime('%H:%M:%S')})")
        print("=" * 60 + "\n")

        return state

    def generate_report(self) -> dict:
        """Generate report without ending session."""
        state = self._load_state()
        if not state:
            print("❌ No active session.")
            return {}

        now = datetime.now()
        start = datetime.fromisoformat(state["start_time"])
        elapsed = (now - start).total_seconds()

        # Calculate durations
        current_pause_duration = 0
        if state.get("current_pause_start"):
            pause_start = datetime.fromisoformat(state["current_pause_start"])
            current_pause_duration = (now - pause_start).total_seconds()

        total_paused = state["total_pause_duration"] + current_pause_duration
        active_time = elapsed - total_paused

        print("\n" + "=" * 60)
        print(f"📊 Session Report (Ongoing) — {state['date']}")
        print("=" * 60)
        print(f"Start:       {start.strftime('%H:%M:%S')}")
        print(f"Current:     {now.strftime('%H:%M:%S')}")
        print(f"Elapsed:     {self._format_duration(elapsed)}")
        print(f"Active Time: {self._format_duration(active_time)}")
        print(f"Total Pause: {self._format_duration(total_paused)}")
        print(f"Breaks:      {len(state['pauses'])} completed")
        print("=" * 60)

        if state["pauses"]:
            print("\n📋 Pause History:")
            for i, pause in enumerate(state["pauses"], 1):
                p_start = datetime.fromisoformat(pause["start"])
                p_end = datetime.fromisoformat(pause["end"])
                print(f"  {i}. {p_start.strftime('%H:%M')} → {p_end.strftime('%H:%M')} "
                      f"({self._format_duration(pause['duration_seconds'])})")

        print()
        return state

    def _load_state(self) -> Optional[dict]:
        """Load current session state."""
        if not self.state_file.exists():
            return None

        with open(self.state_file) as f:
            return json.load(f)

    def _save_state(self, state: dict) -> None:
        """Save session state."""
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration as HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Session Time Tracker with pause/resume support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "action",
        choices=["start", "pause", "resume", "end", "status", "report"],
        help="Action to perform",
    )

    parser.add_argument(
        "--reason",
        help="Reason for pause (optional)",
    )

    args = parser.parse_args()

    tracker = SessionTimeTracker()

    if args.action == "start":
        tracker.start()
    elif args.action == "pause":
        tracker.pause(reason=args.reason)
    elif args.action == "resume":
        tracker.resume()
    elif args.action == "end":
        tracker.end()
    elif args.action == "status":
        tracker.get_status()
    elif args.action == "report":
        tracker.generate_report()


if __name__ == "__main__":
    main()
