# BUILD PLAN — INTEGRATE INTO THE PRODUCTION REPO (patalaorg) + TEST LIKE THEY DO

*2026-08-15. How to integrate our server2 POST-C1 work + server3 products into the production-grade
canonical reference (`/root/smellycock`), and validate it EXACTLY like the production repo validates
(per-layer deterministic gates + live-monitored runs + drift validators).*

---

## 0. THE PRODUCTION TESTING PATTERN (what "test like they do" means)

The production repo validates with **three layers of gates**, all deterministic + reproducible:

1. **Per-layer deterministic validators** — `t1_validator`, ARGMAP, L2, C1 validators + the live
   quality gate (`translation_gate.py`, verifiable reward, PASS/BLOCK, BLOCKED never commits). Each
   layer's "definition of done" is its gate passing on real data.
2. **Test suites** — `test_canonical_translate.py` (10/10), `test_factory_scheduler.py`,
   `test_translation_gate.py` (6/6), the epistemic products `test.py` (80/80) +
   `test_live_integrations.py` (16/16).
3. **Drift validators** — `check.py` (docs refs/naming/manifest) + `check_epistemic.py` (counts
   reconcile to the LIVE registries). A doc that names a count that doesn't reconcile is flagged.

**The status ladders (frozen):** Object `MACHINE_PROPOSED → ENGINEERING_VALIDATED → SCHOLARLY_CORROBORATED
→ INDEPENDENT_REVIEWED → ADJUDICATED` · Registry `GENERATED → ENGINEERING_VALIDATED → SPECIALIST_REVIEWED`
· Build `DISCOVERED < PROTOTYPED < VALIDATED < INTEGRATED < PRODUCTION`. **Banned:** `PROVED · TRUTH ·
CORRECT · BEST · WINS`.

---

## 1. WHAT TO INTEGRATE (our work → production domains)

| Production domain | Our integration | Status |
|---|---|---|
| `domains/epistemic/` | our grounded C1s/arguments/claims feed the 14 product engines (already documented) | ✅ base |
| `domains/translation/` | our POST-C1 spine consumes the committed commentary/C1 floor | map |
| `domains/openpatala/` | our grounded spine served as PTPROP/PTARG/PTPASS entities | ✅ emitted |
| `runs/` | log our C1→EDUCATION validated run as an official run | ✅ drafted |
| `MANIFEST.json` | register our integration scripts + external repos | do |

---

## 2. THE BUILD STEPS (each gated like production)

### Phase A — Reconcile the epistemic counts (the drift gate must pass)
- [ ] A1: run `check_epistemic.py` → confirm the documented layer counts reconcile to the LIVE
      registries (C1=42, ARGUMENT=8, SYNTHESIS=3, ESSAY=3, EDUCATION=3).
- [ ] A2: if a doc names a stale count, update it to reconcile (docs are a projection; registries truth).

### Phase B — Per-layer gates on the real spine (the production "definition of done")
- [ ] B1: C1/commentary gate — every grounded C1 resolves + carries evidence_quote (G1 fixed).
- [ ] B2: ARGUMENT gate — cite-contract 22/22 (premises carry citation/evidence_quote/source).
- [ ] B3: SYNTHESIS gate — derivation-complete over ENGINEERING_VALIDATED argument+theme.
- [ ] B4: ESSAY gate — sentence has a proof path (depends_on resolves, chain gate PASS).
- [ ] B5: EDUCATION gate — answer + distractor provable (wrong-answer→known-neighbor).
- [ ] B6: live quality gate — `translation_gate.py`-style verifiable reward on a sample.

### Phase C — Live-monitored run (the evidence, matching production runs/)
- [ ] C1: log the full C1→EDUCATION run as an official `runs/` entry with gate evidence.

### Phase D — Drift validators green
- [ ] D1: `check.py --status` PASS.
- [ ] D2: `check_epistemic.py` PASS (counts reconciled).

---

## 3. HOW WE TEST (exactly like production)

```bash
cd /root/smellycock
python3 check.py --status          # docs drift gate
python3 check_epistemic.py         # counts reconcile to live registries
# per-layer gates (deterministic, on real data):
python3 /root/fuck-off/scripts/validate-scholarship-chain.py
python3 /root/fuck-off/scripts/validate_cite_contract.py
python3 /root/fuck-off/scripts/validate_claim_support.py
python3 /root/fuck-off/scripts/validate_event_tamper.py
python3 /root/fuck-off/scripts/validate-signed-attestation.py
# epistemic products (server3):
cd /root/patalacheckpoints && for p in scholar_review claim argument crux comparison research_packet; do python3 pipeline/products/$p/test.py | grep SUMMARY; done
```

**Anti-theatre:** every gate is deterministic + on real data; a green test is reproducible. Nothing is
claimed PRODUCTION without the gate + run evidence.

---

## 4. DEFINITION OF DONE

- All 5 per-layer gates (B1–B5) PASS on the real grounded spine.
- `check.py` + `check_epistemic.py` both PASS.
- The run is logged in `runs/` with gate evidence.
- Our integration scripts are registered in `MANIFEST.json`.

*Then the production repo's canonical spine (commentary→theme/argument→synthesis→essay→lesson) is
INTEGRATED and VALIDATED exactly like the factory — real, logged, drift-proof.*
