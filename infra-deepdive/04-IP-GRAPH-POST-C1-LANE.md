# INFRA DEEP-DIVE 04 — THE IP-GRAPH POST-C1 LANE

*2026-08-15 · a full-context audit of `/mnt/HC_Volume_106427611/ip-graph` (remote `prx0r/fuck-off`) and the
post-C1 scholarship layer (THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION) + the epistemic products. What is real,
what the gates actually check, the real seam to the translation lane, and the cross-server reality.*

---

## 1. STRUCTURE
**ip-graph** is the **validation/read-plane lab**: `scripts/` (152 files), `lib/` (52 kernels), `layers/`
(10 layer docs), `site/` (built static output), `specs/`, `skills/` (6 Hermes skills), `data/`,
`tantraloka/`, `migration/` (v2/v3), `docs/`, `ecosystem/` (vendored: RKA, eigenius, fojin, kappa-graph),
`handover/`, `notes/`.
- **Build scripts in `scripts/`** are mostly VALIDATORS + EXPERIMENTS: ~90 `validate-*.py` (one per kernel),
  ~45 `experiment-*.py`, `theatre-check.py`/`theatre-check-all.py` (the audit), `run-tests.py` (suite
  driver), `build-static-site.py` (read-plane → `site/`), `run-tantraloka-*.py` (E2E/organism wiring).
- **There is NO `build_plan.py` in ip-graph** — the spine driver lives in **patala**:
  `/root/projects/patala/pipeline/build_plan.py`.
- **Real registries/products live in patala** (`data/corpus/registries/*-registry.jsonl`) + the built
  read-plane in `ip-graph/site/openpatala/`.

## 2. THE POST-C1 SPINE
### The driver: `build_plan.py` (`/root/projects/patala/pipeline/build_plan.py`, 174 lines)
A **generic checkpoint-DAG engine**, not a layer-specific spine. Loads a JSON plan, computes eligibility
from `prereqs`, runs each checkpoint's `action` then its `validator`, and marks **DONE only if the
validator exits 0** (91-137). It shells out; not wired directly to the layer registry.

The layer DAG is declared in `pipeline/object_registry.py` (LAYERS list):
`SOURCE, T1, ARGMAP, L0, L1L2, L1, L2, L200, C1, THEME, ARGUMENT, SYNTHESIS, ESSAY, EDUCATION`.

The **definitive two-lane split** is in `/root/projects/patala/migration/shared/HANDOFF-POST-C1.md`:
**agentgraph (this box) owns `SOURCE→…→C1`; the post-C1 lane owns `THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION`
+ organism loops.**

### The actual plans + checkpoint DAG (`data/plans/`)
- `build-plan-2026-08-15.json`: `p50-theme` ("THEME over real C1") prereq `p30-argument-bench`, action
  `factory_batch.py --layers THEME`; `p51-synthesis` ("SYNTHESIS over adjudicated ARGUMENT+THEME") — action
  `true`, validator **only prints the count (so it "passes" even when SYNTHESIS=0)**; `endgoal-fullwork-c1`
  ("kramasadbhava driven fully SOURCE→C1").
- `build-plan-production-2026-08-15.json`: `p1` whole-chain commit → `p2` RAW→C1 chunk → `p3` full work to
  C1 → `p4` graph-memory.
- **State files show `p50-theme` and `p51-synthesis` marked DONE/PASS on 2026-08-15 — but the p51 "PASS" is
  VACUOUS (count-print only), and p50 produced exactly 1 THEME object.**

### The real layer producers (wired in `pipeline/autonomy.py:107-216`, in patala)
- **THEME** → `theme_worker.py` (180) · **ESSAY** → `essay_worker.py` (188) · **EDUCATION** →
  `education_worker.py` (196) · **ARGUMENT / SYNTHESIS** → `epistemic_worker.py` (205, 213). ESSAY/EDUCATION
  also have a generative fallback `generative_worker.py` (thin structural gate).

