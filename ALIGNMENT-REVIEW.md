# ALIGNMENT REVIEW — the merged two-lane repo (2026-08-15)

*A critical review of `prx0r/smellycock` after merging both lanes: the translation lane (agentgraph) +
the epistemic/education/post-C1 lane (the other agents on server2). Is it aligned? Where are the gaps?
This is the honest cross-lane audit before the next agent integrates further.*

---

## 1. WHAT'S IN THE MERGED REPO (both lanes)
| Lane | Domains | Runs | Code location |
|---|---|---|---|
| **Translation (us)** | `domains/translation`, `factory`, `read-plane`, `openpatala` | `live-run-1..5`, `experiments`, `BRAINSTORM-*` | `/root/projects/patala` + `ip-graph/scripts` |
| **Post-C1 (them)** | `domains/post-c1`, `domains/epistemic` (products, validation, agentic, GENIUS-PINCHES, compatibility-matrix) | `education-organism-run-4`, `server2-post-c1-spine` | **server2** (only pointers + docs here) |

## 2. IS IT ALIGNED? — the honest verdict
**Mostly aligned, with real gaps.**
### ✅ Aligned
- **The ONE RULE + AXIOMS are shared** by both lanes (the doc that opens every domain repeats them).
- **The DAG matches:** `OBJECT-MODEL.md` names `…→theme/argument→synthesis→essay→lesson(education)`, and
  `domains/post-c1` implements exactly that. The seam is correct: **we produce C1, they build above it.**
- **Both use deterministic gates + Hermes.** Their post-c1 claims gates (Nyāya, cite-contract, quality,
  blind-assessor, tension) + Hermes-kanban driving — the same philosophy as our E2E testing.
- **check.py PASSES** (exit 0) after reconciling cross-server paths.

### ⚠️ Gaps / misalignments (the real issues)
1. **`domains/post-c1` is NOT in the MANIFEST** — it's unregistered + unvalidated by `check.py`. (The
   epistemic domain IS registered; post-c1 is not.)
2. **Cross-server dependency:** the post-c1 + epistemic PRODUCTS live on **server2**, not this box — here
   there are only docs + pointers (`pipeline/products/README.md`, `runs/server2-post-c1-spine/`). So the
   post-c1 build CANNOT be run/validated here yet.
3. **No unified full-stack E2E:** our `test_full_chain_timing.py` proves RAW→C1 on this box; their
   C1→ESSAY build is on server2. There is **no single RAW→ESSAY test** that spans both lanes end-to-end.
4. **Separate run sets:** ours (`live-run-1..5`) vs theirs (`education-organism-run-4`,
   `server2-post-c1-spine`) are not connected into one progression.
5. **No cross-lane gold/human gate:** neither lane has independently-reviewed, human-adjudicated output
   yet (AGENTS.md ONE RULE — nothing is "real" until gold + blind eval + human adjudication).

---

## 3. THE INTEGRATION PLAN FOR THE NEXT AGENT (grounded in AXIOMS + the formal E2E + Hermes/kanban)

### Step 1 — Register `domains/post-c1` (make it validated, per AXIOMS: one concern = one MANIFEST entry + a validator)
- Add `domains/post-c1/*` to `MANIFEST.json` (id/owner/validator).
- Confirm `check.py` passes with it registered.

### Step 2 — Reconcile the cross-server reality (AXIOMS: docs are a projection; the truth is executable)
- The post-c1/epistemic products live on server2. The next agent must either:
  (a) **pull the products onto this box** (or clone server2) so they're runnable/validated here, OR
  (b) mark post-c1/epistemic honestly as `server2-deployed` (not claim they run here).
- Do NOT fabricate a local run of server2 products.

### Step 3 — Build the unified full-stack E2E (the formal test, extended across both lanes)
- Extend `test_full_chain_timing.py` (our RAW→C1 E2E) to ALSO drive the post-c1 spine (C1→THEME→ARGUMENT→
  SYNTHESIS→ESSAY→LESSON) via the other agents' Hermes-kanban + gates — producing ONE
  **RAW→LESSON(EDUCATION)** repeatable test.
- Each layer keeps a deterministic gate + per-layer time + api-call count (the formal method we used).
- The gate: a single repeatable command that runs a raw verse ALL the way to a validated lesson.

### Step 4 — Hermes/kanban drives it (the autonomous integration)
- Create a **kanban board** for the full stack (one card per layer per work, RAW→EDUCATION).
- Wire Hermes (via the `patala` profile + the MCP verbs + skills) to claim cards, run the layer's
  generation (batched, context-loaded once), verify with the deterministic gate, commit + mark done.
- Use the existing watchdog/build-plan pattern (`build_plan.py`) so the integration is enforced + tracked.

### Step 5 — Close the gold/human gate (AGENTS.md ONE RULE — the final "real" test)
- Add the semantic gold scorer (embeddings/LLM-as-judge, not Jaccard) across the full RAW→EDUCATION chain.
- Wire `human_authorize()` as the promotion gate on committed objects (only humans promote to canonical).

### Step 6 — The live benchmark dashboard (make progress measurable + public)
- Wire per-work: layers done (RAW→EDUCATION), time, api-calls, the exact method, and the
  `trace_object.py` RAW→EDUCATION proof — served by openpatala.

---

## 4. THE HONEST BOTTOM LINE
> **The two lanes are architecturally aligned (same ONE RULE, AXIOMS, DAG, deterministic gates, Hermes),
> but they are not yet integrated into ONE runnable system: post-c1 isn't in the MANIFEST, its products
> live on server2 (not this box), and there is no unified RAW→EDUCATION E2E. The next agent's job is:
> register post-c1, reconcile the server2 reality, build the one RAW→EDUCATION E2E, drive it with
> Hermes/kanban, add the semantic gold + human gate, and surface a live benchmark.**

*This is the honest cross-lane review. Read `FLAWS.md` + `HANDOVER-NEXT-AGENT.md` for the deeper counter-
evidence and the prioritized plan.*
