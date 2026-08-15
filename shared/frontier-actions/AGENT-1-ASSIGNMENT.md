# AGENT 1 (THIS LANE) — ASSIGNMENT: SCHOLAR + SERVING SURFACE (the guards)

*2026-08-15 · ASSIGNMENT doc for Agent 1 (this lane). I am Agent 1. My lane: the scholar + serving
surface — making the serve-time output HONEST via the enforcement guards. All responsibilities,
deliverables, and checkpoints are in this doc. I own this; Agent 2 has its own separate doc. We meet on
the shared gates. Read `shared/README.md` (the lane map) + `education-organism/FRONTIER-REVIEW.md` first.*

---

## MY LANE (what I own, what I do NOT)

| Own (Agent 1) | Do NOT touch (Agent 2's) |
|---|---|
| The serve-time surface guards (FoJin port) | The learning kernels (pyBKT, RKA, DML, dream-cycle) |
| `verify_quote` / citation enforcement | The learner-store legitimacy stack (graphiti/MKG/MemOS) |
| Answer-quality regression harness | The OpenEvolve retain-loop / flywheel |
| Retrieval rankers (GFM-RAG rankers, RoG path utils) | The measured-learning eval (B-F5) |
| SciFact review-gold + Storm generation | `kernels/misconception.py`, `pedagogy.py`, `memory.py` |
| Where I work: `/root/patalacheckpoints/pipeline/products/` + `mcp/index.mjs` + the UI | Where Agent 2 works: `/root/smellycock/education-organism/kernels/` |

**The rule:** I enforce *truth at serve-time* (no fabricated quotes/citations on the surface). Agent 2
proves *learning at eval-time*. No overlap.

---

## RESPONSIBILITIES (ordered by priority)

### R1 — `guard.py` kernel: verbatim-quote verifier (HIGH) ⭐
Port FoJin's `quote_verifier.py` mechanism (confirmed at
`/root/fuck-off/ecosystem/translation/fojin/backend/app/services/quote_verifier.py`, 602 lines) to Pāṭala
answers (L2/essay/education). Detect quoted spans + bounded citation gap; `_normalise` then substring-test
against the retrieved source; on a miss → **downgrade** (strip quote marks, still cite) — never serve a
false verbatim quote. Record `QuoteMutation` (reason, similarity, bucket) for telemetry. Measure
`near_miss (≥0.85)` vs `absent` via `_windowed_ratio`.

### R2 — `guard.py` kernel: citation whitelist backstop (HIGH) ⭐
Port FoJin's `citation_guard.py` (confirmed at
`/root/fuck-off/ecosystem/translation/fojin/backend/app/services/citation_guard.py`, 313 lines).
Whitelist = retrieved sources' `(title, juan)`; hallucinated title → stripped to bare form (no false
click-through); wrong fascicle → rewritten to closest real one. Every served citation resolves to a
retrieved source.

### R3 — `verify_quote` + retrieval rankers (MEDIUM) ⭐
- Add `verify_quote` (and `resolve_urn` surface) to `mcp/index.mjs` beside `resolve_ref` (fojin-mcp
  surface).
- Lift **GFM-RAG sparse entity→doc projection rankers** (`RManLuo_gfm-rag/gfmrag/models/gfm_rag_v1/
  rankers.py`, ~110 lines, dependency-free) + **RoG rule-constrained BFS + random-walk negative-path
  sampling** (`RManLuo_reasoning-on-graphs/src/utils/graph_utils.py`, networkx-only) into
  `research_packet`/graph-retrieval — go from "find paths" to "rank documents."

### R4 — answer-quality regression harness (MEDIUM)
Port FoJin's `fojin-eval-regression.sh` → a daily `run-gate.py` over our QA toolchain with baselines
(Recall@5, faithfulness). Use **SciFact** (`science/scifact`, SUPPORT/CONTRADICT/NEI gold, fetch via
`download-data.sh`) as independent review/quote-verifier gold. Wire into `run-tests.py`.

### R5 — wire guards into the live surface (MEDIUM)
Call `guard.py` from `serve-education.py` / `tutor-agent.py` at answer-time; keep `/resolve` provenance.
Consider **Storm** (`science/knowledge_storm`, pip-installable) as the essay/education *generation* engine
— it emits grounded citations that feed my verifier. This is a generation choice; adoption optional per
RAM.

---

## DELIVERABLES (concrete artifacts I ship)

| # | Deliverable | File / location |
|---|---|---|
| D1 | `guard.py` kernel (quote verifier + citation whitelist) | `patalacheckpoints/pipeline/products/guard/engine.py` (+ `test.py`) |
| D2 | `patala_verify_quote` MCP tool | `patalacheckpoints/mcp/index.mjs` |
| D3 | GFM-RAG rankers + RoG path utils lifted | `patalacheckpoints/pipeline/products/research_packet/engine.py` (upgrade) |
| D4 | `run-gate.py` answer-quality regression (SciFact gold) | `patalacheckpoints/pipeline/products/guard/` or scripts |
| D5 | guards wired into serve-education/tutor | `smellycock/education-organism/scripts/serve-education.py`, `tutor-agent.py` |
| D6 | `guard` registered in MANIFEST + docs | `smellycock/MANIFEST.json` + `domains/epistemic/README.md` |

---

## CHECKPOINTS (falsifiable — gate a deliverable done, not a file exists)

| Checkpoint | How I prove it | Status |
|---|---|---|
| **C1** (R1) | A fabricated quote served on the surface is **downgraded** (not served verbatim); a real quote is preserved; `count_checked_quotes ≠ 0` for a citation | pending |
| **C2** (R2) | A hallucinated citation is **corrected** (not served as-is); every served citation resolves to a retrieved source | pending |
| **C3** (R3) | `patala_verify_quote` returns the guard verdict for a real vs fabricated quote; `research_packet` now *ranks* docs (not just finds paths) | pending |
| **C4** (R4) | `run-gate.py` produces a baseline + pass/fail against SciFact gold; a quality regression blocks | pending |
| **C5** (R5) | Every served education/scholar answer passes the quote + citation guards (or is downgraded); gates stay green | pending |
| **C6** (ALL) | `check.py` PASS, `check_epistemic.py` PASS, `run-tests.py` 22/22, `test-e2e.py` 5/5 — all still green after my changes | pending |

**My gates (the shared invariants + my new guard gate):**
```bash
cd /root/smellycock
python3 check.py --status && python3 check_epistemic.py
cd education-organism && python3 scripts/run-tests.py   # 22/22
cd /root/patalacheckpoints && PYTHONPATH=pipeline python3 pipeline/products/guard/test.py | grep SUMMARY
```

**Banned words:** PROVED · TRUTH · CORRECT · BEST · WINS. **Use:** SUPPORTED BY · PASSED CHECK X ·
MACHINE-PROPOSED · REVIEWED BY.

---

## WHAT "DONE" MEANS FOR ME

The `UNANCHORED → reject` rule is **enforced, not designed**: a fabricated quote or citation on the
serving surface is downgraded or corrected at serve-time (C1, C2). My guard + verify_quote + rankers are
real, tested, and wired into the live surface. All shared gates green. Provenance moat untouched.

---

*This is Agent 1's assignment. I own the guards + serving surface + retrieval rankers. Agent 2 owns the
learning kernels + eval. We meet on the shared gates. Nothing is real without a checkpointed gate.*
