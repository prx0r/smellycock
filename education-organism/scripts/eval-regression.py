#!/usr/bin/env python3
"""scripts/eval-regression.py — the deterministic guard eval + regression gate (fojin "eval-regression gate").

What it measures: does the anti-hallucination guard correctly (a) keep REAL quoted passages and their
citations `verified`, and (b) downgrade/strip FABRICATED quotes and citations? This is a guard-correctness
eval over hand-labelled {answer, source_text, expected_trust} cases.

Source of truth: the SciFact COVID-19 `claims.txt` at
`/root/fuck-off/ecosystem/science/scifact/covid/claims.txt`. Honest note: the full SciFact gold
(claim↔evidence SUPPORT/CONTRADICT/NEI + corpus) ships as a separate download (script/download-data.sh,
needs torch + network), and this box's rules are stdlib-only + no network. What IS present locally is the
plain COVID claim list — real, human-curated claim SENTENCES but with no offline evidence/label mapping.
So we reuse those REAL sentences as grounded `source_text` and author deterministic `expected_trust`
labels over them (an honest fixture set, documented — not a claim of reproducing SciFact NLI scores).

Deterministic + stdlib + fast (no LLM, no network). Two modes:
  --baseline   store the current score to data/eval/regression-baseline.json
  (default)    compare against the baseline; FAIL (exit 1) on any regression
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
from guard import guard_answer  # noqa: E402

SCIFACT_CLAIMS = Path("/root/fuck-off/ecosystem/science/scifact/covid/claims.txt")
BASELINE_FILE = ROOT / "data" / "eval" / "regression-baseline.json"


# ── the eval set: {answer, sources, retrieved_titles, expected_trust} ──────────
# sources = {title: passage}; a real quote is verbatim, a fabricated one differs.
# expected_trust: "real" → guard must leave it clean (no mutations); "fabricated" → must flag it.
def _covid_line(pred):
    """Pull a real COVID-19 claim sentence from claims.txt matching `pred` (first, case-folded)."""
    if not SCIFACT_CLAIMS.exists():
        raise FileNotFoundError(f"SciFact claims.txt missing: {SCIFACT_CLAIMS}")
    for line in SCIFACT_CLAIMS.read_text().splitlines():
        if pred in line.lower():
            return line
    raise ValueError(f"no COVID claim matching: {pred}")


_SRC = _covid_line("binds ace2 receptor to gain entry into cells")   # real sentence → grounded source
_SRC2 = _covid_line("cannot thrive in warmer climates")
_SRC3 = _covid_line("masking reduces covid")   # 'covid' is a substring of 'covid-19'
_SRC4 = _covid_line("approved treatments")

CASES = [
    # REAL: verbatim quote + correct citation → verified, untouched.
    {"name": "real-verbatim-cite",
     "answer": f'As the study reports: “{_SRC}” 【《Zhang et al. 2020》第1节】',
     "sources": {"Zhang et al. 2020": _SRC},
     "retrieved_titles": ["Zhang et al. 2020"],
     "expected_trust": "real"},
    {"name": "real-parenthesised-cite",
     "answer": f'The authors state “{_SRC2}” (Wang, ch. 2)',
     "sources": {"Wang": _SRC2},
     "retrieved_titles": ["Wang"],
     "expected_trust": "real"},
    # FABRICATED quote (off-by-one-word) bound to a real source → must be downgraded (quote_relaxed).
    {"name": "fabricated-near-miss",
     "answer": f'One analysis asserts: “{_SRC3.replace("transmission", "spread")}” 【《Li et al. 2020》第3节】',
     "sources": {"Li et al. 2020": _SRC3},
     "retrieved_titles": ["Li et al. 2020"],
     "expected_trust": "fabricated"},
    # FABRICATED quote entirely different → must be downgraded.
    {"name": "fabricated-invented-quote",
     "answer": f'“Masks are completely ineffective in any setting whatsoever and cause harm.” 【《Li et al. 2020》第3节】',
     "sources": {"Li et al. 2020": _SRC3},
     "retrieved_titles": ["Li et al. 2020"],
     "expected_trust": "fabricated"},
    # FABRICATED citation: real verbatim quote, but title NOT in whitelist → citation stripped.
    {"name": "fabricated-citation-title",
     "answer": f'As reported: “{_SRC4}” 【《Fabricated Trial 2022》第1节】',
     "sources": {"Real Author": _SRC4},
     "retrieved_titles": ["Real Author"],
     "expected_trust": "fabricated"},
    # REAL blockquote verbatim → verified.
    {"name": "real-blockquote",
     "answer": f'> {_SRC}\n\n【《Zhang et al. 2020》第1节】',
     "sources": {"Zhang et al. 2020": _SRC},
     "retrieved_titles": ["Zhang et al. 2020"],
     "expected_trust": "real"},
    # FABRICATED blockquote → downgraded.
    {"name": "fabricated-blockquote",
     "answer": f'> The virus thrives and spreads faster in warm tropical climates everywhere.\n\n【《Wang》第2章】',
     "sources": {"Wang": _SRC2},
     "retrieved_titles": ["Wang"],
     "expected_trust": "fabricated"},
    # REAL: unquoted citation (no quote bound) → not a verified quote, but also not a fabricated one.
    # Guard policy: a bare citation is a stripped/repaired no-op on quotes; treat as REAL (no fabrication).
    {"name": "real-unquoted-citation",
     "answer": f"This mechanism is detailed in 【《Zhang et al. 2020》第1节】.",
     "sources": {"Zhang et al. 2020": _SRC},
     "retrieved_titles": ["Zhang et al. 2020"],
     "expected_trust": "real"},
]


def _case_outcome(case: dict) -> dict:
    res = guard_answer(case["answer"], case["sources"], case["retrieved_titles"])
    n_muts = len(res["quote_mutations"]) + len(res["citation_mutations"])
    return {
        "trust": res["trust"],
        "n_mutations": n_muts,
        "flagged_fabrication": n_muts > 0,
    }


def _is_correct(case: dict, out: dict) -> bool:
    if case["expected_trust"] == "real":
        return out["n_mutations"] == 0
    return out["flagged_fabrication"]


def _score() -> dict:
    tp = fp = tn = fn = 0
    per = []
    for c in CASES:
        out = _case_outcome(c)
        pos_expected = c["expected_trust"] == "fabricated"
        pos_pred = out["flagged_fabrication"]
        tp += pos_expected and pos_pred
        fp += (not pos_expected) and pos_pred
        fn += pos_expected and (not pos_pred)
        tn += (not pos_expected) and (not pos_pred)
        per.append({"name": c["name"], "expected": c["expected_trust"],
                    "pred": out["trust"], "n_mutations": out["n_mutations"],
                    "correct": _is_correct(c, out)})
    correct = sum(1 for p in per if p["correct"])
    total = len(per)
    return {
        "total": total,
        "correct": correct,
        "pass_rate": correct / total if total else 0.0,
        "recall": (tp / (tp + fn)) if (tp + fn) else 0.0,      # fabricated caught
        "precision": (tp / (tp + fp)) if (tp + fp) else 0.0,   # flagged were really fabricated
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "per_case": per,
    }


def main() -> int:
    baseline = "--baseline" in sys.argv
    score = _score()
    # per-case detail
    print("=== eval-regression: guard correctness over fixture set ===")
    for p in score["per_case"]:
        print(f"  [{'OK ' if p['correct'] else 'BAD'}] {p['name']:28s} "
              f"expected={p['expected']:10s} pred={p['pred']:12s} mutations={p['n_mutations']}")
    summary = (f"eval-regression: {score['correct']}/{score['total']} passed "
               f"(recall={score['recall']:.3f}, precision={score['precision']:.3f}, "
               f"tp={score['tp']} fp={score['fp']} fn={score['fn']})")
    print(summary)

    if baseline:
        BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "total": score["total"],
            "correct": score["correct"],
            "pass_rate": score["pass_rate"],
            "recall": score["recall"],
            "precision": score["precision"],
            "note": "SciFact COVID claims.txt as grounded source text; hand-authored expected_trust "
                    "labels (offline gold labels unavailable under no-network rule).",
        }
        BASELINE_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        print(f"  baseline written → {BASELINE_FILE}")
        return 0

    if not BASELINE_FILE.exists():
        print("  no baseline file — run once with --baseline to establish it (this run: default/compare)")
        return 1

    base = json.loads(BASELINE_FILE.read_text())
    # regression = pass-rate OR recall OR precision dropped below baseline (strict fail on any regression)
    regressed = []
    for metric in ("pass_rate", "recall", "precision"):
        if score[metric] < base.get(metric, 0.0) - 1e-9:
            regressed.append(f"{metric}: {score[metric]:.3f} < baseline {base.get(metric):.3f}")
    if regressed:
        print("  REGRESSION detected:")
        for r in regressed:
            print(f"    - {r}")
        print(f"  baseline: {base['correct']}/{base['total']} "
              f"(recall={base['recall']:.3f}, precision={base['precision']:.3f})")
        return 1
    print(f"  no regression vs baseline {base['correct']}/{base['total']} "
          f"(recall={base['recall']:.3f}, precision={base['precision']:.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
