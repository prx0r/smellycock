# epistemic — REFERENCE (wire mechanics)

*2026-08-15. The wire mechanics of the epistemic layer: the CLI entrypoints, the MCP tools, the API
routes, and the gates. Semantics in `model.md`; how-to in `recipes.md`. Everything below reflects the
current working implementation at `/root/projects/patala/`.*

---

## 1. The CLI entrypoints (one per product)

Every product is a standalone module at `pipeline/products/<product>/engine.py` with a CLI:

```bash
cd /root/projects/patala
PYTHONPATH=pipeline python3 pipeline/products/<product>/engine.py [args]
```

| Product | CLI | Example |
|---|---|---|
| `scholar_review` | `audit | list_objects | panel | attest | submit \| simulate` | `engine.py audit` |
| `translation_proof` | `[passage_id]` | `engine.py "pt:passage:ipvv:chunkD-memory-pramana.md"` |
| `argument` | `[argument_id]` | `engine.py` (all 49) |
| `crux` | `<a> <b>` | `engine.py ARG:...A ARG:...B` |
| `research_packet` | `<question>` | `engine.py "eternal self"` |
| `comparison` | `<a> <b>` | `engine.py ARG:...A ARG:...B` |
| `claim` | (none — all) | `engine.py` (49 claims, gated) |
| `context_bundle` | `<question> <variant>` | `engine.py "eternal self" deep` |
| `passage` | `<ref> <op>` | `engine.py chunkD get` |
| `benchmark` | (none — all) | `engine.py` (compile + metric) |
| `passage_workbench` | `disagree\|approve\|reject\|list` | `engine.py disagree chunkD "..." sandhi_resolution` |
| `terminology` | `<lemma> <op>` | `engine.py kula trajectory` |
| `timeline` | `<op> [id]` | `engine.py lineage trika` |
| `evidence_independence` | `live\|offline` | `engine.py live` |

---

## 2. The MCP surface (what agents call)

The MCP server (`mcp/index.mjs`) exposes the epistemic products as `patala_*` tools — **24 product
tools** + the 29 pre-existing read tools = **47 total**:

| Tool | Product |
|---|---|
| `patala_scholar_audit / panel / attest / impact / simulate / list / object` | scholar_review |
| `patala_translation_proof` | translation_proof |
| `patala_argument` | argument |
| `patala_crux` | crux |
| `patala_research_packet` | research_packet |
| `patala_compare` | comparison |
| `patala_claim` | claim |
| `patala_context_bundle` | context_bundle |
| `patala_passage` | passage |
| `patala_terminology` | terminology |
| `patala_timeline` | timeline |

The MCP shells to the product engines (`spawnSync` → `engine.py`); the logic lives in the kernels, the
MCP is a thin adapter (same pattern as the production translation MCP).

---

## 3. The API routes

- `GET /api/products?verb=...` — proof/argument/crux/packet/compare/claim/bundle/passage/terminology/
  timeline.
- `GET /api/scholar?verb=...` — list/audit/object/impact/panel/simulate/attest.

Both are thin proxies over `engine.py` (the ONLY place the logic lives).

---

## 4. The gates

| Gate | What | Exit |
|---|---|---|
| `test.py` (each product) | deterministic proof on real data | 0 = pass |
| `test_live_integrations.py` | 16 live checks (real Crossref/OpenAlex/OpenCitations + real registries) | 0 = all pass |
| `scholar_review/gate.py` | durable review gate (dead-ref check) | 0 = pass |
| `scholar_review/signing.py` | Ed25519 attestation (public-key verify) | 0 = pass |
| `benchmark` + inspect_ai | `inspect_claim_envelope.py` → accuracy 1.000 | — |

**Env:** `PYTHONPATH=pipeline` to import the product packages; the engines add `pipeline/` to
`sys.path` themselves so they run from any cwd.

---

## 5. The identity / authority contract (canonical)

- Products join on canonical object/version ids (`PT*`), never fuzzy strings.
- Every output carries the 4-axis authority vector; `authority(projection) ≤ authority(parent)`.
- Banned words never appear; outputs say `MACHINE_PROPOSED`, `PASSED CHECK X`, `SUPPORTED BY`,
  `REVIEWED BY`, `NO CONFLICT DETECTED`.

---

*This is the wire reference. The logic is deterministic + CPU-only; the MCP/API are thin adapters over
the kernels, matching the production stack's "Hermes for generation, .py for reduction" split.*
