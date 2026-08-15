# epistemic — VALIDATION (the gates + the evidence)

*2026-08-15. The validation layer for the epistemic products: the deterministic gates, the live
integration proof, and the drift validator. A product is real only when its gate passes on real data —
same discipline as the production stack.*

---

## 1. The gates (every product has a reproducible proof)

| Gate | What it proves | Expected |
|---|---|---|
| `test.py` (each product) | deterministic proof on real data | 80/80 PASS |
| `test_live_integrations.py` | real Crossref/OpenAlex/OpenCitations + real registries | 16/16 PASS |
| `scholar_review/gate.py` | durable review gate: dead-ref blocks approval | PASS |
| `scholar_review/signing.py` | Ed25519 attestation: sign + verify + tamper-detect | PASS |
| `benchmark` + `inspect_ai` | real samples → eval | accuracy 1.000 |

## 2. The live monitored run (the evidence, matching the production runs/)

Just as the production repo records live factory runs in `runs/`, the epistemic layer records a
**live epistemic run** proving the products in action — real commit counts, real throughput, real
network results. See `runs/` for the logged run.

## 3. The drift validator — `check_epistemic.py`

A gate that keeps the epistemic docs true (mirrors `check.py`):

```bash
cd /root/smellycock
python3 check_epistemic.py    # resolves refs + reconciles the documented counts to the live registries
```

It checks:
- **refs:** every path in the epistemic docs resolves (the product engines exist on this box).
- **counts:** the documented layer counts reconcile to the live registries (C1, argument, synthesis,
  essay, education, assertion, corroboration).
- **naming:** no banned words in filenames/prose.

## 4. The anti-theatre gate

Every product hydrates from REAL data or REAL network. A green test is reproducible and honest. GPU
tools (COMET/xCOMET/pyBKT) are **not** runnable products here — cloned for code-reading only, and the
docs say so (never presented as built).

---

*This is the validation contract. Run `check_epistemic.py` after any doc change (AXIOMS §10: run a gate
when you changed something).*
