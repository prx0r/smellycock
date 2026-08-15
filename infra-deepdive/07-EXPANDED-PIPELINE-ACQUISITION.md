# EXPANDED PIPELINE — the full FACTORIAL from acquisition to translation (RAW→EDUCATION)

*2026-08-15 · the handover expanded BACKWARDS. The RAW→C1 translation machine is CONFIRMED by logged runs
(`/tmp/opencode/e2e-trace.json`: 412.2s / 3 api calls / 7 layers committed / `chain_ok:true`; live watchdog
+ gateway; 76 C1 committed). This doc adds the missing FRONT of the pipeline: deciding where to ingest from,
source-state assessment, OCR routing, categorical tagging, R2 byte-truth, verse recovery, and explicit
queueing — the full FACTORIAL process, built on the SAME stack (Hermes for generation, .py for reduction,
deterministic gates, logged-run evidence, R2 content-addressing). It reuses what is already specced
(`docs/global/ingestion-refinery.md`, `SPEC-18-COMPLETE-PIPELINE.md`) and is honest about what is logged-real
vs designed.*

---

## 0. THE ONE FRAME (grounded in the confirmed stack + AXIOMS)
Every stage below obeys THE ONE RULE: **real = logged run + gold + a reproducible gate.** A stage is DONE
only when a machine-readable trace shows it committed. This is the same evidenced way of working that proved
RAW→C1 — applied now to the acquisition front.

## 1. THE FULL FACTORIAL DAG (the expanded pipeline)
```
ACQUIRE ──► ASSESS ──► ROUTE ──► TAG ──► R2(bronze) ──► NORMALIZE ──► RECONCILE ──► SOURCE ──► QUEUE ──► TRANSLATE ──► POST-C1 ──► OPENPATALA
(choose     (state:     (adapter/  (categorical  (byte truth,  (silver,     (EXACT/POSSIBLE/ (verse     (ranked    (CONFIRMED  (THEME→ESSAY→  (public
 source)    clean/ocr/ process   tag → route)  sha256)        source-       CONFLICT →       recovery  queue      by logged  →EDUCATION)   surface)
             lacuna)    decision)                                    bound)    scholar-queue)    P0        + priority) run 412s)
```

### The sub-DAG per work (the "factorial" — every work passes every gate)
| # | Stage | Exists? (logged) | The gate | Owner |
|---|---|---|---|---|
| S1 | **ACQUIRE** — decide which source + which adapter | ✅ adapters (PANDIT/GRETIL/SARIT/MUKTABODHA/CTS/ngmcp/iiif) implemented; `ingestion-refinery.md` specced | connector emits `ExternalRecord` + snapshot manifest | ingestion |
| S2 | **ASSESS** — is the raw text clean, needs OCR, or is it lacuna/empty? | ⚠️ scattered (`source_ready._clean_signal`, `auto_run._is_ocr_noise`, `certificate_l0` OCR→SOURCE_BLOCKED); **not consolidated, not stored** | a `source_state` field stored on the registry object: `CLEAN_ETEXT` / `NEEDS_OCR` / `LACUNA_BLOCKED` / `AMBIGUOUS` | new |
| S3 | **ROUTE** — pick the process: adapter→R2→normalize (e-text) vs OCR-engine (scanned) vs scholar-queue (ambiguous) | ⚠️ only a binary format discriminator (`corpus_state.detect_source_format`: AND_GLOSS/RAW_SANSKRIT/UNKNOWN) | a routing decision emitted + logged | new |
| S4 | **TAG** — categorical tagging → route to the correct queue/process | ❌ **nothing** (CATEGORIES.md is a vision-doc index, not a work taxonomy) | a `category` + `priority` tag assigned per work | new |
| S5 | **R2(bronze)** — exact bytes, content-addressed | ✅ client exists (`infra/r2_assets.py` sha256 blob store, `ingestion/r2.py` SnapshotStore) **but is a one-way writer** | `SnapshotStore.put_snapshot` writes the manifest | r2 wiring (G1-G9) |
| S6 | **NORMALIZE** — source-bound silver | ⚠️ harvest extraction exists (`harvest_to_factory.py`) but not wired to R2/ingestion | normalized source-bound record with `verse` in payload | new |
| S7 | **RECONCILE** — identity EXACT/PROBABLE→gold, else scholar-queue | ✅ `entity_reconciliation.py`; `SourceAsserter` | EXACT/PROBABLE persisted; CONFLICT never auto-merged | ingestion |
| S8 | **SOURCE + VERSE RECOVERY** — commit SOURCE with `payload.verse` | ⚠️ **THE BIGGEST BLOCKER** — SOURCE payloads are metadata-only (empty verse) for works not run through `register_harvest_sources`; `harvest_to_factory.py` not run for all works | `payload.verse` non-empty for every committed SOURCE (the P0 fix) | **P0** |
| S9 | **QUEUE** — promote assessed source into the translation queue with a priority tag | ⚠️ implicit today (any on-disk source auto-enters `factory_scheduler`); no explicit assessed→queue step | a work enters the queue only after S2-S4 pass + priority set | new |
| S10 | **TRANSLATE** — the confirmed stack | ✅ **CONFIRMED by logged run** | `e2e-trace.json` RAW→C1 chain_ok:true | confirmed |
| S11 | **POST-C1** — THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION | ⚠️ mechanism present, data EMPTY (0 committed) | SYNTHESIS/ESSAY/EDUCATION registries non-empty | next |
| S12 | **OPENPATALA** — populate the public surface | ✅ `build-static-site.py` → per-layer counts + `translation.json` (112 works) | a new work appears in the ledger + read-plane | next |

