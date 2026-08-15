# epistemic — the epistemic/validation layer (products index)

*2026-08-15. The clean canonical reference for the **epistemic layer** — the 14 deterministic product
engines that sit ABOVE C1 and BELOW the upper spine (ARGUMENT → SYNTHESIS → ESSAY → LESSON). These are
the validation kernels the production DAG consumes: they derive, gate, review, and measure scholarship
from the real committed objects. The reference is the code at `/root/projects/patala/pipeline/products/`
(works locally; the canonical deployment path is the working patala repo).*

> **Why this domain exists:** `OBJECT-MODEL.md` names the DAG (`... → theme/argument → synthesis → essay →
> lesson`), but the *epistemic semantics* of those layers — the gates, the review, the measurement — live
> in these products. This domain documents them against the canonical model, so an agent can run, gate,
> and review scholarship the same way the production factory produces it.

---

## The one rule (same as the whole stack)

> **Nothing is real because code exists. It is real when an independent task + gold + a reproducible gate
> show it does what it claims.** Every product has a `test.py` (deterministic proof) + a live-integration
> path (real Crossref/OpenAlex/OpenCitations + real registries). A green test is reproducible and honest.

---

## The product index (19 engines, all CPU-only + deterministic)

### The substrate (14 — the epistemic layer above C1)
| # | Product | Canonical layer | PT* ID | Proof | What it does |
|---|---|---|---|---|---|
| 1 | `translation_proof` | `translation_proof` (L200) | PTL200 | 6/6 | non-aggregate audit vector + publication gate |
| 2 | `claim` | `argument` floor | PTPROP | 7/7 | real C1 → honest-envelope Proposition |
| 3 | `argument` | `argument` | PTARG | 6/6 | real C1 → thesis/premises/inference/defeaters |
| 4 | `crux` | `synthesis` | PTCRUX | 4/4 | minimal divergence between positions |
| 5 | `comparison` | `synthesis` | PTCOMP | 3/3 | AGREEMENT / REAL CRUX |
| 6 | `research_packet` | `synthesis`/read-plane | PTPACK | 5/5 | question → evidence packet (PathRAG) |
| 7 | `evidence_independence` | corroboration | PTCORR | 5/5 | SOURCE_ECHO + dedup, live OpenCitations |
| 8 | `scholar_review` | `review` | PTREV | 11/11 | panel + reducer + durable gate + attestation |
| 9 | `context_bundle` | read-plane bundle | PTPACK | 6/6 | token-budgeted agent bundle (2k/8k/32k) |
| 10 | `passage` | read-plane / passage | PTPASS | 6/6 | canonical Passage + KG2Code query |
| 11 | `passage_workbench` | read-plane / philology | PTPASS | 5/5 | record a scholar's disagreement → review gate |
| 12 | `terminology` | read-plane / lexical | PTTERM | 6/6 | lemma-through-time sense trajectory |
| 13 | `timeline` | read-plane / atlas | PTTL | 5/5 | diachronic Śiva source-tree |
| 14 | `benchmark` | eval plane | PTBENCH | 5/5 + inspect 1.000 | real samples → inspect_ai eval |
| | | | | **80/80** | |

### The scholar-workflow layer (5 — what a scholar actually does)
| # | Product | Role | Proof |
|---|---|---|---|
| 15 | `review_queue` | the scholar's "what do I review next" (prioritized) | 6/6 |
| 16 | `scholar_identity` | ORCID-backed identity + domain scope + Ed25519 keypair | 7/7 |
| 17 | `review_workbench` | one object's full review context + decision surface | 6/6 |
| 18 | `scholar_profile` | the contribution ledger (reviews + attestations per scholar) | 6/6 |
| 19 | `review_policy` | what each review kind grants (authority semantics) | 7/7 |
| 20 | `tension_finder` | the vision's /find-interesting-tension (5 kinds, real IPVV) | 6/6 |
| 21 | `scholar_publication` | the Astro-servable JSON-LD scholar records (CV-legible) | 5/5 |
| 22 | `scholar_vertical` | the Scholar Attestation Vertical (review→attest→propagate→publish) | 5/5 |
| 23 | `manuscript_routing` | the manuscript-onboarding diagnostic (vision E3) | 7/7 |
| 24 | `manuscript_ingest` | manuscript+OCR → labelled, quality-scored Pāṭala SOURCE | 8/8 |
| 25 | `collation` | N witnesses → variant apparatus (Saktumiva critical-edition process) | 7/7 |
| | | | **54/54** |

**Total: 134/134 PASS** (+ 16/16 live).

---

## How to read this domain

| File | What it is |
|---|---|
| `README.md` (this) | the product index + the one rule |
| `compatibility-matrix.md` | each product → canonical layer / PT* ID / authority / validator |
| `model.md` | the object contracts + authority, canonical naming |
| `reference.md` | wire mechanics: CLI / API / MCP / env / gates |
| `recipes.md` | how-to: run, validate, live-test each product |
| `agentic.md` | how agents drive the epistemic layer (Hermes → .py) |
| `validation.md` | the gates + the live monitored run evidence |

---

## The run everything command (the proof gate)

```bash
cd /root/projects/patala
python3 test_live_integrations.py                     # 16/16 live (real network + real data)
for p in scholar_review translation_proof argument crux research_packet comparison evidence_independence \
         claim context_bundle passage benchmark passage_workbench terminology timeline \
         review_queue scholar_identity review_workbench scholar_profile review_policy tension_finder \
         scholar_publication scholar_vertical manuscript_routing; do
  echo "--- $p ---"; PYTHONPATH=pipeline python3 pipeline/products/$p/test.py | grep SUMMARY
done
```

Expected: `127/127` deterministic PASS + `16/16` live PASS.

---

## The honesty rule (anti-theatre, same as the stack)

Every product hydrates from REAL data (`_shared/ipvv.py`, the registries, `trajectories.json`,
`historyTimeline.json`) or REAL network (Crossref/OpenAlex/OpenCitations). No fixtures, no
feeding-the-answer. A green result means the product works against the live world. GPU tools
(COMET/xCOMET/pyBKT) are **not** here — they're cloned for code-reading only, never as runnable
products on this box.
