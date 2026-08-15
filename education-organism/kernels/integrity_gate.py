"""lib/integrity_gate.py — integrity_status tri-state + primary-source gate (EleutherIA GEM 6.2).

EleutherIA's highest-value lesson: layer identity + integrity state are PERSISTED schema and retrieval
ENFORCES them mechanically — not metadata the LLM is left to reason about. Two adoptions:

1. **integrity_status tri-state** (`clean | demoted | excluded`): a human-adjudicated flag silently
   PRUNES a node from context at query time. `excluded` = never reaches the agent as evidence;
   `demoted` = annotated, never presented as verified. This upgrades our staleness/review into a
   retrieval-time enforcement, not a score.

2. **Primary-source HARD gate** (EleutherIA `dialectical_synthesis.py`): a synthesis answer requires ≥1
   PRIMARY-source citation or it FAILS. We adopt: a claim's evidence must include ≥1 primary-source
   (original-text) reference or the answer is rejected as ungrounded — not just "preferred."
"""
from __future__ import annotations


class IntegrityStatus:
    CLEAN = "clean"
    DEMOTED = "demoted"
    EXCLUDED = "excluded"


class SourceLayer:
    PRIMARY = "primary"       # original source text (the reality graph)
    SECONDARY = "secondary"   # modern reception / interpretation (the literature graph)


class IntegrityGate:
    """Persisted integrity tri-state + primary-source gate, enforced at retrieval."""

    def __init__(self):
        self._integrity = {}   # node_id -> IntegrityStatus
        self._layer = {}       # node_id -> SourceLayer

    def set_integrity(self, node_id, status):
        self._integrity[node_id] = status
        return status

    def set_layer(self, node_id, layer):
        self._layer[node_id] = layer
        return layer

    def status_of(self, node_id):
        return self._integrity.get(node_id, IntegrityStatus.CLEAN)

    def layer_of(self, node_id):
        return self._layer.get(node_id, SourceLayer.SECONDARY)

    # ---- retrieval-time filtering (mechanical, not LLM-reasoned) ----
    def filter_context(self, node_ids):
        """Return only the nodes that can reach an agent as evidence (excluded pruned)."""
        return [n for n in node_ids if self.status_of(n) != IntegrityStatus.EXCLUDED]

    def is_usable_as_verified(self, node_id):
        """A node is usable-as-verified only if clean (demoted is annotated, not verified)."""
        return self.status_of(node_id) == IntegrityStatus.CLEAN

    # ---- the primary-source hard gate (EleutherIA: ≥1 primary cite or FAIL) ----
    def synthesis_gate(self, evidence_sources):
        """A synthesis answer requires ≥1 PRIMARY-source citation or it FAILS (rejected as ungrounded)."""
        primaries = [s for s in evidence_sources if self.layer_of(s) == SourceLayer.PRIMARY
                     and self.status_of(s) == IntegrityStatus.CLEAN]
        return {"pass": len(primaries) >= 1,
                "primary_citations": primaries,
                "reason": "PASS (primary-grounded)" if primaries else "FAIL (no primary-source citation)"}
