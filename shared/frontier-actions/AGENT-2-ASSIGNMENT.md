# AGENT 2 — ASSIGNMENT: ORGANISM + FLYWHEEL + DATA (the learning kernels)

*2026-08-15 · ASSIGNMENT doc for Agent 2 (the organism/flywheel lane). Agent 2 owns the learning kernels +
the measured-learning eval. All responsibilities, deliverables, and checkpoints are in this doc. Agent 1
has its own separate doc. We meet on the shared gates. Read `shared/README.md` (the lane map) +
`education-organism/FRONTIER-REVIEW.md` first.*

---

## YOUR LANE (what you own, what you do NOT)

| Own (Agent 2) | Do NOT touch (Agent 1's) |
|---|---|
| The learning kernels: pyBKT, RKA weighted, DML replay, dream-cycle | The serve-time guards (FoJin quote/citation port) |
| The **learner-store legitimacy stack** (graphiti + MKG + MemOS) | `verify_quote` / citation enforcement |
| The OpenEvolve retain-loop (flywheel evolutionary core) | Answer-quality regression harness |
| **The measured-learning eval** (the gap nothing covers) | GFM-RAG rankers / RoG path utils / SciFact |
| Where you work: `/root/smellycock/education-organism/kernels/` + `pipeline/products/education_organism/` | Where Agent 1 works: `/root/patalacheckpoints/pipeline/products/` + `mcp/index.mjs` |

**The rule:** Agent 1 enforces *truth at serve-time*. You prove *learning at eval-time* — a falsifiable
"did the learner actually learn" signal. No overlap.

---

## RESPONSIBILITIES (ordered by priority)

### R1 — adopt pyBKT for live mastery (HIGH)
Replace the hand-rolled BKT in `kernels/pedagogy.py` with **pyBKT** (confirmed at
`/root/fuck-off/ecosystem/learner-modeling/pyBKT`): `Model.fit/partial_fit/predict/evaluate/
crossvalidate` + `Roster.update_state()` (live per-learner mastery). MIT, numpy/sklearn.

### R2 — RKA weighted propagation (HIGH)
Adopt **infinitywings_rka** `_propagate` (`child = parent * edge_weight`) so `kernels/misconception.py`
`blast_radius` is weighted (derived_from=1.0, contradicts=1.1, cites=0.7). Confirmed at
`/root/fuck-off/ecosystem/infinitywings_rka`.

### R3 — DML deterministic replay + eigenius shape (HIGH)
Adopt **deterministic-memory-layer** `replay_to/compare_states/replay_excluding` in
`kernels/reconciliation.py`; emit eigenius `JustificationTerm` shape (`Verified ⊂ Derived ⊂ Observed ⊂
Declared`) for the ceiling. Confirmed at `/root/fuck-off/ecosystem/replay/deterministic-memory-layer` +
`eigenius_eigenius`.

### R4 — ⭐ THE LEARNER-STORE LEGITIMACY STACK (HIGH — the §8.1 build) ⭐
Three logic-only/schema-only lifts onto your existing store (no Neo4j, no GPU):
- **graphiti temporal model** (`getzep_graphiti/graphiti_core/edges.py`): `valid_at`/`invalid_at` +
  `episode_id` — a corrected misconception invalidates the old fact (`invalid_at=now`) WITHOUT deleting
  it. arXiv 2501.13956.
- **MKG 2-tier authority gate** (`neo4j-labs_meta-knowledge-graph/hooks/consistency_gate.py` +
  `server.py:1197/1258`): auto-gate (GENUINELY CONTRADICTS?/ALREADY LEARNED?) with conservative
  precedence; genuine ambiguity punted to a HUMAN stamped `reviewed_by='human'`.
- **MemOS feedback guards** (`MemTensor_MemOS/src/memos/mem_feedback/feedback.py`): LLM-emitted ids
  mapped back to real ids (`correct_item`), UPDATE > ADD, change-ratio guard downgrades update→add,
  old node ARCHIVED with `covered_history` link — never deleted.

### R5 — OpenEvolve retain-loop (the flywheel's evolutionary core) (MEDIUM)
Adopt the **generate→verify→retain-elite** pattern from
`evolution/openevolve/database.py` (`ProgramDatabase` MAP-Elites island grid + cascade evaluator +
checkpoint/resume). Replace the code-evaluator with YOUR verifier as the fitness. Token-heavy but
I/O-bound → fine on 8GB.

### R6 — ⭐ THE MEASURED-LEARNING EVAL (the gap nothing covers) (HIGH — must build) ⭐
**The single highest-value build in the whole frontier review.** A falsifiable learner-mastery eval: a
gold set of "this learner had misconception X, did/didn't repair" → blind BKT + misconception-repair
prediction → measured against real learning outcomes. Every clone gives storage + recall; none gives
mastery dynamics. Build it — this is exactly the anti-theatre doctrine.

---

## DELIVERABLES (concrete artifacts you ship)

| # | Deliverable | File / location |
|---|---|---|
| D1 | pyBKT-backed pedagogy | `smellycock/education-organism/kernels/pedagogy.py` (upgrade) |
| D2 | RKA weighted blast_radius | `smellycock/education-organism/kernels/misconception.py` (upgrade) |
| D3 | DML replay + eigenius shape | `smellycock/education-organism/kernels/reconciliation.py` (upgrade) |
| D4 | learner-store legitimacy stack (graphiti + MKG + MemOS) | `smellycock/education-organism/kernels/memory.py`, new `learner_store.py` |
| D5 | OpenEvolve retain-loop | `smellycock/education-organism/kernels/organism_loop.py` (upgrade) |
| D6 | **learner-mastery eval** (gold set + blind eval) | `smellycock/education-organism/kernels/learning_eval.py` + gold data |
| D7 | new gates wired | `run-tests.py` + `run-learning-eval.py` |
| D8 | registered in MANIFEST + docs | `smellycock/MANIFEST.json` + `domains/epistemic/README.md` |

---

## CHECKPOINTS (falsifiable — gate a deliverable done, not a file exists)

| Checkpoint | How you prove it | Status |
|---|---|---|
| **C1** (R1) | A mastery prediction is reproducible + cross-validated on real learner rows | pending |
| **C2** (R2) | A source change propagates with the right weights; a contradicts-edge outranks a cites-edge | pending |
| **C3** (R3) | A source-preserving replay PASSES; a source-dropping replay BLOCKS; the ceiling shape is enforced | pending |
| **C4** (R4) | A corrected misconception invalidates the old fact (`invalid_at=now`) WITHOUT deleting it; a genuinely-ambiguous correction is punted to a human stamped `reviewed_by='human'` | pending |
| **C5** (R5) | `organism_loop.py` retains elites over the MAP-Elites grid; the verifier is the fitness | pending |
| **C6** (R6) ⭐ | **The learner-mastery eval produces a real accuracy/dissolution metric on a gold set — not a synthetic hand-feed. If the learner didn't actually learn, the eval says so.** | pending |
| **C7** (ALL) | `check.py` PASS, `check_epistemic.py` PASS, `run-tests.py` 22/22, `test-e2e.py` 5/5 — all still green after your changes | pending |

**Your gates (the shared invariants + your new learning gate):**
```bash
cd /root/smellycock
python3 check.py --status && python3 check_epistemic.py
cd education-organism && python3 scripts/run-tests.py   # 22/22
python3 scripts/run-learning-eval.py                    # learner-mastery on the gold set (new)
```

**Banned words:** PROVED · TRUTH · CORRECT · BEST · WINS. **Use:** SUPPORTED BY · PASSED CHECK X ·
MACHINE-PROPOSED · REVIEWED BY.

---

## WHAT "DONE" MEANS FOR YOU

The flywheel is **measured, not just storage**: real learner interactions flow into pyBKT mastery +
RKA-weighted misconception cascade + the learner-store legitimacy stack (time-bounded, authority-gated,
correction-safe). The **learner-mastery eval** reports a real, falsifiable metric (C6) — the gap nothing
in the frontier covers. All shared gates green. Provenance moat untouched.

---

*This is Agent 2's assignment. You own the learning kernels + eval. Agent 1 owns the guards + serving
surface. We meet on the shared gates. Nothing is real without a checkpointed gate.*
