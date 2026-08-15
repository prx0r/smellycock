# translation — the LAYER (complete)

*The translation layer — the production spine `SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1`. This layer is
**comprehensive and complete**: agentic docs, references, features, recipes, and extensions — structured
like Hermes's own documentation. Every doc reflects the **current working implementation** (real files +
real code + live gates), and everything not yet implemented is specced precisely in `extension.md`.
Production code lives in `/root/projects/patala/`.*

> **ACTIVE TRANSLATION BUILD = the KANBAN build** (`pipeline/kanban_translation.py` + `layer_agent.py`) — a
> durable, resumable, auditable work queue driven by per-layer agents. **Read `BUILDS.md` for the canonical
> comparison + why the kanban build is best (the others are SUPERSEDED / building blocks).**

---

## 0. LAYER-COMPLETION PROTOCOL (what "comprehensive" means — this is the bar for EVERY layer)

A layer is COMPLETE when it has ALL of:
| # | Artifact | Where | Present? |
|---|---|---|---|
| 1 | **Reference (wire)** — endpoints, CLI, MCP, env, gates | `reference.md` | ✅ |
| 2 | **Model (semantics)** — DAG, object shapes, JSONL, registry, authority, tracking | `model.md` | ✅ |
| 3 | **Recipes (how-to)** — run, monitor, recover, validate, use | `recipes.md` | ✅ |
| 4 | **Agentic** — how an agent drives it (Hermes calling, skills, JSONL contract, safety) | `agentic.md` | ✅ |
| 5 | **Extensions** — how to extend + NOT-IMPLEMENTED roadmap + patterns to borrow | `extension.md` | ✅ |
| 6 | **Working code** — every doc resolves to a real file + real gate | this README + the code | ✅ |
| 7 | **Registered + validated** — MANIFEST entry + `check.py` passes | `MANIFEST.json` | ✅ |

A layer is NOT complete until 1-7 all hold. **Do not advance to the next layer until this passes.**

---

## 1. THE DOC MAP (read in order)

| Doc | What it is | Read when |
|---|---|---|
| **this README** | the layer index + completion protocol + state | orienting |
| **`ORCHESTRATION.md`** | **the agent runbook** — see state, advance, stay safe, track (the one page agents read) | driving it as an agent |
| **`BUILDS.md`** | **the build review** — the kanban build (best/production) + the full comparison | deciding which build |
| `reference.md` | the wire mechanics — factory scheduler CLI, canonical generator, Atlas API endpoints, MCP tools, env, gates | you're calling it |
| `model.md` | the semantics — the DAG, object shapes, JSONL contract, registry/ledger, authority, tracking | you need to know what an object/field means |
| `recipes.md` | concrete how-to — run, monitor, recover, validate, use the API/MCP | you want a "do this" recipe |
| `agentic.md` | how an agent drives it — Hermes calling, skills, the JSONL contract, safety, tracking | you're an LLM/agent |
| `extension.md` | how to extend — extension ideas, the NOT-IMPLEMENTED roadmap, and the git-clone patterns to borrow | you're planning the next increment |

---

## 2. CURRENT STATE (honest, verified)

**WORKS (real + gated):**
- Factory DAG (T1 597 · L0 796 · ARGMAP 50 · L2 3 · L200 67 · C1 66; 111-work ledger). **Counts are live —
  stream `pipeline/factory_status.py --all` for the current state.**
- **THE ASSEMBLY-LINE FACTORY** (the production driver): `factory_scheduler.py` batches into chunks of 50
  (`PATALA_FACTORY_CHUNK=50`) with `FACTORY_PARALLEL=4` — **~1 model call per 50 verses** (the 1M-context
  win), per-layer queues, `--retry`. OOM fixed: `factory_batch._source_objects` streams the SOURCE
  registry (was the 4.5GB `R._load("SOURCE")`). Run via `factory_long.sh` (logged to `log5long.log`).
- **Canonical T1 generator** (`pipeline/canonical_translate.py` + `t1_jsonl.py`) — JSONL contract,
  adaptive chunking. `test_canonical_translate.py` **10/10 + real-Hermes smoke PASS**.
- **Low-RAM scheduler** (`pipeline/factory_scheduler.py`) — streamed + bounded, **1.85GB → 124MB**,
  `test_factory_scheduler.py` ALL PASS.
- **openpatala integration** — `compile_translation_status()` → `translation.json` → served by the Atlas
  API (`/openpatala/translation*`) + MCP (`get_translation_status*`).
- **Benchmark + projector** — `translation_db.py` (JSONL progress registry, model-tagged) ·
  `benchmark_translation.py` · `project_translation.py` (the estimator) · `/benchmarks` dashboard.

**NOT-IMPLEMENTED (specced in `extension.md`):** compile-on-commit, translation-*content* surface, live
validation gate, the three-version flow (R1/T2/R2), the council/adversarial-review pattern, the
verifiable-reward self-improvement loop.

---

## 3. THE NON-NEGOTIABLES (this layer, from `AXIOMS.md`)
1. **Hermes for GENERATION, .py for REDUCTION** — never hand-feed a validator, never fabricate both sides.
2. **Eligibility is deterministic Python, never an LLM judgment.**
3. **Fail-closed, validate-first** — wrong is worse than none; abstain rather than fabricate.
4. **The gate is done, not a file existing.**
5. **Compute on write, read from bytes** (ETag/304 + immutable; one question = one request).

*This layer is complete per the protocol. The next layer starts only when this one's 7 artifacts all hold.*
