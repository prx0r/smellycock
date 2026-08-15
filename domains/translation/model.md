# translation — MODEL (semantics)

*What the translation objects ARE and how they're stored: the DAG, the object shapes, the JSONL contract,
the registry/ledger, authority, and tracking. Wire mechanics in `reference.md`.*

---

## 1. THE LAYER DAG

```text
source → draft_translation → tokenization → [argument_outline] → translation → translation_proof →
commentary → theme / argument → synthesis → essay → lesson
```
(clear names from `migration/v2/LAYERS.yaml`; legacy codes in parens below.)

| pos | id | legacy | deterministic | requires | gate |
|---|---|---|---|---|---|
| 0 | source | SOURCE | yes | — | source binding + hash |
| 1 | draft_translation | T1 | no | source | `t1_validator` |
| 2 | tokenization | L0 | **yes (free-drain)** | draft_translation | `verify_l0.p0_proof` + `validate_l0_spec` |
| 3 | argument_outline | ARGMAP | no | **source + tokenization** | ARGMAP validator |
| 4 | translation | L2 | no | **tokenization + argument_outline** | L2 validator |
| 5 | translation_proof | L200 | no | translation | 8-section audit |
| 6 | commentary | C1 | no | translation_proof | C1 validator |

**Multi-parent rule:** a layer is eligible only when EVERY required parent is committed. `translation`
needs `[tokenization, argument_outline]` — unguided prose is the 0.118 bug. `L0` is deterministic and
free-draining (never consumes the model budget).

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

### 2.2 The JSONL output record (the canonical Hermes contract)
Hermes emits **one JSON record per verse per line** (never one `{"verses":[...]}`):
```json
{"object_id":"kramasadbhava:v2","tokens":{"kālī":{"gloss":"the goddess Kālī","quoted":false}}}
```

### 2.3 The authority envelope (on every object)
`epistemic_ceiling` + the 4-axis `authority {generation, evidence, review, publication}` + `review_state`,
with the invariant **`authority(projection) ≤ authority(parent)`**. `authority ≠ max(axes)`; object TYPE
≠ epistemic STATE.

---

## 3. THE REGISTRY / LEDGER CONTRACTS

| Store | Path (under `/root/projects/patala/`) | Holds | Immutable? |
|---|---|---|---|
| Registries | `data/corpus/registries/<layer>-registry.jsonl` | per-layer objects, versioned | append + versioned |
| Event ledger | `data/corpus/registries/object-events.jsonl` | hash-chained ObjectEvent trail | YES |
| Failure queue | `data/corpus/downloads/factory-failure-queue.jsonl` | retryable failures, `OPEN`/`RESOLVED` | append, upserted |
| Corpus-state ledger | `data/corpus/downloads/translation-state-ledger.json` | per-work `next_action` | — |

- **Idempotency:** commits dedup by `input_hash` (never double-commit).
- **Truth:** registry = canonical; JSONL = export; Postgres (`patala-atlas`) = streaming/append layer when
  up. Never bulk-load a registry (stream with `object_registry.iter_object_ids` / `committed_ids`).
- **Supersession:** a new version replaces an old one — never an in-place edit.

---

## 4. TRACKING (what is recorded where)

| Signal | Where |
|---|---|
| per-verse produced/committed | `data/corpus/downloads/t1-stream.jsonl` (`ts`, `object_id`, `status`, `gloss_count`) |
| each commit/retry/reject | `data/corpus/registries/factory-audit.jsonl` |
| per-pass summary | `/tmp/opencode/factory-loop.log` |
| per-work status (served) | `site/openpatala/translation.json` (compiled) |

**Idempotency check:** `python3 pipeline/factory_certificate.py` → 0 dup = healthy.

---

*Semantics only. Wire mechanics: `reference.md`. How-to: `recipes.md`. Agents: `agentic.md`.*
