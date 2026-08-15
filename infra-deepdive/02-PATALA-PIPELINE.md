# INFRA DEEP-DIVE 02 — THE PATALA TRANSLATION PIPELINE

*2026-08-15 · a full-context audit of the working repo `/root/projects/patala` (remote `prx0r/patala`,
branch `agent2`). The RAW→C1 translation DAG, the E2E harness, the skills, the autonomous loop, the state
and runs, and the MCP verbs — with the honest verdict on whether "RAW→C1 proven repeatable" holds.*

---

## 1. THE DAG — what is REAL vs DOCUMENTED
**Canonical manifest** `contracts/CANONICAL-DAG.yaml:19-42` (the declared source of truth):
```
SOURCE → T1 → L0 → [ARGMAP] → L2 → L200 → C1 → THEME/ARGUMENT → SYNTHESIS → ESSAY → EDUCATION
```
Scheduler (`pipeline/factory_scheduler.py:43-44`):
```python
LAYER_ORDER = ["T1", "ARGMAP", "L0", "L2", "L200", "C1"]   # L1 absent
MODEL_LAYERS = {"T1", "ARGMAP", "L2", "L200", "C1"}        # L0 deterministic free-draining
```

### ⚠️ THE L1 INCONSISTENCY (a real, unresolved bug)
`L1` appears in the **live-run-4/5 READMEs** and in `test_full_chain_timing.py:24`, but is **NOT** in
`CANONICAL-DAG.yaml`, **NOT** in `factory_scheduler.py` (LAYER_ORDER), and is only wired as a handler
(`autonomy.py:144-150`) — never scheduled. **Two DAG definitions coexist** — the exact "three competing
DAG definitions" problem `A2-ARCH-HARDEN` claimed to have fixed.

### Per-layer reality (generators wired in `autonomy.py:107-216`)
| Layer | Type | Evidence |
|---|---|---|
| **T1** | BATCHED MODEL (1 call/many verses, `chat_agentic`) | `t1_worker.py:477-492` `canonical_t1_generator`; Hermes reads file + emits JSONL (`:394`). |
| **L0** | DETERMINISTIC free-draining, no model | `l0_worker.py:34-71` Vidyut RAW-L0; gloss enrichment OFF by default (`PATALA_GLOSS_ENRICH!=1`). |
| **L1** | DETERMINISTIC scaffold | `l1_l2_worker.py:38-71` controlled segments from L0; enrichment optional/off. |
| **ARGMAP** | BATCHED MODEL (`extract-argmap` skill) | `argument_map_worker.py:117-193` (`argmap_generator_batched` default, `:228-232`). |
| **L2** | BATCHED MODEL (`translate-reading` skill) | `l1_l2_worker.py:171-245` (`l2_generator_argmap_guided`). |
| **L200** | MODEL bounded-classifier (deterministic scaffold + constrained classify) | `l200_worker.py:164-209`; `chat` classifies candidates, `IGNORE` default (`:88-147`). |
| **C1** | MODEL batched JSONL via `chat` | `c1_worker.py:113-181` (`c1_generator_batched`). |
| **L1L2** | Legacy combined path, NOT in scheduler/DAG | `l1_l2_translate.py:136-186`. |

## 2. THE E2E TEST HARNESS (the formal test)
- **`pipeline/test_full_chain_timing.py`** — the integration test. Runs each layer in DAG order
  (`LAYERS=[T1,L0,L1,ARGMAP,L2,L200,C1]`, line 24) via the real factory path `FB._produce_layer`, times
  each, counts model calls via a `CallCounter` wrapping `model.chat` + `model.chat_agentic` (50-74),
  validates + commits, writes `/tmp/opencode/e2e-trace.json`. Invoke: `python3 pipeline/test_full_chain_timing.py --work kramasadbhava`.
- **`pipeline/prove_full_chain.py`** — anti-theatre read-only proof: prints each committed layer's content
  + the gating validator for a `(work:loc)`. No model calls. `LAYERS=[T1,L0,ARGMAP,L2,L200,C1]` (no L1).
  Exits 1 if any layer missing.
- **`pipeline/trace_object.py`** — machine-readable C1→RAW audit for one `--oid`: per-layer validator,
  status, input_hash, content (`CHAIN` incl. L1). Returns `chain_ok`.

