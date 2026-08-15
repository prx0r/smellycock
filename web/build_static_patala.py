#!/usr/bin/env python3
"""build_static_patala.py — the OG patala projection compiler → static site (0-JS read plane).

Turns the REAL patala data into a fully static, deployable site (Astro serves it):
  web/static/
    index.json          the site manifest (bibliography + clusters + passages)
    bibliography.json   254 works
    clusters.json       9 themes
    passages.json       49 IPVV published passages
    lemma.json          the term/lemma data
    timeline.json       the school/tradition chronology
  All static bytes — compute on write, read from CDN (the perf doctrine).

Grounded in the REAL patala data (data/corpus/ + data/published/ + data/atlas/), not synthetic.
"""
import os, sys, json
from pathlib import Path

ROOT = Path(os.environ.get("PATALA_ROOT", "/root/patalacheckpoints"))
OUT = ROOT / "web" / "static"
# the deployable site's static surface — emit the SAME projections here so the served site
# (smellycock) and the code repo stay aligned in one build (the perf doctrine: compute once, serve many).
SITE_OUT = Path(os.environ.get("PATALA_SITE_STATIC", "/root/smellycock/web/static"))
DATA = {
    "bibliography": ROOT / "data" / "corpus" / "atlas-bibliography.json",
    "clusters": ROOT / "data" / "published" / "ipvv" / "clusters.json",
    "published_index": ROOT / "data" / "published" / "ipvv" / "index.json",
    "timeline": ROOT / "data" / "atlas" / "historyTimeline.json",
}
# the materialized translation-status registry (translation-existence + location) — the alignment fix.
# If present, the static bibliography carries the real English-translation urls/language per work,
# so the public site answers "where is the English translation of X?" instead of dropping it.
TRANSLATION_STATUS = ROOT / "data" / "corpus" / "translation-status.json"
_TS_CACHE = None


def _translation_status() -> dict:
    global _TS_CACHE
    if _TS_CACHE is None:
        try:
            _TS_CACHE = json.load(open(TRANSLATION_STATUS))
        except Exception:
            _TS_CACHE = {}
    return _TS_CACHE

def _to_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "1", "yes")
    return bool(v)

def _keep_text_sources(rec):
    """Carry the real edition/etext/translation/scholarship depth, compacted."""
    out = []
    for s in rec.get("text_sources", []):
        if not isinstance(s, dict):
            continue
        out.append({k: s.get(k) for k in ("type", "editor", "year", "provider", "tier", "coverage", "title", "url") if s.get(k)})
    return out

def _write_both(name: str, data, indent=1):
    """Write the same projection to the code-repo static AND the deployable site static (one build)."""
    SITE_OUT.mkdir(parents=True, exist_ok=True)
    for d in (OUT, SITE_OUT):
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SITE_OUT.mkdir(parents=True, exist_ok=True)

    # 1. bibliography (254 works)
    bib = json.load(open(DATA["bibliography"]))
    ts = _translation_status()
    works = []
    for wid, rec in bib.get("records", {}).items():
        translations = rec.get("translations", []) or []
        # alignment fix: if the atlas record dropped the translation detail, enrich from the
        # materialized translation-status registry so the public site carries url/language/location.
        if not translations and wid in ts:
            t = ts[wid]
            translations = t.get("translations", []) or []
            if not translations and t.get("english_urls"):
                translations = [{"language": "en", "url": u, "coverage": "", "complete": False,
                                 "type": "", "tier": "", "translator": ""} for u in t["english_urls"]]
        works.append({
            "id": wid,
            "title": rec.get("canonical_title") or rec.get("title") or wid,
            "work": rec.get("work") or wid,
            "verified": _to_bool(rec.get("verified", False)),
            "translation_status": rec.get("translation_status") or rec.get("translationStatus")
                                 or (ts.get(wid, {}).get("translationStatus", "none") if wid in ts else "none"),
            "traditions": rec.get("traditions", []),
            "period": rec.get("period"),
            "text_sources": _keep_text_sources(rec),
            "edition_count": rec.get("edition_count", 0),
            "etext_count": rec.get("etext_count", 0),
            "translations": translations,
            "copyright_hint": ts.get(wid, {}).get("copyrightHint", "UNKNOWN") if wid in ts else "UNKNOWN",
            "scholarship": rec.get("scholarship", []),
            "related": rec.get("related", []),
        })
    works.sort(key=lambda x: x["title"].lower())
    _write_both("bibliography.json", {"count": len(works), "works": works})

    # 2. clusters (9 themes)
    cl = json.load(open(DATA["clusters"]))
    _write_both("clusters.json", cl)

    # 3. published IPVV passages (49)
    idx = json.load(open(DATA["published_index"]))
    passages = []
    pdir = ROOT / "data" / "published" / "ipvv"
    for p in idx.get("passages", []):
        f = pdir / p["file"]
        if f.exists():
            d = json.load(open(f))
            passages.append({
                "id": d.get("id"), "chunk": d.get("chunk"), "vol": d.get("vol"),
                "reading": (d.get("l2_text") or d.get("l2") or "")[:400],
                "has_c1": d.get("c1") is not None,
            })
    _write_both("passages.json", {"count": len(passages), "passages": passages})

    # 4. lemma (the accepted term ledger)
    lemma_terms = []
    try:
        tj = json.load(open(ROOT / "data" / "terms.json"))
        terms = tj.get("terms", {})
        if isinstance(terms, dict):
            for lemma, senses in terms.items():
                lemma_terms.append({"lemma": lemma, "senses": len(senses) if isinstance(senses, list) else 1})
        elif isinstance(terms, list):
            for t in terms:
                lemma_terms.append({"lemma": t.get("lemma", t.get("id", "")), "senses": len(t.get("senses", []))})
    except Exception as e:
        print("  lemma parse note:", e)
    _write_both("lemma.json", {"count": len(lemma_terms), "terms": lemma_terms})

    # 5. timeline
    try:
        tl = json.load(open(DATA["timeline"]))
        _write_both("timeline.json", tl)
    except Exception:
        _write_both("timeline.json", {"count": 0})

    # 6. manifest
    manifest = {
        "schema": "patala.og.static-site.v1",
        "counts": {"works": len(works), "clusters": cl.get("cluster_count", 0),
                   "passages": len(passages), "terms": len(lemma_terms)},
        "generated": True,
    }
    _write_both("index.json", manifest, indent=1)
    print("=== OG patala static projections built ===")
    print(json.dumps(manifest, indent=1))

if __name__ == "__main__":
    main()
