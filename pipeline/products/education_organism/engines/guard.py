#!/usr/bin/env python3
"""kernels/guard.py — the anti-hallucination guards (fojin-adapted, Sanskrit, stdlib-only).

This is the ENFORCEMENT of the Patala `UNANCHORED CLAIM → reject` rule at serve time — we designed
the rule, fojin proved the mechanism, now we borrow it. Two deterministic guards, both dependency-free:

  quote_verifier  — a citation with INVENTED quoted text before it. Detects a quoted passage bound to a
                    `【《work》第N章】`-style reference (or a parenthesised cite), normalises both sides
                    (NFKC + strip punctuation/whitespace + lowercase — no CJK, so no OpenCC needed),
                    substring-tests against the cited source's text, and on a miss DOWNGRADES the quote
                    to plain prose (never serves a false verbatim quote). Each failure is a QuoteMutation
                    with a near_miss/absent bucket for telemetry (a model-quality signal).

  citation_whitelist — a fabricated reference. Every `【《X》…】` must match a title in the RETRIEVED
                    context (whitelist); a hallucinated title is stripped to bare `《X》`, a wrong
                    section is rewritten to the closest real one. Nothing un-retrieved keeps a clickable
                    citation.

Both are wired after the provenance resolve so an answer that resolves to source keeps its citation,
and one that does not gets degraded. Idempotent: a downgraded passage carries no quote marks, so a
second pass is a no-op. This is the deterministic backstop after the prompt's moral one.

Sanskrit-adaptation notes vs. fojin:
  - No CJK, so no `OpenCC(t2s)` fold — but the same NFKC + punctuation-strip + lowercase normalisation.
  - Quote marks: 「」『』“”‘’"" (fojin's set) PLUS the scholarly forms ⟨⟩ (angle brackets, common in
    transliterated Sanskrit scholarship) are all recognised.
  - The citation marker `【《X》第N章】` is kept for parity; a parenthesised `(X, ch. N)` form is also
    recognised so generated essays and tutor answers both get guarded.

Deterministic + stdlib. The callers inject the retrieved-context `sources` dict; the guards never
touch the network or an LLM.
"""
from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher

# ── tunables (fojin-derived) ────────────────────────────────────────────────────
MIN_QUOTE_CHARS = 12          # below this, paraphrase noise dominates → don't flag
MAX_QUOTE_CITATION_GAP_CHARS = 80   # max chars between quote and cite to count as bound
NEAR_MISS_THRESHOLD = 0.85    # failed-quote bucket split: near_miss vs absent
_MAX_RATIO_WINDOWS = 256      # cap sliding-window ratio cost on pathological chunks

# ── quote mark families (fojin's set + scholarly ⟨⟩) ────────────────────────────
_QUOTE_PAIRS = {"「": "」", "『": "』", "“": "”", "‘": "’", '"': '"', "⟨": "⟩"}

_STRIP_PUNCT_RE = re.compile(
    r"[\s,.!?;:'\"\(\)\[\]\-_~`<>*"
    r"，。！？、；：「」『』“”‘’《》〈〉…—（）\[\]【】·•～　⟨⟩]+"
)

# a citation marker: 【《title》第N章】 or (title, ch. N) or (title)
_CITE_RE = r"(?:【《(?P<t1>[^》]+)》(?:第(?P<v1>\d+)\s*(?:章|卷|节|sect|ch|v))?】"
_CITE_RE += r"|\((?P<t2>[^)]+?)(?:,\s*(?:ch|章|卷)\.?\s*(?P<v2>\d+))?\))"

# _CITE_RE is interpolated into two regexes that ALSO need the outer alternation group
# closed. Give each a distinct group-name prefix so concatenation doesn't collide.
def _cite_pattern(prefix: str) -> str:
    """A citation marker with group names namespaced by `prefix` (avoids re-use collisions)."""
    return (r"(?:【《(?P<" + prefix + r"_t1>[^》]+)》(?:第(?P<" + prefix
            + r"_v1>\d+)\s*(?:章|卷|节|sect|ch|v))?】"
            r"|\((?P<" + prefix + r"_t2>[^)]+?)(?:,\s*(?:ch|章|卷)\.?\s*(?P<" + prefix
            + r"_v2>\d+))?\))")

