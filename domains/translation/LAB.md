# The TRANSLATION SCIENCE LAB — spec + README

*2026-08-15 · a durable, reproducible experiment framework for optimizing each translation layer. Make a
hypothesis per layer → run it on a FIXED test set under a CONFIG → measure → compare → keep the winner.
Every run is a named, labeled experiment stored durably + tracked on a kanban board.*

---

## 1. THE EXPERIMENT NAMING FORMAT (every run has a stable id)
```
EXP-<LAYER>-<config_key>-<data_hash>-<ts>
  e.g. EXP-T1-t1-batch-chars-500-abc123def456-20260816T001159
```
- `<LAYER>` — the layer (T1, ARGMAP, L2, L200, C1, ...).
- `<config_key>` — which hypothesis config ran (from the matrix below).
- `<data_hash>` — the content hash of the FIXED test set (so we know exactly which data).
- `<ts>` — timestamp (uniqueness).
- **Labeling:** every run record carries `experiment_id, layer, model, config, config_key, data_hash,
  verses, time_s, calls, committed, rejected, verses_per_100s, sec_per_verse` — fully traceable.

## 2. THE FIXED TEST SET (reproducible data)
- Deterministic: kramasadbhava's first N verses via `_source_objects` (the verse-recovery path).
- Content-hashed → the `data_hash` — every experiment runs on the SAME verses, so results are comparable.
- `TEST_WORK=kramasadbhava`, `TEST_N=20` (configurable).

## 3. THE CONFIG / HYPOTHESIS MATRIX (what we test per layer)
| config_key | hypothesis |
|---|---|
| `t1-batch-verses` | batch by N verses/call |
| `t1-batch-chars-500` | **batch by ~500 chars** (the "don't load by verse, load by chars" idea) |
| `t1-batch-chars-2000` | batch by ~2000 chars |
| `t1-no-stream` | agentic path (vs `-z` stream) — the stream speedup |
| `t1-pro` | deepseek-v4-pro vs flash |

Each can be parameterized further: `{model, batch_mode (verses|chars), batch_n, batch_chars, vidyut, stream}`.

## 4. DURABLE INFRA (kanban + registry + logs)
- **Registry** (the truth, per AXIOM 5): `data/corpus/registries/experiments.jsonl` — streamed append,
  every experiment a row, git-able.
- **Kanban** (`experiments` board): one card per experiment (`EXP-...`), durable + resumable — claim → run
  → complete. The board IS the experiment tracker.
- **Logs**: each experiment prints its result + is stored in the registry; the `--report` view compares.

## 5. HOW TO RUN (the science method)
```bash
# list the hypotheses
python3 pipeline/experiment_lab.py --list-configs
# run one hypothesis on the fixed test set (creates a named experiment + kanban card + registry row)
python3 pipeline/experiment_lab.py --layer T1 --config t1-batch-chars-500
# compare all logged experiments (time / calls / throughput / sec-per-verse)
python3 pipeline/experiment_lab.py --report
# watch the experiment board
hermes kanban --board experiments list
```

## 6. WHAT TO TEST NEXT (the open hypotheses per layer)
- **T1**: batch-by-chars (500/2000) vs by-verses · stream vs agentic · flash vs pro · with vs without Vidyut.
- **ARGMAP**: skill vs inline prompt · flash vs pro.
- **L2**: argmap-guided prose · pro (quality-critical).
- **L200**: a cheap/fast model (bounded classifier) vs flash.
- **C1**: pro (the final scholarly product).

## 7. BOTTOM LINE
> **The science lab makes per-layer optimization reproducible and durable: fixed data, named + labeled
> experiments, a registry + kanban + logs for the audit trail, and a compare view to keep the winner.**

*Source: `pipeline/experiment_lab.py`, `data/corpus/registries/experiments.jsonl`, the `experiments` kanban
board.*