---

## 2. THE NEW DESIGN SPACE (what must be built — the frontier)

### 2.1 The SOURCE-STATE assessment ladder (S2) — store it, don't recompute
The raw text "state" must become a **stored, machine-checkable field** on the SOURCE registry object, not an
on-the-fly heuristic. Extend the existing signals into one ladder:
```
CLEAN_ETEXT   — IAST/Devanagari-dense, verse-bounded, no noise  → route to S5/S6 (normalize)
NEEDS_OCR     — scanned/image, low Sanskrit density, high noise → route to the OCR integrator
LACUNA_BLOCKED— genuine lacuna or empty payload                  → SOURCE_BLOCKED, scholar review
AMBIGUOUS     — mixed gloss/translation/English                  → scholar-queue (never auto-decide)
```
**Reuse:** `source_ready._clean_signal`, `auto_run._is_ocr_noise`, `certificate_l0`, `corpus_state.detect_source_format`.

### 2.2 Categorical tagging (S4) — net-new, maps tag → process
A work's `category` drives which process it takes. **This does not exist — build it.** Proposed taxonomy
(grounded in `sivaqueue_targets` period/tradition/genre + the source format + copyright):
| Category | Example | Routes to |
|---|---|---|
| `KRAMA_PACKET` | kramasadbhava, tantraloka | translate NOW (highest priority, the confirmed stack) |
| `TIER1_TRANSLATION` | ipvv, cidgagana | translate |
| `SCANNED_MANUSCRIPT` | NGMCP/IIIF image works | **OCR integrator → then translate** |
| `E_TEXT_READY` | GRETIL/SARIT/Muktabodha clean text | normalize → translate |
| `IDENTITY_PENDING` | ambiguous source identity | scholar-queue (adjudicate first) |
| `COPYRIGHT_RESTRICTED` | CC BY-NC-SA encumbrance | register, don't publish |
Each tag carries a `priority` that feeds `translation_targets.priority` (S9).

