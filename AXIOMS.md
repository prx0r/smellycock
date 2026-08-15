# AXIOMS — the strict rules for the Pāṭala codebase

*The non-negotiable conventions every agent/machine follows: **naming**, **file organisation**, the
**operating axioms**, the status ladders, and the banned words. This is the frozen standard — deviations
are bugs.*

---

## 1. NAMING CONVENTIONS (the exact patterns)

### 1.1 Files / directories
| Kind | Pattern | Example |
|---|---|---|
| scripts | `dash-case-action-verb.py` | `build-static-site.py`, `factory_scheduler.py` |
| kernels / python modules | `snake_case.py` | `object_registry.py`, `t1_jsonl.py` |
| data files | `snake_case.ext` | `translation-state-ledger.json` |
| docs | `NN-topic.md` (numbered) | `01-corpus.md`, `05-performance.md` |
| specs | `SPEC-NN-TOPIC.md` | `SPEC-49-PERFORMANCE-BUILD-DECISION.md` |
| layer pages | `NN-layer-name.md` | `00-core-engine.md` |
| skills | `kebab-case/` | `canonical-translate/` |
| config / contracts | `kebab-case.yaml` | `CANONICAL-DAG.yaml`, `LAYERS.yaml` |

### 1.2 Identifiers
| Kind | Pattern | Example |
|---|---|---|
| passage object | `<work>:<locator>` | `kramasadbhava:v2` |
| native identity | `PT<type>:<id>` | `PTW:tantraloka` |
| citation | `urn:cts:patala:<work>.<layer>.<version>:<passage>` | `urn:cts:patala:tantraloka.source.patala` |
| ip-graph entity | `ip:<type>:<slug>` | `ip:concept:free-will` |
| content-address | `sha256:<hex>` | `sha256:9e7b6be0…` |

### 1.3 The ONE canonical layer taxonomy

> **CANONICAL TRANSLATION BUILD (2026-08-15):** the KANBAN build (`pipeline/kanban_translation.py` +
> `layer_agent.py`) — a durable, resumable, auditable work queue driven by per-layer agents (90%-context
> Hermes calls, per-model per layer). It is the ACTIVE build; the E2E harness, translate_work, and
> factory_scheduler are SUPERSEDED (proof/benchmark/build-blocks). See `domains/translation/BUILDS.md`.
**Source of truth: `patala/migration/v2/LAYERS.yaml`.** The production DAG (clear name · legacy · pos):
```text
 0 source           (SOURCE)
 1 draft_translation(T1)
 2 tokenization     (L0)         deterministic, free-draining
 3 argument_outline (ARGMAP)     lateral guide, requires [source, tokenization]
 4 translation      (L2)         guided by the outline over the token floor
 5 translation_proof(L200)       the 8-section derivational audit (the moat)
 6 commentary       (C1)
 7 theme / argument
 8 synthesis
 9 essay
10 lesson           (EDUCATION)
```
The `layers/00-09` taxonomy is the **read-plane/validation** concern; the v3 organism is the **conceptual**
view. Do not conflate the three.

---

## 2. FILE ORGANISATION (where things live)

### 2.1 The working repos (PRODUCES + VALIDATES)
```text
patala/
  pipeline/      the factory: scheduler, batch, workers, object_registry, model (Hermes), validators
  contracts/     CANONICAL-DAG.yaml (the dependency manifest)
  data/          corpus/, registries/, published/, atlas/
  ingestion/     the harvest adapters (PANDIT/GRETIL/SARIT/MUKTABODHA/CTS)
  python/patala_core/atlas/   the OpenAlex-grammar API
  openpatala/    the openpatala docs + openapi.yaml
  translation/   the canonical translation reference (the production spine)
  skills/        the Hermes skills
  web/           the OG Astro static site
  migration/     the versioned blueprints (shared/ = cross-repo coordination)

ip-graph/
  lib/           the reusable kernels (52)
  scripts/       the pipeline (build-static-site.py, rebuild-on-commit.py, validate-*)
  site/          the compiled read-plane output (works/, concepts/, openpatala/ layers)
  layers/        the read-plane/validation layer pages (00-09)
  docs/          the concern docs (05-performance.md = the perf doctrine)
  specs/         SPEC-NN designs
  handover/      the Hermes + coordination notes
```

### 2.2 patalaorg (the clean reference)
```text
patalaorg/
  AGENTS.md         the governing file (read first)
  README.md         the constitution
  AXIOMS.md         the strict rules (this file)
  OBJECT-MODEL.md   the canonical DAG + object/registry contracts
  MANIFEST.json     the machine pointer (docs → id + owner + validator)
  check.py          the drift validator
  performance/      the consolidated perf doctrine + references
  domains/          per-domain canonical references (translation/, atlas/, factory/, read-plane/, …)
  reference/        links to the working repos (never copies)
```

