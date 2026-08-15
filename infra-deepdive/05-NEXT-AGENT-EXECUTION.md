# INFRA DEEP-DIVE 05 — SYNTHESIS, GAPS, AND THE NEXT-AGENT EXECUTION PATH

*2026-08-15 · the actionable close of this deep-dive. It distills the four audits (00-04) into: the honest
current state, the exact gaps that block "real" output, and a concrete, gate-ordered execution path the
next agent can follow. This supersedes any optimistic reading of the docs — it is what the machines
actually show.*

---

## 1. THE HONEST CURRENT STATE (one paragraph)
We have a **large, real, locally-runnable mechanism for the FULL stack** — RAW→C1 translation workers +
registries + a working E2E harness + MCP verbs + 22 Hermes skills, and a post-C1 mechanism spine
(theme/essay/education/epistemic workers, Nyāya gate, essay audit, education organism libs). **But none of
it has been driven to real, promoted, gold-validated, human-gated output.** The committed scholarly
output is thin (kramasadbhava C1 on 13/248; SYNTHESIS=0, ESSAY=0, EDUCATION=0), the E2E **OOM-kills during
ARGMAP** on this 7.6GB box, the provider is **rate-limited**, and the post-C1 layers have produced only ~11
non-promoted `GENERATED` proposals. The docs claim more than the machines back up. **The gap is EXECUTION +
GOLD + the human gate, not missing machinery.**

## 2. THE GAPS THAT BLOCK "REAL" OUTPUT (each must be closed, in order)
| # | Gap | Evidence (from 01-04) | Closes |
|---|---|---|---|
| G1 | **OOM during ARGMAP** — the E2E cannot complete on this box | live run: 4.5GB RSS → SIGKILL (137) at ARGMAP | reduce batch size / free RAM / stream — must be fixed before any scale |
| G2 | **Provider rate-limit** — `opencode-go` 429, resets ~Aug 15-16 | `~/.hermes/profiles/patala/auth.json` `last_status: exhausted` | wait for reset or add a second credential |
| G3 | **L1 DAG inconsistency** — L1 in the test DAG but not the manifest/scheduler | `test_full_chain_timing.py:24` vs `CANONICAL-DAG.yaml` + `factory_scheduler.py:43` | pick ONE DAG; align all layers |
| G4 | **Empty post-C1 layers** — SYNTHESIS/ESSAY/EDUCATION = 0; THEME/ARGUMENT not promoted | live registry counts | run the spine on real committed C1 |
| G5 | **Vacuous gates** — `p51-synthesis` "PASS" prints a count only; structure/lexicon gates ≠ content/gold | `build-plan-2026-08-15.json`; `GOLD-VALIDATION-NOTES.md` | real content/gold validators |
| G6 | **Gold scoring is meaningless** — Jaccard 0.091; golds are commentary-level vs kārikā-level objects | `FLAWS.md #7`, `GOLD-VALIDATION-NOTES.md` | semantic/embedding scorer + aligned golds |
| G7 | **Nothing promoted or human-gated** — 0 `COMMITTED` status anywhere | registries | `human_authorize` promotion gate |
| G8 | **Unbacked docs / dangling refs** — post-C1 products, epistemic engines, `/root/fuck-off`, `/root/serveragent3` don't exist here | `check_epistemic.py` 58 failures; `check.py --status` hangs | honest reconciliation; fix `check.py --status` to not load 850MB |

## 3. THE EXECUTION PATH (gate-ordered — do each, run its gate, then next)
### Step 1 — Stabilize the machine (unblock G1, G2)
- Fix the ARGMAP OOM (smaller batches, memory cap, or free RAM) so `test_full_chain_timing.py --work
  kramasadbhava` completes RAW→C1. **Gate:** E2E finishes with all layers committed + per-layer time/api-calls.
- Confirm the provider is usable (`hermes status`); plan for the reset window.

### Step 2 — Reconcile the DAG + the record (unblock G3, G8)
- Pick ONE canonical DAG; make `CANONICAL-DAG.yaml`, `factory_scheduler.py:43`, `test_full_chain_timing.py:24`,
  and the skill layer-names agree.
- Make `check.py --status` terminate (don't load the 850MB registry inline).
- Reconcile the epistemic/post-c1 docs to what actually exists (or mark honestly).

### Step 3 — Drive the spine on real C1 (unblock G4)
- Run `build_plan.py` so THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION actually consume committed C1 and
  produce + promote objects. **Gate:** SYNTHESIS/ESSAY/EDUCATION registries non-empty with promoted objects.

### Step 4 — Real gates + gold (unblock G5, G6)
- Replace vacuous/structure gates with content validators; add the semantic (embedding) gold scorer aligned
  to the object granularity. **Gate:** committed output scores above threshold vs the real golds.

### Step 5 — Human gate + benchmarks (unblock G7, and deliver)
- Wire `human_authorize` as the promotion gate; surface per-work RAW→EDUCATION benchmarks (layers, time,
  calls, method, `trace_object` proof) via openpatala. **Gate:** a real, promoted, human-signed RAW→EDUCATION work exists.

## 4. THE CRITICAL HERMES OPERATING FACTS (repeat of the one thing that changes everything)
1. **Pass file PATHS, not contents** — Hermes can read the whole filebase itself.
2. **Correct call:** `hermes chat -Q -q "<ask>" --skills <skill> --yolo --max-turns 8 -m deepseek-v4-flash
   --provider opencode-go -p patala` — NEVER blind `hermes -z` for real work (~3.8% yield).
3. **Hermes task DONE ≠ Pāṭala object ACCEPTED** — the deterministic gate decides what's real.
4. **MCP verbs** are NOT registered in Hermes — call `python3 /root/projects/patala/pipeline/patala_orchestration.py
   {--next,--state,--summary,--limit}` directly or register `node /root/projects/patala/mcp/index.mjs`.
5. **Kanban** drives the queue but is "the task board, not the truth" — `hermes kanban --board translation list`.

## 5. THE ONE-LINE CARRY-FORWARD
> **Fix the ARGMAP OOM + provider reset (Step 1), reconcile the DAG + record (Step 2), run the post-C1 spine
> on real C1 (Step 3), replace vacuous gates with real gold (Step 4), then add the human gate + live
> benchmarks (Step 5) — so one repeatable command produces a real, promoted, gold-validated, human-signed
> RAW→EDUCATION object.**

## 6. INDEX OF THIS DEEP-DIVE
- `00-OVERVIEW.md` — the big picture + the honest scorecard.
- `01-PATALAORG-REPOSITORY.md` — the production docs repo, both lanes, validators.
- `02-PATALA-PIPELINE.md` — the translation DAG, E2E harness, skills, autonomous loop, MCP.
- `03-HERMES-INFRASTRUCTURE.md` — the Hermes install/config/profile/kanban/skills/MCP/sessions.
- `04-IP-GRAPH-POST-C1-LANE.md` — the post-C1 spine, products, gates, education organism, cross-lane seam.
