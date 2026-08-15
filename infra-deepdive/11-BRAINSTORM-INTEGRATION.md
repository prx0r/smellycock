# BRAINSTORM — what's best + the live-experiment plan for the whole integration

*2026-08-15 · a review of the entire stack + the brainstorm of what to integrate and in what order, decided
by LIVE experiments (the evidenced way of working — test both/alternatives, keep the winner, log it). Not
opinion: each tool-to-layer mapping below was probed against REAL committed data.*

---

## 1. WHERE WE STAND (honest, evidence-based)
| Area | State | Evidence |
|---|---|---|
| RAW→C1 translation | ✅ REAL, logged | `e2e-trace.json` 412s/3 calls/7 layers/`chain_ok:true`; 76 C1 |
| BS in post-C1 | ✅ Killed | `audit_postc1.py` PASS; registry honest (SYNTH/ESSAY/EDU=0); docs corrected |
| AI guards integrated | ✅ 10/10 real-data | `test_ai_guards_integration.py` |
| Post-C1 spine | ⚠️ mechanism, 0 data | THEME/ARGUMENT archived; SYNTH/ESSAY/EDU empty |
| Verse recovery | ⚠️ blocked (R2 G2) | noisy Devanagari can't be trusted; clean TEI unreachable |
| R2 read-path | ❌ not wired | client exists, factory reads local disk only |

## 2. THE KEY BRAINSTORM INSIGHT (from the live experiments)
**Tool-to-layer mapping matters — forcing a tool onto the wrong layer creates BS.** Two live experiments proved it:

### Experiment 1 — the quote-guard on all 74 committed C1 → SKIPPED all 74
C1 objects are **structured commentary with no `“”` quote markers**, so the quote-verifier has nothing to
check. **The guard is NOT for C1 commentary.** It IS for the prose layers (ESSAY/LESSON/tutor answers) that
carry `“...” 【《X》第N章】` citations — exactly where the BS lived (server3's single-word EDUCATION).

### Experiment 2 — GEM-C (word-preservation) on 4 real L2 translations → BLOCKED 3/4
L2 rephrases **Sanskrit→English**, so word-preservation drift is natural (drift 0.91-1.0). **GEM-C is NOT a
translation-fidelity gate.** It IS for **tag-preserving derivations** (L200's 8-section audit wraps L2
content; claim/XML wrapping) where bulk content-drops must be caught.

### The resulting mapping (the "what's best")
| Tool | Right layer | Why | Wrong layer (would be BS) |
|---|---|---|---|
| **guard** (quote-verify + citation whitelist) | ESSAY, LESSON, tutor answers | prose with citations | C1 commentary (no quotes) |
| **GEM-C reconciliation** (word-preservation) | L200 8-section audit, claim-wrapping, XML derivations | tag-preserving, must not drop source | L2 translation (cross-language drift) |
| **GEM-A segment keys** | object identity | stable `segment:version` | — |
| **semantic gold** (embedding/LLM-judge) | T1/L2/C1 quality | the real "is it faithful" measure | Jaccard (0.091, meaningless) |
| **L200 derivational audit** | C1 provenance | the 8-section moat (already exists) | — |

## 3. THE STRATEGIC FORK — depth-first vs breadth-first
| Strategy | What | Risk | Evidence to get |
|---|---|---|---|
| **DEPTH-first** (recommended) | Prove **ONE** work RAW→EDUCATION end-to-end: real C1 → THEME → ESSAY → LESSON, gold-scored, guarded, human-signed | slower to "more works" | the full spine + the gold/human/guard standard, ONCE |
| **BREADTH-first** | grind the 100-work sivaqueue through RAW→C1 with guards | produces volume without the gold/human closure (repeats the current "thin C1" problem) | throughput only |

**Recommendation: DEPTH-first.** It de-risks everything: it forces ONE real essay + ONE real lesson (which the
guard can then verify), sets the gold + human + guard standard on real output, and proves the RAW→EDUCATION
E2E. Breadth is then a mechanical grind on a proven spine.

## 4. THE EXPERIMENT QUEUE (each live-log-tested, alternatives compared, winner kept)
| # | Experiment | Test both | Log-test gate | Decides |
|---|---|---|---|---|
| E1 | **Verse recovery: R2-TEI vs Devanagari-split** | wire R2 read (G2) + `harvest_to_factory` vs `verse_recover` on the same work | verse quality (danda/structure, no titles) | the real verse-recovery path |
| E2 | **Gold scorer: Jaccard vs embedding vs LLM-judge** | all 3 on the same committed T1/L2 vs real golds | discriminative (separates good from bad) | the "is it faithful" gate |
| E3 | **Guard on ONE real essay** | build 1 essay via the spine, run the guard | guard verifies real cites, downgrades fabricated | enforce-in-factory vs flag |
| E4 | **GEM-C on L200 audit** | run GEM-C on a real L200 8-section wrap | catches a bulk content-drop | wire as an L200 sub-gate |
| E5 | **Post-C1 order** | THEME→ESSAY vs ESSAY-direct | real promoted output | the rebuild path |

## 5. THE RECOMMENDED BUILD ORDER (integrating everything, not BS)
1. **E1 — wire the R2 read-path (G2)** → real verse recovery (unblocks the data). Highest leverage.
2. **DEPTH — one work RAW→EDUCATION**: real C1 → THEME → ESSAY → LESSON on real, gold-scored, guarded content.
3. **E2 — semantic gold scorer** → makes "faithful" measurable (the real C1/L2 gate, NOT Jaccard/GEM-C).
4. **E3 — wire the guard into the ESSAY/LESSON validator** (enforce, fail-closed on fabricated cites).
5. **E4 — GEM-C into the L200 audit** (catch bulk content-drops).
6. **E5 — the human + promotion gate** → nothing is "real" without it (THE ONE RULE).
7. Then **BREADTH** — grind the sivaqueue on the proven, gold-scored, guarded spine.

## 6. THE ONE-LINE
> **The experiments proved the tools must map to the right layers (guard→ESSAY/LESSON, GEM-C→L200-audit,
> semantic-gold→T1/L2/C1, never the wrong one). Go DEPTH-first: wire R2 verse recovery, prove ONE work
> RAW→EDUCATION with real gold + guards + human sign-off, then scale breadth on the proven spine.**

*Sources: `audit_postc1.py`, `test_ai_guards_integration.py` (10/10), Experiment 1 (guard skipped all 74 C1),
Experiment 2 (GEM-C blocked 3/4 L2), `/tmp/opencode/e2e-trace.json`, the server3 suite (52/53 on this box).*