### 2.3 OCR routing (S3) — INTEGRATE, do not build
`SPEC-18-COMPLETE-PIPELINE.md` + `docs/global/README.md:45` are explicit: **not another OCR project** —
use **Kraken / eScriptorium / Transkribus / Vidyut**. So S3's OCR path = an adapter that calls an existing
HTR engine and emits normalized text that re-enters at S6. (This is the "something better found specced in
ip-graph" — SPEC-18 names the exact engines.)

### 2.4 Verse recovery (S8) — P0, the biggest data blocker
`FLAWS.md`, `HANDOVER`, `LAYER-DIVISION-OF-LABOUR` all name it. The mechanism exists
(`harvest_to_factory.py` extracts real verses from R2 TEI; `register_sources.py`/`register_harvest_sources.py`
commit `payload.verse`). **The gap: it isn't run for all works, and `run_r2_ingestion._commit_source` writes
metadata-only (no verse).** Fix = wire S8 so EVERY committed SOURCE carries `payload.verse`, closing
tantraloka's empty-SOURCE block. **Gate:** every committed SOURCE has non-empty `payload.verse`.

### 2.5 R2 as byte-truth (S5) — wire the read + artifact path (gaps G1-G9)
The client + content-addressing work. To make R2 the true byte store for sources + factory artifacts:
- **G1** env loader (var mismatch: code reads `PATALA_R2_BUCKET`, env has `R2_BUCKET_PATALA`).
- **G2** a `SnapshotStore.download(source, id)` pull helper (currently only `put_snapshot`).
- **G3** re-point intake (`register_sources`, `harvest_to_factory`, `corpus_state`, `acquire_*`) off local disk onto `SnapshotStore`.
- **G4** a factory-artifact sink (`put_asset` per T1/L0/.../C1 output).
- **G5** `object_id ↔ storage_key` linkage in the registry (the "artifact truth" identity).
- **G6** broaden R2 reads beyond SARIT (GRETIL/PANDIT/Muktabodha).
- **G7** a blob read/serve endpoint (R2 = *served* artifact truth).
- **G8** add boto3 to the Atlas venv.
- **G9** reconcile the bucket-model (one `patala` bucket vs the "four buckets" blueprint).

### 2.6 Explicit queueing (S9) — assessed→queued, tied to tags
Today any on-disk source auto-enters the scheduler. Build the explicit step: **a work may only be promoted
into the translation queue after S2 (state), S3 (route), S4 (tag+priority) all pass and S8 (verse) is
present** — so `queue=10` reflects *assessed, verse-carrying* works, not raw discoveries.

---

## 3. HOW IT CONNECTS TO THE CONFIRMED STACK (one machine, one evidence standard)
The expanded front produces the SAME artifact the translation stack already consumes: **a committed SOURCE
registry object with `payload.verse`**. Once S8 is met, the confirmed RAW→C1 run (S10) takes over unchanged.
So the integration is a clean seam: **front (S1-S9) → SOURCE with verse → confirmed translation (S10) →
post-C1 (S11) → openpatala (S12)**. Every stage logs a machine-readable trace; a full work's RAW→EDUCATION
trace is the "frontier proof."

## 4. PRIORITY ORDER FOR THE NEXT AGENT (gate-ordered)
| P | Task | Gate |
|---|---|---|
| **P0** | **Verse recovery (S8)** — wire `harvest_to_factory` + `register_harvest_sources` so every SOURCE has `payload.verse`; unblock tantraloka | every committed SOURCE has non-empty verse; tantraloka builds L0/L2 |
| **P1** | **Source-state assessment + storage (S2)** — consolidate into one stored `source_state` ladder | `source_state` stored + `check.py` validates it |
| **P2** | **Categorical tagging (S4)** + explicit queueing (S9) | a work is tagged + only assessed works enter the queue |
| **P3** | **R2 wiring (G1-G9)** — read + artifact path | sources + artifacts live in R2; served via an endpoint |
| **P4** | **OCR integrator (S3)** for scanned manuscripts | an OCR adapter re-enters normalized text at S6 |
| **P5** | **openpatala population (S12)** + lineage on served results | a new work appears in the ledger + read-plane with provenance |

## 5. THE HONEST BOTTOM LINE
**The RAW→C1 machine is confirmed by logged run; the acquisition front is 40% built (adapters + R2 client +
refinery spec + scattered state signals) but not consolidated into one assessed→tagged→queued→verse-carrying
flow.** The frontier is: close verse recovery (P0), consolidate source-state + categorical tagging (P1/P2),
wire R2 as real byte-truth (P3), integrate an OCR engine for manuscripts (P4), and populate openpatala with
provenance (P5) — all with the same logged-run, deterministic-gate, machine-readable-evidence method that
proved translation works.

*Sources: `docs/global/ingestion-refinery.md`, `ingestion/adapters/*`, `infra/r2_assets.py`, `ingestion/r2.py`,
`docs/process/04-r2-storage.md`, `pipeline/{source_ready,corpus_state,certificate_l0,harvest_to_factory,
register_sources,register_harvest_sources,factory_scheduler}.py`, `source-evidence/.../entity_reconciliation.py`,
`translation_targets.py`, `sivaqueue_targets.py`, `ip-graph/specs/SPEC-18-COMPLETE-PIPELINE.md`,
`/tmp/opencode/e2e-trace.json`.*
