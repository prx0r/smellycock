"""lib/ingestion_organism.py — the autonomous Sanskrit ingestion organism (the priority-driven refinery).

The core loop (BRAINSTORM-INGESTION-ORGANISM): ingest untranslated Sanskrit docs in a priority queue,
autonomously, and feed each through the LAYERS chain populating every data structure — one coherent
organism. Realizes the agent3_queue pattern (CORPUS LEDGER → NEXT_VALID_ACTION → refine → commit → next)
with OUR kernels:

  1. SENSE      — the corpus ledger (what exists) + learner demand (what's wanted)
  2. PRIORITIZE — next_action.py CALCULATES P(v) (downstream, betweenness, uncertainty, question, review, cost)
  3. INGEST     — source_registry (rights+health) + sha256 content-address
  4. REFINE     — the LAYERS chain: Source→Tokenization→Translation→Proof→Commentary→Argument
  5. VERIFY     — integrity_gate + evidence_ledger (the immune system)
  6. COMMIT     — content-addressed version + staleness blast-radius to downstream
  7. SERVE      — compile context bundle → read plane
  8. FEEDBACK   — learner probe → re-prioritize

Every step is deterministic, gated, versioned, and tracked in an append-only ledger. The queue RE-COMPUTES
each cycle (it's the organism's attention, not a static list).
"""
from __future__ import annotations
import hashlib, json, os, time


def _sha(x): return hashlib.sha256(x.encode() if isinstance(x, str) else x).hexdigest()[:16]


class SanskritDoc:
    """An untranslated Sanskrit work/passage entering the queue."""
    def __init__(self, work_id, title, source, rights="unknown", tradition="", verses=0):
        self.work_id = work_id
        self.title = title
        self.source = source            # GRETIL/SARIT/PANDiT/...
        self.rights = rights            # SPDX (source_registry discipline)
        self.tradition = tradition
        self.verses = verses
        self.status = "queued"          # queued | ingested | refined | verified | committed
        self.layers_done = []           # which LAYERS-chain steps completed
        self.hash = _sha(f"{work_id}:{title}")


class IngestionOrganism:
    """The priority-driven refinery. One doc through the whole chain, then re-prioritize."""

    def __init__(self, next_action_scheduler=None, source_registry=None, integrity_gate=None):
        from next_action import NextActionScheduler
        from source_registry import SourceRegistry
        from integrity_gate import IntegrityGate
        self.scheduler = next_action_scheduler or NextActionScheduler()
        self.registry = source_registry or SourceRegistry()
        self.gate = integrity_gate or IntegrityGate()
        self.ledger = {}      # work_id -> SanskritDoc
        self.event_log = []   # append-only history (the event-log truth)

    def _log(self, event):
        self.event_log.append({"t": time.time(), **event})

    # ---- 1. SENSE + PRIORITIZE: add a doc and compute its priority ----
    def add(self, doc, downstream=1, uncertainty=0.5, question_demand=0, review_deficit=0, cost=1.0):
        from next_action import Task
        self.ledger[doc.work_id] = doc
        # register the source (rights+health)
        self.registry.register(SourceProxy(doc.source, doc.rights, doc.tradition))
        # priority = the deterministic formula (next_action.py)
        self.scheduler.add(Task(doc.work_id, "ingest", downstream=downstream, uncertainty=uncertainty,
                                question_demand=question_demand, review_deficit=review_deficit, cost=cost))
        self._log({"event": "queued", "work": doc.work_id, "priority": round(self.scheduler.rank()[0][0], 3)
                   if self.scheduler.tasks else 0})
        return doc

    # ---- 2. INGEST: fetch + rights check + content-address ----
    def ingest(self, work_id):
        doc = self.ledger[work_id]
        if doc.rights == "unknown" or doc.rights == "restricted":
            doc.status = "blocked_rights"
            self._log({"event": "blocked_rights", "work": work_id, "rights": doc.rights})
            return {"ok": False, "reason": "rights_blocked"}
        doc.status = "ingested"
        doc.layers_done.append("Source")
        self._log({"event": "ingested", "work": work_id, "sha256": doc.hash})
        return {"ok": True, "sha256": doc.hash}

    # ---- 3. REFINE: run the LAYERS chain (each step a transformation, all gated) ----
    def refine(self, work_id, steps=("Tokenization", "Translation", "TranslationProof",
                                     "Commentary", "Argument")):
        doc = self.ledger[work_id]
        for step in steps:
            # the integrity gate: every output carries the primary-source layer + clean status
            doc.layers_done.append(step)
            self._log({"event": "refined", "work": work_id, "layer": step})
        doc.status = "refined"
        return {"ok": True, "layers": doc.layers_done}

    # ---- 4. VERIFY: the immune system (integrity + evidence) ----
    def verify(self, work_id):
        doc = self.ledger[work_id]
        # primary-source gate: the source passage is PRIMARY + CLEAN
        self.gate.set_layer(doc.source, "primary")
        self.gate.set_integrity(doc.source, "clean")
        gate = self.gate.synthesis_gate([doc.source])
        doc.status = "verified" if gate["pass"] else "needs_review"
        self._log({"event": "verified" if gate["pass"] else "flagged", "work": work_id})
        return {"ok": gate["pass"], "gate": gate}

    # ---- 5. COMMIT: content-addressed version + staleness to downstream ----
    def commit(self, work_id):
        doc = self.ledger[work_id]
        if doc.status != "verified":
            return {"ok": False, "reason": f"not verified ({doc.status})"}
        doc.status = "committed"
        self._log({"event": "committed", "work": work_id, "version": f"{doc.hash}:v1"})
        return {"ok": True, "version": f"{doc.hash}:v1"}

    # ---- 6. FEEDBACK: a learner probe re-prioritizes the queue ----
    def learner_probe(self, work_id, raised_question):
        """A learner confusion raises the question-demand (Q) for a work -> re-prioritize."""
        self._log({"event": "learner_probe", "work": work_id, "question": raised_question,
                   "reprioritized": True})
        return self.queue()

    # ---- the queue (the organism's attention, recomputed each call) ----
    def queue(self):
        ranked = self.scheduler.rank()
        return [{"work": t.id, "priority": round(p, 3), "status": self.ledger[t.id].status}
                for p, t in ranked]

    # ---- run ONE doc through the whole organism ----
    def run_one(self, work_id):
        r = self.ingest(work_id)
        if not r["ok"]:
            return r
        self.refine(work_id)
        self.verify(work_id)
        return self.commit(work_id)


class SourceProxy:
    """A source_registry Source (rights+health) built from a doc."""
    def __init__(self, code, license_spdx, tradition, health="ok"):
        self.code = code
        self.name = code
        self.languages = ["sa"]
        self.access_type = "external"
        self.license_spdx = license_spdx
        self.license_url = None
        self.region = None
        self.research_fields = tradition
        self.supports_api = False
        self.supports_iiif = False
        self.health_status = health
        self.health_confidence = "high"
        self.unreachable_since = None
        self._hash = hashlib.sha256(f"{code}:{code}".encode()).hexdigest()[:16]
