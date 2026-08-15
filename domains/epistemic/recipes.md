# epistemic — RECIPES (how-to run, validate, live-test)

*2026-08-15. The how-to for the epistemic layer: run every product, validate it deterministically,
live-test it against the real world, and review scholarship. Each recipe is a concrete command with the
expected real result.*

---

## 1. Run the whole epistemic layer (the proof gate)

```bash
cd /root/projects/patala
python3 test_live_integrations.py                     # 16/16 live (real network + real data)
for p in scholar_review translation_proof argument crux research_packet comparison evidence_independence \
         claim context_bundle passage benchmark passage_workbench terminology timeline; do
  echo "--- $p ---"; PYTHONPATH=pipeline python3 pipeline/products/$p/test.py | grep SUMMARY
done
```
**Expected:** `80/80` deterministic PASS + `16/16` live PASS.

---

## 2. Run each product (the recipes)

### scholar_review — review + attest + audit
```bash
PYTHONPATH=pipeline python3 pipeline/products/scholar_review/engine.py audit
PYTHONPATH=pipeline python3 pipeline/products/scholar_review/engine.py panel \
  '{"target_ref":"V2-L-sastho-vimarsa-smrti-apohana:c1","reviewers":["r1","r2","r3"],"judge":"j1"}'
PYTHONPATH=pipeline python3 pipeline/products/scholar_review/engine.py attest \
  '{"target_ref":"V2-L-sastho-vimarsa-smrti-apohana:c1","reviewer":"scholar-A","verdict":"ACCEPT_WITH_QUALIFICATIONS"}'
```
**Real result:** panel → `BLOCKED` (dissent surfaced); attest → `Ed25519 verified` (production signing).

### translation_proof — the audit vector
```bash
PYTHONPATH=pipeline python3 pipeline/products/translation_proof/engine.py \
  "pt:passage:ipvv:chunkD-memory-pramana.md"
```
**Real result:** 10-dim audit vector + `publication_gate {decision:BLOCKED, blocking_dimensions:
[SOURCE_COVERAGE]}` — honest, blocks on the weak dimension.

### argument / crux / comparison
```bash
PYTHONPATH=pipeline python3 pipeline/products/argument/engine.py
PYTHONPATH=pipeline python3 pipeline/products/crux/engine.py ARG:pt:passage:ipvv:chunkA-svatyandya.md ARG:pt:passage:ipvv:chunkB-eligibility-gita.md
PYTHONPATH=pipeline python3 pipeline/products/comparison/engine.py ARG:...A ARG:...B
```
**Real result:** crux_count 6; comparison `REAL CRUX` (a_asserts=3, b_asserts=3).

### claim — honest envelope
```bash
PYTHONPATH=pipeline python3 pipeline/products/claim/engine.py
```
**Real result:** 49 claims, all `MACHINE_PROPOSED`, all pass the honesty gate.

### research_packet / context_bundle
```bash
PYTHONPATH=pipeline python3 pipeline/products/research_packet/engine.py "eternal self"
PYTHONPATH=pipeline python3 pipeline/products/context_bundle/engine.py "eternal self" micro
```
**Real result:** packet 4 passages (relevance_score 1.0); bundle micro 1053 tokens / deep 9923 tokens.

### passage / passage_workbench
```bash
PYTHONPATH=pipeline python3 pipeline/products/passage/engine.py chunkD get
PYTHONPATH=pipeline python3 pipeline/products/passage_workbench/engine.py demo
```
**Real result:** passage resolves to `pt:pid:ipvv:80f9c7f414ed`; workbench records + approves a
disagreement on a real passage.

### terminology / timeline
```bash
PYTHONPATH=pipeline python3 pipeline/products/terminology/engine.py kula trajectory
PYTHONPATH=pipeline python3 pipeline/products/timeline/engine.py lineage trika
```
**Real result:** kula lineage→body/power diachronic shift; trika 11-ancestor genealogy.

### benchmark
```bash
PYTHONPATH=pipeline python3 pipeline/products/benchmark/test.py
cd source-evidence/evals && /root/venv/bin/python -m inspect_ai eval inspect_claim_envelope.py
```
**Real result:** 49 samples, honest_ceiling_rate 1.0, inspect accuracy 1.000.

### evidence_independence
```bash
PYTHONPATH=pipeline python3 pipeline/products/evidence_independence/engine.py live
```
**Real result:** 6 recorded corroborations → 2 unique sources (1 dup); live OpenCitations classification.

---

## 3. Live-test against the real world (anti-theatre)

`test_live_integrations.py` hits REAL Crossref/OpenAlex/OpenCitations + real registries. A FAIL is
honest (API down / parse bug), never masked. GPU tools are **not** here — cloned for code-reading only.

---

## 4. Review scholarship (the human-authority path)

```bash
# a machine proposes; only an authorized scholar submits (executable boundary)
PYTHONPATH=pipeline python3 pipeline/products/scholar_review/engine.py submit \
  '{"actor_id":"scholar-A","actor_kind":"scholar","authorization_scope":"*","target_ref":"...","decision":"ACCEPT","rationale":"..."}'
# a machine trying to promote is FORBIDDEN (PermissionError)
```
A scholar can also record a disagreement on a passage (`passage_workbench disagree`) → durable review
gate → approve/reject with dead-ref check.

---

*This is the how-to. Every recipe gives a real, reproducible result on real data. Run a gate ONLY when
you changed something or a claim is in doubt (AXIOMS §10: running tests is not work).*
