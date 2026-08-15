# AGENTS.md — governing file for serveragent3

*2026-08-15. This is a **production-grade POST-C1 scholarship engine** — the derivational spine
(THEME → ARGUMENT → SYNTHESIS → ESSAY → LESSON) over a grounded C1 floor, driven by Hermes for
GENERATION and deterministic `.py` for REDUCTION. Built to the smellycock/patalaorg AXIOMS.*

---

## 0. THE ONE RULE

> **Nothing is "real" because code exists. It is real only when an independently defined task, human-
> grounded gold, and a reproducible gate show it does what it claims. A gate is done, not a file.**

## 1. THE ARCHITECTURE (mirrors the production stack)

- **Hermes for GENERATION, `.py` for REDUCTION.** Hermes reads real files and derives content; the
  deterministic kernels validate, aggregate, gate, and commit. Never hand-feed a validator.
- **Eligibility is deterministic Python**, never an LLM judgment.
- **Fail-closed, validate-first** — wrong is worse than none; abstain rather than fabricate.
- **Authority invariant:** `authority(projection) ≤ authority(parent)`. Object TYPE ≠ epistemic STATE.

## 2. THE LAYER DAG (canonical)

```text
source → draft_translation(T1) → tokenization(L0) → [argument_outline] → translation(L2) →
translation_proof(L200) → commentary(C1) → theme/argument → synthesis → essay → lesson
```
- Multi-parent rule: a layer is eligible only when EVERY required parent is committed.
- We operate ABOVE C1: `commentary(C1) → theme/argument → synthesis → essay → lesson`.

## 3. THE STATUS LADDERS (frozen — never invent a 5th)

- Object epistemic: `MACHINE_PROPOSED → ENGINEERING_VALIDATED → SCHOLARLY_CORROBORATED →
  INDEPENDENT_REVIEWED → ADJUDICATED`.
- Registry object: `GENERATED → ENGINEERING_VALIDATED → SPECIALIST_REVIEWED`.
- Build: `DISCOVERED < PROTOTYPED < VALIDATED < INTEGRATED < PRODUCTION`.
- How-known (Eigenius): `ASSERTED · EXTRACTED · RECONSTRUCTED · EVIDENCE_GROUNDED · HUMAN_REVIEWED ·
  ADJUDICATED`.

## 4. THE BANNED WORDS

- **Banned:** `PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS`.
- **Use:** `SUPPORTED BY · PASSED CHECK X · MACHINE-PROPOSED · REVIEWED BY · NO CONFLICT DETECTED`.

## 5. THE OPERATING AXIOMS (non-negotiable)

1. **Never `sleep` to wait** — background long jobs (`setsid … &`), poll the log.
2. **Never `pkill`** — find the exact PID, `kill <PID>`.
3. **RAM is the scarcest resource** (4-core/8GB/no-swap, 2 agents) — stream, never bulk-load.
4. **Compute on write, read from bytes.** One question = one request.
5. **RUNNING TESTS IS NOT WORK** — a green suite on unchanged code is noise.
6. **Every result resolves** to `result_id · benchmark · gold · model · code_commit · split · seed ·
   config · date`, or it doesn't exist.

## 6. THE GATE (before claiming done)

```bash
cd /root/smellycock/education-organism
python3 scripts/check.py --status   # resolves refs + reconciles counts + gates
```

*This is a projection of the real build. Run the validators after any change; never present DESIGN as
BUILT.*
