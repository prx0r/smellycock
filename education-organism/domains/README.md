# serveragent3 — domains (brainstorms + reference)

*2026-08-15. The POST-C1 scholarship engine + the deep-dive/mine/feed-essays vision, documented as
brainstorms (the visionary opportunities) + reference (the production implementation).*

## The brainstorms (visionary opportunities)

| Doc | What it is |
|---|---|
| `PUSHING-DEEPDIVE-BRAINSTORM.md` | the pushing/deep-dive method (3 passes, round loop, question-DNA, truth-packets) + how it feeds essays |
| `LOGICVID-MINE-ESSAY-BRAINSTORM.md` | the LOGICVID deep-dive: the merge-attempt epistemology + adversarial double-pass + the 9 mine-for-essay mechanisms |
| `EDUCATION-ORGANISM-BRAINSTORM.md` | the education/organism vision: wrong-answer→neighbor, executable corrections, progressive zoom, the Gap Engine |
| `VISIONARY-OPPORTUNITIES-BRAINSTORM.md` | the top-10 cross-cutting opportunities from all 47 specs |

## The reference (production implementation)

| Doc | What it is |
|---|---|
| `../AGENTS.md` | the governing file |
| `../contracts/CANONICAL-DAG.yaml` | the layer dependency manifest |
| `../kernels/object_registry.py` | versioned registry + event ledger |
| `../kernels/gates.py` | deterministic gates (nyaya/cite/quality/chain/blind) |
| `../kernels/generation.py` | the Hermes generation engine |

## How it connects

The brainstorms identify the visionary opportunities; the reference implements the production-grade
foundation (registry + gates + generation) to realize them. The pushing/deep-dive method (brainstorm)
becomes a Hermes skill + `.py` reducer that mines texts into argument truth-packets, which feed the
ESSAY layer of the POST-C1 spine.