### The claimed gates vs what they ACTUALLY check
**The dev-plan gate names (Nyāya, cite-contract, quality, blind-assessor, tension) do NOT all exist as
code under those names.** Real gate code:
| Claimed gate | Actual code | What it checks |
|---|---|---|
| **Nyāya** | `/root/projects/patala/machinelearning/research/patala_ml/nyayagate.py` `gate_claim()` (98-184) | 5-hetvābhāsa heuristic gate: detects *asiddha, savyabhicara, viruddha, badhita, satpratipaksa* via **keyword lexicons** (line 38 `STRONG_WORDS`, 134 `UNIVERSAL_OVERRECH`). Bounded; NEVER declares truth. `check_viruddha_graph()` (187) adds graph-aware viruddha. |
| **THEME gate** | `theme_worker.py:137` `theme_validator()` | deterministic: status==MACHINE_PROPOSED, has members, each member has strength+role, member resolves to a committed C1, boundary present. |
| **ESSAY gate** | `essay_worker.py:139` `essay_validator()` + reused `verify_essay` (SentenceEvidenceAudit) | every sentence has claims, claims present, `_audit_ok==True` (independent audit, fail-closed on certainty-inflation / boundary-erasure / orphan sentences). |
| **EDUCATION gate** | `education_worker.py:94` `education_validator()` | derived from a committed essay, has summary, <1500 chars (distill not re-run), no overreach lexicon (line 27 `_OVERREACH`). |
| **Cite-check** | `ip-graph/lib/scholar_review.py` `verify_citations()` | citation resolves to a known ref → else PHANTOM. Plus `ReviewPanel.anti_groupthink()` (56) + verdict (66). |
| **cite-contract / blind-assessor / tension** | **Do not exist as code** | Planned (DEV-PLAN Phases 1.1, 4.3). `tension_id` is only a data field in `patala_ml/argument.py:87`. |

**Critical caveat:** these are **structure/lexicon gates, NOT content/gold gates.** `notes/GOLD-VALIDATION-NOTES.md`
documents that committed factory output scores ~0 recall against the published IPVV golds (L0 49/49 scored
but `mean_recall 0.0`, T1 0/49, ARGMAP 0/49, L2 0.0) — the golds are commentary/chunk-level while the
factory emits kārikā-level objects.

### Does the spine run on THIS box?
**The code is here and dependencies resolve** (verified: `patala_ml.cluster`/`essayverify` import cleanly;
`model.py`, `epistemic_worker.py`, `generative_worker.py` all exist). **BUT the autonomous spine has never
committed real post-C1 output** (see §3).

## 3. THE PRODUCTS — what ACTUALLY exists (committed registry counts)
Streamed from live registries (`committed_ids` = non-superseded objects):
```
C1:       74   (76 lines, all GENERATED, 0 "COMMITTED")
L200:     84
THEME:    1    (1 line, GENERATED)
ARGUMENT: 10   (10 lines, GENERATED)
L2:       20
SYNTHESIS: 0   (NO registry file exists)
ESSAY:     0   (NO registry file exists)
EDUCATION: 0   (NO registry file exists)
```
**The post-C1 layers are essentially EMPTY.** Only 1 THEME + 10 ARGUMENT proposals exist, none promoted past
`GENERATED`. SYNTHESIS/ESSAY/EDUCATION have **zero** committed objects.

### Read-plane products (in ip-graph `site/`)
- `site/works/` — **2000 near-empty placeholder pages** (e.g. `site/works/k22.json` =
  `{"id":"ipvv:V2L:k22","title":"ipvv:V2L:k22","author":"","source":""}`). Title = object-id, no content, all `MACHINE_PROPOSED`.
- `site/concepts/` — 31 real concept pages (from `data/graph/graph.json`) · `site/argument/` — 6 ·
  `site/bibliography/` — 254 thin records · `site/openpatala/` — per-layer counts + real `translation.json` status.

### Product claims vs reality
`BUILT-BY-LAYER.md` + `migration/v2/PRODUCTS.md` claim 13/16 products proven as MECHANISMS, with
Essay/Synthesis/Education as PROVEN-MECHANISM / NEEDS-BUILD. **Accurate as mechanism (kernel + synthetic
validator) but NONE are wired to real committed post-C1 objects.** The scholar-workflow/manuscript/
education-*organism* production code is in `ecosystem/epistemic/rka/` + `ecosystem/translation/fojin/` —
vendored third-party repos, NOT wired into this spine.

