#!/usr/bin/env python3
"""scripts/test-guards.py — hard, real-world stress of the anti-hallucination guards.

Extends the happy-path guard coverage in run-tests.py with robustness cases that a model serving
real lessons will hit: title normalisation, near-miss fabricated quotes, blockquote + parenthesised
citation forms, idempotency, the short-quote carve-out, and the "cited-but-quoted-nothing" metric bug.

Deterministic, stdlib-only, no network, no LLM. Importable (run()) so run-tests.py can fold these in.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
from guard import (  # noqa: E402
    verify_quoted_content,
    citation_whitelist,
    guard_answer,
    count_checked_quotes,
    MIN_QUOTE_CHARS,
)

RESULTS = []


def t(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


# A realistic retrieved source: one work, one section, one canonical sentence.
SRC = {"Tantraloka": {1: "The flashing has an order-less support, the great Lord, required by ordered experience."}}
REAL_QUOTE = "The flashing has an order-less support, the great Lord, required by ordered experience."


def test_title_normalisation():
    """A real quote cited under a slightly different-but-normalised title must NOT false-flag."""
    # "Tantra loka" (space) normalises identically to "Tantraloka" (case/punct/space fold).
    answer = f"As the master writes: “{REAL_QUOTE}” 【《Tantra loka》第1章】"
    guarded, muts = verify_quoted_content(answer, SRC)
    t("title normalisation: real quote verifies under a space-variant title", len(muts) == 0)
    t("title normalisation: verified citation kept", "【" in guarded)


def test_near_miss_fabricated():
    """A fabricated quote off by ONE word lands in the near_miss bucket (sim >= 0.85), not absent."""
    near = REAL_QUOTE.replace("experience", "existence")  # one-word change → high similarity
    answer = f"He states: “{near}” 【《Tantraloka》第1章】"
    guarded, muts = verify_quoted_content(answer, SRC)
    assert len(muts) == 1, f"expected 1 mutation, got {len(muts)}"
    m = muts[0]
    t("near-miss: fabricated quote is flagged (quote_not_in_source)",
      m.reason == "quote_not_in_source")
    t("near-miss: lands in near_miss bucket (similarity >= 0.85)",
      m.bucket == "near_miss" and m.similarity >= 0.85,
      f"bucket={m.bucket} sim={m.similarity:.3f}")
    t("near-miss: guard_answer reports quote_relaxed",
      guard_answer(answer, SRC, ["Tantraloka"])["trust"] == "quote_relaxed")


def test_blockquote_fabricated():
    """A Markdown blockquote-form fabricated quote is downgraded."""
    answer = ("> " + "The flashing is the order itself and nothing else whatsoever, ever."
              + "\n\n【《Tantraloka》第1章】")
    guarded, muts = verify_quoted_content(answer, SRC)
    assert len(muts) == 1, f"expected 1 mutation, got {len(muts)}"
    t("blockquote: fabricated blockquote flagged", muts[0].reason == "blockquote_not_in_source")
    t("blockquote: quote marks/boundary dropped, citation still present",
      "【" in guarded and ">" not in guarded.split("【")[0])


def test_parenthesised_citation():
    """The parenthesised `(Title, ch. N)` form is recognised."""
    # real quote with a parenthesised citation verifies (no mutation)
    good = f"The text states “{REAL_QUOTE}” (Tantraloka, ch. 1)"
    g, gm = verify_quoted_content(good, SRC)
    t("parenthesised cite: real quote verifies (no mutation)", len(gm) == 0)
    t("parenthesised cite: quote counted as checked", count_checked_quotes(good) >= 1)
    # fabricated quote with a parenthesised citation is downgraded
    bad = f"He asserts “{REAL_QUOTE.replace('experience', 'existence')}” (Tantraloka, ch. 1)"
    bg, bm = verify_quoted_content(bad, SRC)
    t("parenthesised cite: fabricated quote downgraded", len(bm) == 1)


def test_idempotency():
    """Guarding a guarded answer is a no-op."""
    bad = f"He writes: “{REAL_QUOTE.replace('experience', 'existence')}” 【《Tantraloka》第1章】"
    g1 = guard_answer(bad, SRC, ["Tantraloka"])
    g2 = guard_answer(g1["answer"], SRC, ["Tantraloka"])
    t("idempotency: second pass adds no quote mutations", len(g2["quote_mutations"]) == 0)
    t("idempotency: second pass adds no citation mutations", len(g2["citation_mutations"]) == 0)
    t("idempotency: guarded answer stable", g1["answer"] == g2["answer"])


def test_short_quote_not_downgraded():
    """A very short quote (< MIN_QUOTE_CHARS) is NOT downgraded (paraphrase noise carve-out)."""
    short = "the support"  # 11 chars < MIN_QUOTE_CHARS
    assert len(short) < MIN_QUOTE_CHARS, "fixture must stay under the threshold"
    answer = f"Concerning {short}, see 【《Tantraloka》第1章】"
    guarded, muts = verify_quoted_content(answer, SRC)
    t("short quote: left intact (not downgraded)", len(muts) == 0)
    t("short quote: still carries its citation", "【" in guarded)
    t("short quote: not counted as a checked quote",
      count_checked_quotes(answer) == 0)


def test_cited_but_no_quote():
    """A citation with no quoted passage is NOT scored as a checked/verified quote (metric bug fix)."""
    t("cited-but-no-quote: count_checked_quotes == 0",
      count_checked_quotes("This point is developed in 【《Tantraloka》第1章】.") == 0)
    t("cited-but-no-quote: a bare parenthesised cite also counts 0",
      count_checked_quotes("See (Tantraloka, ch. 1).") == 0)


def test_diacritic_fold():
    """Sanskrit diacritic fold: a macron-variant title must NOT false-flag a real quote, and must
    STILL catch a fabricated one (the fold only helps matching, never loosens fabrication detection)."""
    # cite Tantrāloka (macron) against a source indexed as "Tantraloka" → must verify, not false-flag
    macron_title = "Tantr\u0101loka"  # ā
    real = f"As the master writes: \u201c{REAL_QUOTE}\u201d 【\u300a{macron_title}\u300b第1章】"
    guarded, muts = verify_quoted_content(real, SRC)
    t("diacritic fold: macron-variant title verifies a real quote", len(muts) == 0)
    # a fabricated quote under the macron title must still be downgraded
    bad = f"He claims: \u201cThe flashing is the order itself and nothing else.\u201d 【\u300a{macron_title}\u300b第1章】"
    guarded, muts = verify_quoted_content(bad, SRC)
    t("diacritic fold: still downgrades a fabricated quote under a macron title",
      len(muts) == 1 and muts[0].bucket in ("near_miss", "absent"))


def run() -> int:
    print("=== test-guards.py: hard anti-hallucination guard stress ===")
    test_title_normalisation()
    test_near_miss_fabricated()
    test_blockquote_fabricated()
    test_parenthesised_citation()
    test_idempotency()
    test_short_quote_not_downgraded()
    test_cited_but_no_quote()
    test_diacritic_fold()
    n = sum(RESULTS)
    print(f"\n=== GUARDS HARD: {n}/{len(RESULTS)} passed ===")
    return n


if __name__ == "__main__":
    run()
    sys.exit(0 if all(RESULTS) else 1)
