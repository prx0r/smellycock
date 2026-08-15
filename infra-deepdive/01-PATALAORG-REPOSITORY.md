# INFRA DEEP-DIVE 01 — THE PATALAORG REPOSITORY (both lanes)

*2026-08-15 · a full-context audit of `/root/projects/patalaorg` (remote `prx0r/smellycock`). What is
actually in the production docs repo, both lanes, the MANIFEST, and the validators — with the honest
verdict on whether the "fully merged, aligned, check.py PASS" claim holds.*

---

## 1. WHAT PATALAORG IS
The **canonical documentation repo**. It holds the doctrine (AGENTS/AXIOMS/OBJECT-MODEL/MANIFEST), both
lanes' domain docs, and the run records. The CODE lives elsewhere (patala + ip-graph); patalaorg is the
**projection** — which is exactly the ONE RULE's warning: a doc is a projection, the truth is the registry.

## 2. TOP-LEVEL DOCTRINE
- **`AGENTS.md`** — the ONE RULE (nothing "real" without task + gold + reproducible gate) + operating rules.
- **`AXIOMS.md`** — 8 naming conventions, the ONE layer taxonomy (§1.3, 11 layers), 12 operating axioms
  (§3), 4 status ladders (§4, "never invent a 5th"), banned words `PROVED/TRUTH/CORRECT/EDITOR APPROVED/
  BEST/WINS` (§5), commit conventions (§6), "final production docs only" (§7), agent-speed (§8).
- **`OBJECT-MODEL.md`** — the canonical DAG
  `source → draft_translation → tokenization → [argument_outline] → translation → translation_proof →
  commentary → theme/argument → synthesis → essay → lesson` (lines 11-28) + multi-parent eligibility rules.
- **`MANIFEST.json`** — registers **30 docs** (translation 8, openpatala 5, factory 1, read-plane 1,
  epistemic 8, post-c1 1, plus top-level + performance). Also has an `implementation` section (29 entries)
  with paths to code.
- **`check.py`** — the validators (below).

## 3. THE TWO LANES (the split)

### Lane A — TRANSLATION (real code, present)
| Domain | Claims | Reality |
|---|---|---|
| `domains/translation/` (8 files) | complete RAW→C1 pipeline, counts T1 608/L0 796/ARGMAP 50/L2 3/L200 67/C1 66 | ✅ **REAL.** All pipeline code present in `/root/projects/patala/pipeline/`. Counts now HIGHER (T1 631/L0 948/ARGMAP 79/L2 22/L200 86/C1 76). Docs slightly stale but directionally true. |
| `domains/factory/` (1) | 11 pipeline pieces, each gated | ✅ **REAL.** Files present. |
| `domains/read-plane/` (1) | static-site builder, status compiler, gold scorer | ✅ **REAL.** In `ip-graph/scripts/`. |
| `domains/openpatala/` (5) | OpenAlex-grammar API + edge site | ✅ **REAL.** Docs + `openpatala/` + `web/` + `site/` present. |

### Lane B — POST-C1 / EPISTEMIC (docs only on this box)
| Domain | Claims | Reality |
|---|---|---|
| `domains/post-c1/` (1 of 6 files present) | product index of 9 gate scripts (Nyāya, cite-contract, blind-assessor, signed-attestation, ingest-ipvv, emit-openpatala) | ❌ **ALL 9 scripts MISSING** from `ip-graph/scripts/`. 5 of 6 doc files (`model.md`, `reference.md`, `agentic.md`, `recipes.md`, `validation.md`) missing. |
| `domains/epistemic/` (8) | "25 product engines" | ❌ **Only `pipeline/products/README.md` (a pointer) exists.** The pointer admits modules are "on server2". Counts in docs are mutually inconsistent (134/134, 80/80, 127/127, 19, 25, 26). |

**THE KEY FACT:** the epistemic/post-C1 lane is **unbacked documentation on this machine** — every
referenced `engine.py`/`test.py` and 5 of 8 registry files are missing. `check_epistemic.py` FAILS with 58
issues (48 = missing product engines under the checkpoints dir `patalacheckpoints`, 8 = empty/missing registries).

