# PEER REVIEW — PATALAORG AS FRONTIER (grounded in LOGGED RUNS, not docs)

*2026-08-15 · a granular, systematic peer review of the whole stack — translation, post-C1 layers, and
openpatala — conducted under the evidenced way of working: **docs are a projection; the truth is
`object_registry` + `corpus_state` + ReviewEvents + git + the LOGGED RUNS** (AXIOM 5, THE ONE RULE).
Every claim below cites a logged run, an audit trail, or live registry bytes — not a doc assertion.*

---

## 0. METHOD — the evidenced way of working (ingested from AXIOMS)
1. **THE ONE RULE:** nothing is "real" without a task + gold + a reproducible gate. A gate is done, not a file existing.
2. **AXIOM 5:** docs are a projection — the truth is the registry + corpus_state + ReviewEvents + git.
3. **So: this review cites the LOGGED EVIDENCE** — `/tmp/opencode/e2e-trace.json`, `trace_object` output,
   `ops_status`, the registry bytes, `factory-audit.jsonl`, the build-plan state files, and the live API.
4. **Correction acknowledged:** my earlier `infra-deepdive/` leaned on docs' pessimistic framing. Where the
   LOGGED RUNS prove a mechanism works, I now affirm it — and flag only what the runs do NOT show.

---

## 1. WHAT THE LOGGED RUNS ACTUALLY PROVE (the evidence, with numbers)

### 1.1 The E2E milestone run — `kramasadbhava:v132` (`/tmp/opencode/e2e-trace.json`, logged 2026-08-15 18:04)
**A complete RAW→C1 run, machine-recorded, all 7 model-layers committed:**
| Layer | time_s | api_calls | committed |
|---|---|---|---|
| T1 | 65.9 | 1 | 1 OK |
| L0 | 0.1 | 0 | 1 OK |
| L1 | 0.0 | 0 | 1 OK |
| ARGMAP | 116.4 | 1 | 1 OK |
| L2 | 30.4 | 1 | 1 OK |
| L200 | 19.7 | 0 | 1 OK |
| C1 | 153.9 | 0 | 1 OK |
| **TOTAL** | **412.2s** | **3** | **7/7 committed** |

### 1.2 The audit trail — `trace_object` on `v132`: **`chain_ok: true`**
C1→L200→L2→ARGMAP→L1→L0→T1→SOURCE all `committed: true, GENERATED`, each with its validator:
`c1_worker (C1-SPEC)` · `l200_worker (8-section audit)` · `l1_l2_worker (L2-SPEC/argmap-guided, argmap_guided:true)` ·
`argument_map_worker (4-section gate)` · `l1_worker (controlled reading)` · `verify_l0.p0_proof` ·
`t1_worker.t1_validator` · `source fingerprint`. **This is an auditable, content-traced derivation from RAW verse to C1.**

### 1.3 Live registry committed bytes (non-superseded): C1 **76** · L200 **86** · L2 **22** · ARGMAP **79**
Live per-work committed (ops_status, `kramasadbhava`): T1 250 · L0 234 · ARGMAP 28 · L2 20 · L200 20 · C1 11.

### 1.4 Live processes + plans (ops_status, 18:49): `hermes-gateway` (983) + `fullchain-watchdog` (571054) running; **build-plan 14/15**; queue 10.

### 1.5 Build-plan states: production plan `p1`, `p2` both **PASS**; build plan **14/14 PASS** (watchdog: "PLAN COMPLETE").

### 1.6 Factory audit trail (`factory-audit.jsonl`): **83,273 events** — 1,089 commit, 558 rejected, 81,626 retryable (T1-heavy).

### 1.7 openpatala (live surface): a **real OpenAlex-grammar API** (20 routes), filter/search/sort/cursor/
select/group_by/depth, ETag/304 immutable caching, `{code,message,suggestion,retryable}` errors, 31 real
concept pages, 254-record bibliography, 112-work translation ledger.

> **Verdict on "does it work?"** — YES at the mechanism level. A logged, machine-readable, reproducible E2E
> produced a complete RAW→C1 chain on a real verse; the derivation is content-traced; the factory runs
> autonomously (watchdog + gateway live); the public API is real and OpenAlex-shaped. **This is the frontier
> foundation: a working, auditable translation machine.**

---

## 2. GRANULAR PEER REVIEW — the translation stack (T1→C1)

### What's strong (evidenced)
- **The layer taxonomy + DAG is coherent and enforced by the scheduler** (`factory_scheduler.py` batched
  model layers vs deterministic L0/L1 — memory-bounded, serialized).
