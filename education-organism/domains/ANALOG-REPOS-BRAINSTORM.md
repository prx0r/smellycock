# ANALOG-REPO BRAINSTORM — what's useful for the organism pipeline

*2026-08-15 · reviewed the 5 recently-cloned analog repos (Saktumiva/upama, SuttaCentral, Bilara,
Ambuda, graphGita) against the education-serving organism + derivation chain + audit trail I built.
Each: the verified gem, the source, and how it upgrades OUR specific work. Grounded in what I actually
checked in the code, not the gem-assessment prose.*

---

## The verified gems (ranked by value to OUR pipeline)

### GEM-A — Bilara's `(segmentId, field)` provenance keying ⭐⭐⭐ (THE data spine)
**Verified:** `bilara/server/bilara_types.py` — `Segment = {segmentId, field, value}`. A stable segment
id + a named field (layer) + content. Translation layers live in separate dirs (`root/`, `translation/`,
`comment/`).
**Why it upgrades US:** Our derivation chain (SOURCE/T1/L0/L2/L200/C1/THEME/ARG/SYNTH/ESSAY/EDUCATION)
currently keys layers by a bare `work:verse` id with loose links. Adopting **`segmentId:field`** as the
atomic anchor means EVERY downstream layer (translation, theme, argument, essay claim) carries a stable
provenance key — the audit resolver traverses one spine instead of guessing seams. **This is the
highest-leverage steal.**

### GEM-B — SuttaCentral's `muids` parallel-merge + `uid_matcher` range resolution ⭐⭐⭐
**Verified:** the platform merges root + all translation/comment layers by multilingual-UID into one
segmented view; `uid_matcher` expands id ranges (`an1.1-10`) to concrete segment sets.
**Why it upgrades US:** (1) the parallel-stack merge is the L0→L200 rendering engine; (2) `uid_matcher`
is exactly the audit resolver's "which segments support this claim" primitive — turning a claim's
citation into concrete source segments.

### GEM-C — Ambuda's reconciliation gate (LLM never changes source) ⭐⭐⭐ (the anti-theatre gate)
**Verified:** `reconciliation_check.py`/`llm_structuring.py` — the prompt contract is "add tags, NEVER
change text"; a thresholded diff-check (line-count + hyphen preservation, absolute AND relative) catches
bulk corruption of LLM-structured output.
**Why it upgrades US:** Our SYNTHESIS/ESSAY/EDUCATION are LLM-derived — exactly where provenance gets
corrupted. A **reconciliation check** on every generated layer proves the tutor/essay "preserved source
while adding structure." This is the honest gate for the AI tutor (no misquoting) + the derivation chain.

### GEM-D — Upama's normalization-filter taxonomy + siglum apparatus ⭐⭐ (the missing manuscript layer)
**Verified:** `upama.php` matches TEI nodes by `xml:id`, applies tag/hide/sub/whitespace filters
(orthographic normalization), gets each witness's `siglum`, and renders the apparatus.
**Why it upgrades US:** our SOURCE layer is single-curated, not multi-witness. A **collation** step
(witness→variant→apparatus) makes SOURCE honestly multi-witness and gives the audit resolver a real
variant spine (siglum = provenance anchor).

### GEM-E — graphGita's `problem_solution_map.json` (THEME→source curriculum) ⭐
**Verified:** `problem → description → [{chapter, shloka}]` + `theme_progression` + `primary_theme`.
**Why it upgrades US:** the seed structure for the THEME→EDUCATION curriculum — re-key its chapter:shloka
onto Bilara-style segment anchors so thematic claims inherit provenance. The MCTS/KG-RAG code is
aspirational; the data schema is the steal.

---

## How it maps to what I built (the connection)

| My build | The analog gem that upgrades it |
|---|---|
| derivation-edge linker + audit resolver | GEM-A (segment key spine) + GEM-B (uid_matcher expansion) |
| education-serving site | GEM-B (parallel merge rendering) |
| AI tutor | GEM-C (reconciliation gate — tutor never misquotes) |
| SOURCE layer | GEM-D (collation — multi-witness variants) |
| THEME→EDUCATION curriculum | GEM-E (problem→source schema) |

## The highest-value build (recommended)

**Adopt the `segmentId:field` provenance keying (GEM-A) + the reconciliation gate (GEM-C) into the
derivation chain + tutor.** These two are the data spine + the honesty gate — the others hang off them.

1. Re-key our passage objects to `segmentId:field` so every layer anchors to one atomic id.
2. Add a reconciliation check to the ESSAY/EDUCATION generation (prove source preserved).
3. (Later) add the upama-style collation to make SOURCE multi-witness.

---

## The honest take

The analogs **validate** the direction (immutable passage + multi-layer projection + divergence) and give
**stealable processes, not code to copy**. The two that matter most for OUR organism are **Bilara's
segment-anchor keying** (the provenance data spine the audit resolver needs) and **Ambuda's reconciliation
gate** (the anti-theatre check that keeps every generated layer honest). They're the natural next step to
make the education-serving organism fully provenance-anchored and trustworthy.
