# translation — ORCHESTRATION (the agent runbook for the foolproof system)

*The definitive agent-facing manual for driving the translation system end-to-end, autonomously,
foolproof. This is the ONE page an agent reads to: see what's done/next/blocked, advance translation,
stay safe, and track everything. Everything is deterministic, gated, PROPOSE-only, and live.*

---

## 0. THE MENTAL MODEL (30 seconds)

```text
THE BRAIN      pipeline/patala_orchestration.py  (deterministic: next_action / work_state / progress)
THE ENGINE     pipeline/factory_scheduler.py      (DAG controller: streamed, bounded, low-RAM)
THE GENERATOR  pipeline/canonical_translate.py    (Hermes reads the file -> JSONL per record -> gate)
THE TRUTH      data/corpus/registries/*.jsonl     (committed, versioned, idempotent)
THE SURFACE    /openpatala/translation*  +  MCP    (live progress, compiled bytes)
```

**The one law:** Hermes only PROPOSES; a deterministic validator gates; a human + the factory advance.
You never guess what's next — you ASK the brain, then run the engine.

---

## 1. SEE THE STATE (always ask first, never guess)

```python
from patala_orchestration import progress_summary, work_state, next_action, eligible_next
eligible_next(10)          # the works you can legally advance now  -> [{work_id, next_action}]
work_state("kramasadbhava") # committed counts + next_action + blocked reason + source
next_action("ipvv")         # the deterministic next step (never an LLM judgment)
```
Or over MCP: `patala_next_action` · `patala_get_work_state` · `patala_get_translation_progress`.
Or HTTP: `GET /openpatala/translation` / `GET /openpatala/translation/{work_id}` (compiled bytes, live).

**Read it as:** `eligible_for_agent3: true` + `next_action` = you may advance this work. `blocked: true`
+ `reason` = do NOT force it (e.g. `BUILD_L0_SOURCE_MODE_REQUIRED` = the source floor isn't ready).

---

## 2. ADVANCE TRANSLATION (the gated flow)

### 2.1 One work through the canonical generator (the proven path)
```bash
cd /root/projects/patala
python3 pipeline/canonical_translate.py --work kramasadbhava --verses kramasadbhava:v2   # produce + commit
python3 pipeline/canonical_translate.py --work kramasadbhava --verses kramasadbhava:v2 --dry-run  # no model
```

### 2.2 The factory (autonomous, low-RAM, one pass)
```bash
cd /root/projects/patala
setsid nohup env PATALA_COMPILE_ON_COMMIT=1 FACTORY_PARALLEL=3 \
  python3 pipeline/factory_scheduler.py --works <work> --max-model-calls 6 --throttle 1 \
  > /tmp/opencode/factory-pass.log 2>&1 &
```
- **ONE owner at a time** — never run a second scheduler while one is running (or the overnight loop).
- Backgrounded (`setsid … &`) per the no-timeout doctrine; poll the log, never block.
- `PATALA_COMPILE_ON_COMMIT=1` makes progress live to all agents after the pass.

### 2.3 The overnight loop (fully autonomous)
```bash
bash pipeline/start_overnight.sh start     # both drivers + cron watchdogs, unattended
bash pipeline/start_overnight.sh status
```

---

## 3. STAY SAFE (the protection contract — non-negotiable)
- **PROPOSE-only:** you (or MCP) can ask and propose; you can NEVER accept/promote. Promotion is human.
- **Fail-closed:** a `GENERATION_FAILED` object never commits; abstain rather than fabricate.
- **Idempotent:** commits dedup by `input_hash` — re-running never double-commits
  (`factory_certificate.py` → 0 dup = healthy).
- **One owner:** one scheduler at a time; `FACTORY_PARALLEL ≤ 4`; background everything.
- **RAM-safe:** the brain + scheduler stream (never bulk-load a registry); check `free -h` before heavy work.

---

## 4. TRACK + AUTO-UPDATE (everything recorded + reflected — no duplication)
| Signal | Where |
|---|---|
| live per-verse output | `data/corpus/downloads/t1-stream.jsonl` |
| per-pass summary | `/tmp/opencode/factory-loop.log` |
| per-work progress (live) | `site/openpatala/translation.json` + the API/MCP |
| idempotency health | `python3 pipeline/factory_certificate.py` |
| committed counts | `python3 pipeline/factory_status.py --all` |
| derived next_action + ledger/bib refresh | `python3 pipeline/translation_state.py --refresh` |

**The state-refresh keeps everything consistent after a commit** (derived from actual counts, never guessed):
```bash
python3 pipeline/translation_state.py --refresh   # derive next_action + write ledger + recompile bib/projection
```

**Agent handover queue (the translation kanban board):**
```bash
hermes kanban boards switch translation    # one card per work: ready→running→review→done
hermes kanban list                          # claim a card, advance it, hand over
```
Each card body tells the agent how to advance that work (`translation_supervisor.py --advance --work <work>`).

**The full loop (translate → track → update → hand over, all gated):**
```text
supervisor --advance → the factory runs (Hermes) → committed objects
      → translation_state --refresh → ledger next_action + bibliography + projection recompiled
      → compile-on-commit → served translation.json is live
      → the kanban board → agents claim/advance/hand over; no duplication
```
Every object is immutable + versioned + idempotent (`input_hash` dedup); nothing double-commits.

---

## 5. THE GATES (the definition of done — never skip)
Run before claiming anything works:
```bash
cd /root/projects/patala
python3 pipeline/test_canonical_translate.py          # 10/10 deterministic (no model)
python3 pipeline/test_patala_orchestration.py         # 5/5 deterministic (no model)
python3 pipeline/test_factory_scheduler.py            # canonical-DAG ALL PASS
cd /root/projects/patalaorg && python3 check.py --refs --naming --manifest   # the doc gate
```

---

## 6. A WORKED EXAMPLE (the full autonomous loop)
```python
from patala_orchestration import eligible_next, work_state
candidates = eligible_next(5)                 # the works you may advance
assert candidates["count"] > 0, "nothing eligible — check for ACQUIRE_SOURCE/BUILD_L0 first"
work = candidates["eligible"][0]["work_id"]   # e.g. "ipvv" -> GENERATE_TRANSLATION
print(work_state(work))                        # confirm committed counts + next_action
# then run the factory on it (backgrounded, gated):
#   setsid nohup env PATALA_COMPILE_ON_COMMIT=1 FACTORY_PARALLEL=3 \
#     python3 pipeline/factory_scheduler.py --works <work> --max-model-calls 6 --throttle 1 \
#     > /tmp/opencode/factory-pass.log 2>&1 &
# then verify: factory_certificate 0 dup + committed counts grew + translation.json refreshed.
```

---

## 7. THE FALLBACK LADDER (if something fails, in order)
1. Model output → the canonical JSONL + adaptive chunking self-heal. 
2. Validation → fail-closed to retry/rejected (never a silent pass).
3. Orchestration → one-owner / bounded RAM / background.
4. Infra (disk/PG/R2) → R2 + JSONL fallback + free disk.
5. A documented decision → follow it; do NOT re-solve it.

**Meta-rule:** if you're about to "patch the factory by hand", STOP — the canonical path already handles
it. Read `../FALLBACKS.md` (if it exists) / this runbook.

---

*This is the agent runbook. Wire mechanics: `reference.md`. Semantics: `model.md`. Recipes: `recipes.md`.
Build order: `DEV-PLAN.md`. Everything here is the current working implementation, gated + live.*
