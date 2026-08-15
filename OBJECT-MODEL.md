# OBJECT-MODEL — the canonical object model (the DAG + object/registry contracts)

*The canonical structure of Pāṭala objects: the layer DAG, the object shapes, the registry/ledger
contracts, and authority. Source of truth for the layer contract: `patala/migration/v2/LAYERS.yaml`.
Semantics only — wire mechanics live in the domain docs.*

---

## 1. THE LAYER DAG (the production spine)

```text
source → draft_translation → tokenization → [argument_outline] → translation → translation_proof →
commentary → theme / argument → synthesis → essay → lesson
```

| pos | id | legacy | deterministic | requires | produces | verifier |
|---|---|---|---|---|---|---|
| 0 | source | SOURCE | yes | — | tokenization | source_fingerprint |
| 1 | draft_translation | T1 | no | source | tokenization | gloss_precision, losslessness, no_dupes |
| 2 | tokenization | L0 | **yes** (free-drain) | draft_translation | translation | token↔verse binding |
| 3 | argument_outline | ARGMAP | no | **source + tokenization** | translation | 4-section outline |
| 4 | translation | L2 | no | **tokenization + argument_outline** | translation_proof | prose fidelity |
| 5 | translation_proof | L200 | no | translation | commentary | 8-section audit |
| 6 | commentary | C1 | no | translation_proof | theme, argument | compact, passage-local |
| 7 | theme / argument | THEME/ARGUMENT | no | commentary | synthesis | cluster / structural validity |
| 8 | synthesis | SYNTHESIS | no | argument + theme | essay | derivation-complete (0 until inputs real) |
| 9 | essay | ESSAY | no | synthesis | lesson | sentence has a proof path |
| 10 | lesson | EDUCATION | no | essay | — | answer + distractor provable |

**The DAG rule:** a layer is eligible only when EVERY required parent is committed (multi-parent).
`translation` needs `[tokenization, argument_outline]` — unguided prose is the 0.118 bug. `L0` is
deterministic and free-draining (never consumes the model budget).

---

## 2. OBJECT SHAPES

### 2.1 The T1 proposal (canonical, machine-checkable)
```json
{ "object_id": "kramasadbhava:v2", "input_hash": "<sha256>", "verse": "<sanskrit>",
  "t1_status": "MACHINE_PROPOSED",
  "t1": { "status": "MACHINE_PROPOSED", "source_sha256": "<sha256>", "source_text": "<verse>",
          "tokens": [ { "idx": 0, "surface": "cakre", "iast": "cakre", "sanskrit": "cakre",
                        "gloss": "in the wheel", "status": "GLOSSED", "lemma": null,
                        "quoted": false, "form": "[and]-in-the-wheel (cakre)" } ] } }
```
- `surface` must appear in the source verse (source-bound); `form` must be `[and]-` grammar.
- Empty gloss = `ABSTAIN` (honest), never fabricated. `GENERATION_FAILED` never commits.

### 2.2 The canonical JSONL output record (Hermes contract)
Hermes emits **one JSON record per verse per line** (never one `{"verses":[...]}`):
```json
{"object_id":"kramasadbhava:v2","tokens":{"kālī":{"gloss":"the goddess Kālī","quoted":false}}}
```

### 2.3 Authority envelope (on every object)
`epistemic_ceiling` + the 4-axis `authority {generation, evidence, review, publication}` + `review_state`,
with the invariant **`authority(projection) ≤ authority(parent)`**. `authority ≠ max(axes)`; object TYPE
≠ epistemic STATE (a Source is not `SCHOLARLY_CORROBORATED` by type).

---

## 3. THE REGISTRY / LEDGER CONTRACTS

| Store | Path | What it holds | Immutable? |
|---|---|---|---|
| Registries | `data/corpus/registries/<layer>-registry.jsonl` | per-layer objects, versioned (`object_id`, `input_hash`, `status`, `superseded`) | append + versioned |
| Event ledger | `data/corpus/registries/object-events.jsonl` | hash-chained append-only ObjectEvent trail | YES |
| Failure queue | `data/corpus/downloads/factory-failure-queue.jsonl` | retryable failures, deduped per (object, layer), `OPEN`/`RESOLVED` | append, upserted |
| Corpus-state ledger | `data/corpus/downloads/translation-state-ledger.json` | per-work state machine + `next_action` | — |

- **Idempotency:** commits are deduped by `input_hash` (never double-commit).
- **Truth:** registry = canonical; JSONL = export; Postgres (`patala-atlas`) = streaming/append layer when
  up. Never bulk-load a registry (stream with `iter_object_ids` / `committed_ids`).
- **Supersession:** a new version replaces an old one — never an in-place edit.

---

## 4. THE PER-WORK STATE MACHINE (next_action)

`ACQUIRE_SOURCE → BUILD_L0_SOURCE_MODE → GENERATE_TRANSLATION → …`. The scheduler reads this to know the
legal next step; a work is `eligible_for_agent3` only when its source is acquired and the preceding floors
are committed.

---

*This is the object model. The DAG is authoritative in `LAYERS.yaml`; these shapes are the machine
contracts. Domain specifics live in `domains/`.*
