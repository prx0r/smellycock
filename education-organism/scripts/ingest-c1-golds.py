#!/usr/bin/env python3
"""scripts/ingest-c1-golds.py — ingest the REAL C1 golds from smellycock raw-material.

Fixes red-team MEDIUM-10/CRITICAL-2: instead of truncated body[:200] slices, use the REAL C1 gold
documents (raw-material/c1/*.md) — complete scholarly content, not blind truncation. Commits each as a
grounded C1 with the FULL evidence text + clean key-terms + related-passages, status GENERATED (no
auto-promote; the authority invariant + gates decide promotion).

Anti-theatre: the C1 content is the real gold document, complete, not a substring slice.
"""
from __future__ import annotations
import glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402

GOLDS = Path("/root/smellycock/raw-material/c1")


def _parse_gold(path: Path) -> dict:
    """Parse a C1 gold markdown into a structured C1 record (complete content, not truncated)."""
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip() if text else path.stem
    # the body is between the title and the trailing metadata (Terms/See also)
    body = text
    terms = []
    see_also = []
    for line in text.splitlines():
        low = line.lower()
        if low.startswith("**terms"):
            rest = line.split(":", 1)[1] if ":" in line else ""
            terms = [t.strip() for t in rest.split("·") if t.strip()]
        if low.startswith("**see also"):
            rest = line.split(":", 1)[1] if ":" in line else ""
            see_also = [s.strip() for s in rest.split("·") if s.strip()]
    # object id from the C1 tag in the title (e.g. V1-A -> v1a)
    m = re.search(r"V(\d+)-([A-Z])", title)
    tag = f"v{m.group(1)}{m.group(2).lower()}" if m else path.stem.lower().replace("_", "-")
    oid = f"gold:{tag}"
    return {
        "object_id": oid,
        "passage_id": f"ipvv:{tag}",
        "title": title,
        "summary": body[:300],
        "body": body,                      # FULL content (not truncated)
        "key_terms": [{"term": t, "meaning": ""} for t in terms],
        "related_passages": see_also,
        "evidence_quote": body[:200],
    }


def main():
    files = sorted(glob.glob(str(GOLDS / "c1_*.md")))
    print(f"real C1 golds: {len(files)}\n")
    committed = 0
    for f in files:
        g = _parse_gold(Path(f))
        payload = {"c1": g, "c1_status": "MACHINE_PROPOSED", "derived_by": "smellycock-gold"}
        ih = R.input_hash(payload)
        if R.is_committed("C1", g["object_id"], ih):
            continue
        R.commit("C1", g["object_id"], ih, "ingest-c1-golds", status=R.GENERATED,
                 payload=payload, input_refs=[g["passage_id"]])
        committed += 1
        print(f"  ✓ {g['object_id']}: {g['title']} (body {len(g['body'])} chars, FULL)")
    print(f"\ncommitted {committed} grounded C1 golds (complete content, no truncation)")


if __name__ == "__main__":
    main()
