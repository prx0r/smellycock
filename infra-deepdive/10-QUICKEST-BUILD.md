# QUICKEST BUILD — the fastest path from "BS" to "REAL" (for agents + humans)

*2026-08-15 · the minimal, gated critical path to make the claimed stack real. Dense by design (AXIOM 8:
agent-speed, no prose walls; perf doctrine: compute-on-write, one-request, incremental — never a full
rebuild). Each step is fast, gated, and logged-run evidenced. Do them in order; a step is DONE only when
its gate passes.*

---

## THE FASTEST CRITICAL PATH (to first REAL RAW→EDUCATION object)

| # | Step (agent-action) | Human-reason | Gate (fast check) | Est. |
|---|---|---|---|---|
| **0** | **Fix the gamed validators** — post-C1 commits bypass gates (hardcoded `ENGINEERING_VALIDATED`); ARGUMENT quality gate reads the wrong key | the BS is stored because the gates don't check content | a single-word EDUCATION + quality-0 ARGUMENT are REJECTED by the layer validator | <1h |
| **1** | **Archive the garbage** — supersede the 11 BS post-C1 objects (1 THEME, 10 ARGUMENT) + the vacuous `p51-synthesis` PASS; mark NOT-REAL | no claimed layer is trusted unless evidenced | registry has no object that fails its own gate | <30m |
| **2** | **Verse recovery (P0)** — wire `harvest_to_factory` + `register_harvest_sources` so every SOURCE carries `payload.verse` | empty-SOURCE works (tantraloka, 100-work sivaqueue) are blocked | `_verse_for(anypassage)` returns a real verse for every queued work | ~2-3h |
| **3** | **Semantic gold scorer** — embeddings/LLM-as-judge, not Jaccard 0.091 | "it works" must be measurable on real golds | committed T1/L2/C1 score > threshold vs the kārikā golds | ~2-3h |
| **4** | **Wire the human + promotion gate** — `review_engine`/`human_authorize` → registry (machine proposes, human promotes) | THE ONE RULE: nothing is "real" without human adjudication | a promoted (non-GENERATED) object via a persisted ReviewEvent | ~1-2h |
| **5** | **Emit result lineage** — `result_id/benchmark_version/gold_version/model_version/code_commit/split/seed/config/date` on every served + traced object | a consumer can tell which gold/model/code produced a result | a served/traced result resolves full lineage | ~1h |
| **6** | **One RAW→EDUCATION E2E on REAL output** — extend `test_full_chain_timing` + `trace_object` (hash-chain integrity, not presence) | the single command that proves a verse → a validated lesson | `trace_object` asserts hash-chain integrity to RAW, exit 0, on real output | ~2-3h |
| **7** | **Live benchmark + openpatala** — serve per-work layers/time/calls/method/proof/lineage; `GET /benchmarks/{work}` + incremental read-plane build | progress is public + queryable | a new work appears in the ledger + read-plane WITHOUT a full rebuild | ~1-2h |

**Total to first REAL RAW→EDUCATION object: ~10-14h of focused work.** Then the post-C1 rebuild (C1-C2:
THEME→ESSAY→EDUCATION on REAL gold-scored C1 with real gates) can proceed on real foundation — it is the
SLOWEST step, so it comes last / can be delegated to the other agent.

---

## WHY THIS ORDER (leverage-first, perf-doctrine)
1. **Steps 0-1 kill the BS first** (cheap, stops trusting garbage — nothing after is built on sand).
2. **Step 2 unblocks all data** (the biggest enabler; empty SOURCE blocks everything downstream).
3. **Steps 3-5 make "real" measurable + auditable** (gold + human + lineage = THE ONE RULE closed).
4. **Steps 6-7 prove it + surface it** (the logged-run E2E + incremental read-plane — no full rebuild, per the build budget).
5. The post-C1 scholarship rebuild is deferred until C1 is itself real — otherwise we rebuild BS on BS.

## THE TWO-SPEED RULE (agents + humans)
- **Agents** run this table top-to-bottom, `MANIFEST.json` as the resolver, each gate a single command. No prose walls — the table IS the spec.
- **Humans** see the "Human-reason" column + a live `GET /benchmarks/{work}` — progress they can read, not doc claims.

## THE ONE-LINE
> **Kill the BS (fix gates + archive garbage) → unblock data (verse recovery) → make real measurable
> (gold + human + lineage) → prove it (RAW→EDUCATION E2E + live benchmark) — ~10-14h to the first real,
> evidenced, human-signed RAW→EDUCATION object.**

*Sources: AXIOMS (esp. #3 deterministic, #7 RAM-scarce, #8 agent-speed), performance/README.md (10-rule
doctrine + budgets), `09-MAKE-IT-NOT-BS-PLAN.md`, `06-PEER-REVIEW-FRONTIER.md`, `08-CANONICAL-ASSESS-FLOW.md`,
RED-TEAM-REVIEW.md, `/tmp/opencode/e2e-trace.json`.*
