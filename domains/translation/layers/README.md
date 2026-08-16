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

## PER-LAYER PROFILE (data transformations · predicted speed · best model + why)
| Layer | Data transformation | Predicted speed | Backlog (now) | Best model | Why |
|---|---|---|---|---|---|
| **L0** | verse → tokens/lemmas (Vidyut, deterministic) | **instant** (free) | 7 works | none | no model — deterministic |
| **L1** | L0 → controlled segments (deterministic scaffold) | **instant** | — | none | no model |
| **T1** | verse → word-gloss JSONL (**mostly prompting**: light Vidyut split + "translate to T1 JSONL") | **~9s/verse** (`-z`, ALL verses in ONE call) | **20,000** | **flash** | **FASTEST BUILD (science-lab-confirmed): `-z` stream + one big batch (all verses/call) + flash → 5/5 committed, 1 call, 9s/verse** |
| **ARGMAP** | SOURCE+L0 → 4-section argument map (skill) | ~60-90s/call | 787 | flash (pro if quality-critical) | needs reasoning + `extract-argmap` skill, not scale |
| **L2** | L1+ARGMAP → guided philosophical prose (skill) | ~30-60s/call | 0 (blocked) | **flash or pro** | the philosophical frame matters — pro for higher quality, 3× cost |
| **L200** | L2 vs L1 → bounded 8-section audit (classifier) | ~12-45s/call | 0 (blocked) | **cheap/fast** | bounded classifier (IGNORE default) — doesn't need a big model |
| **C1** | L200 → scholarly commentary (summary + key terms) | ~150s/call | 0 (blocked) | **pro** | the final product — scholarly quality is the payoff |

## PER-LAYER TELEMETRY (what we track for each)
- queue length (committed vs pending) — `factory_status.py --layers`
- avg time + model calls + quality — the progress registry `layers[]`
- productivity over time — the benchmark projection
- trial a different model per layer — set `HERMES_MODEL` per layer worker
