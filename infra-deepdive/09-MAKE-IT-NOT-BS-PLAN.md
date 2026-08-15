# MAKE-IT-NOT-BS — the master plan to make the claimed stack REAL (supersedes + aligns handover/dev-plan)

*2026-08-15 · the docs claim "all the way up to essays/education." The evidence says otherwise. This plan
makes it not BS. It supersedes `HANDOVER-NEXT-AGENT.md` + `DEV-PLAN-NEXT-AGENT.md` by fixing their one
critical misalignment (they trust the post-C1 lane) and adding what they lack (garbage remediation, an
explicit verse-recovery phase, and the acquisition front). Everything is gated per AXIOMS; the evidence
standard is the confirmed logged run (RAW→C1 412s/3 calls, `chain_ok:true`).*

---

## 1. THE HONEST VERDICT (why it's BS, from evidence + the other agents' OWN red-team)
| Claim | Evidence |
|---|---|
| "post-C1 built to essays/education" | SYNTHESIS=**0**, ESSAY=**0**, EDUCATION=**0** committed objects; THEME=1, ARGUMENT=10 |
| "gated, production-grade" | RED-TEAM-REVIEW: all 10 post-C1 objects `ENGINEERING_VALIDATED` with **no gate** (hardcoded); EDUCATION = `{"EDUCATION":"Postgraduate"}` (single-word garbage); ARGUMENT quality **0.0→BLOCK** (gate reads wrong key); SYNTHESIS `input_refs` violates the DAG |
| "RAW→C1 works" | ✅ **TRUE — the only non-BS part**: logged run 412s/3 calls/7 layers/`chain_ok:true`, 76 C1 committed |

**Our job: keep the REAL (RAW→C1 + the mechanism), and rebuild/delete the BS (garbage post-C1 objects, vacuous gates) so every claimed layer is evidenced.**

---

## 2. THE MASTER PLAN (the priority order — every step gated, evidence-standard)

### PHASE A — STOP THE BS (remediation first; nothing "real" is trusted)
| # | Task | Gate |
|---|---|---|
| A1 | **Hard-fix the validators so they cannot be gamed.** The post-C1 commits bypass gates (`status=R.ENGINEERING_VALIDATED` hardcoded); the ARGUMENT quality gate reads the wrong payload key → fix it to score 0.0→BLOCK correctly. Every layer must gate on real content, not presence. | every layer's validator rejects garbage (single-word EDUCATION, quality-0 ARGUMENT) |
| A2 | **Archive the BS, don't present it as real.** Supersede/archive the 11 garbage post-C1 objects (1 THEME, 10 ARGUMENT) + the vacuous `p51-synthesis` "PASS". Mark them `NOT-REAL/garbage` per the status ladders. | the registries contain no object that fails its own gate |
| A3 | **Make the post-C1 gates real code.** `blind-assessor`, `cite-contract`, `tension` do not exist as code (DEV-PLAN Phase 1.1 assumed them). Build them or drop the claim. | each named post-C1 gate exists + fails-closed on garbage |

### PHASE B — MAKE THE FOUNDATION REAL (verse recovery + the acquisition front)
| # | Task | Gate |
|---|---|---|
| B1 | **Verse recovery (the P0 library enabler, present in handover but MISSING from dev-plan phases).** Wire `harvest_to_factory` + `register_harvest_sources` so every SOURCE carries `payload.verse`; unblock tantraloka + the 100-work sivaqueue. | `_verse_for(anypassage)` returns the real verse for every queued work |
| B2 | **The acquisition front (08-CANONICAL-ASSESS-FLOW):** consolidate the deterministic `assess.py` (tag/state/format/verse/identity/priority/route) + materialize translation-existence+location into the ledger + `source-ready.json`. | every work has an auditable `{tag,state,route,priority}`; "English translation exists + where" is queryable |

