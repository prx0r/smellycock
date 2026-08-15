# translation — REFERENCE (wire mechanics)

*The wire mechanics of the translation layer: the factory scheduler CLI, the canonical generator CLI, the
Atlas API endpoints, the MCP tools, the env switches, and the gates. Semantics in `model.md`. How-to in
`recipes.md`. Everything below reflects the current working implementation.*

---

## 1. THE FACTORY (the orchestrator)

### 1.1 The scheduler CLI — `pipeline/factory_scheduler.py` (deterministic DAG controller)
```bash
cd /root/projects/patala
python3 pipeline/factory_scheduler.py --queue                         # read-only priority preview
python3 pipeline/factory_scheduler.py --works kramasadbhava --max-model-calls 6   # one DAG pass
```
| Arg | Default | Meaning |
|---|---|---|
| `--works` | all registered | comma-separated work ids, or `--works <id> --queue` |
| `--layers` | `T1,ARGMAP,L0,L2,L200,C1` | layers to schedule |
| `--max-model-calls` | 6 | model-call budget per pass |
| `--throttle` | 0 | seconds between chunk commits (gentle pacing) |
| `--per-layer` | 2 | deterministic jobs per layer per pass |
| `--max-works` | 0 (all) | cap the works enumerated |
| `--retry` | — | retry durable failures first |
| `--queue` | — | read-only ordered preview (no production) |

**Env:** `PATALA_T1_CANONICAL=1` (use the canonical generator) · `PATALA_TURN_VERSES` (8) ·
`PATALA_MAX_ELIGIBLE` (20000) · `PATALA_MAX_WORKS` (0=all) · `FACTORY_PARALLEL` (≤4) ·
`PATALA_CONTEXT`/`PATALA_INPUT_FRAC`/`PATALA_FACTORY_BATCH_MAX`/`PATALA_FACTORY_CHUNK`.

### 1.2 The canonical generator CLI — `pipeline/canonical_translate.py`
```bash
python3 pipeline/canonical_translate.py --work kramasadbhava --verses kramasadbhava:v2      # produce + commit
python3 pipeline/canonical_translate.py --work kramasadbhava --verses kramasadbhava:v2 --dry-run  # segment only
```

### 1.3 The overnight loop — `pipeline/start_overnight.sh`
```bash
bash pipeline/start_overnight.sh start     # both drivers + cron watchdogs
bash pipeline/start_overnight.sh status    # what's running
bash pipeline/start_overnight.sh stop      # stop the factory loop
```

---

## 2. THE ATLAS API (translation status — served as compiled bytes)

Base: dev `http://localhost:8787` · prod `https://patala.tradesprior.workers.dev/`

| Endpoint | Returns | Caching |
|---|---|---|
| `GET /openpatala/translation` | every work's T1/L2/C1 ledger status + `next_action` + committed layer counts | ETag/304 + `immutable` |
| `GET /openpatala/translation/{work_id}` | one work's record; `?select=work_id,committed` projects | ETag/304 + `immutable` |
| `GET /openpatala/translation/{work_id}/content` | one work's **committed translation CONTENT** — T1 glosses, L2 readings, L200 audits, C1 commentaries (`?select=C1`) | ETag/304 + `immutable` |
| `GET /openpatala/translation/latest` | short-TTL pointer to the current projection | `max-age=300` |
| `GET /works/{work_id}/bundle?depth=2` | the work bundle incl. its `translation` record | ETag/304 + `immutable` |
| `GET /works/{work_id}?select=translation` | the bibliography record's `translation` block (committed counts + content, via `enrich_bibliography`) | ETag/304 + `immutable` |

**Bibliography↔translation linkage:** `pipeline/enrich_bibliography.py` adds `rec['translation'] =
{status, committed: {layer: count}, has_content}` to every work record (streamed, low-RAM), so the
bibliography and the site surface committed translation without a separate lookup.