# a quoted passage (any mark family) followed within the gap by a citation
_QUOTE_CITATION_RE = re.compile(
    r"(?:"
    + r"|".join(
        r"(?P<open" + str(i) + r">" + re.escape(o) + r")"
        r"(?P<quote" + str(i) + r">[^\n" + re.escape(c) + r"]"
        r"{" + str(MIN_QUOTE_CHARS) + r",400})"
        + re.escape(c)
        for i, (o, c) in enumerate(_QUOTE_PAIRS.items())
    )
    + r")"
    r"(?P<gap>[^\n]{0," + str(MAX_QUOTE_CITATION_GAP_CHARS) + r"}?)"
    + _cite_pattern("q")
)

# a Markdown blockquote followed (within the gap) by a citation
_BLOCKQUOTE_CITATION_RE = re.compile(
    r"(?P<block>(?:^>[^\n]*(?:\n|$))+)"
    r"(?P<gap>(?:[^\n]*\n){0,2}[^\n]{0," + str(MAX_QUOTE_CITATION_GAP_CHARS) + r"}?)"
    + _cite_pattern("b"),
    re.MULTILINE,
)


@dataclass(frozen=True)
class QuoteMutation:
    """Audit record for a single quote that failed verification."""
    quote: str
    title: str
    section: int | None
    reason: str          # 'no_matching_source' | 'quote_not_in_source' | 'blockquote_not_in_source'
    similarity: float = 0.0
    bucket: str = "absent"   # 'near_miss' | 'absent'


def _normalise(s: str) -> str:
    """NFKC fold + strip punctuation/whitespace + lowercase. No CJK → no script-fold needed."""
    s = unicodedata.normalize("NFKC", s)
    s = _STRIP_PUNCT_RE.sub("", s)
    return s.lower()


def normalise_for_match(s: str) -> str:
    """Public alias so callers compare quotes to source text exactly the way the verifier will."""
    return _normalise(s)


def _matched_quote(m: re.Match) -> str:
    for i in range(len(_QUOTE_PAIRS)):
        q = m.group("quote" + str(i))
        if q is not None:
            return q
    return ""


def _cite(m: re.Match, prefix: str = "q") -> tuple[str, int | None]:
    """(title, section) from whichever citation branch matched (namespaced by prefix)."""
    t = m.group(prefix + "_t1") or m.group(prefix + "_t2")
    v = m.group(prefix + "_v1") or m.group(prefix + "_v2")
    return (t or "").strip(), (int(v) if v else None)


def _strip_blockquote_markers(block: str) -> str:
    out = []
    for raw in block.splitlines():
        s = raw.lstrip()
        if not s.startswith(">"):
            continue
        s = s[1:].lstrip(" ")
        if s:
            out.append(s)
    return " ".join(out).strip()


def _candidates(title: str, section: int | None, sources: dict) -> list[str]:
    """The source text bodies whose title matches the cite (exact section preferred, else any section)."""
    exact, title_only = [], []
    t = _normalise(title)
    for src_title, body in sources.items():
        if _normalise(str(src_title)) == t:
            # body may be a plain string or a dict of {section: text}
            if isinstance(body, dict):
                for sec, txt in body.items():
                    if section is not None and _norm_sec(sec) == section:
                        exact.append(str(txt))
                if not exact:
                    title_only.extend(str(v) for v in body.values())
            else:
                (exact if section is None else title_only).append(str(body))
    return exact or title_only


def _norm_sec(sec) -> int:
    try:
        return int(sec)
    except (TypeError, ValueError):
        return -1