### ⚠️ A LIVE RUN OF THE E2E (the honest, current behavior)
Running the harness on THIS machine on 2026-08-15:
```
RAW: sarvenokteṣvagamyam vai ... ||1/50||
  T1   47.6s  1 api calls  committed=1  OK
  L0    0.1s  0 api calls  committed=1  OK
  L1    0.1s  0 api calls  committed=1  OK
  [OOM-KILLED here]
EXIT_CODE=137 (SIGKILL)   # dmesg: global_oom ... anon-rss:4584252kB (4.5GB) on a 7.6GB box, 4.0GB avail
```
**The E2E did NOT complete on this machine** — it committed T1/L0/L1 (~48s) then was OOM-killed during
ARGMAP. This **contradicts the "RAW→C1 proven repeatable" claim in the current environment.** Two more
honest caveats baked in: the api-call counter **under-counts** (L200/C1 import `chat` at module load, not
through the wrapped `model.chat` — the run READMEs admit this), and live-run-3's README records that
**L2/L200/C1 did NOT commit** on the harness test object (a "harness linkage issue, not a pipeline failure").

## 3. THE SKILLS (at `/root/projects/patala/skills/` — there is NO `pipeline/skills/`)
List: `assemble-stack, autonomous-layer, canonical-translate, extract-argmap, patala-translate, push-text,
raw-l0, translate-passage, translate-reading, translate-work, use-api, validate-passage, write-commentary`.

| Skill | What the model is told | File-reading? | Rigid vs intelligent |
|---|---|---|---|
| **canonical-translate** (`SKILL.md:13-60`) | READ the work's Sanskrit from a FILE PATH, emit JSONL per verse, adaptive chunk-halving | ✅ path is the mechanism | Intelligent + file-reading; deterministic assemble/gate on `.py` |
| **extract-argmap** (`:19-52`) | READ the real passage (Sanskrit + T1 + L0) yourself, reason out 4 sections | ✅ reads gold exemplars at `/root/sanskritree/...` | Explicitly intelligence-based ("no rigid template") |
| **translate-reading** (`:18-40`) | READ real L1 + ARGMAP `decision_for_l2`, render philosophically-grounded prose | ✅ reads L1 + ARGMAP | Intelligence-based (the 0.118 fix) |
| **patala-translate** (`:15-63`) | OLDER A3 loop: read ledger, `batch_translate.py` → L0 glosses + close translations via `hermes -z`, whole batch one call | ✅ ledger + files | Agentic loop |
| **raw-l0** (`:26-160`) | Deterministic RAW-L0 (Vidyut) → propose glosses + self-challenge → validate with `validate_l0_spec.py` | ✅ | Hybrid |
| **translate-passage** (`:20-79`) | OLD hand-flow `T1→R1→T2→R2→T3→T3.1→C1` (different layer names, NOT the factory DAG) | some | Legacy — documents a DIVERGENT DAG |
| **validate-passage** (`:20-52`) | Run `validate.py --report` | no | Deterministic |

**Takeaway:** the live model layers (T1/ARGMAP/L2) are **intelligence + file-reading based** (Hermes reads
the batch file with its file tool), not rigid templates — consistent with the `chat_agentic` (file-access)
invocation. The skills are the HOW-TO that the model reads.

## 4. THE AUTONOMOUS LOOP
`pipeline/translation_supervisor.py` is the self-driving brain:
- `advance()` (72-108) deterministically picks a work (requires a committed T1 floor, `:84-89`) then shells
  out `[sys.executable, "pipeline/factory_scheduler.py", "--works", <work>, "--max-model-calls", N, "--throttle", "1", "--per-layer", "2"]`
  (cwd `/root/projects/patala`, detached `subprocess.Popen`; env sets `PATALA_COMPILE_ON_COMMIT=1
  PATALA_T1_GATE=1`).
- It is **PROPOSE-only** — it never accepts/promotes.
- `factory_scheduler.py` spends the model budget per work, one at a time in target-priority order (`:244-245`),
  batching same-work verses, running generators in parallel via `ThreadPoolExecutor` (`:319-329`), committing serially.

### The exact Hermes invocations (`pipeline/model.py`)
- Non-agentic `chat`: `hermes -z <prompt> -m deepseek-v4-flash --provider opencode-go` (line 93).
- **Agentic `chat_agentic`** (used by T1/ARGMAP/L2): `hermes chat -Q -q <prompt> --yolo --max-turns N -m
  deepseek-v4-flash --provider opencode-go [--skills <S>]` (164-167).
- Both run with `start_new_session=True`, process-group-killed on timeout (`:40-63`, `:176-181`).

