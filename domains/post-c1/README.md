# post-c1 — the POST-C1 scholarship layer (products index)

*2026-08-15. The clean canonical reference for the **POST-C1 scholarship layers** — the derivational
spine ABOVE C1: THEME → ARGUMENT → SYNTHESIS → ESSAY → LESSON(EDUCATION), driven by Hermes kanban and
gated deterministically. This domain documents the integrated build: the grounded IPVV C1 floor, the
Hermes-driven layer generation, and the gates (Nyāya, cite-contract, quality, blind-assessor, tension).
Reference is the code at `/root/fuck-off/scripts/` + the registries at `/root/projects/patala/`
(works locally; canonical deployment is the working patala repo).*

> **Why this domain exists:** `OBJECT-MODEL.md` names the DAG (`... → theme/argument → synthesis →
> essay → lesson`). This domain documents the POST-C1 implementation — how Hermes drives the layer
> generation and how the deterministic gates make it machine-checkable.

---

## The one rule (same as the whole stack)

> **Nothing is real because code exists. It is real when an independent task + gold + a reproducible
> gate show it does what it claims.** Every layer has a deterministic gate; a green gate is honest.

## The layer DAG (what we built)

```
C1 (39 real IPVV + 3 kramasadbhava)
   ↓ theme/argument
THEME (cluster/recall-first) · ARGUMENT (Nyāya-gated)
   ↓ synthesis
SYNTHESIS (derivation-complete, tension-aware)
   ↓ essay
ESSAY (reactive, depends_on proof paths)
   ↓ lesson
EDUCATION (learning claims, blind-assessor graded)
```

## The product index (the integration scripts)

| Script | Layer | What it does | Gate |
|---|---|---|---|
| `validate-nyaya-gate.py` | ARGUMENT | the 5-hetvābhāsa Nyāya gate (verify_claim_semantic) | PASS/PASS_WITH_OPEN/FAIL |
| `validate_cite_contract.py` | ARGUMENT | `(cite: id)` citation contract + hard set-validation | every claim cited |
| `detect-synthesis-tensions.py` | SYNTHESIS | vada contradiction_finder pattern → tensions_with | honest divergence |
| `validate-scholarship-chain.py` | ALL | every POST-C1 object resolves to C1 (proof path) | GATE PASS |
| `validate-quality-gate.py` | ALL | verifiable-reward quality gate (PASS/BLOCK) | ≥0.6 |
| `validate-blind-assessor.py` | EDUCATION | engram blind rubric-grader | recalled/partial/lapsed |
| `validate-signed-attestation.py` | G7/GapE | Ed25519 attestation + tamper-detect | verify + tamper |
| `ingest-ipvv-grounded.py` | C1 floor | ingest real IPVV C1s (fixes G1) | evidence_quote |
| `emit-openpatala-entities.py` | openpatala | emit PTPROP/PTARG/PTPASS entities | entity-model compat |

## How to read this domain

| File | What it is |
|---|---|
| `README.md` (this) | the product index + the one rule |
| `model.md` | the object contracts + authority (mirrors OBJECT-MODEL) |
| `reference.md` | the wire mechanics: CLI entrypoints, gates, API, env |
| `agentic.md` | how Hermes drives it (generation vs reduction) |
| `recipes.md` | how-to: run, gate, validate, use the API |
| `validation.md` | the gates + the evidence + the drift validator |

*This is a projection of the real build at `/root/fuck-off/scripts/` + `/root/projects/patala/`. Run
the gates after any change; never present DESIGN as BUILT.*
