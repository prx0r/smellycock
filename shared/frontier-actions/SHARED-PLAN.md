# SHARED — the seam between the two lanes (the frontier-action plan)

*2026-08-15. This is the coordination folder BOTH lanes read before building. It turns the
`education-organism/FRONTIER-REVIEW.md` gap analysis into concrete, non-overlapping work split across
the two lanes, with the shared seam, the verified assets, and the gates. Both lanes own their lane; this
folder is the shared map — no agent rebuilds the other's lane, no agent breaks the shared gates.*

---

## 0. WHO IS WHO (the lane split — read this first)

| Lane | Repo / ownership | Owns (the frontier-action scope) |
|---|---|---|
| **Agent A (this lane) — SCHOLAR + SERVING SURFACE** | `/root/patalacheckpoints/pipeline/products/` (the `scholar_*`, `review_*`, `manuscript_*`, `collation` engines) + the MCP + the UI | the **guards** (FoJin port) + the **verification enforcement** + the **serve-time surface** |
| **Agent B — ORGANISM + FLYWHEEL + DATA** | `/root/smellycock/education-organism/kernels/` + `pipeline/products/education_organism/` | the **learning kernels** (pyBKT, RKA, DML) + the **measured-learning eval** |

**The rule of the seam:** Agent A enforces *truth at serve-time* (no fabricated quotes/citations on the
surface); Agent B proves *learning at eval-time* (a falsifiable "did the learner actually learn" signal).
Neither overlaps the other.

---

## 1. THE VERIFIED BASELINE (re-ran this session — do not trust, verify)

| Gate | Result |
|---|---|
| `smellycock/check.py --status` | PASS |
| `smellycock/check_epistemic.py` | PASS (25 products, 8 layers) |
| `smellycock/education-organism/scripts/run-tests.py` | 22/22 |
| `smellycock/education-organism/scripts/test-e2e.py` | 5/5 |
| `smellycock/education-organism/scripts/audit-resolve.py` | resolves to SOURCE |
| `patalacheckpoints` scholar engines | scholar_identity 7/7 · review_policy 7/7 · scholar_vertical 5/5 · scholar_publication 5/5 · review_queue 6/6 · review_workbench 6/6 · scholar_review 11/11 |

All frontier assets the review cites are **cloned and verified present** at
`/root/fuck-off/ecosystem/`:
`translation/fojin` (40M, 685 py) · `learner-modeling/pyBKT` · `retrieval/PathRAG` ·
`OSU-NLP-Group_HippoRAG` · `agent-memory/evolving-memory` · `infinitywings_rka` ·
`replay/deterministic-memory-layer` · `eigenius_eigenius`.
FoJin's two crown jewels confirmed: `fojin/backend/app/services/quote_verifier.py` (602 lines) +
`citation_guard.py` (313 lines).

---

## 2. AGENT A (THIS LANE) — THE SURFACE GUARDS + VERIFICATION ENFORCEMENT

**Job: make the serve-time surface honest.** Our rule "UNANCHORED → reject" is *designed, not enforced*.
FoJin proves the enforcement is buildable. Port the mechanism, keep our provenance moat.

### A-F1 — `guard.py` kernel: verbatim-quote verifier (HIGH) ⭐
Port FoJin's `quote_verifier.py` mechanism to Pāṭala answers (L2/essay/education).
- Detect quoted spans + a bounded citation gap; `_normalise` (NFKC + strip-punct + lowercase) then
  substring-test against the retrieved source.
- On a miss → **downgrade** (strip quote marks → honest prose, still cites), never serve a false verbatim
  quote. Record a `QuoteMutation` (reason, similarity, bucket) for telemetry.
- Measure, not just pass/fail: `_windowed_ratio` buckets `near_miss (≥0.85)` vs `absent`.
- **CHECKPOINT:** a fabricated quote on the serve surface is downgraded (not served verbatim); a real
  quote is preserved; `count_checked_quotes` ≠ 0 for a citation.

### A-F2 — `guard.py` kernel: citation whitelist backstop (HIGH) ⭐
Port FoJin's `citation_guard.py`: whitelist = retrieved sources' `(title, juan)`.
- Hallucinated title → stripped to bare form (no false click-through); wrong fascicle → rewritten to the
  closest real one.
- **CHECKPOINT:** a hallucinated citation is corrected (not served as-is); every served citation resolves
  to a retrieved source.

### A-F3 — `verify_quote` MCP verb (MEDIUM)
Add `verify_quote` (and `resolve_urn` surface) to `mcp/index.mjs` beside `resolve_ref`, per FoJin's
`fojin-mcp` tool surface.
- **CHECKPOINT:** the MCP server exposes `patala_verify_quote`; it returns the guard verdict for a
  real vs fabricated quote.