---

## 3. THE OPERATING AXIOMS (non-negotiable)

1. **THE ONE RULE:** nothing is "real" without a task + gold + a reproducible gate. A gate is done, not a file existing.
2. **Hermes for GENERATION, .py for REDUCTION.** Hermes reads files and derives; `.py` validates, aggregates, commits. Never hand-feed a validator; never fabricate both sides of a comparison.
3. **Eligibility is deterministic Python, never an LLM judgment.**
4. **Fail-closed, validate-first.** Wrong is worse than none; the factory never outruns the validator; abstain rather than fabricate.
5. **Docs are a projection; run the validators after any change.** The truth is `object_registry` + `corpus_state` + ReviewEvents + git.
6. **Archive, don't delete.** Superseded docs get `ARCHIVED/SUPERSEDED` + a `DOCS-AUDIT.json` entry.
7. **RAM is the scarcest resource** (4-core / 8 GB / no swap, 2 agents). Stream, never bulk-load a registry; one heavy job at a time; kill by PID.
8. **Never `sleep` to wait; never foreground a long job.** Background with `setsid … > log 2>&1 &`; poll the log.
9. **R2 is the byte truth; content-address everything.** External sources → R2, not local disk.
10. **RUNNING TESTS IS NOT WORK** — a green suite on unchanged code is noise; run a gate only when you changed something or a claim is in doubt.
11. **Crosswalk = identity MAPPING, never external corroboration.** Native identity is canonical; the rights firewall holds.
12. **Compute on write, read from bytes.** Precompute projections; readers get static bytes with `ETag`/304 + immutable. One question = one request (`?select=`, `?depth=`, bounded).

---

## 4. THE STATUS LADDERS (never invent a 5th)

- **Object epistemic:** `MACHINE_PROPOSED → ENGINEERING_VALIDATED → SCHOLARLY_CORROBORATED →
  INDEPENDENT_REVIEWED → ADJUDICATED` (a thesis edge never exceeds the corroborated physics under it).
- **Registry object:** `GENERATED → ENGINEERING_VALIDATED → SPECIALIST_REVIEWED`.
- **Per-layer build:** `DISCOVERED < PROTOTYPED < VALIDATED < INTEGRATED < PRODUCTION`.
- **How-known (Eigenius):** `ASSERTED · EXTRACTED · RECONSTRUCTED · EVIDENCE_GROUNDED · HUMAN_REVIEWED ·
  ADJUDICATED` — never one mushy confidence score.
- **Authority:** the 4 axes `generation · evidence · review · publication`, a **partial order** (`A ⪯ B
  ⟺ ∀i A_i ≤ B_i`); NEVER a scalar max. Object TYPE ≠ epistemic STATE.

## 5. THE BANNED WORDS / REPLACEMENTS
- **Banned:** `PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS`
- **Use:** `SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY ·
  NO CONFLICT DETECTED`

## 6. COMMIT / RESPONSE CONVENTIONS
- A commit ships code + the affected HAND-WRITTEN docs together; run the validators first.
- API responses carry a `provenance` envelope (`api_version`, `surface`, `served`); errors carry
  `error.code / message / retryable`.
- Every result resolves to `result_id · benchmark_version · gold_version · model_version · code_commit ·
  split · seed · config · date` (Result Lineage). If it can't resolve, it doesn't exist.

## 7. PATALAORG IS FINAL PRODUCTION DOCS ONLY (no bloat — non-negotiable)
- **patalaorg holds ONLY the crystal-refined docs actually used by production, agents, and public
  surfaces** — API references, the performance doctrine, the object model, the standards.
- **NO research, NO experiment write-ups, NO gems/synthesis, NO exploration notes.** Those live in the
  working repos (`patala/`, `ip-graph/`), never here.
- **Every doc must reflect the CURRENT working implementation** — it references a real file + the real
  code, and reconciles to a live validator. If it isn't implemented, it is documented as
  `NOT-IMPLEMENTED` precisely (the exact gap), never presented as built.
- **If it can't be used by an agent or shipped to production, it doesn't belong in patalaorg.**

## 8. AGENT-SPEED (how agents use these docs fast)
- The `MANIFEST.json` is the resolver: an agent reads one JSON → every doc → id/owner/validator → the
  real file.
- **Dense tables, no prose walls.** Stable IDs. Every reference resolves (`check.py` enforces it).
- One concern = one doc = one owner = one validator. Duplicate roles are rejected.
- A doc answers "what is it / where is the code / how do I use it / what's the gate" in under a screen
  when possible.

---

*This is the frozen axiom set. Deviations are bugs — fix the code/doc, never loosen the standard.
Every rule maps to a validator where one can exist.*
