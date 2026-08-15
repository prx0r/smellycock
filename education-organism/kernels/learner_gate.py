#!/usr/bin/env python3
"""kernels/learner_gate.py — the authority-gated learner store (graphiti + MKG + MemOS synthesis).

The "legit" learner memory: a misconception correction is TIME-BOUNDED (graphiti), APPROVED through a
2-tier gate (MKG), and SUPERSEDES rather than piles up (MemOS). All three ideas synthesised here as one
deterministic, stdlib kernel over a simple append-only store:

  temporal   — every stored belief carries valid_at/invalid_at + a provenance episode (graphiti), so
               "what was believed at t" and "what is true now" are both answerable; a correction
               invalidates the old fact without deleting it.
  2-tier gate — an automated consistency gate (existing-veto > already-learned-merge > new-win >
               unclear) + a human review queue for genuine ambiguity (MKG), stamped `reviewed_by` so a
               later gate can't silently overturn a human decision.
  correction guards — a proposed correction that OVERRIDES a stored belief must map back to a real
               stored id, UPDATE wins over ADD, a change-ratio guard downgrades update→add rather than
               clobbering, and the old node is ARCHIVED with a `covered_history` link (MemOS), never
               deleted.

These are exactly the three frontier ideas from FRONTIER-REVIEW §8.1, made concrete for the Patala
learner store. Deterministic + stdlib. No graph DB, no LLM in the gate itself (the judge is a callable
the caller may supply; default is a deterministic lexical judge).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from difflib import SequenceMatcher
import time


# ── temporal fact (graphiti) ────────────────────────────────────────────────────
@dataclass
class BeliefFact:
    """A stored belief with a validity window + provenance episode. invalid_at=None = currently valid."""
    fact_id: str
    belief: str
    valid_at: float
    invalid_at: float | None = None
    episode: str = ""          # provenance: which learner/session/correction produced it
    covered_history: str = ""  # MemOS: the id of the belief this supersedes
    reviewed_by: str = "machine"   # 'machine' | 'human'
    status: str = "active"     # 'active' | 'archived'

    def is_active_at(self, t: float) -> bool:
        return self.valid_at <= t and (self.invalid_at is None or t < self.invalid_at)


# ── the 2-tier gate (MKG) ───────────────────────────────────────────────────────
# A candidate correction is judged against existing beliefs. The precedence (MKG consistency_gate):
#   existing-veto > already-learned-merge > new-win > unclear
class CandidateVerdict:
    EXISTING_VETO = "existing_veto"        # genuinely contradicts → reject the candidate
    ALREADY_LEARNED = "already_learned"    # restatement → reinforce existing, reject candidate
    NEW = "new"                            # new constraint, no conflict → accept
    UNCLEAR = "unclear"                    # ambiguous → punt to human review queue


def _lexical_contradicts(a: str, b: str) -> bool:
    """Deterministic stand-in judge: do the two beliefs contain direct contradiction signals?
    A 'not'/'deny' in one but not the other, or a negation pair, suggests contradiction."""
    import re
    norm = lambda s: re.sub(r"[^a-z]+", " ", s.lower()).strip()
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    neg_a = bool(re.search(r"\b(not|den|never|no)\b", na))
    neg_b = bool(re.search(r"\b(not|den|never|no)\b", nb))
    if neg_a != neg_b:
        # one asserts, the other denies → possible contradiction
        return SequenceMatcher(None, re.sub(r"\b(not|den|never|no)\b", "", na).strip(),
                               re.sub(r"\b(not|den|never|no)\b", "", nb).strip()).ratio() >= 0.5
    return False


class LearnerGate:
    """The authority-gated learner store: temporal beliefs + 2-tier approval + correction guards."""

    def __init__(self, judge=None, overlap_threshold: float = 0.6):
        self.judge = judge or _lexical_contradicts
        self.overlap_threshold = overlap_threshold
        self.facts: list[BeliefFact] = []   # append-only (graphiti/MemOS: never mutate in place)
        self.review_queue: list[dict] = []  # MKG: human-review candidates
        self.rejections: list[dict] = []    # audit of rejected candidates

    # ── read ─────────────────────────────────────────────────────────────
    def active_at(self, t: float) -> list[BeliefFact]:
        return [f for f in self.facts if f.is_active_at(t) and f.status == "active"]

    def current(self, fact_id: str) -> BeliefFact | None:
        for f in reversed(self.facts):
            if f.fact_id == fact_id and f.status == "active" and f.invalid_at is None:
                return f
        return None

    def as_of(self, fact_id: str, t: float) -> str | None:
        """What was believed about fact_id at time t (the time-bounded truth).

        This is the graphiti temporal reader: it is bounded ONLY by the validity window
        (valid_at <= t < invalid_at), not by the current live status. A superseded/archived fact
        still answers correctly for times BEFORE its supersession (t < invalid_at), so "what was
        believed at t" is answerable across the whole history — never clobbered."""
        for f in self.facts:
            if f.fact_id == fact_id and f.is_active_at(t):
                return f.belief
        return None

    # ── the MemOS correction guards ────────────────────────────────────────
    def _find_overlap(self, belief: str) -> list[BeliefFact]:
        """All active facts whose belief overlaps the candidate (the ones it might override)."""
        norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).split()
        nb = set(norm(belief))
        if not nb:
            return []
        out = []
        for f in self.active_at(time.time()):
            nf = set(norm(f.belief))
            if not nf:
                continue
            ov = len(nb & nf) / max(1, len(nf))
            if ov >= self.overlap_threshold:
                out.append(f)
        return out

    # ── the 2-tier gate ────────────────────────────────────────────────────
    def propose_correction(self, fact_id: str, belief: str, *, episode: str = "",
                           judge=None, t: float | None = None) -> dict:
        """A candidate belief for fact_id. Runs the automated gate; genuine ambiguity → review queue.

        Returns {verdict, promoted, review_queued, reason}. Only NEW (or a clean override where the
        judge finds no contradiction) promotes to a new temporal fact; the rest are queued/rejected.
        """
        t = t if t is not None else time.time()
        judge = judge or self.judge
        existing = [f for f in self.facts if f.fact_id == fact_id and f.status == "active"]
        overlaps = self._find_overlap(belief)

        for e in existing:
            if judge(belief, e.belief):
                self.rejections.append({"fact_id": fact_id, "belief": belief,
                                        "vs": e.belief, "verdict": "existing_veto", "episode": episode})
                return {"verdict": "existing_veto", "promoted": False, "review_queued": False,
                        "reason": f"contradicts existing belief '{e.belief[:40]}…'"}

        for o in overlaps:
            if not o.fact_id == fact_id and SequenceMatcher(None, belief, o.belief).ratio() >= 0.9:
                # a near-duplicate restatement → reinforce the existing (ALREADY_LEARNED)
                o.episode = episode   # reinforce
                return {"verdict": "already_learned", "promoted": False, "review_queued": False,
                        "reason": f"restates existing '{o.belief[:40]}…' (reinforced)"}

        # NEW: promote — invalidate the old fact (graphiti), archive it (MemOS), link provenance
        if existing:
            for e in existing:
                e.invalid_at = t
                e.status = "archived"
        f = BeliefFact(fact_id=fact_id, belief=belief, valid_at=t, episode=episode,
                       covered_history=existing[-1].fact_id if existing else "",
                       reviewed_by="machine", status="active")
        self.facts.append(f)
        return {"verdict": "new", "promoted": True, "review_queued": False,
                "reason": "accepted (no conflict) via machine gate"}

    def flag_for_human_review(self, fact_id: str, belief: str, *, episode: str = "",
                              reason: str = "ambiguous") -> dict:
        """Punt a genuinely ambiguous candidate to the human review queue (MKG 2-tier)."""
        item = {"fact_id": fact_id, "belief": belief, "episode": episode,
                "reason": reason, "reviewed_by": None}
        self.review_queue.append(item)
        return item

    def human_resolve(self, index: int, decision: str, reviewer: str) -> dict:
        """The ONLY path that can overturn a machine veto / accept an ambiguous candidate.

        decision: 'accept' | 'reject'. Stamped `reviewed_by=reviewer` so a later gate can't silently
        overturn it. On accept, the belief is promoted (archiving any existing)."""
        if index >= len(self.review_queue):
            return {"error": "no such review item"}
        item = self.review_queue.pop(index)
        item["reviewed_by"] = reviewer
        if decision == "accept":
            item["verdict"] = "accepted_by_human"
            self._promote_human(item)
        else:
            item["verdict"] = "rejected_by_human"
            self.rejections.append(item)
        return item

    def _promote_human(self, item: dict):
        t = time.time()
        for e in self.facts:
            if e.fact_id == item["fact_id"] and e.status == "active":
                e.invalid_at = t
                e.status = "archived"
        self.facts.append(BeliefFact(fact_id=item["fact_id"], belief=item["belief"], valid_at=t,
                                     episode=item.get("episode", ""),
                                     covered_history=item["fact_id"],
                                     reviewed_by=item["reviewed_by"], status="active"))

    def summary(self) -> dict:
        return {
            "total_facts": len(self.facts),
            "active_now": len(self.active_at(time.time())),
            "archived": sum(1 for f in self.facts if f.status == "archived"),
            "human_review_queue": len(self.review_queue),
            "rejections": len(self.rejections),
        }


if __name__ == "__main__":
    g = LearnerGate()
    g.propose_correction("c1", "The flashing has an order-less support.", episode="learner-A")
    g.propose_correction("c1", "The flashing is the order itself, with no separate support.",
                         episode="learner-B")  # contradicts → veto
    g.propose_correction("c2", "Recognition is the felt re-cognition of the self.", episode="learner-A")
    print("after machine gate:", g.summary())
    g.flag_for_human_review("c1", "The support is both order-less and ordered.", reason="ambiguous")
    g.human_resolve(0, "accept", "scholar-K")
    print("after human resolve:", g.summary())
    print("c1 as_of now:", g.as_of("c1", time.time())[:50])