### A-F4 — gated answer-quality regression harness (MEDIUM)
Port FoJin's `fojin-eval-regression.sh` → a daily `run-gate.py` over our QA toolchain with baselines
(Recall@5, faithfulness), wired to `run-tests.py`.
- **CHECKPOINT:** a regression run produces a baseline + a pass/fail; a quality regression blocks.

### A-F5 — wire guards into the live surface (MEDIUM)
Call `guard.py` from `serve-education.py` / `tutor-agent.py` at answer-time; keep the `/resolve`
provenance endpoint.
- **CHECKPOINT:** every served education/scholar answer passes the quote + citation guards (or is
  downgraded); gates stay green.

---

## 3. AGENT B — THE LEARNING KERNELS + THE MEASURED-LEARNING EVAL

**Job: make the flywheel *measured*, not just storage.** Every cloned repo gives storage + recall; NONE
gives a falsifiable "did the learner actually learn" signal. That is the anti-theatre gap — build it.

### B-F1 — adopt pyBKT for live mastery (HIGH)
Replace the hand-rolled BKT in `kernels/pedagogy.py` with `pyBKT Model.fit/partial_fit/predict/
evaluate/crossvalidate` + `Roster.update_state()` (live per-learner mastery).
- **CHECKPOINT:** a mastery prediction is reproducible + cross-validated on real learner rows.

### B-F2 — RKA weighted propagation (HIGH)
Adopt `infinitywings_rka/_propagate` (`child = parent * edge_weight`) so `kernels/misconception.py`
`blast_radius` is **weighted** (derived_from=1.0, contradicts=1.1, cites=0.7).
- **CHECKPOINT:** a source change propagates with the right weights; a contradicts-edge outranks a cites-edge.

### B-F3 — deterministic replay + justification shape (HIGH)
Adopt DML `replay_to/compare_states/replay_excluding` in `kernels/reconciliation.py`; emit eigenius
`JustificationTerm` shape (`Verified ⊂ Derived ⊂ Observed ⊂ Declared`) for the ceiling.
- **CHECKPOINT:** a source-preserving replay PASSES; a source-dropping replay BLOCKS; the ceiling
  shape is enforced.

### B-F4 — dream-cycle + skill files (MEDIUM)
Adopt `evolving-memory` dream cycle (SWS→REM→Consolidation→Compaction) + EverOS markdown-versionable
skill files for `organism_loop.py` + `memory.py`.
- **CHECKPOINT:** after ≥2 sessions, the tutor targets the weakest skill from history (from the learner DB).

### B-F5 — ⭐ THE GAP NOTHING COVERS: learner-mastery eval (HIGH — must build) ⭐
**The single highest-value build in the whole frontier review.** A falsifiable learner-mastery eval:
a gold set of "this learner had misconception X, did/didn't repair" → blind BKT + misconception-repair
prediction → measured against real learning outcomes.
- **CHECKPOINT:** the eval produces a real accuracy/dissolution metric on a gold set — not a synthetic
  hand-feed. If the learner didn't actually learn, the eval says so.

---

## 4. THE SEAM (the shared gates — both lanes keep green)

```bash
# THE shared invariants (run by either lane before claiming done)
cd /root/smellycock
python3 check.py --status            # refs resolve
python3 check_epistemic.py           # products reconcile
cd education-organism
python3 scripts/run-tests.py         # 22/22
python3 scripts/test-e2e.py          # 5/5
python3 scripts/audit-resolve.py     # claim → source

# Agent A's new guard gate (after A-F1/F2)
python3 scripts/run-guard-tests.py   # quote + citation guards (new)

# Agent B's new learning gate (after B-F5)
python3 scripts/run-learning-eval.py # learner-mastery on the gold set (new)
```

**Banned words:** PROVED · TRUTH · CORRECT · BEST · WINS. **Use:** SUPPORTED BY · PASSED CHECK X ·
MACHINE-PROPOSED · REVIEWED BY.

---

## 5. THE DEFINITION OF DONE (the next milestone — falsifiable)

1. **Agent A:** a fabricated quote OR citation served on the education/scholar surface is **downgraded or
   corrected at serve-time** (A-F1/F2 checkpoints) — the UNANCHORED→reject rule is now *enforced*, not
   designed.
2. **Agent B:** a real learner's interactions flow into the pyBKT mastery model + RKA-weighted
   misconception cascade, and the **learner-mastery eval** reports a real, falsifiable metric (B-F5
   checkpoint) — the gap nothing in the frontier covers.
3. Both lanes' shared gates stay green; every new object resolves to source.

---

*This is the shared frontier-action plan. Agent A owns the surface guards + verification enforcement
(FoJin port, keeping our provenance); Agent B owns the learning kernels + the measured-learning eval
(the gap no clone covers). They meet on the shared gates. Nothing is real without a checkpointed gate.*