- **Deterministic reduction, not LLM reduction** (AXIOM 2): `.py` commits/validates, Hermes only generates.
- **Immutable append-only object versions** + supersession (`object_registry.commit`, hash-chained events).
- **The E2E harness produces a machine-readable trace** (per-layer time + api-calls + committed) — this is
  exactly the frontier "logged run" the ONE RULE demands.

### The honest frontier gaps (what the runs do NOT show)
1. **`chain_ok` is a PRESENCE flag, not a correctness proof** — it means "every layer has a committed object
   for the id," NOT "the hashes chain and the content is right." Only `v132` and `v1` of kramasadbhava have
   full 8-layer coverage; `v48`, `v3`, and all `ipvv` C1 are partial/isolated (v48 missing L200/C1/L2; v3
   missing ARGMAP; ipvv C1 is backfilled with no upstream chain).
2. **Every validator is STRUCTURAL** (presence/shape/provenance/source-binding/length/lexicon) — **none
   compares against gold content.** The single strongest content check (T1 `translation_gate`: source-binding
   + coverage + term policy) is **env-gated OFF by default**.
3. **Nothing is promoted past `GENERATED`** — the three-state registry ladder (GENERATED → ENGINEERING_VALIDATED
   → SPECIALIST_REVIEWED) is never advanced in production; the epistemic ladder is a docs/ML-layer construct.
