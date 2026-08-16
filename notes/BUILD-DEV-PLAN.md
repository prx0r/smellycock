# BUILD DEV PLAN v2 — smellycock / openpatala / ingestor (post-review)

*2026-08-16 · a fresh build plan rebuilt from the full project context + the 4-agent deep review of the
ingestor, translator-finder, red-team, and Sanskrit/research layers. This supersedes the earlier v1 plan.
It is organized by PRIORITY, not by plane: correctness first (the review found real bugs + over-claims),
then the honest feature gaps. Every item maps to a real module + a reproducible gate.*

---

## 0. WHAT THE DEEP REVIEW FOUND (the ground truth the plan is built on)

A 4-parallel-agent review audited the ingestor, translator-finder, red-team, and Sanskrit layers. Verdict:
**the core is real and the gates reproduce** — but there are 3 correctness bugs, several over-claims, and
2 structural issues. These are the input to this plan.

### Verified solid (reproduced, don't redo)
- `translation_locator_test.py` → 10/10, genuinely live OpenAlex/Crossref/Unpaywall (real DOIs, not mocked)
- `translation_availability_test.py` → 11/11 (254 works / 60 EN / 192 none)
- `assess_test.py` → 16/16; `project_translation_test.py` → 10/10
- Red-team fixes are REAL — 6 fixes reproduce against the quarantined `data/_errors/redteam/` inputs
- IndicParam `llama4-scout-outputs.json` independently reproduces the paper's 44%/46% (strongest artifact)
- Cost projections ($428/$133) reproduce live; 413 OpenRouter models confirmed

### Real bugs to fix (correctness)
| # | Bug | Where |
|---|---|---|
| B1 | `live_checked` logic is INVERTED (reports True when no check ran) | `translation_availability.py:113` |
| B2 | `--live` is not live (reads static GRETIL registry; docstring claims archive.org) | `translation_availability.py:76-88` |
| B3 | eval answer-extraction regex breaks `"The answer is A."` → scored wrong | `eval_sanskrit.py:60` |
| B4 | `corpus_state.discover_works()` hard-crashes (MOUNT gone) → ledger frozen; source_ready/assess run on stale artifact | `corpus_state.py:30,146` |
| B5 | committed `assess.json` is schema-stale (no `projection` key) | `assess.py:275-281` |
| B6 | `build_translation_index` shipped a 0-live-call artifact while docstring claims live-at-build; meta file untracked | `build_translation_index.py` |
| B7 | `_enrich` "per-language" claim not implemented (any attestation → all translations `found_live`) | `translation_availability.py:58-59` |
| B8 | llama-3.2-3b score inconsistent: doc 26.7 vs committed 26.7 vs working-tree 20.0 | `model-quality.json` |

### Over-claims / honesty fixes (anti-theatre, Result-Lineage)
| # | Issue | Where |
|---|---|---|
| O1 | "17/17 valid Sanskrit words" is fabricated (real list = 14, 13 hit) | ROUND2 log |
| O2 | "Every model's Sanskrit quality is now MEASURED" — only 2 of ~11 measured (n=50/n=30 smoke tests); rest assumed/paper | SANSKRIT-EVAL-ROUTER.md |
| O3 | Red-team "verified/regression" framing — no committed test guards the density/word-validity/empty-author fixes; verification was ad-hoc | ROUND reports + tests |
| O4 | measured scout 60% vs gold 44% — 16-pt gap unexplained; 60% treated as more authoritative than reproducible 44% | SANSKRIT-EVAL-ROUTER.md |
| O5 | measured entries lack Result-Lineage (no result_id/seed/n/date/commit) | model-quality.json |
| O6 | `REPORT-15-REPOSITORIES.md` is byte-identical to `SANSKRIT-REPOSITORIES-SURVEY.md` (duplicate) | research/ |

---

## 1. PHASE 0 — CORRECTNESS + HONESTY (do FIRST; all cheap, all block honest claims)

### 0A. Fix the 3 correctness bugs (B1, B2, B3) — the highest-priority items
- **B1** `translation_availability.py:113`: fix `live_checked` so it means "a live check actually ran." Add a
  regression gate (test that `live=False` → `live_checked=False`).
- **B2** `translation_availability.py:76-88`: EITHER implement the real archive.org/`verify_editions` live
  call, OR downgrade the docstring/CLI so `--live` honestly says "read the static verification registry."
  Anti-theatre: the docstring must match behavior.
- **B3** `eval_sanskrit.py:60`: fix the extraction regex to handle `"The answer is A."`/`"Answer: A"` etc.;
  add a unit test for extraction; re-measure the two models with correct extraction + record Result-Lineage.

