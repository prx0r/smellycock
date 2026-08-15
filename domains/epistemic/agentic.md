# epistemic — AGENTIC (how agents drive the epistemic layer)

*2026-08-15. How an agent uses the epistemic layer: the split (Hermes generates, .py reduces), the MCP
verbs, the safety boundaries, and the anti-theatre rules. Mirrors the production stack's agent contract.*

---

## 1. The split (same as the whole stack)

> **Hermes for GENERATION, .py for REDUCTION.**

- **Hermes** (the model) reads real files and derives content — a real C1 into a real claim, a real
  passage into a proposition.
- **The `.py` engines** validate, aggregate, gate, review, and commit — deterministically. Never
  hand-feed a validator; never fabricate both sides of a comparison.

The epistemic products are the **reduction/validation** layer. They make the model's derivations
machine-checkable.

---

## 2. The MCP verbs an agent calls

The epistemic layer is exposed as MCP tools (`patala_*`). An agent:

```text
# read / derive (deterministic, no model)
patala_claim            → 49 honest-envelope propositions from real C1s
patala_argument         → 49 real arguments (thesis/premises/defeaters)
patala_crux             → minimal divergence between two positions
patala_research_packet  → question → evidence packet (PathRAG)
patala_passage          → canonical passage + KG2Code query
patala_terminology      → lemma-through-time sense trajectory
patala_timeline         → diachronic source-tree

# gate / review (the scholar-adjudication boundary)
patala_scholar_panel    → adversarial panel (BLOCKED on any blocking finding)
patala_scholar_attest   → Ed25519-signed attestation (public-key verify)
patala_scholar_simulate → zero-write hypothetical impact
```

---

## 3. The safety boundaries (non-negotiable)

- **A machine actor may PROPOSE but NEVER submit a state-changing review.** `submit_review` with
  `actor_kind="machine"` raises `PermissionError`. Only an authorized scholar/editor advances.
- **Reviews are append-only.** A REJECT does not delete; a REVISE does not overwrite; a new version
  supersedes an old one.
- **The durable review gate resolves cited refs against real objects.** A ghost citation blocks
  approval (dead-ref check). No fabricated citations.
- **Attestations are content-addressed + Ed25519-signed.** Any tamper breaks verification. The public
  key is embedded, so a third party verifies without the private key.

---

## 4. The anti-theatre rules

1. **Real data only** — hydrate from `_shared/ipvv.py`, the registries, `trajectories.json`,
   `historyTimeline.json`, or live Crossref/OpenAlex/OpenCitations. Never a fixture.
2. **Deterministic + CPU-only** — no GPU, no embedding models. A green result is reproducible.
3. **Honest ceilings** — a PĀṬALA-INFERS claim stays `MACHINE_PROPOSED`; never inflate.
4. **Live, not BS** — `test_live_integrations.py` (16/16) hits real external systems. A FAIL is honest.
5. **RUNNING TESTS IS NOT WORK** — run a gate only when you changed something or a claim is in doubt.

---

## 5. How an agent verifies a product is real

```bash
cd /root/projects/patala
PYTHONPATH=pipeline python3 pipeline/products/<product>/test.py   # deterministic proof
python3 test_live_integrations.py                                  # live integration proof
```

A product is "real" (per the ONE RULE) only when its `test.py` passes on real data AND (where
applicable) its live path returns real results.

---

*This is the agent contract for the epistemic layer. The machinery is deterministic; the boundaries are
executable; the doctrine is the same as the production stack.*