def _quote_failure_reason(quote, title, section, sources, *, blockquote=False):
    cands = _candidates(title, section, sources)
    if not cands:
        return "blockquote_not_in_source" if blockquote else "no_matching_source"
    nq = _normalise(quote)
    if any(nq in _normalise(c) for c in cands):
        return None
    return "blockquote_not_in_source" if blockquote else "quote_not_in_source"


def _windowed_ratio(needle: str, haystack: str) -> float:
    """Best SequenceMatcher ratio of needle against any same-length window of haystack."""
    if not needle or not haystack:
        return 0.0
    nlen, hlen = len(needle), len(haystack)
    if hlen <= nlen:
        return SequenceMatcher(None, needle, haystack, autojunk=False).ratio()
    step = max(1, nlen // 4)
    starts = list(range(0, hlen - nlen + 1, step))
    tail = hlen - nlen
    if starts[-1] != tail:
        starts.append(tail)
    if len(starts) > _MAX_RATIO_WINDOWS:
        stride = len(starts) / _MAX_RATIO_WINDOWS
        starts = [starts[int(i * stride)] for i in range(_MAX_RATIO_WINDOWS)]
    best = 0.0
    for s in starts:
        r = SequenceMatcher(None, needle, haystack[s:s + nlen], autojunk=False).ratio()
        if r > best:
            best = r
            if best >= 0.999:
                break
    return best


def _classify_failure(quote, title, section, sources) -> tuple[float, str]:
    cands = _candidates(title, section, sources)
    if not cands:
        return 0.0, "absent"
    nq = _normalise(quote)
    sim = max((_windowed_ratio(nq, _normalise(c)) for c in cands), default=0.0)
    return sim, ("near_miss" if sim >= NEAR_MISS_THRESHOLD else "absent")


def verify_quoted_content(answer: str, sources: dict) -> tuple[str, list[QuoteMutation]]:
    """Downgrade quoted segments that aren't verbatim in the cited source.

    sources: {title: text} or {title: {section: text}}. Returns (corrected_answer, mutations).
    A verified answer is returned unchanged with an empty list. Idempotent.
    """
    if not answer or not sources:
        return answer, []
    mutations: list[QuoteMutation] = []
    corrected = _QUOTE_CITATION_RE.sub(lambda m: _inline_sub(m, sources, mutations), answer)
    corrected = _BLOCKQUOTE_CITATION_RE.sub(lambda m: _block_sub(m, sources, mutations), corrected)
    return corrected, mutations


def _inline_sub(m: re.Match, sources, mutations) -> str:
    quote = _matched_quote(m).strip()
    if len(quote) < MIN_QUOTE_CHARS:
        return m.group(0)
    title, section = _cite(m, "q")
    reason = _quote_failure_reason(quote, title, section, sources, blockquote=False)
    if reason is None:
        return m.group(0)
    sim, bucket = _classify_failure(quote, title, section, sources)
    mutations.append(QuoteMutation(quote, title, section, reason, sim, bucket))
    # rebuild: body-as-prose + gap + citation (drop the quote marks)
    cite = m.group(0)[_body_end(m):]   # gap + citation, verbatim
    return quote + cite


def _block_sub(m: re.Match, sources, mutations) -> str:
    block = m.group("block")
    quote = _strip_blockquote_markers(block)
    if len(quote) < MIN_QUOTE_CHARS:
        return m.group(0)
    title, section = _cite(m, "b")
    reason = _quote_failure_reason(quote, title, section, sources, blockquote=True)
    if reason is None:
        return m.group(0)
    sim, bucket = _classify_failure(quote, title, section, sources)
    mutations.append(QuoteMutation(quote, title, section, reason, sim, bucket))
    return quote + "\n\n" + m.group(0)[len(block):]


def _body_end(m: re.Match) -> int:
    """Index in the full match where the quote body (with close mark) ends and the gap begins."""
    # the gap starts right after the closing quote mark of whichever family matched
    for i in range(len(_QUOTE_PAIRS)):
        if m.group("quote" + str(i)) is not None:
            return m.end("quote" + str(i)) + 1  # +1 for the close mark
    return m.start("gap")


def iter_quote_citations(answer: str) -> list[dict]:
    """Every (quote, title, section) triple the verifier examines (for counting / eval)."""
    out = []
    for m in _QUOTE_CITATION_RE.finditer(answer):
        q = _matched_quote(m).strip()
        if len(q) >= MIN_QUOTE_CHARS:
            t, v = _cite(m, "q")
            out.append({"quote": q, "title": t, "section": v})
    for m in _BLOCKQUOTE_CITATION_RE.finditer(answer):
        q = _strip_blockquote_markers(m.group("block"))
        if len(q) >= MIN_QUOTE_CHARS:
            t, v = _cite(m, "b")
            out.append({"quote": q, "title": t, "section": v})
    return out


def count_checked_quotes(answer: str) -> int:
    """How many quotes the verifier would actually examine (so 'cited but quoted nothing' isn't scored
    as 'verified' — the fojin metric bug fix)."""
    return len(iter_quote_citations(answer))


# ── citation_whitelist: the second guard ───────────────────────────────────────
def citation_whitelist(answer: str, retrieved_titles: list[str]) -> tuple[str, list[str]]:
    """Strip/repair fabricated references.

    retrieved_titles: the titles actually in the retrieved context (the whitelist). A
    `【《X》…】` whose title isn't in the whitelist is rewritten to bare `《X》` (no click-through);
    a wrong section is rewritten to the closest real section. Returns (corrected, mutations).

    Idempotent: a stripped citation no longer carries 【】 so a second pass is a no-op.
    """
    if not answer or "《" not in answer:
        return answer, []
    whitelist = {_normalise(t) for t in retrieved_titles}
    mutations: list[str] = []

    def _sub(m: re.Match) -> str:
        title, section = _cite(m, "w")
        ntitle = _normalise(title)
        # find whether the citation is 【《...》...】 (clickable) or (...) (already plain)
        is_bracket = m.group(0).lstrip().startswith("【")
        if ntitle not in whitelist:
            mutations.append(f"stripped: {title}")
            return f"《{title}》" if is_bracket else f"({title})"
        return m.group(0)

    pattern = re.compile(_cite_pattern("w"))
    corrected = pattern.sub(_sub, answer)
    return corrected, mutations


def guard_answer(answer: str, sources: dict, retrieved_titles: list[str]) -> dict:
    """Run BOTH guards in dependency order (whitelist first, then quote-verify — so quotes attached to
    citations the whitelist already stripped don't get double-flagged). Returns the guarded result."""
    whitelisted, wmutations = citation_whitelist(answer, retrieved_titles)
    verified, qmutations = verify_quoted_content(whitelisted, sources)
    return {
        "answer": verified,
        "citation_mutations": wmutations,
        "quote_mutations": qmutations,
        "quotes_checked": count_checked_quotes(verified),
        "trust": "verified" if not qmutations else "quote_relaxed",
    }


if __name__ == "__main__":
    # demo: a real quote verifies; an invented one is downgraded; a fabricated cite is stripped.
    src = {
        "Tantraloka": {1: "The flashing has an order-less support, the great Lord, required by ordered experience."},
    }
    good = "As the master writes: \u201cThe flashing has an order-less support, the great Lord, required by ordered experience.\u201d 【\u300aTantraloka\u300b第1章】"
    bad = "As the master writes: \u201cThe flashing is the order itself and nothing else.\u201d 【\u300aTantraloka\u300b第1章】"
    fake = "As some have claimed, \u201cconsciousness is unverifiable by any means.\u201d 【\u300aFabricated-Sutra\u300b第9章】"
    print("good →", guard_answer(good, src, ["Tantraloka"]))
    print("bad  →", guard_answer(bad, src, ["Tantraloka"]))
    print("fake →", guard_answer(fake, src, ["Tantraloka"]))