## 4. KANBAN + HERMES in the post-C1 lane
- **There is NO code that drives a Hermes kanban board in ip-graph.** All kanban references are documentation
  (DEV-PLAN-NEXT-AGENT.md Phase 2 — "all planned, none built"). `docs/hermes-official/KANBAN.md:54-55`:
  *"Kanban is the task board, not the truth."*
- The MCP verbs are **spec'd, not built** (CONTEXT-REVIEW-3.md:96: "THE single biggest gap … spec'd, not built").
- **The Hermes execution path that DOES exist:** `ip-graph/lib/hermes_exec.py` — `agentic()` shells
  `hermes chat -Q -q ... --yolo --max-turns N -m deepseek-v4-flash --provider opencode-go -p patala`
  (line 50). Used by `validate-essay-ingest.py` + `translate_karika()`.
- Skills in ip-graph: `skills/hermes-generate-reduce/` (GENERATION via Hermes / REDUCTION via .py),
  `hermes-derive-essay`, `hermes-derive-enquiry`, `hermes-derive-translation`, `theatre-check`, `vcreate` —
  all invoke `hermes chat` agentic, never blind `-z`.

## 5. THE EDUCATION ORGANISM
- **There is NO "education-organism-run-4"** anywhere. (The nearest match is patala's `live-run-4`, the
  TRANSLATION lane's RAW→C1 run — different thing.)
- **What the education organism actually IS (built, mechanism-level):**
  - `ip-graph/lib/education.py` — `LearningClaim`, `MasteryEvidence`, `compile_interactions()`,
    `wrong_answer_to_neighbor()` (the "moat": a wrong answer resolves to a known epistemic neighbor, not an
    invented distractor), counterfactual `PremiseRetract`.
  - `ip-graph/lib/organism.py` — `UserKnowledgeState`, `MisconceptionGraph`.
  - `ip-graph/lib/misconception.py` — `MisconceptionRepairCascade` (confusion → source-repair → RKA propagate).
  - `ip-graph/lib/pedagogy.py` — distractor generation; `lib/organism_loop.py`; `lib/agent_delivery.py`.
  - Specs: `SPEC-20-EDUCATION-ORGANISM.md`, `SPEC-26/27/28/29`. Validator: `scripts/validate-education-organism.py` (9/9, **on synthetic/hand-fed data**).
  - Production worker: `/root/projects/patala/pipeline/education_worker.py` (distills a committed ESSAY → 3-min explainer; gate = derived-from-essay, concise, no overreach).
- **What it produced:** only `data/checkpoints/Education-Organism.json` (a checkpoint DAG spec, not output)
  + a synthetic-data validator PASS. **Zero committed EDUCATION objects** (EDUCATION registry file doesn't exist).

## 6. ALIGNMENT WITH THE TRANSLATION LANE — CONFIRMED
The seam is REAL and explicit:
- `ip-graph/scripts/run-tantraloka-e2e.py:37` — `sys.path.insert(0, "/root/projects/patala/pipeline");
  import object_registry as R` — STAGE A reads committed `SOURCE/T1/L0` from patala's registry.
- `build-static-site.py:88-91,105` — `_registry_summary()`/`_per_work_committed_counts()` import
  `object_registry` + stream committed ids per layer (`T1, ARGMAP, L0, L2, L200, C1`).
- `theme_worker.py:50` — `R.current("C1", oid)` consumes patala's committed C1; `essay_worker.py` and
  `education_worker.py` consume committed THEME/C1 and ESSAY from the same registry.
- `HANDOFF-POST-C1.md:22` — the input contract: "committed C1 from `data/corpus/registries/c1-registry.jsonl`."

**True integration status:** the seam is real + the code references it, and patala lives on this same box
(branch `agent2`). The E2E driver (`run-tantraloka-e2e.py`) genuinely chains factory→validator→flywheel→
read-plane→scheduler. **However, the post-C1 layers do NOT consume C1 at scale** — only 1 THEME / 10
ARGUMENT proposals exist, produced by `backfill_pg`/direct commit (`created_by: backfill_pg`), NOT by the
autonomous spine running on real committed C1. SYNTHESIS→ESSAY→EDUCATION are unwired downstream (registries empty).

## 7. CROSS-SERVER REALITY — the "server2 only" claim is FALSE for this box
**The full stack is LOCAL, but it is a doc/mechanism mirror, not a running production spine.**
Verified on THIS box:
1. **patala exists here** (branch `agent2`) with real registries: SOURCE **890MB** (501,248 objects),
   C1 76 lines, T1 1.6MB, L200, L2, ARGUMENT, THEME — all local files, not pointers.
2. **The product code (theme/essay/education/argument/synthesis workers) is local** + deps import cleanly.
3. **`build_plan.py` is local + executable** — state files show `p50-theme`/`p51-synthesis` DONE/PASS.

**BUT the honest reality:**
- Post-C1 commit counts are **0 for SYNTHESIS/ESSAY/EDUCATION**; THEME/ARGUMENT are **GENERATED-only**.
- The `p51-synthesis` "PASS" is **vacuous** (count-print only); `p50-theme` produced exactly 1 THEME.
- **Not a single C1/L200/THEME/ARGUMENT object is promoted past `GENERATED`** (0 `COMMITTED` status; they're
  counted because non-superseded, not because COMMITTED).
- **The docs are aspirational pointers:** `pipeline/products/README.md:3` literally says the 25 products
  "are built and run on server2 … This directory is a pointer." `patalaorg/runs/server2-post-c1-spine/`
  **does not exist** (patalaorg absent from this machine's expectation — it IS at `/root/projects/patalaorg`).
  `site/works/` pages are empty placeholders. CONTEXT-REVIEW-3.md:78 confirms `/dev/sdb` was 100% full
  (disk-exhaustion blocked PG→JSONL export). Both sites are built but NOT deployed.
- **The spine is not running autonomously now** — no active scheduler/heartbeat (`factory_loop.sh:37` only
  runs `T1,ARGMAP,L0,L2,L200,C1`; `BUILD-GATE-INFRA.md:71` marks "THEME/ESSAY/EDUCATION in the loop: ⚠️ PARTIAL").

**Bottom line:** the mechanism is present + runnable (workers + deps + registry all local), but it has NOT
been run to real post-C1 output. Committed SYNTHESIS/ESSAY/EDUCATION are empty, the gates above THEME
haven't produced objects, and the "server2" split is a **documentation fiction on this machine** — everything
is local but essentially un-executed for the post-C1 layers. Honest status: **a fully-built, locally-runnable
mechanism spine that has produced ~11 non-promoted proposal objects, with the real post-C1 products at zero
and the blind-assessor/cite-contract/tension gates not built.**

## 8. KEY PATHS
- Spine driver: `/root/projects/patala/pipeline/build_plan.py`
- Layer DAG: `/root/projects/patala/pipeline/object_registry.py`
- Post-C1 handoff: `/root/projects/patala/migration/shared/HANDOFF-POST-C1.md`
- Dev plan (gates/kanban): `/root/projects/patala/migration/shared/DEV-PLAN-NEXT-AGENT.md`
- Workers: `theme_worker.py`, `essay_worker.py`, `education_worker.py`, `epistemic_worker.py`, `generative_worker.py` (in `/root/projects/patala/pipeline`); wiring `autonomy.py`
- Nyāya gate: `/root/projects/patala/machinelearning/research/patala_ml/nyayagate.py`
- Citecheck: `/mnt/HC_Volume_106427611/ip-graph/lib/scholar_review.py`
- Hermes exec: `/mnt/HC_Volume_106427611/ip-graph/lib/hermes_exec.py`
- E2E + site: `run-tantraloka-e2e.py` + `build-static-site.py` (in `/mnt/HC_Volume_106427611/ip-graph/scripts`)
- Education organism: `education.py`, `organism.py`, `misconception.py`, `pedagogy.py` (in `/mnt/HC_Volume_106427611/ip-graph/lib`), `specs/SPEC-20-EDUCATION-ORGANISM.md`
- Honest gold audit: `/mnt/HC_Volume_106427611/ip-graph/notes/GOLD-VALIDATION-NOTES.md`
