# LAYER ARGMAP — the argument outline (the lateral guide)

*The argument map: reasons out the passage's structure (what's at issue + decision_for_l2) that GUIDES L2.
Agentic, skill-based.*

## Contract
| | |
|---|---|
| **Consumes** | SOURCE + L0 |
| **Produces** | 4-section argument map (what_is_at_issue, decision_for_l2, ...) |
| **Gate** | deterministic 4-section validator |
| **Where** | `pipeline/argument_map_worker.py` (`argmap_generator_batched`) |

## Hermes call (per-layer logic)
- **`chat_agentic` + the `extract-argmap` skill** (intelligence-based, reads the real passage itself).
- Batched (can fill 90% context in one call).

## Queue
- SOURCE+L0-complete passages with no committed ARGMAP.

## Model / context
- `deepseek-v4-flash` · 1M context · batched.

## Productivity signal
- avg time/call (~60-90s), committed/call, success rate — the progress registry.
