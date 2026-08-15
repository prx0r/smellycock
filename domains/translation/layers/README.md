# layers/ — each translation layer is its own stage (contract + agent + queue)

*2026-08-15 · every layer is an independent assembly-line stage: its own README (the contract), its own
Hermes API call (drains its queue up to ~90% context in one call), its own generator + validator. This
lets us track each layer's productivity, global queue numbers over time, benchmark speeds, and trial a
different model per layer.*

## THE MENTAL MODEL (each layer = a stage)
```
[its queue] ──> [layer agent: ONE Hermes API call, drains up to 90% context] ──> [commit] ──> [next layer's queue]
```

## THE LAYERS (read the per-layer README for each)
| Layer | Type | Hermes call | Consumes | Produces | Measured avg time |
|---|---|---|---|---|---|
| [L0](L0.md) | **DETERMINISTIC** (Vidyut) | none | SOURCE verse | tokens/lemmas | instant (~185/pass, free) |
| [L1](L1.md) | **DETERMINISTIC** scaffold | none | L0 | controlled segments | instant |
| [T1](T1.md) | MODEL (rough translation) | `-z` stream (or agentic) | SOURCE | T1 gloss JSONL | **~12s/verse** (`-z`) |
| [ARGMAP](ARGMAP.md) | MODEL | agentic `extract-argmap` | SOURCE+L0 | 4-section arg map | ~60-90s |
| [L2](L2.md) | MODEL | agentic `translate-reading` | L1+ARGMAP | guided prose | ~30-60s |
| [L200](L200.md) | MODEL (bounded classifier) | plain `chat` | L2 | 8-section audit | ~12-45s |
| [C1](C1.md) | MODEL (batched) | plain `chat` | L200 | scholarly commentary | ~150s |

## THE PER-LAYER AGENT (one API call, drains its queue)
Each layer agent: pulls its queue (eligible passages), sizes the batch to **~90% of the model's context**
(`model_registry.max_verses_per_call`), makes **ONE Hermes call** (streaming, commit-per-verse), and hands
off. Independent per layer — so they run in parallel across works.

## PER-LAYER TELEMETRY (what we track for each)
- queue length (committed vs pending) — `factory_status.py --layers`
- avg time + model calls + quality — the progress registry `layers[]`
- productivity over time — the benchmark projection
- trial a different model per layer — set `HERMES_MODEL` per layer worker