## 4. THE RUNS
| Run | What it actually proves |
|---|---|
| `live-run-1/` | L0 drain 168→180 (12 commits, ~550MB stable). Real logs (`factory-pass.log`, `fullchain-watchdog.log`, `MONITOR-REPORT`, `samples-30s.jsonl`, `status-constant.jsonl`). Proves L0 — the EASY layer. |
| `live-run-2/` | L0 198→217, memory stable, "10 passages, plan 2/4". Real logs present. |
| `live-run-3..5` | ❌ **DO NOT EXIST in patalaorg.** They live in the working patala repo's `data/ops/`. |
| `education-organism-run-4/` | ❌ **Misleading name.** There is NO "education organism run 4" — that string appears nowhere. (In patala, `live-run-4` is the TRANSLATION lane's RAW→C1 run.) The patalaorg `education-organism-run-4/` has pre-recorded logs (`e2e.log` 5/5, `tests.log` 17/17, `check.log` "PASS") pointing at scripts (`link-derivation-chain.py`, `audit-resolve.py`, `compile-education.py`, `tutor-agent.py`, `test-e2e.py`) that **do not exist here** (the `serveragent3` dir is missing). |
| `server2-post-c1-spine/` | Docs only (README + BUILD-PLAN). No executable evidence. |
| `BRAINSTORM-3-BUILDS.md` | **Design, not build** — a brainstorm for 3 architectures. Violates "no DESIGN as BUILT" if presented as done. |
| `MONITOR-REPORT`, `OPTIMIZATION-ANALYSIS`, `experiments/` | Real monitoring + analysis. `experiments/EXPERIMENT-COMPARISON.md` honestly records a **POST-RUN CORRECTION**: whole-chain (Build 1) is "UNRELIABLE AT SCALE", per-layer factory (Build 3) is the production path. |

## 5. THE VALIDATORS — what `check.py` actually does
- `check.py --refs` (lines 62-87): asserts MANIFEST docs exist on disk + scans `.md` files for backticked
  backticked absolute paths (of the form an absolute path beginning in root or mnt), resolving through `PATH_ALIASES` (31-42). **Only backticked absolute
  paths in `.md` are checked** — bare relative refs (e.g. `pipeline/x.py`) are NOT validated.
- `check.py --naming` (90-103): banned-word filenames + `SPEC-NN` pattern. Trivial.
- `check.py --manifest` (106-116): JSON valid + has `docs`/`axioms` keys. **Does NOT validate
  `implementation`/`performance`/`runs` paths** — a dangling entry is silently accepted.
- `check.py --status`/`--counts` (119-137): imports `object_registry` + calls `R.summary()`, which scans the
  **850MB `source-registry.jsonl`** → **times out (exit 124).** The documented drift gate does not terminate.
- `check_epistemic.py`: the epistemic lane's validator → **FAILS, 58 issues** (missing products + registries).

## 6. ALIGNMENT VERDICT (verify the claim)
| Claim | Verdict |
|---|---|
| "check.py PASS" | ⚠️ **Only `--refs --naming --manifest` passes.** The full `--status` gate hangs. |
| "fully merged" | ❌ **No two real git lanes.** `master == origin/main` (both `0fecc49`), single linear history. The "merge" is narrative in ALIGNMENT-REVIEW.md, not git structure. |
| "both lanes aligned" | ❌ **Not aligned on this box.** Lane A is real; Lane B is docs/pointers only. |
| ONE RULE + AXIOMS shared | ✅ **Consistent across both lanes' docs.** |
| Canonical DAG consistent | ✅ `OBJECT-MODEL.md` ↔ `domains/post-c1` README ↔ `AXIOMS.md`. |
| ALIGNMENT-REVIEW.md honesty | ✅ It honestly admits gaps #2/#3 (products on server2, no unified E2E). Gap #1 (post-c1 not in MANIFEST) is now STALE — post-c1 was registered in commit `1340f57`. |

## 7. CONCRETE GAPS / DANGLING REFS (all verified missing)
1. All 9 post-C1 gate scripts in `domains/post-c1/README.md:39-47` + `MANIFEST.json:256-303`.
2. 5 of 6 `domains/post-c1/` doc files.
3. All 26 epistemic product engines (only the `products/README.md` pointer exists).
4. `check_epistemic.py`'s checkpoints path (`patalacheckpoints`) doesn't exist → 56 missing-file errors.
5. Registries synthesis/essay/education missing; argument=10 vs claimed 23; C1=76 vs claimed 42/43.
6. `runs/live-run-3,4,5` don't exist in patalaorg.
7. MANIFEST `implementation` paths for `fuck-off`, `serveragent3`, `patalacheckpoints` (the other agents' boxes) are dangling (unvalidated by `check.py`).
8. Disk is **90% full** (51G/59G), not "100% full" as AGENTS.md:74 claims.

## 8. KEY PATHS
- Doctrine: `AGENTS.md`, `AXIOMS.md`, `OBJECT-MODEL.md`, `MANIFEST.json` (all in `/root/projects/patalaorg`)
- Validators: `check.py`, `check_epistemic.py`
- Lanes: `domains/translation/`, `domains/post-c1/`, `domains/epistemic/`
- Runs: `runs/`
- My audit: `ALIGNMENT-REVIEW.md`, this `infra-deepdive/`
