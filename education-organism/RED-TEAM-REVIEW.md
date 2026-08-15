# RED-TEAM / FLAWS REVIEW — serveragent3 (external adversarial audit)

*2026-08-15. A hostile external audit of serveragent3, the "production-grade POST-C1 scholarship
engine." Every flaw below was independently VERIFIED against the actual code + committed data (not just
claimed). This is the anti-theatre audit applied to my own build — and it does not survive.*

---

## VERDICT

> **serveragent3 is not production-grade. Its own "anti-theatre" doctrine is itself the largest piece
> of theatre.** The deterministic gates are never wired to the commit path; data the gates would reject
> is already committed as ENGINEERING_VALIDATED; the DAG and authority invariant are unimplemented
> comments; the test suite green-lights broken real data while passing on synthetic inputs. It is a
> well-organized demo of a design, not a production epistemic engine.

---

## CRITICAL FLAWS (verified)

### CRITICAL-1 — ENGINEERING_VALIDATED granted with NO gate for 5/6 layers
`build-spine.py:56-60`:
```python
if layer == "ARGUMENT":
    g = gates.cite_contract("ARGUMENT")
    status = R.ENGINEERING_VALIDATED if not g["problems"] else R.GENERATED
else:
    status = R.ENGINEERING_VALIDATED   # <-- THEME/SYNTHESIS/ESSAY/EDUCATION: no gate
```
**Verified:** all 10 THEME/SYNTHESIS/ESSAY/EDUCATION objects are ENGINEERING_VALIDATED with no
validation. The one "gated" layer (ARGUMENT) is vacuous + order-dependent: `cite_contract` reads
`payload.argument` but the build stores content in `payload.derived`, so 0 premises are examined. Live:
ARGUMENT = 1 EV + 9 GENERATED (an artifact of processing order, not content).

### CRITICAL-2 — Committed data fails the engine's own quality gate; garbage stored as EV
**Verified:** EDUCATION objects contain `{"EDUCATION": "Postgraduate"}` and `{"EDUCATION":
"Pratyabhijñā (Kashmir Shaivism)"}` — the model returned a single-word answer and it was committed as
ENGINEERING_VALIDATED. The `quality` gate PASSes these because for non-ARGUMENT/C1 layers it only checks
`input_refs` resolve + payload non-empty — it never inspects whether the text is meaningful. All 10
committed ARGUMENT objects score quality **0.0 → BLOCK** (the gate looks in the wrong payload key).

### CRITICAL-3 — Authority invariant unenforced AND violated
**Verified:** `grep authority kernels/ scripts/` → nothing enforces it. It exists only as a comment.
Data violates it: `seed-c1.py` writes registry status `ENGINEERING_VALIDATED` while the object's own
`c1_status` is `"MACHINE_PROPOSED"` — a self-contradicting record. Upper layers (EV) sit at the same
authority as a C1 explicitly labeled MACHINE_PROPOSED.

### CRITICAL-4 — Multi-parent DAG eligibility not implemented
**Verified:** CANONICAL-DAG requires `SYNTHESIS: requires [ARGUMENT, THEME]`, but the committed
SYNTHESIS has `input_refs=['ipvv:165115d8eb7d']` — a single C1. `object_registry.eligible()` ignores
PREREQS and is **never called** anywhere. `chain` gate accepts any ref-to-C1, not the required parent set.
The pipeline is a flat C1→everything loop, not the DAG it claims.

---

## HIGH FLAWS (verified)

### HIGH-5 — input_hash is self-referential (no provenance anchor)
`input_hash = sha256(payload)` — the hash of the object's OWN output, not its parents/source/prompt.
Nothing links an object to what it was derived from. A forged object merely relabeling its source passes.

### HIGH-6 — Event ledger is forgeable
The chain has no secret/external anchor/signing key. Any writer of the file can recompute all hashes and
regenerate a "pristine" chain. Events carry no payload digest, so a registry record's content can be
swapped without the ledger noticing. "Tamper detection" only catches naive edits that don't re-hash.

