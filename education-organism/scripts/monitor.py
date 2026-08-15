#!/usr/bin/env python3
"""scripts/monitor.py — live status sampling (mirrors smellycock ops_status --watch).

Samples the serveragent3 state (registry counts, process count, memory) and appends to a snapshot log.
Use: python3 scripts/monitor.py --watch 30 --snapshots 11
"""
from __future__ import annotations
import json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402


def _snapshot() -> dict:
    summary = R.summary()
    # memory
    mem = 0
    try:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())], capture_output=True, text=True)
        mem = int(out.stdout.strip() or 0) // 1024  # MB
    except Exception:
        mem = 0
    procs = 0
    try:
        out = subprocess.run(["ps", "-eo", "cmd"], capture_output=True, text=True)
        procs = sum(1 for l in out.stdout.splitlines() if "serveragent3" in l)
    except Exception:
        procs = 0
    return {"ts": time.strftime("%H:%M:%S"),
            "procs": procs, "rss_mb": mem,
            "C1": summary.get("C1", {}).get("objects", 0),
            "THEME": summary.get("THEME", {}).get("objects", 0),
            "ARGUMENT": summary.get("ARGUMENT", {}).get("objects", 0),
            "SYNTHESIS": summary.get("SYNTHESIS", {}).get("objects", 0),
            "ESSAY": summary.get("ESSAY", {}).get("objects", 0),
            "EDUCATION": summary.get("EDUCATION", {}).get("objects", 0)}


def main():
    args = sys.argv[1:]
    watch = 5
    n = 3
    out = ROOT / "data" / "runs" / "run-1" / "monitor-snapshots.jsonl"
    for i in range(len(args)):
        if args[i] == "--watch" and i + 1 < len(args):
            watch = int(args[i + 1])
        if args[i] == "--snapshots" and i + 1 < len(args):
            n = int(args[i + 1])
    out.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(n):
        snap = _snapshot()
        with out.open("a") as fh:
            fh.write(json.dumps(snap) + "\n")
        print(json.dumps(snap))
        time.sleep(watch)


if __name__ == "__main__":
    main()
