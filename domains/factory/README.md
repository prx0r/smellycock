# factory — the production translation factory (complete reference)

*The clean, canonical reference for the **factory** — the deterministic DAG that produces the committed
translation spine. This is the PRODUCE side; `domains/translation/` is the layer reference; `openpatala`
is the SERVE side. Everything is gated, idempotent, low-RAM, tracked.*

## The DAG (from `contracts/CANONICAL-DAG.yaml`)
`SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1 → THEME → ARGUMENT → …`

## The pieces (all real + tested)
| Piece | File | Role | Gate |
|---|---|---|---|
| DAG controller (deterministic) | `pipeline/factory_scheduler.py` | enumerates eligible jobs (streamed, bounded), drains deterministic L0 free, spends model budget | `test_factory_scheduler.py` |
| Batch/commit path | `pipeline/factory_batch.py` | per-batch isolation, idempotent commits | — |
| Canonical T1 generator | `pipeline/canonical_translate.py` + `t1_jsonl.py` | Hermes reads file → JSONL → adaptive chunk | `test_canonical_translate.py` |
| Live quality gate | `pipeline/translation_gate.py` | deterministic verifiable-reward gate on T1 | `test_translation_gate.py` |
| Orchestration brain | `pipeline/patala_orchestration.py` | next_action / work_state / progress (PROPOSE-only) | `test_patala_orchestration.py` |
| State refresh | `pipeline/translation_state.py` | derive next_action + ledger + bibliography + projection | `test_translation_state.py` |
| Self-driving supervisor | `pipeline/translation_supervisor.py` | one command: pick best recoverable work → advance → verify | — |
| Full-chain watchdog | `pipeline/watchdog_fullchain.py` | drive one work RAW→C1 autonomously, one-owner | — |
| Checkpoint-DAG engine | `pipeline/build_plan.py` | enforced build plan (can't pass a failed validator) | `test_build_plan.py` |
| Ops status + trace | `pipeline/ops_status.py` + `trace_log.py` | live board + per-op observability traces | — |

## The invariants (never break)
- **Hermes for GENERATION, .py for REDUCTION.** Hermes reads files and derives; `.py` validates/commits.
- **Eligibility is deterministic Python, never an LLM judgment.**
- **Fail-closed, idempotent** (`input_hash` dedup); `GENERATION_FAILED` never commits.
- **One owner** (one scheduler at a time); **low-RAM** (stream, never bulk-load a registry — the 4.5GB→545MB fix).
- **PROPOSE-only** — agents/verbs report and propose; only a human + the factory advance/promote.

## Run it
```bash
python3 pipeline/translation_supervisor.py --advance        # one autonomous pass
python3 pipeline/translation_state.py --refresh             # keep ledger/bib/projection in sync
python3 pipeline/prove_full_chain.py --work <w> --loc <l>   # evidence a RAW->C1 chunk
```