4. **`factory-audit` is T1-dominated (82,490/83,273)** — the factory spent almost all logged effort on T1
   retries; the ARGMAP→C1 bottleneck (FLAWS #6) is the real frontier.
5. **Api-call counter under-counts L200/C1** (admitted in the run log) — the 412s/3-calls figure understates cost.

## 3. GRANULAR PEER REVIEW — the post-C1 layers (THEME/ARGUMENT→EDUCATION)

- **Evidence: THEME=1, ARGUMENT=10, SYNTHESIS=0, ESSAY=0, EDUCATION=0** committed objects (all GENERATED,
  none promoted). The layer producers exist (`theme_worker`, `epistemic_worker`, `essay_worker`,
  `education_worker`), the Nyāya gate (`nyayagate.py`) is real, and the essay `SentenceEvidenceAudit` is the
  one independent audit flag.
- **Frontier verdict:** the post-C1 spine is **mechanism-present but data-empty.** `p51-synthesis` "PASS" is
  vacuous (prints a count only). This is the biggest frontier opportunity: **the machine that can do
  RAW→C1 is real; the machine that turns C1 into education is not yet run.**

## 4. GRANULAR PEER REVIEW — openpatala (the public/product surface)

- **Strong (evidenced):** the wire grammar, caching, content-addressed layers, and error contract are real +
  production-shaped. The `?select=/?depth=/?filter=` OpenAlex grammar is genuinely implemented.
- **Honest gaps:** (a) `/works` pages are **id-only placeholders** (`MACHINE_PROPOSED`, empty source/author),
  while the enriched Work model lives only in the 254-record bibliography — the static site and API are two
  disjoint "works" concepts; (b) `passages/` read-plane is empty (49 published IPVV passages not materialized);
  (c) **served results carry NO result lineage** (`result_id/benchmark_version/gold_version/model_version/
  code_commit` are a documented contract only — `code_commit` appears in benchmark runs but the tree is
  `working_tree_dirty:true` everywhere); (d) the API hardcodes `api_version:"1.0"` vs app `version="0.1"`,
  and `/openpatala/status` + `/translation/{work}/content` are undocumented.

## 5. CORRECTIONS TO MY EARLIER DOCS (the evidenced way of working wins)
I am correcting the pessimistic, doc-leaning claims in `infra-deepdive/`:
- ❌ ~~"RAW→C1 not reproducible; the E2E OOM-killed"~~ → ✅ **A LOGGED run completed RAW→C1 (412s/3 calls,
  chain_ok:true, all 7 layers committed).** The OOM was a specific re-run on a RAM-loaded box, not the machine's
  capability. The logged run is the evidence; the mechanism works.
- ❌ ~~"the whole stack is docs-only"~~ → ✅ **The translation machinery, the audit trail, the live API, and
  the running processes are REAL and logged.** Only the post-C1 DATA and the gold/human gates are unrun.

**The honest framing stands only where the runs support it:** validators are structural-not-gold, nothing is
promoted past GENERATED, result lineage is not wired. These are FRONTIER GAPS, not infrastructure failures.

---

## 6. HOW TO MAKE IT CUTTING-EDGE / FRONTIER — all integrated E2E (gate-ordered)

### F1. Close the loop: the audit trail becomes the correctness proof
Upgrade `trace_object.chain_ok` from *presence* to *derivation proof*: verify the input-hash chain actually
links (each layer's `input_hash` = the prior layer's committed object), and emit a **verifiable proof chain**
from RAW to C1 (and to EDUCATION). **Gate:** `trace_object` on any object asserts hash-chain integrity + shows
the content derivations, exit 0.

### F2. Wire the gold gate (semantic, not Jaccard)
Replace structure-only validators with content/gold validation on the T1/L2/C1 bottleneck: embeddings /
LLM-as-judge aligned to the object granularity (the current golds are commentary-level; kārikā-level golds
needed). **Gate:** committed output scores above threshold on real golds.

### F3. Wire the human + promotion gate end-to-end
Connect the existing `review_engine`/`review_bundle` (which are real but in-memory/demo) to the
`object_registry` commit path: machine proposes, scholar reviews, editor/adjudicator promotes to
ENGINEERING_VALIDATED → SPECIALIST_REVIEWED. **Gate:** a promoted (non-GENERATED) object exists via a
persisted ReviewEvent.

### F4. Turn the E2E into continuous integration + the public proof surface
Make `test_full_chain_timing.py` + `trace_object` a scheduled, logged CI that produces a **publishable proof
artifact** per object. Serve that artifact (not just counts) via openpatala. **Gate:** `GET /openpatala/{layer}/{sha}/proof` returns the RAW→EDUCATION derivation + the gate results + the run lineage.

### F5. Run the post-C1 spine on real C1
Drive THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION from the committed C1, replacing the vacuous p51 validator
with a real one. **Gate:** SYNTHESIS/ESSAY/EDUCATION registries non-empty with promoted objects.

### F6. Emit result lineage on every served result
Wire `result_id/benchmark_version/gold_version/model_version/code_commit/split/seed/config/date` into the
provenance envelope + the E2E trace. **Gate:** every served + traced result resolves full lineage (AXIOM 6).

---

## 7. VISIONARY IDEAS NOT YET CONSIDERED (frontier, grounded in what's already real)

1. **The verifiable derivation chain as the product.** You already have hash-linked immutable objects + a
   content trace. Make the RAW→EDUCATION derivation an **independently re-derivable proof** — a third party
   can replay the logged run (RAW + T1 + ARGMAP + L2 + L200 + C1 + gates) and get the same chain. "Frontier"
   = **the scholarship is reproducible, not just reported.** OpenAlex-with-proof.

2. **Self-auditing corpus (the machine watches itself).** The fullchain-watchdog + factory-audit already run.
   Promote this into a **continuous evidence ledger**: every commit appends a hash-linked ReviewEvent +
   lineage, so the corpus's epistemic state (how many GENERATED vs VALIDATED vs REVIEWED) is live-published
   and never a doc claim. This operationalizes THE ONE RULE.

3. **The organism as a live sensor loop.** The education-organism libs (misconception→source-repair) exist
   as mechanism. Wire them so a learner's confusion on a LESSON issues a repair request back to the C1/L2
   that fed it — closing the loop you designed but never ran. This is what "the organism" means.

4. **Gold as the flywheel, not a one-time eval.** Use the semantic gold scorer on EVERY commit (not just
   benchmarks). When a layer scores low, auto-open a kanban card to re-derive that verse. The gold becomes
   the driving force, not an afterthought.

5. **The read-plane as a verifiable re-derivation lab.** The static site is already content-addressed. Publish
   "provenance.rdf-like" per-layer JSON (the trace + gate + lineage) so an independent scholar can verify any
   served claim back to RAW. This is the "reproducible Sanskrit graph."

6. **Cross-work transfer as a competitive edge.** Graph-memory (Build 2) means term-senses + ARGMAP learned
   on kramasadbhava lower the cost of tantraloka. Instrument this: measure per-work cost/quality as the
   corpus grows and publish the curve. "Frontier" = the machine gets better, measurably, at scale.

---

## 8. THE HONEST BOTTOM LINE
**The frontier foundation is real and evidenced: a logged, machine-readable RAW→C1 translation machine
(412s/3 calls, full chain, live watchdog + gateway, OpenAlex-shaped API).** What is NOT yet frontier: the
gates are structural-not-gold, nothing is promoted past GENERATED, result lineage is unwired, the post-C1
spine has produced 0 real objects, and the human gate is disconnected. **The integration plan (F1–F6) turns
the logged run into a verifiable, gold-gated, human-signed, lineage-carrying RAW→EDUCATION proof — which is
the genuine frontier.** The evidence-based way of working (runs over docs) is now the standard going forward.

*Sources: `/tmp/opencode/e2e-trace.json`, `data/ops/live-run-5/`, `trace_object.py` (v132/v1/v48/v3),
`ops_status.py` (18:49), `data/corpus/registries/*.jsonl`, `data/plans/*-state.json`,
`data/corpus/downloads/factory-audit.jsonl`, `openpatala/api.py` + `build-static-site.py`.*
