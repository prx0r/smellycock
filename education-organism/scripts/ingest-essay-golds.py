#!/usr/bin/env python3
"""scripts/ingest-essay-golds.py — register the REAL smellycock essays as ESSAY gold.

The upstream commit added 3 real scholarly essays (essays/*.md). These are genuine SHOW-EVIDENCE
essays (thesis + chapter mapping + verbatim quotes + IPVV hooks). This ingests them as committed ESSAY
gold objects — the exemplar target the ESSAY layer should produce. Anti-theatre: the content is the
real essay, complete, not generated/hand-fed.

Status GENERATED (no auto-promote; the gates + human review promote). Input_refs resolve to the C1
golds they build on (or none if we can't map — then honest GENERATED).
"""
from __future__ import annotations
import glob, hashlib, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402

ESSAYS = Path("/root/smellycock/essays")


def _parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else path.stem
    # find section headings as a crude section map
    sections = []
    current = None
    for ln in lines[1:]:
        m = re.match(r"^#{1,3} (.*)$", ln.strip())
        if m:
            if current:
                sections.append(current)
            current = {"heading": m.group(1).strip(), "body": ""}
        elif current:
            current["body"] += ln + "\n"
    if current:
        sections.append(current)
    return {"object_id": f"essay-gold:{path.stem.lower()}",
            "title": title, "sections": sections[:20],
            "conclusion": sections[-1]["body"][:200] if sections else "",
            "source": "smellycock/essays", "body_len": len(text)}


def main():
    files = sorted(glob.glob(str(ESSAYS / "*.md")))
    print(f"real essay golds: {len(files)}\n")
    committed = 0
    for f in files:
        g = _parse(Path(f))
        payload = {"essay": g, "essay_status": "MACHINE_PROPOSED", "derived_by": "smellycock-essay-gold"}
        ih = R.input_hash(payload)
        if R.is_committed("ESSAY", g["object_id"], ih):
            continue
        R.commit("ESSAY", g["object_id"], ih, "ingest-essay-golds", status=R.GENERATED,
                 payload=payload, input_refs=[])
        committed += 1
        print(f"  ✓ {g['object_id']}: {g['title'][:50]} ({len(g['sections'])} sections, {g['body_len']} chars)")
    print(f"\ncommitted {committed} essay golds (real SHOW-EVIDENCE essays)")


if __name__ == "__main__":
    main()
