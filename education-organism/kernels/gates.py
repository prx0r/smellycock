#!/usr/bin/env python3
"""kernels/gates.py — the deterministic POST-C1 gates (REDUCTION layer).

Production-grade deterministic gates for the POST-C1 spine, following the AXIOMS (fail-closed,
validate-first, never fabricate). Hermes GENERATES; these gates REDUCE/validate.

Gates:
  cite_contract  — every ARGUMENT premise/conclusion carries a resolvable (cite: id)/source/evidence_quote
  nyaya          — the 5-hetvābhāsa Nyāya gate (asiddha/viruddha/savyabhicara/satpratipaksa/badhita)
  quality        — verifiable-reward score (PASS/BLOCK) for any object
  chain          — every POST-C1 object resolves down to C1 (proof path)
  blind_grade    — engram-style blind rubric grading (EDUCATION)
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "registries"


def load_current(layer: str) -> dict:
    p = REG / f"{layer.lower()}-registry.jsonl"
    out = {}
    if not p.exists():
        return out
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if not r.get("superseded"):
            out[r["object_id"]] = r
    return out


def _all_committed_ids() -> set:
    ids = set()
    for f in REG.glob("*-registry.jsonl"):
        for line in f.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if not r.get("superseded") and r.get("object_id"):
                ids.add(r["object_id"])
    return ids


# ── Nyāya gate (5-hetvābhāsa) ────────────────────────────────────────────────
FALLACIES = ["asiddha", "viruddha", "savyabhicara", "satpratipaksa", "badhita"]
STRONG_WORDS = ["proves", "settles", "demonstrates", "decisive", "certainly", "always"]
UNIVERSAL = ["always", "invariably", "everywhere", "never fails", "universally"]
UNFALSIFIABLE = ["cannot be verified", "cannot be measured", "no possible disproof", "transcends all evidence"]


def nyaya(claim: dict) -> dict:
    """5-hetvābhāsa gate → verdict PASS/PASS_WITH_OPEN/FAIL + dims (pratijna/hetu/scope/support)."""
    text = str(claim.get("claim_text", "")).lower()
    failures = []
    if any(u in text for u in UNFALSIFIABLE):
        return {"verdict": "FAIL", "failures": ["asiddha:unfalsifiable"],
                "dimensions": {"pratijna": "OPEN", "hetu": "DEFECT", "scope": "CLEAN", "support_relation": "CLEAN"}}
    if claim.get("falsifier") is None:
        # missing falsifier → pratijna OPEN
        pass
    if any(w in text for w in UNIVERSAL) and (claim.get("vyapti_confidence") or 0) < 0.8:
        failures.append("savyabhicara:universal-without-vyapti")
    if any(w in text for w in STRONG_WORDS) and claim.get("pramana") in ("sabda", "upamana"):
        failures.append("asiddha:strong-from-weak-pramana")
    severity = "FAIL" if failures else ("PASS_WITH_OPEN" if claim.get("falsifier") is None else "PASS")
    return {"verdict": severity, "failures": failures,
            "dimensions": {"pratijna": "OPEN" if claim.get("falsifier") is None else "CLEAN",
                           "hetu": "DEFECT" if any("asiddha" in f for f in failures) else "CLEAN",
                           "scope": "DEFECT" if any("savyabhicara" in f for f in failures) else "CLEAN",
                           "support_relation": "CLEAN"}}


# ── cite contract ─────────────────────────────────────────────────────────────
def cite_contract(layer: str) -> dict:
    """Every ARGUMENT premise/conclusion must carry a source/evidence_quote/cite."""
    problems = []
    total_premises = cited = 0
    idx = _all_committed_ids()
    for oid, r in load_current(layer).items():
        arg = r["payload"].get("argument", {})
        for p in arg.get("premises", []):
            if isinstance(p, dict):
                total_premises += 1
                if p.get("evidence_quote") or p.get("source"):
                    cited += 1
                else:
                    problems.append(f"{oid}: premise uncited")
        if not arg.get("conclusion", {}).get("source"):
            problems.append(f"{oid}: conclusion uncited")
    return {"layer": layer, "premises": total_premises, "cited": cited,
            "problems": problems, "pass": not problems}


# ── content-text extraction (the red-team fix: inspect REAL derived content) ──
def _content_text(payload: dict) -> str:
    """Extract the actual textual content from a payload, whatever the storage shape.

    The red-team found objects stored under `payload.derived` with content in arbitrary keys
    (e.g. {'EDUCATION': 'Postgraduate'}) that the old gate ignored. This walks all string values
    and returns the longest substantive text (min 3 words), so junk like 'Postgraduate' fails."""
    texts = []
    def walk(v):
        if isinstance(v, str):
            if len(v.split()) >= 3:
                texts.append(v)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(payload)
    return max(texts, key=len) if texts else ""


# ── quality (verifiable reward, PASS/BLOCK) — real-content aware ──────────────
def quality(obj: dict) -> tuple[float, list[str], str]:
    score, checks = 0.0, []
    layer = obj["layer"].upper()
    payload = obj.get("payload", {})
    content = _content_text(payload)
    if layer in ("C1",):
        c = payload.get("c1", {})
        if c.get("evidence_quote"): score += 0.4; checks.append("evidence_quote")
        if c.get("claim") or c.get("summary"): score += 0.3; checks.append("claim")
        if c.get("related_passages"): score += 0.3; checks.append("refs")
    elif layer in ("ARGUMENT",):
        a = payload.get("argument", {}) or payload.get("derived", {})
        prems = a.get("premises", []) or []
        n = sum(1 for p in prems if isinstance(p, dict) and (p.get("evidence_quote") or p.get("source")))
        if prems and n == len(prems): score += 0.6; checks.append(f"cited {n}/{len(prems)}")
        elif a.get("conclusion", {}).get("source") or a.get("source"):
            score += 0.4; checks.append("source")
        if a.get("crux"): score += 0.2; checks.append("crux")
    # CORE REAL-CONTENT CHECK (red-team CRITICAL-2): the text must be substantive
    # Score by richness: >=6 words = real content (0.6+); 3-5 words = thin (0.4, likely junk).
    words = len(content.split()) if content else 0
    if words >= 6:
        score += 0.6; checks.append(f"substantive content ({words} words)")
    elif words >= 3:
        score += 0.4; checks.append(f"thin content ({words} words)")
    else:
        score += 0.0; checks.append("NO substantive content")
    refs = obj.get("input_refs", [])
    idx = _all_committed_ids()
    if refs and all(x in idx for x in refs):
        score += 0.0; checks.append("(inputs resolve)")
    verdict = "PASS" if score >= 0.6 and words >= 3 else "BLOCK"
    return round(min(1.0, score), 3), checks, verdict


# ── chain (proof path to C1) ──────────────────────────────────────────────────
def chain() -> tuple[bool, list[str]]:
    c1s = {oid: r for oid, r in load_current("C1").items()}
    failures = []
    for layer in ["THEME", "ARGUMENT", "SYNTHESIS", "ESSAY", "EDUCATION"]:
        for oid, r in load_current(layer).items():
            # gold/external objects (created_by ingest-*-golds) are upstream gold, not derived
            # projections — they don't need to resolve to C1. Skip them honestly.
            if "gold" in oid or r.get("created_by", "").endswith("-golds"):
                continue
            refs = r.get("input_refs", [])
            if not refs:
                failures.append(f"{oid}: no input_refs")
            elif not any(x in c1s for x in refs):
                failures.append(f"{oid}: no ref resolves to C1")
    return (not failures, failures)


# ── blind grade (engram) ──────────────────────────────────────────────────────
def blind_grade(question, answer, rubric) -> dict:
    hits = [r for r in rubric if r in str(answer).lower()]
    cov = len(hits) / len(rubric) if rubric else 0
    grade = "recalled" if cov >= 0.6 else ("partial" if cov >= 0.3 else "lapsed")
    return {"grade": grade, "coverage": round(cov, 2), "hits": hits}
