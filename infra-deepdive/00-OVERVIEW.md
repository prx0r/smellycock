# INFRA DEEP-DIVE 00 — THE BIG PICTURE, HONESTLY

*2026-08-15 · the master synthesis of a full-context parallel audit of every relevant system: the
`patalaorg` production repo, the `patala` translation pipeline, the Hermes agent install, and the
`ip-graph` post-C1 scholarship lane. This is the honest map a next agent needs BEFORE touching anything.
It states what is REAL vs what is DOCUMENTED-AS-REAL, and where the two disagree.*

---

## 1. THE SYSTEMS AND WHAT EACH IS FOR

| System | Location | Remote | What it is |
|---|---|---|---|
| **patalaorg** | `/root/projects/patalaorg` | `prx0r/smellycock` | The canonical **docs** repo (AGENTS/AXIOMS/OBJECT-MODEL/MANIFEST + both lanes' docs + runs) + `check.py` validators |
| **patala** | `/root/projects/patala` | `prx0r/patala` | The **working code** repo: the RAW→C1 translation pipeline (factory, workers, skills, MCP, registries) + the post-C1 workers |
| **ip-graph** | `/mnt/HC_Volume_106427611/ip-graph` | `prx0r/fuck-off` | The **validation/read-plane lab**: kernels, validators, post-C1/education organism libs, built `site/` |
| **Hermes** | `/usr/local/bin/hermes` (v0.18.2), home `~/.hermes` | — | The agent engine; active profile `patala`, active project `patala`, gateway running |

## 2. THE ONE RULE (what "real" means — AGENTS.md:11-14, AXIOMS.md:96)
> **Nothing is "real" because a file exists. It is real only when an independently defined task, human-
> grounded gold, and a reproducible gate show it does what its name claims. A doc is a projection; the
> truth is `object_registry` + `corpus_state` + ReviewEvents + git.**

Every honest verdict in this deep-dive is measured against this rule.

## 3. THE CANONICAL DAG
```
SOURCE → T1 → L0 → [ARGMAP] → L2 → L200 → C1 → THEME/ARGUMENT → SYNTHESIS → ESSAY → EDUCATION
```
- **Batched model (Hermes) layers:** T1, ARGMAP, L2 (and C1 batched). **Bounded classifier:** L200.
  **Deterministic (free-draining, no model):** L0, L1.
- **The seam between the two lanes:** we produce **C1**; the post-C1 lane builds **THEME→…→EDUCATION above it**.
- **⚠️ DAG conflict:** `L1` appears in the live-run/test E2E DAG but is **absent** from
  `contracts/CANONICAL-DAG.yaml` and from `factory_scheduler.py:43` (`LAYER_ORDER`). Two DAG definitions
  coexist — an unresolved inconsistency (the very thing `A2-ARCH-HARDEN` claimed to have fixed).

## 4. THE HONEST SCORECARD — what is REAL vs DOCUMENTED

| Claim | Verdict | Evidence |
|---|---|---|
| "check.py PASS" | ⚠️ **Only the 3-flag subset passes.** `check.py --refs --naming --manifest` → exit 0. | verified live |
| "check.py --status is the full gate" | ❌ **Hangs/times out (exit 124).** `--counts` loads an **850MB** `source-registry.jsonl`. | verified live |
| "both lanes aligned" | ❌ **Not on this box.** Translation lane = real code; epistemic/post-C1 lane = docs/pointers only. `check_epistemic.py` **fails 58 issues**. | verified |
| "RAW→C1 proven repeatable" | ❌ **Not reproducible here.** A live E2E run **OOM-killed during ARGMAP** (4.5GB RSS on a 7.6GB box). | verified live |
| "products built on server2" | ❌ **Fiction on this box.** All code is local; the post-C1 layers just haven't been run to real output. | verified |
| "25 products / 134 PASS" | ❌ **Unbacked.** Only `pipeline/products/README.md` (a pointer) exists. Counts in docs are mutually inconsistent (19/25/26). | verified |
| Translation infra (T1/L0/ARGMAP/L2/L200/C1) | ✅ **Real + present** in `/root/projects/patala/pipeline/`. Registries have real lines. | verified |
| The ONE RULE + AXIOMS shared | ✅ **Consistent across both lanes' docs.** | verified |

## 5. THE HONEST BOTTOM LINE
We built a **large, real, mostly-working translation INFRASTRUCTURE** (T1→C1 code + registries + a working
E2E harness + MCP verbs + 22 Hermes skills). But:

1. **The committed scholarly output is thin:** kramasadbhava has C1 on **13/248** passages, L2 on **22/248**.
2. **The current machine cannot complete the E2E** — it OOM-kills during ARGMAP.
3. **Post-C1 is essentially empty:** SYNTHESIS=0, ESSAY=0, EDUCATION=0 committed objects; THEME=1,
   ARGUMENT=10 (all `GENERATED`, none promoted). The `p51-synthesis` "PASS" is vacuous (prints a count only).
4. **`FLAWS.md` (the repo's own counter-evidence) agrees:** the goal (a full work to C1, tracked and gated)
   is **NOT met**; gold scoring Jaccard=0.091 is meaningless; nothing has passed the human gate.
5. **The provider is rate-limited:** the `opencode-go` credential is **exhausted (429 weekly limit, resets
   ~Aug 15-16)** — expect Hermes model calls to fail until reset.
6. **The Hermes kanban `translation` board has 6 ready tasks and no running worker** — consistent with the
   rate limit.

## 6. THE OPPORTUNITY (why this still matters)
The mechanism for the FULL stack is **local and runnable**: real translation workers, real post-C1 workers
(theme/essay/education/epistemic), the Nyāya gate, the essay audit, `build_plan.py`, 22 Hermes skills, the
MCP verbs, and a working read-plane builder. It has simply **not been driven to real output**. The gap is
EXECUTION + GOLD + the rate-limit, not missing machinery. That is the next agent's job.

## 7. HOW TO READ THE REST OF THIS DEEP-DIVE
- **01-PATALAORG-REPOSITORY.md** — the production docs repo, both lanes, MANIFEST, the check validators.
- **02-PATALA-PIPELINE.md** — the translation DAG, E2E harness, skills, autonomous loop, state/runs, MCP.
- **03-HERMES-INFRASTRUCTURE.md** — the Hermes install, config, profile, kanban, skills, MCP, sessions.
- **04-IP-GRAPH-POST-C1-LANE.md** — the post-C1 spine, products, gates, education organism, cross-lane seam.
