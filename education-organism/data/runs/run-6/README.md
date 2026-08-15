# RUN 6 — the audited endgame site (live)

*2026-08-15 · made the education-serving organism LIVE and aligned it with the OG patala site's
endgame surface (schools, timeline, foundations, tantraloka resources) — but audited through the
organism.*

---

## What was made live

| Surface | Route | HTTP | What |
|---|---|---|---|
| Static Astro site | `/` + `/bibliography/` + `/themes/` | 200 | the OG surface (compiled, 0-JS) |
| **Audited learning** | `/learning/` | 200 | 7 schools · 3 foundations · timeline — each with epistemic_ceiling + provenance |
| **Education lessons** | `/education/` + `/education/{lesson}/` | 200 | the LearningPackets (real, ENGINEERING_VALIDATED) |
| Education API | :8787 `/education` · `/resolve` · `/answer` | 200 | index + audit trail + tutor grading |
| Learner store | SQLite | — | learner events persisted |

## The astro build (the key product-surface fix)

- Installed `astro` (+ approved esbuild/sharp), ran `build_static_patala.py` with the correct
  `PATALA_ROOT`, built the site: **10 pages** (bibliography, themes, passages, scholars, education ×4,
  learning, index). Reading pages are **0-JS** (perf doctrine rule 4).
- The OG education pages now compile + serve (they were dead files before — the red-team found they
  couldn't build).

## The audited endgame (the OG site, organism-grounded)

The OG learning page (schools, shared foundations, timeline, geography) is now compiled into an
**audited projection** (`site/learning/learning-index.json`): each foundation carries an honest
`epistemic_ceiling` (MACHINE_PROPOSED / ENGINEERING_VALIDATED) + provenance, and resolves via
`/resolve` to its source chain — not free-floating prose.

## Performance (perf doctrine budgets)

- API `/education`: **~1.4ms** (cached p95 target < 50ms ✅)
- `/resolve`: 0.19s (the audit resolver)
- Lesson page: **4.8KB** (< 100KB target ✅); **0 JS** on reading pages ✅

## Files

- `site/learning/learning-index.json` — the audited learning projection
- `scripts/serve-education.py` — the API (stdlib, :8787)
- `scripts/compile-og-learning.py` — the OG→audited compiler
- `web/dist/` — the built static site (10 pages)

*Replayable: `npx astro build` + `python3 scripts/serve-education.py 8787`. This is the OG endgame
surface, made audited + live through the organism.*