### HIGH-7 — Test suite is circular; 10/10 green on broken data
`nyaya`/`blind_grade`/`quality` tests hand-feed synthetic dicts designed to hit the function's own
branches. `blind_grade` passes because the answer literally contains all rubric words. **No test asserts
quality ≥ PASS or cite_contract clean on the committed registries.** The suite passes while all 10
committed ARGUMENT objects score quality BLOCK and EDUCATION holds junk.

---

## MEDIUM FLAWS (verified)

- **MEDIUM-8** — `check.py --status` only runs `chain` + `verify_event_chain`; it never runs
  `quality`/`nyaya`/`cite_contract` on real data. Reports PASS on data its own engine would BLOCK.
- **MEDIUM-9** — `commit()` accepts arbitrary caller-supplied `status` with no enforcement; any script
  can commit ENGINEERING_VALIDATED/SPECIALIST_REVIEWED without a gate.
- **MEDIUM-10** — `seed-c1.py` auto-promotes the floor to EV with no gate; `evidence_quote`/`claim`/
  `summary` are blind `body[:200]`/`body[:150]` truncations (some mid-sentence), not real extraction.
- **MEDIUM-11** — the run log (`run-1/README.md`) overstates: claims "every object ENGINEERING_VALIDATED"
  but 9/10 ARGUMENT are GENERATED; claims "0 abstains" but EDUCATION is single-word junk; the "anti-cheat"
  section shows only ONE cherry-picked argument. The monitor snapshots are 3 identical rows 2s apart.

---

## LOW FLAWS

- **LOW-12** — `generation.py` `BASE` is env-overridable (a compromised env can exfiltrate the bearer
  key); no TLS pinning; passage text embedded in the prompt with no injection hardening.
- **LOW-13** — `run-tests.py` mutates the REAL live ledger during the tamper test (swaps it in, then
  restores); an interruption between swap and restore corrupts production data. Tests should use a copy.

---

## SUMMARY TABLE

| # | Severity | Flaw |
|---|---|---|
| 1 | CRITICAL | EV granted with no gate (5/6 layers); ARGUMENT gate vacuous + order-dependent |
| 2 | CRITICAL | "Postgraduate" EDUCATION stored as EV; all ARGUMENT score quality BLOCK |
| 3 | CRITICAL | Authority invariant unenforced + violated (EV vs MACHINE_PROPOSED) |
| 4 | CRITICAL | Multi-parent DAG not implemented; SYNTHESIS refs single C1; eligible() never called |
| 5 | HIGH | input_hash = self-hash (no provenance anchor) |
| 6 | HIGH | Event ledger forgeable, unanchored, no payload digest |
| 7 | HIGH | Test suite circular; 10/10 green on broken data |
| 8 | MEDIUM | check --status doesn't run production gates |
| 9 | MEDIUM | commit() accepts arbitrary status |
| 10 | MEDIUM | seed-c1 auto-promotes floor; evidence = blind truncation |
| 11 | MEDIUM | Run log overstates validity (theatre in evidence) |
| 12 | LOW | generation.py base-URL override / prompt injection surface |
| 13 | LOW | run-tests mutates live ledger |

---

## THE FIX (what "production-grade" actually requires)

1. **Wire gates to the commit path**: run `quality` + `nyaya` (ARGUMENT) + `chain` + `cite_contract` on
   the freshly-derived payload BEFORE commit; promote to EV only if that specific object passes.
2. **Make `quality` inspect actual derived content** (length, structure), not just non-empty payload.
3. **Implement + enforce the authority invariant** and the **multi-parent DAG eligibility** (`eligible()`
   must check every `requires` parent commits the required object id; `build-spine` must call it).
4. **Anchored, signed, payload-digested event ledger** + a real external anchor for tamper-detection.
5. **Regression tests on real committed data**: assert every committed object passes its layer gate; a
   two-word EDUCATION object must FAIL. Add a "junk content" test.
6. **Honest run logs**: report per-object gate verdicts, not just commit counts; document the GENERATED
   statuses and any weak content.
7. **`check.py --status`** must run every gate over the real registries and fail on any BLOCK/FAIL.
8. **`commit()`** must reject a status above the highest gate actually passed.
9. **`run-tests.py`** must operate on a temp copy, never the live ledger.

*This audit is the honest starting point: serveragent3 is a prototype with a sound DESIGN, not a
production system. The fix list is the production-grade bar it must reach.*
