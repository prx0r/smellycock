# PĀṬALA ORG — the production-grade canonical reference + official runs

*The clean, final, production-grade documentation for the Pāṭala stack — the canonical reference
(`patalaorg`) plus the **official runs** (logged, monitored, traceable evidence of the system in action).
Everything here is crystal-refined: rules, standards, the object model, the performance doctrine, and the
per-domain references — no research bloat.*

---

## What this repo is
- **The canonical reference** — `AGENTS.md` (read first), `AXIOMS.md` (strict rules), `OBJECT-MODEL.md`,
  `MANIFEST.json` (the machine resolver), `check.py` (the drift gate), `performance/`, and `domains/`
  (translation · openpatala · factory · read-plane).
- **The official runs** — `runs/` holds every logged, monitored autonomous run (Run 1, Run 2, the
  experiments, the 3-build comparison, the brainstorm) — the evidence that the system is real.
- **The one rule:** nothing is real without a task + gold + a reproducible gate. The `check.py` gate
  enforces the docs; the `runs/` are the proof.

## The doc map
| Path | What |
|---|---|
| `AGENTS.md` | the governing file (read first) |
| `AXIOMS.md` | naming conventions, file organisation, operating axioms, status ladders, banned words |
| `OBJECT-MODEL.md` | the canonical DAG + object/registry contracts |
| `MANIFEST.json` | the machine pointer (every doc → id/owner/validator) |
| `check.py` | the drift validator (run after any change) |
| `performance/` | the perf doctrine + budgets + references |
| `domains/translation/` | the translation layer (complete reference + agent runbook) |
| `domains/openpatala/` | the OpenAlex-of-Sanskrit surface |
| `domains/factory/` | the production translation factory |
| `domains/read-plane/` | the compiled read plane |
| `runs/` | the official logged + monitored autonomous runs |

## The production state (as of the official runs)
- The translation factory is **real and autonomous**: canonical T1 generator, live quality gate, state
  refresh, full-chain watchdog, checkpoint-DAG build plan, ops status board, trace log, gold scorer.
- **Run 1:** L0 168→180, memory stable (~550MB), full logs. **Run 2:** L0 198→217. Both fully logged.
- The whole-chain single-pass (1M context) was proven on small cases and honestly documented as
  unreliable at scale; the per-layer factory is the reliable production path.

## The division
patala PRODUCES → ip-graph VALIDATES + SERVES → Hermes is the execution kernel → this repo documents +
validates the contracts. Both agents work the plan, never skip a validator.

*This is the production repo. Keep it crystal-refined: final docs + official runs only. No research bloat.
Run `check.py` after any change.*