### PHASE C — THE REAL POST-C1 (rebuild on REAL C1, not trust)
| # | Task | Gate |
|---|---|---|
| C1 | **Only build THEME→ESSAY→EDUCATION on C1 that is itself real** (promoted + gold-scored). The current post-C1 consumed backfilled, non-promoted C1. | post-C1 consumes only promoted C1 (per the authority ladder) |
| C2 | **Real gates on real output:** THEME (member→committed C1), ARGUMENT (quality/content), SYNTHESIS (correct `[ARGUMENT,THEME]` refs + tension), ESSAY (`SentenceEvidenceAudit`), EDUCATION (distill + no-overreach). | SYNTHESIS/ESSAY/EDUCATION registries non-empty with gate-passing, promoted objects |

### PHASE D — CLOSE THE ONE-RULE LOOP (gold + human + lineage)
| # | Task | Gate |
|---|---|---|
| D1 | **Semantic gold scoring** (embeddings/LLM-as-judge, not Jaccard 0.091) on the real golds aligned to object granularity. | committed T1/L2/C1 score > threshold on real golds |
| D2 | **Human gate** wired (`human_authorize`/review_engine → registry): machine proposes, human promotes. | a promoted (non-GENERATED) object exists via a persisted ReviewEvent |
| D3 | **Result lineage on every served + traced object** (`result_id/benchmark_version/gold_version/model_version/code_commit/split/seed/config/date`). | a served/traced result resolves full lineage |

### PHASE E — PROVE IT, LIVE (the benchmark + openpatala)
| # | Task | Gate |
|---|---|---|
| E1 | **One repeatable RAW→EDUCATION E2E** (`test_full_chain_timing` + `trace_object` extended to the real post-C1), producing a publishable proof artifact. | a RAW→EDUCATION trace resolves to RAW with CHAIN OK on REAL output |
| E2 | **Live benchmark dashboard** served by openpatala (layers, time, calls, method, proof, lineage). | `GET /benchmarks/{work}` returns live, evidenced data |

---

## 3. ALIGNMENT REVIEW — handover + dev-plan vs this plan
**Aligned (keep):**
- ✅ The evidence standard (logged runs, deterministic gates, THE ONE RULE) — the deep-dive's method.
- ✅ Verse recovery as P0 (handover §P0) — this plan makes it an explicit phase (B1).
- ✅ Semantic gold + human gate (dev-plan Phase 4 = this plan D1/D2).
- ✅ Live benchmark dashboard (dev-plan Phase 5 = E1/E2).
- ✅ Division of labor (post-C1 to the other agent).

**Misaligned (this plan fixes):**
- ❌ **Both docs trust the post-C1 lane as "theirs, on server2" and Phase 1.1 assumes its gates exist.** The evidence (red-team + registries) shows it's BS. → **A (remediate) + C (rebuild on real C1) must come BEFORE any "extend the E2E to their lane."**
- ❌ **Verse recovery is P0 in the handover but has no named phase in the dev-plan.** → **B1.**
- ❌ **Neither doc has a garbage-remediation step** (archive the BS, fix gamed validators). → **Phase A.**
- ❌ **Neither doc includes the acquisition front** (assess/route/tag/R2/verse/queue — the expanded pipeline 07/08). → **B2.**
- ❌ **The "server2" framing is a doc fiction** — everything is local here; the post-C1 is a demo not wired to real C1. → Phase A/C run HERE, not "on server2."

---

## 4. THE ONE-LINE
> **Fix the gamed validators + archive the garbage (A), close verse-recovery + the acquisition front (B),
> rebuild the post-C1 ONLY on real, gold-scored, promoted C1 with real gates (C), close the ONE-RULE loop
> with semantic gold + human gate + lineage (D), then prove it with a live RAW→EDUCATION benchmark (E) —
> so every claimed layer is evidenced, and the docs stop being BS.**

*Sources: RED-TEAM-REVIEW.md (the other agents' own hostile audit), the registry counts (THEME 1/ARG 10/
SYNTH 0/ESSAY 0/EDU 0), `06-PEER-REVIEW-FRONTIER.md`, `FLAWS.md`, `HANDOVER-NEXT-AGENT.md`,
`DEV-PLAN-NEXT-AGENT.md`, `/tmp/opencode/e2e-trace.json`.*
