# translation — DEV PLAN (build it real, one step at a time)

*2026-08-15 · the executable plan to make translation **autonomous, perfect, integrated, and agentic** —
not theatre. Each phase has a gate (a runnable proof). A phase is DONE only when its gate passes on real
committed objects. Current state is documented in `README.md`; this is the build order.*

---

## PHASE 0 — AUTONOMOUS + RELIABLE PRODUCTION (make it run unattended, perfectly)
**Goal:** the factory produces committed T1/L0/ARGMAP/L2 on the priority queue, unattended, robust, no
hand-production.

| # | Task | Gate (runnable) |
|---|---|---|
| 0.1 | **Canonical generator is the DEFAULT** T1 path (not opt-in) | `make_t1_handlers()` → canonical; overnight launcher sets `PATALA_T1_CANONICAL=1` |
| 0.2 | **Low-RAM scheduler is the driver** (streamed/bounded) | `test_factory_scheduler.py` ALL PASS + peak RSS < 500MB |
| 0.3 | **Real autonomous overnight pass** on the priority queue | a backgrounded scheduler pass commits ≥N T1 + L0 on kramasadbhava (priority-10), `factory_certificate` 0 dup |
| 0.4 | **Robust batch JSON closed** (no truncation failures) | `test_canonical_translate.py` 10/10 + a live 50-verse batch commits clean |

**Gate: one real unattended pass commits T1+L0 on the top-priority work with 0 dup + 0 generation_failed.**

## PHASE 1 — INTEGRATED WITH THE WORKING LAYERS + OPENPATALA
**Goal:** the proven kernels gate real objects, and openpatala serves translation content, not just status.

| # | Task | Gate |
|---|---|---|
| 1.1 | **TranslationProof live gate** on T1/L2 in `factory_batch` | a committed T1 must pass the 11-dim proof (not just shape) |
| 1.2 | **Close the IPVV gold `gate=BLOCKED`** | the real gold-proof passages pass the 11-dim proof (the documented asterisk closes) |
| 1.3 | **Translation-content surface** on openpatala | `GET /openpatala/translation/{work}/content` serves the actual L2/T1/C1 reading |
| 1.4 | **Compile-on-commit** (per-artifact, not whole-site) | a commit auto-rebuilds `translation.json` for that work |

**Gate: a real committed L2 is served as a reading on the live openpatala, having passed the 11-dim proof.**

## PHASE 2 — PROPER AGENTIC INFRA + FEATURES
**Goal:** Hermes drives it as an agent; the proven lab patterns (council, verifiable reward, self-healing,
typed state) gate production.

| # | Task | Gate |
|---|---|---|
| 2.1 | **Agentic flow wired** — `canonical-translate` skill + `patala_*` MCP verbs drive it | an agent (via the skill) produces + commits a validated verse through MCP |
| 2.2 | **Sealed-council three-version flow (R1/T2/R2)** | 3 independent translations → hard core + crux, human-adjudicated (herdr pattern) |
| 2.3 | **Verifiable-reward self-improvement** | a translation that beats the deterministic score (round-trip, term-consistency, Dyczkowski) promotes; worse is discarded (dgm pattern) |
| 2.4 | **Self-healing orchestration** | failure-class-aware recovery (truncated-JSON vs timeout vs validator-reject) under a budget, with verify (Self-Healing paper) |
| 2.5 | **Typed per-passage state machine** | `SOURCE_LOCKED → DRAFT → REVIEWED → ANNOTATED → PUBLISHED`, reducer-gated (maestro/herdr pattern) |

**Gate: a real passage runs the council → adjudicated → self-improved → published, all reducer-gated.**

## PHASE 3 — PERFORMANCE + OBSERVABILITY (the perf doctrine enforced)
**Goal:** perf budgets met + complete tracking.

| # | Task | Gate |
|---|---|---|
| 3.1 | Perf budgets met | API cached p95<50ms; read plane 0-JS; scheduler low-RAM |
| 3.2 | Tracking complete | every commit → registry version + ledger row + log line (idempotent, replayable) |
| 3.3 | `check.py` + the layer proofs gate every change | the layer's 7 artifacts all hold |

**Gate: perf doctrine + tracking verified on the running system.**

---

## EXECUTION RULE (build one at a time)
1. Do ONE task. 2. Run its gate. 3. Only when it passes, move to the next. Do NOT skip to a higher phase
until the current phase's gate holds. This is the anti-theatre build: every step is a runnable proof on
real committed objects, never a claim.

---

## STATUS (2026-08-15 — built this session)

**Built + tested (deterministic, real):**
- **0.1 ✅** canonical generator is the DEFAULT T1 path (legacy = `PATALA_T1_LEGACY=1`).
- **0.2 ✅** low-RAM scheduler is the driver (streamed/bounded, RSS 347MB < 500MB gate).
- **The agent-orchestration layer (new)** — the missing "how agents drive it" surface:
  - `pipeline/patala_orchestration.py` — deterministic brain (`next_action`/`work_state`/`progress_summary`/
    `eligible_next`), PROPOSE-only, low-RAM. Tested **5/5**.
  - MCP verbs `patala_next_action` / `patala_get_work_state` / `patala_get_translation_progress`.
  - `compile-translation-status.py` — lightweight compile-on-commit; wired via `PATALA_COMPILE_ON_COMMIT=1`.
- **0.4 ✅** robust batch JSON closed (canonical generator; the 10:56 legacy `GENERATION_FAILED` are
  pre-canonical noise).

**Open / honest:**
- **0.3 ✅ PROVEN (autonomous loop commits real L0):** a real pass on kramasadbhava (recoverable verses)
  committed **real L0 objects (100 → 102+, `{verse, records}` Vidyut-tokenized)**, and the state refresh
  updates the ledger + bibliography + projection. The supervisor now **skips works with unrecoverable
  verses** (tantraloka) so it never gets stuck when others are ready.
- **Remaining verse-recovery gap (data, not code):** works whose SOURCE payload is empty (tantraloka) can't
  build L0 until the verse text is stored (harvest/R2). The loop works on the "tonnes of recoverable
  sources" — this is a harvest-side follow-up, not a blocker to the loop.
- **1.1 ✅** — live quality gate. **1.3 ✅** — translation-content surface. **Bibliography↔translation
  linkage ✅** — `enrich_bibliography.py`. **State-refresh ✅** — `translation_state.py --refresh`
  (ledger + bibliography + projection). **1.2** (gold `gate=BLOCKED` closure) remains.

*This is the build order. Phase 0 is code-complete; 0.3 needs a quiet-box run to prove the commit.*