## 5. STATE + RUNS
### `data/ops/FLAWS.md` — the honest counter-evidence (12 items; read BEFORE trusting any "it works")
- **#1 Biggest flaw:** "we built enormous infra but shipped almost no scholarly output" — kramasadbhava C1 on only ~10/248 passages.
- **#2 Whole-chain over-claimed:** model does NOT reliably emit strict per-layer JSONL at batch ≥2; the "8 distinct C1" were largely pre-existing (v1–v4 already existed).
- **#3 Batched ARGMAP proven in isolation, scheduler integration NOT** (scheduler hung at 96% CPU).
- **#4 One-owner discipline failed repeatedly** — the guard is advisory, not enforced in `factory_scheduler.main()`.
- **#5 Weak validators** — presence/import checks gamed by pre-existing objects; whole-chain committed "junk records" (v1 C1 = "source is empty") as GENERATED.
- **#6 Metrics measure the EASY layer (L0)**, not the ARGMAP→C1 bottleneck.
- **#7 Gold scoring Jaccard = 0.091 — meaningless.**
- **#8 Verse-recovery gap still open** (tantraloka empty SOURCE) — never fixed.
- **#9 Shallow observability** — no quality signal.
- **#10 Docs misrepresent reality** (aspirational).
- **#11 Reliance on unreliable model JSONL behavior.**
- **#12 No shipped, human-reviewed scholarship** — nothing passed the final gates.
> Bottom line (verbatim): "We built a large, real, mostly-working INFRASTRUCTURE ... but the goal (a full
> work to C1, tracked and gated) is NOT met."

### Live runs (what each actually claims)
- **Run 1:** L0 drain 168→180 (+12, 0 model calls), ~550MB stable. Proves L0 (the easy layer).
- **Run 2:** L0 198→217 (+19), full chain "populated to 10 passages."
- **Run 3:** First E2E RAW→ARGMAP timing — **but L2/L200/C1 did NOT commit** on the harness object ("harness linkage issue").
- **Run 4:** Repeatable RAW→C1 (T1 39.7s, L200 28.9s, C1 152.1s, total 247s). First claimed full-chain commit.
- **Run 5:** The "milestone" — ARGMAP-guided RAW→C1, all 8 layers, 412s / 3 api calls, `trace_object`
  C1→RAW `CHAIN OK: True` on `kramasadbhava:v132`.
> **Counter-evidence from MY live run:** the harness **OOM-killed during ARGMAP** on this machine — so
> "RAW→C1 proven repeatable" does NOT hold in the current environment.

### Factory registry state (`data/corpus/registries/*.jsonl` line counts)
- `source-registry`: **1,312,882** (the giant SOURCE layer) · `t1`: 631 · `l0`: 947 · `l1`: 7 · `l1l2`: 12 ·
  `argmap`: 79 · `l2`: 22 · `l200`: 86 · `c1`: 76 · `theme`: 1 · `argument`: 10.
- **kramasadbhava specifically:** T1 282, L0 248, **L1 7, L2 22, L200 22, C1 13** (of 248 passages) — the
  upper chain is the THIN part (consistent with FLAWS #1).
- There is NO `data/factory` dir; the "factory" is `data/corpus/registries/` + `factory-audit.jsonl` + `factory-failure-queue.jsonl`.

## 6. THE MCP VERBS (`mcp/index.mjs:468-513`)
All four call the deterministic orchestration brain via `spawnSync("python3", pipeline/patala_orchestration.py,
...)`, PROPOSE-only (never accept/promote):
- **`patala_next_action`** (478-486) → `--next <work>` → `patala_orchestration.next_action()` (79-90): ledger →
  `next_action/eligible_for_agent3/blocked/reason`. Deterministic, no LLM.
- **`patala_get_work_state`** (487-495) → `--state <work>` → `work_state()` (58-76): status + source + committed counts (T1/ARGMAP/L0/L2/L200/C1) + next_action + blocked.
- **`patala_get_translation_progress`** (496-504) → `--summary [--limit]` → `progress_summary()` (93-114): whole-corpus per-work progress.
- **`patala_get_ops_status`** (505-513) → Atlas `GET /openpatala/status` → `ops_status.py` (97-110): live processes + per-layer counts + queue + build-plan done/total.
> **⚠️ IMPORTANT:** this MCP server is a **standalone stdio server** (`node /root/projects/patala/mcp/index.mjs`)
> — it is **NOT registered in Hermes or any opencode config**. See 03-HERMES for how to use it.

## 7. BOTTOM LINE — does "RAW→C1 proven repeatable" hold?
**No, not in the current state — and the repo's own honest docs agree.** Concretely:
1. **The DAG is not a single DAG** — `L1` sits in the test/live-run DAG but not the manifest/scheduler.
2. **The E2E OOM-kills during ARGMAP** (4.5GB RSS, 7.6GB box) ~48s in — the current machine cannot complete the chain.
3. **Committed scholarly output is thin:** kramasadbhava C1 on 13/248, L2 on 22/248.
4. **`FLAWS.md` explicitly states** the goal is NOT met, whole-chain is unreliable at scale, ARGMAP
   integration is unproven, validators were weak, gold scoring is meaningless (Jaccard 0.091), and nothing passed the human gate.

**The infrastructure is real and substantial** — the gap is EXECUTION (OOM + rate-limit), GOLD scoring, and
the human gate, not missing machinery.
