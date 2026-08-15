# ORGANISM — CROSS-REPO REVIEW (all organism files, 2026-08-15)

*A complete review of every organism-related file across serveragent3, fuck-off (ip-graph),
patalacheckpoints, and smellycock. What's real, what's validated, what's missing — and what my
serveragent3 build got wrong.*

---

## THE ONE PICTURE (the organism's circulatory system)

```
INGEST (food): Sanskrit → SOURCE → Tokenization → DraftTranslation → Translation →
  TranslationProof → Commentary → Argument → Synthesis
        │
EPISTEMIC GATE (immune system): epistemic · review · scholar_review · evidence_ledger ·
  integrity_gate · verification_ensemble
        │
READ PLANE (serve): context bundles → Astro/JSON-LD (humans) · bundles/MCP (agents)
        │
ORGANISM LOOP (the senses): consumers probe → MisconceptionGraph → confusion=research signal
  → next_action → DeliveryLoop (budget+human gate) → source-repair → RKA propagate
        │
SELF-PROVE + SIGN (Vision F): system_provenance · certificate · signed Merkle root
```

**The one law that makes it an organism, not a database:** *learners are sensors* (SPEC-21). Their
attempts to understand become measurements of the research object itself.

---

## WHAT'S REAL + VALIDATED (fuck-off/lib — the canonical machinery)

| Kernel | What it does | Validator |
|---|---|---|
| `organism.py` | UserKnowledgeState (learner profiles) + MisconceptionGraph (demand: Confusion misreads Claim · Objection attacks Premise · Question about Concept) | 9/9 |
| `organism_loop.py` | the **10-stage consumer→research machine**: interaction → normalize → link → cluster → gap detect → intervention → measure → GraphProposal → verify → human gate | 8/8 |
| `ingestion_organism.py` | the priority-driven refinery: sense → prioritize (next_action formula) → ingest → refine → verify → commit → learner-probe feedback | 10/10 |
| `misconception.py` | **the repair cascade** (the flywheel's closing edge): MisconceptionLikelihood = f(cluster, persistence, ambiguity, novice) → flag source → RKA propagate fix → measure dissolve | 9/9 |
| `education.py` + `pedagogy.py` | LearningClaim, MasteryEvidence, compile_interactions (interaction compiler), wrong_answer_to_neighbor (the moat), BKT mastery | 9/9 + 7/7 |
| `organism_factory_bridge.py` | routes the organism through the factory scheduler | 2/3 (cross-machine) |

**All validators pass** except the factory-bridge (only the cross-machine `/mnt/HC_Volume_106427611/ip-graph` (the agentgraph box) path).

**Stale doc:** `ORGANISM-OPERATING-MODEL.md` calls `misconception.py` "the biggest unbuilt gap" — but
the kernel IS built (9/9). The doc predates the build.

---

## THE CO-EVOLVING FLYWHEEL (the deepest moat — SPEC-21/23)

```
SCHOLARSHIP → LearningClaims → learners → misconceptions (structured)
     ↑                                            ↓
  source-repair ← scholar review ← ambiguity flagged by confusion cluster
```

- **The learner population is a distributed sensor network over the scholarly graph.** A confusion
  recurring across thousands of learners is evidence of an ambiguity in the SOURCE object.
- **The misconception graph is the rarest moat**: unscrapeable (competitors can't copy years of "where
  humans actually fail"), self-improving (every learner improves the scholarship), and feeds back into
  the source.

---

## MY serveragent3 ORGANISM — what it got wrong

`serveragent3/kernels/organism.py` **duplicates** `fuck-off/lib/organism.py` (UserKnowledgeState +
MisconceptionGraph copy-pasted) and adds a `ConsumerSensor`, but it is **MISSING**:

| Missing | Why it matters |
|---|---|
| **The 10-stage OrganismLoop** (`organism_loop.py`) | the actual consumer→research machine (question→gap→proposal→human-gate) |
| **The misconception → source-repair cascade** (`misconception.py`) | the flywheel's CLOSING EDGE — without it, the loop is open, not an organism |
| **The pedagogy/BKT mastery policy** | next_interaction targeting the weakest skill |
| **the ingestion organism** | the priority-driven refinery (sense→commit→feedback) |
| **RKA staleness propagation** | a source change must flag every dependent explanation stale |

**Verdict:** my serveragent3 organism is a partial duplicate of the canonical machinery, missing the
actual loops that make it an organism. I should INTEGRATE the validated fuck-off/lib kernels (reuse,
don't rebuild — the axiom) rather than maintain a copy.

---

## WHAT TO INTEGRATE (the fix)

1. **Reuse `fuck-off/lib/organism_loop.py`** as the consumer→research machine in serveragent3.
2. **Reuse `fuck-off/lib/misconception.py`** (the repair cascade) — closes the flywheel.
3. **Reuse `fuck-off/lib/pedagogy.py`** (BKT mastery + next_interaction).
4. **Wire the closed loop end-to-end**: learners → misconceptions → flag source → scholar repair →
   RKA propagate → dissolve → better teaching → more learners.
5. Delete the duplicated `serveragent3/kernels/organism.py` in favor of importing the canonical kernel.

**The honest gap (unchanged):** no real consumer/learner data yet — the misconception flywheel's fuel is
prospective. But the MACHINERY is real and validated; the next step is wiring it into one closed,
tested loop on the real gold C1s.