### 0B. Fix the staleness + structural bugs (B4-B8, O6)
- **B4** `corpus_state.py`: make `discover_works()` fail-soft when the mount is absent (don't crash) — it must
  reconcile the ledger or explicitly flag it stale. The ledger is the shared dependency of source_ready/assess.
- **B5** `assess.py`: re-run `--write-cache` so the committed `assess.json` gains the `projection` key (reconcile
  the artifact to current code).
- **B6** `build_translation_index.py`: reconcile the claim to behavior — either wire the real live build or mark
  the current artifact `curated_only` honestly + git-track the meta audit file.
- **B7** `translation_availability.py:58-59`: filter `live_attest` by language so `found_live` is per-translation.
- **B8** `model-quality.json`: reconcile the llama-3.2-3b value to ONE source of truth (doc/committed/tree agree).
- **O6** delete (archive) the byte-identical `REPORT-15-REPOSITORIES.md` duplicate; keep the survey.

### 0C. Fix the over-claims (O1, O3, O5) — the anti-theatre pass
- **O1** correct the ROUND2 log's "17/17" to the real 14-word list / 13 hits.
- **O3** add committed regression tests that actually exercise the density gate, word-validity branch, and
  empty-author reconcile rule (currently only ad-hoc verified).
- **O5** add Result-Lineage to the measured model-quality entries (result_id, n, seed, date, commit).
- **O2/O4** soften the SANSKRIT-EVAL-ROUTER claims: state clearly only 2 models are smoke-measured (n=50/n=30)
  and the rest are paper/assumed; explain (or re-verify) the 60-vs-44 gap.

**Phase 0 gate:** all existing suites still pass (assess 16/16, locator 10/10, availability 11/11, projector
10/10) + new regression gates for B1/B3/O3 are green + ROUND2 log + docs agree with code.

---

## 2. PHASE 1 — P1: WIRE THE PER-LAYER MODEL INTO THE TRANSLATION WORKERS (the seam)
*The highest-value feature — but only after Phase 0 so it trains on honest signals.*
- Layer workers read `/layer-config` (or MCP `recommend_model_for_layer`) → set `HERMES_MODEL` per layer.
- Feed per-layer outcomes → `routing.log_feedback()` → LinUCB learns real quality/cost.
- Deliverable: the deal-radar → translation-stack integration actually runs.

---

## 3. PHASE 2 — P2: SERVE THE DEAL-RADAR ON OPENPATALA
- Expose `/recommend`, `/benchmarks`, `/recommend-layer` as public openpatala projections (additive).
- Surface the per-layer config + the model leaderboard.

---

## 4. PHASE 3 — P3: IMPORT MITRASAṂGRAHA GOLD + QUALITY GATE
- Download the Tantrāloka 4,550 pairs → score our L2/C1 output → a real translation-quality number.
- Gate promotion on the benchmark score (the ONE-RULE quality gate).
- NOTE: the eval harness must be fixed (B3) BEFORE this, or the gate is untrustworthy.

---

## 5. PHASE 4 — P4: ATLAS POSTGRES
- Deferred until the read layer measures a need (perf rule 6). Not a build now.

---

## 6. THE GATES (run after any change)

```bash
# ingestor (patalacheckpoints)
cd /root/patalacheckpoints
for p in assess translation_availability translation_locator project_translation; do
  PYTHONPATH=pipeline python3 pipeline/${p}_test.py | grep SUMMARY; done
# deal-radar (the model layer)
cd /root/dealradar && python3 app/test.py   # 7/7 (all test_*.py → 65)
# smellycock (reference)
cd /root/smellycock && python3 check.py --status
```

---

## 7. WHAT'S NOT MINE / NOT A BUILD (keep off the plan)
- **The T1/L0/L2/C1 translation generation** is the other agent's Hermes-driven lane — I feed it (assess/
  availability/projector + per-layer model), I don't own the worker.
- **The 121 uncommitted files in patalacheckpoints** are the other agent's live lane — don't touch.
- **P4 Postgres** — explicitly deferred by the perf doctrine until a measured need.

---

## 8. THE PRIORITY (one line)
**Phase 0 (fix B1/B2/B3 + the staleness + over-claims) → P1 (wire per-layer model) → P2 (serve) → P3
(Mitra gold gate) → P4 (Postgres).** Correctness and honesty first — nothing new is real until the existing
claims reconcile to code.

*This supersedes BUILD-DEV-PLAN v1. Phase 0 is the immediate work; it clears the real bugs + over-claims the
review found, so P1+ build on honest ground.*