**Envelope:** `{ "data": …, "provenance": { "api_version", "surface", "served": "compiled-bytes" } }`.
**Errors:** `{ "error": { "code", "message", "retryable" } }` (see `model.md` §tracking / `errors` in the
Atlas surface).

---

## 3. THE MCP TOOLS — `mcp/index.mjs` (patala profile)

| Tool | Description |
|---|---|
| `get_translation_status` | the whole corpus translation status (compiled bytes, one call) |
| `get_translation_status_for_work` | one work's status; `work_id` required |
| **`patala_next_action`** | the **deterministic** next legal action for a work (ledger, PROPOSE-only) |
| **`patala_get_work_state`** | one work's full state: ledger status + committed counts + source + next_action |
| **`patala_get_translation_progress`** | the whole-corpus progress summary (per-work next_action + counts) |

Env: `ATLAS_API_BASE` (default `http://localhost:8787`) for the read surface; the `patala_*` orchestration
verbs call `pipeline/patala_orchestration.py` directly (deterministic, low-RAM, PROPOSE-only — never
accept/promote).

## 4. THE DETERMINISTIC ORCHESTRATION BRAIN — `pipeline/patala_orchestration.py`

The single surface an agent uses to drive translation without touching files or guessing:
```bash
python3 pipeline/patala_orchestration.py --state kramasadbhava   # full work state (committed + next)
python3 pipeline/patala_orchestration.py --next kramasadbhava    # the deterministic next action
python3 pipeline/patala_orchestration.py --summary               # whole-corpus progress (one call)
python3 pipeline/patala_orchestration.py --eligible 10           # the works an agent can advance
```
**PROPOSE-only:** it reports what should happen; promotion is a human + factory action. Tested by
`pipeline/test_patala_orchestration.py` (5/5 deterministic).

## 4b. COMPILE-ON-COMMIT — the projection is LIVE

`ip-graph/scripts/compile-translation-status.py` rebuilds **only** `translation.json` (fast, streaming,
low-RAM) — not the whole site. Wired into `factory_scheduler` (`PATALA_COMPILE_ON_COMMIT=1`), so after a
pass commits, agents/servers see live progress.

## 4c. THE LIVE QUALITY GATE (the verifiable reward — STOLEN from dgm/herdr, now real)

`pipeline/translation_gate.py` — the **deterministic** quality gate that runs on a T1 proposal without a
model. Computes `SOURCE_COVERAGE` / `SOURCE_BINDING` / `ABSTENTION` / `TERM_CONSISTENCY`, returns a
verifiable reward score (0-1) + `PASS`/`BLOCK`. Wire it: `PATALA_T1_GATE=1` in `factory_batch` → any T1
that fails the gate is BLOCKED (retryable), never committed. Tested 6/6 (`test_translation_gate.py`).
This is the `translation.py` TranslationProof + dgm verifiable-reward made a live production gate.

---

## 4. THE GATES (the definition of done — never skip)

| Layer | Gate (validator) | File |
|---|---|---|
| T1 | `t1_validator` (shape + source-bound + `[and]-` grammar + provenance) | `pipeline/t1_worker.py` |
| L0 | `verify_l0.p0_proof` + `validate_l0_spec` (schema + P0 + abstraction-honesty) | `pipeline/verify_l0.py`, `validate_l0_spec.py` |
| ARGMAP | ARGMAP validator | `pipeline/argument_map_worker.py` |
| L2 | L2 validator | `pipeline/l1_l2_translate.py` |
| L200 | L200 8-section audit | `pipeline/l200_worker.py` |
| C1 | C1 validator | `pipeline/c1_worker.py` |

**Fail-closed:** a `GENERATION_FAILED` proposal NEVER commits. Abstention (empty gloss / `AMBIGUOUS`) is
valid; fabrication is not.

---

*Wire mechanics only. What the objects MEAN: `model.md`. How to use it: `recipes.md`. How agents drive it:
`agentic.md`. What's next: `extension.md`.*
