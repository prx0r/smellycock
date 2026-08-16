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

---

## HOW AN AGENT WORKS WITH THE LAB (the workflow)

The lab is for **deciding the best alternative for a stated end goal**. The agent drives it like this:

### Step 1 — state the end goal
The user/agent names the outcome, e.g. **"I want the fastest T1 build."** The goal defines WHICH axis to
optimize (speed, quality, cost) + for WHICH layer.

### Step 2 — review + design the experiment (which variants to test + why)
1. Look at the layer's profile (`layers/`) + `--plan <LAYER>` (the deal-radar's candidate models + why, and
   our deepseek baseline + pricing).
2. Enumerate the **hypotheses** that could change the outcome — the config knobs:
   - `batch_mode` (verses vs chars) + batch size  ← batching
   - `stream` (‑z vs agentic)                     ← the 5-10× speedup
   - `vidyut` (on/off)                            ← drop the Python pre-step
   - `model` (flash vs pro vs a deal-radar free)  ← model choice
   - `parallel` (multiple layer agents)           ← wall-clock multiplier
3. Pick the variants to test (each = one `experiment_lab.py` run).

### Step 3 — run the experiment
```bash
python3 pipeline/experiment_lab.py --layer T1 --config t1-batch-chars-500   # one variant
# or a sweep over the variants — each writes a named experiment + a kanban card + a registry row
```

### Step 4 — collect the hermes logs + results
- The **registry** (`experiments.jsonl`) has the strict result per run (time, calls, committed, sec/verse,
  v/100s).
- **`hermes logs`** captures the model-call activity (the per-call latency).
- The **`experiments` kanban board** shows each experiment's card.

### Step 5 — compare + pick the best alternative
```bash
python3 pipeline/experiment_lab.py --report   # the side-by-side (same fixed data)
```
Pick the winner on the goal's axis; record the decision + why in the layer profile. Re-run with new
hypotheses to iterate.

### The rule
> **Every claim ("X is faster") must be backed by a logged experiment on the SAME fixed data — never a
> feeling. If it isn't in the registry, it isn't decided.**

---

## THE EXPERIMENT REPORT (write one after EVERY experiment — machine-readable)

After every experiment run, the agent MUST write a structured report to `data/corpus/experiment-reports/`
(`EXP-<id>-report.json`), proving what the experiment showed. This is the fast, validatable reference for
future decisions.

### The report schema (machine-readable — a human + a validator can read it)
```json
{
  "experiment_id": "EXP-T1-t1-batch-verses-abc123-20260816T...",
  "layer": "T1",
  "goal": "fastest T1 build",              // the stated end outcome
  "config": { "model": "...", "batch_mode": "verses", "stream": true, "vidyut": true },
  "data": { "test_set": "kramasadbhava x5", "data_hash": "abc123" },
  "results": { "time_s": 85, "committed": 5, "calls": 1, "sec_per_verse": 17, "quality": 0.8 },
  "control_compared": ["EXP-T1-t1-batch-verses", "EXP-T1-t1-no-stream"],  // what it's compared to
  "finding": "bigger batch -> faster per-verse (5:22.6s/v, 10:10.2s/v)",
  "validated": true,                        // a validator re-checked the numbers
  "decision": "keep -z + one big batch + flash (fastest, 5/5 committed)"
}
```

### The instruction
1. **After every experiment**, write the report JSON (`experiment_id`, `goal`, `config`, `data`,
   `results`, `control_compared`, `finding`, `validated`, `decision`).
2. **Validate** it — a `.py` re-reads the numbers from the registry and confirms the `finding` matches.
3. Reference the report `id` in the layer profile + future decisions (fast recall).

### Why
- **Fast reference:** a future agent reads `EXP-<id>-report.json` → the decision + why + the validated
  numbers, without re-running.
- **Provable:** the `validated` flag + the registry cross-check mean a claim is reproducible, not a feeling.
- **Comparable:** `control_compared` links each experiment to the ones it beats/ties, building a decision
  graph over time.

---

## THE MINI-AGENT-LAB BEST PRACTICES (how an agent uses it autonomously)

This lab is a **self-driving experiment lab**: an agent states a goal, runs controlled experiments, writes
validated reports, and updates the factory config to the winner. These rules keep it rigorous + cheap.

### The autonomous loop
1. **State the goal** (e.g. "fastest T1 build") → the axis to optimize (speed/cost/quality) + the layer.
2. **Brainstorm the hypotheses** (batch size, stream, Vidyut on/off, model, parallel) — the config knobs.
3. **Run the control** on the FIXED gold test set (same data → comparable).
4. **Write the report** (`EXP-<id>-report.json`) — the schema above + `validated`.
5. **Integrate the winner** — update the factory defaults ONLY if the report justifies it; record the
   decision + why in the layer profile + `BUILDS.md`.
6. **Iterate** with the next hypothesis; never change a config without a report.

### The rules (non-negotiable)
- **Control variable:** every experiment runs on the SAME fixed test set (`sanskrit_gold` exemplars) —
  one variable changed at a time.
- **Validated reports:** every report has `validated: true` + a `.py` re-checks the numbers vs the
  registry. No report = no decision.
- **The factory reflects the winner:** the current config IS the experiment's winner (documented in
  `BUILDS.md`); change it only after a new report justifies it.
- **Burn-conscious:** model calls cost balance. Run ONE focused experiment at a time, on a SMALL test set;
  don't sweep blindly. Prefer the batch + cache-hit path (cheap).
- **Per-layer isolation:** you can troubleshoot/experiment on ONE layer without touching the others
  (independent workers/queues) — the factory keeps grinding.
- **Compare, don't assert:** "X is faster" only if a report shows it beats the control on the same data.
- **The report is the proof:** reference `EXP-<id>` in the layer profile + future decisions for fast recall.

### When to use it vs the factory
- **Use the lab** when deciding a config/model/batch choice (a controlled comparison).
- **Use the factory** (kanban daemon) to grind production once the config is decided.
- The lab gates what the factory runs — a config only enters the factory after a validated report.

*Source: `pipeline/experiment_lab.py`, `data/corpus/registries/experiments.jsonl`, the `experiments` kanban
board.*

## THE GOLD CONTROL (the control variable)
Every experiment scores against a **FIXED Sanskrit gold test set** (`pipeline/sanskrit_gold.py` — 8 IPVV
scholarly exemplars, organized by tradition). So results are comparable on the SAME data AND include a
**quality axis** (LLM-judge vs the gold), not just speed/cost.
```python
from sanskrit_gold import exemplars, gold_for, score_vs_gold, traditions
score_vs_gold(produced_text, "IPVV-V2F")   # 0-1 quality vs the gold
```
- **Control variable:** the same 8 exemplars reused for every experiment.
- **Per-tradition benchmarks (ours):** `TRADITIONS` (Pratyabhijñā/Trika, Krama, Śaiva Siddhānta) — assess
  frontier-model performance on specialist schools, not just general Sanskrit.

## THE CONTROL-LED WORKFLOW
1. Pick the **control golds** for the layer (e.g. the IPVV C1 exemplars for C1 quality).
2. Run the experiment variants on the SAME fixed test set.
3. Score each variant's output vs the gold (quality) + record speed/cost.
4. Pick the winner on the goal's axis; add more gold candidates per tradition later.
