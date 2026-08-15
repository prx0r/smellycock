# PĀṬALA ORG — the production-grade canonical reference + official runs

*The clean, final, production-grade documentation for the Pāṭala stack — the canonical reference
(`patalaorg`) plus the **official runs** (logged, monitored, traceable evidence of the system in action).
Everything here is crystal-refined: rules, standards, the object model, the performance doctrine, and the
per-domain references — no research bloat.*

---

## What this repo is
- **The canonical reference** — `AGENTS.md` (read first), `AXIOMS.md` (strict rules), `OBJECT-MODEL.md`,
  `MANIFEST.json` (the machine resolver), `check.py` (the drift gate), `performance/`, and `domains/`
  (translation · openpatala · factory · read-plane · **epistemic**).
- **The epistemic product layer** — `domains/epistemic/` documents the **26 product engines** (proof,
  scholar workflow, manuscript pipeline, serve-time guard) whose code lives in `/root/projects/patala`. **This is the
  highest-value new build.** See the section below.
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
| **`domains/epistemic/`** | **the epistemic product layer — 26 engines, Hermes-MCP, scholar workflow, manuscript pipeline, serve-time guard** |
| `runs/` | the official logged + monitored autonomous runs |
| `openpatala/` | the OpenAlex-of-Sanskrit API docs + OpenAPI spec |
| `web/` | the Astro static-site source + build |
| `site/` | the compiled read-plane (works/concepts/openpatala projections, search, sitemap) |

---

## The epistemic product layer (the high-value build — read this)

**The code lives in `/root/projects/patala`** (the working repo, `prx0r/patalacheckpoints`); this
repo documents it. The products are the **epistemic + scholar + manuscript engines** — the validation
layer above the translation factory. Everything is **CPU-only, deterministic, 150/150 PASS**, exposed
to **humans (UI)** and **agents (Hermes MCP, 64 tools)**.

| Group | Products | What they give |
|---|---|---|
| **Epistemic substrate** (14) | translation_proof · claim · argument · crux · comparison · research_packet · evidence_independence · tension_finder · context_bundle · passage · passage_workbench · terminology · timeline · benchmark | proofs, propositions, arguments, cruxes, retrieval, tension surface |
| **Scholar workflow** (8) | review_queue · scholar_identity · review_workbench · scholar_profile · review_policy · scholar_review · scholar_publication · scholar_vertical | "machines propose, scholars certify" — review, attestation, contribution ledger |
| **Manuscript pipeline** (3) | manuscript_routing · manuscript_ingest · collation | manuscript → OCR (adopted) → quality → critical apparatus |

**Full reference:** `domains/epistemic/README.md` (the 26-product index). **Verify:** `check_epistemic.py`.

**How to use:** `./start.sh` in patalacheckpoints → the scholar UI at `localhost:3000`; the 61 MCP tools
are callable by Hermes as `mcp__patala__<tool>`.

**Dependencies:** `patalacheckpoints/DEPENDENCIES.md` — networkx + cryptography (Python), the MCP SDK
(Node), the internal modules + data. All verified present.

---

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

## The scholarly raw material + essays
| Path | What |
|---|---|
| `raw-material/` | official golds — raw T1 glosses, IPVV C1 commentaries, hand-authored ARGMAP golds |
| `essays/` | scholarly essays — Ratié literature review + recognition essays |
