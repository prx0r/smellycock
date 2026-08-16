# CONTEXTREVIEWCOCK — full working context & review notes (2026-08-15)

*My (the patalacheckpoints-lane agent's) complete working notes on the Pāṭala stack, the smellycock
reference repo, the fuck-off (ip-graph) sibling repo, and the graph-agent frontier. Saved here as the
handover/context-review home. The "cock" suffix mirrors the other lane's `CONTEXT-REVIEW-*.md` naming
convention; this is MY lane's consolidated view.*

---

## 0. THE PROJECT IN ONE LINE

**Pāṭala is a production-grade Sanskrit-to-whatever epistemic protocol**: an autonomous translation
factory that produces *provably-grounded* translations, arguments, syntheses, and lessons from raw
Sanskrit — where **machines propose, deterministic `.py` engines validate, and scholars certify**. Every
claim must trace to a source-bound object with an honest epistemic ceiling.

---

## 1. THE ARCHITECTURE (four moving parts)

```
patala PRODUCES → ip-graph VALIDATES + SERVES → Hermes executes → smellycock documents
```

| Component | Repo / path | Role |
|---|---|---|
| **patala** | `/root/patalacheckpoints` (git: `prx0r/patalacheckpoints`) | the factory + 26 product engines + registries |
| **ip-graph / fuck-off** | `/root/fuck-off` (git: `prx0r/fuck-off`) | the general epistemic-KG engine: builds/serves the graph |
| **Hermes** | `~/.hermes` | the replaceable execution kernel (generation) |
| **smellycock** | `/root/smellycock` (git: `prx0r/smellycock`) | the clean canonical reference + this context review |

**The division:** patala PRODUCES → ip-graph VALIDATES + SERVES → Hermes is the execution kernel →
smellycock documents + validates the contracts.

**The moat:** a scholar's correction becomes a *provenance-carrying graph mutation* that recomputes
downstream arguments, cruxes, and syntheses. "Executable scholarship."

---

## 2. THE LAYER DAG (the production spine, from `OBJECT-MODEL.md`)

```
source → T1 → tokenization(L0) → [argument_outline] → translation(L2) → translation_proof(L200) →
commentary(C1) → theme/argument → synthesis → essay → lesson
```

**The DAG rule:** a layer is eligible only when EVERY required parent is committed (multi-parent).
`translation` needs `[tokenization, argument_outline]` — unguided prose was the 0.118 bug. `L0` is
deterministic + free-draining.

---

## 3. WHAT I (THIS LANE) BUILT — the epistemic product layer

**26 products, all CPU-only + deterministic, 152/152 PASS, exposed as 63 MCP tools** (verified live
2026-08-15) + the scholar UI (localhost:3000 via `./start.sh`).

| Group | Count | Products |
|---|---|---|
| **Epistemic substrate** | 14 | translation_proof · claim · argument · crux · comparison · research_packet · evidence_independence · tension_finder · context_bundle · passage · passage_workbench · terminology · timeline · benchmark |
| **Scholar workflow** | 8 | review_queue · scholar_identity · review_workbench · scholar_profile · review_policy · scholar_review · scholar_publication · scholar_vertical |
| **Manuscript pipeline** | 3 | manuscript_routing · manuscript_ingest · collation |
| **NEW (this session)** | 1 | **translation_studio** — one passage → 5 registers (TECHNICAL/EXPANDED/CONDENSED/GEN_Z/ARGUMENT_DEPTH) from the same proof graph, with vertical-fidelity notes |

**The `product_reducer.py`** (Hermes reduction layer): derive → validate → commit to `object_registry` at
`ENGINEERING_VALIDATED`; self-gating. **`gold_check.py`**: the independent gold check (claim 2/2 grounded).

**State verified:** `check.py` PASS, `check_epistemic.py` PASS (25 products), all product tests pass.

---

## 4. smellycock REVIEW (the canonical reference — reviewed fully this session)

### Structure (4541 tracked files)
- **Core docs (top level):** `AGENTS.md` · `AXIOMS.md` · `OBJECT-MODEL.md` · `MANIFEST.json` (29 docs) ·
  `README.md` · `check.py` + `check_epistemic.py` gates · `.gitignore`
- **`domains/`** (24): per-domain references (epistemic, translation, openpatala, factory, read-plane)
- **`openpatala/`** (99): the OpenAlex-of-Sanskrit API docs + OpenAPI spec
- **`runs/`** (26): the logged autonomous runs (Run 1, Run 2, experiments, brainstorm)
- **`raw-material/`** (9): official golds + hand-authored argmaps
- **`essays/`** (3): Ratié literature review + recognition essays
- **`site/`** (4347): the **compiled read-plane** (4000 works, 254 bibliography, 62 concepts) — 95% of the repo
- **`web/`** (12): Astro source + `build_static_patala.py`

### The gate
`check.py --status` → **PASS**.

### ⚠️ THREE ACCURACY ISSUES FOUND (fix pending)
1. **Stale repo paths everywhere** — `AGENTS.md`/`AXIOMS.md`/`MANIFEST.json` point to
   `/root/projects/patala`, `/mnt/HC_Volume_106427611/ip-graph`, `/root/fuck-off` (the OLD layout). Real
   repos are `/root/patalacheckpoints` + `/root/smellycock`. Pointers resolve, so the gate passes, but they
   send agents to non-existent paths.
2. **Stale test counts** — `domains/epistemic/README.md` says "25 products, 134/134 PASS, 61 MCP tools".
   Reality: **26 products, 152/152 PASS, 63 tools** (translation_studio added).
3. **`site/` dominates** — 95% of tracked files are generated read-plane HTML. Intentional, but the "docs
   repo" is mostly build output.

### The git state (this session)
- Pushed docs → smellycock (`64acf61`), code → patalacheckpoints (`94222b1`).
- Cleaned smellycock: new `.gitignore` (build artifacts: `web/dist/`, `web/.astro/`, `web/static/`,
  `site/learning/`, `openpatala/emitted/`), untracked `web/dist/`, committed `30e9915`.
- Rebased on top of the other lane's 2 reconciliation commits (13a0232, 51fcf42). **smellycock is shared
  by BOTH lanes — always `pull --rebase` before push.**
- **Token** `ghp_8ctHL...` worked as `prx0r`, stored in `~/.git-credentials` (chmod 600). **ROTATE it —
  it's been in chat.**

---

## 5. HOW TO USE HERMES PROPERLY (the key correction)

From `patalacheckpoints/docs/global/HERMES-CALLING.md` + live `~/.hermes/profiles/patala/config.yaml`:

**THE ONE RULE:** `hermes -z "<prompt>"` is **blind** — no file access, no tools, no skills. It was the root
cause of the ~3.8% translation yield. **Use `hermes chat` (agentic).**

```bash
hermes chat -Q -q "<ask>" --skills <skill> --yolo --max-turns 8
```
- `-Q` = quiet/programmatic (clean output) · `-q` = non-interactive · `--max-turns 8` = enough turns ·
  `--yolo` = unattended

**The `patala` profile** (`/root/.hermes/profiles/patala/config.yaml`):
- model: `deepseek-v4-flash` / provider `opencode-go` (must pass both — `HERMES_MODEL` alone fails)
- **MCP server `patala`:** `node /root/patalacheckpoints/mcp/index.mjs` → **63 tools** (verified live,
  includes my `patala_collation` + `patala_translation_studio`)

**Architecture principle:** Hermes for GENERATION (reads files, derives); `.py` for REDUCTION (validates,
gates, commits). Never hand-feed a validator; never fabricate both sides. `Hermes task DONE ≠ Pāṭala
object ACCEPTED`.

---

## 6. THE fuck-off / ip-graph REPO (the graph-agent sibling — reviewed this session)

`/root/fuck-off` = **"Verified Epistemic OS"** — a domain-agnostic epistemic knowledge-graph engine.
490 nodes / 6578 edges from 425 docs. 53 kernels in `lib/`, 177 scripts, 47 specs, 32 arxiv papers.

**The genuinely valuable assets (worth adopting):**
1. **`lib/epistemic.py`** — the **epistemic-ceiling invariant**: every node carries `epistemic_ceiling` +
   4-axis authority + `authority(projection) ≤ authority(parent)`. A structural honesty mechanism for
   graph-RAG that **no frontier paper has**. ← the moat.
2. **`lib/retrieval.py`** — **liftable implementations of PathRAG + HippoRAG + ToG-2** over networkx,
   dependency-light. Pāṭala's `research_packet` already does a one-off PathRAG flow; this is the mature
   version.
3. **`lib/context_compiler.py`** + `lib/bundle_router.py` — content-addressed, token-budgeted context
   bundles ("one agent question = one request").
4. **`lib/system_provenance.py` / `lib/design_provenance.py`** — the OS audits its own kernels with
   Merkle-rooted signed provenance.
5. **`lib/query.py`** — KG2Code-style executable graph-query DSL.
6. **The anti-theatre tooling** (`scripts/audit-theatre-dataflow.py`, `skills/theatre-check/`) — flags
   validators that hand-feed the object they claim to validate.

**Honesty caveat:** the repo's docs run AHEAD of verification — many validators are PROVEN-MECHANISM
(synthetic/hand-fed). The genuinely data-grounded paths are the read-plane validators + the Tantrāloka
corpus run + `system_provenance.py`. Treat documented claims as intent until code-inspected.

---

## 7. THE GRAPH-AGENT FRONTIER (verified arxiv survey, 2026-08-15)

**Two converging poles:**
1. **Trained graph foundation models** replacing hand-built indexes: GFM-RAG (2502.01113, NeurIPS),
   GNN-RAG (2405.20139).
2. **Agent-native memory/construction**: HippoRAG-2 (2502.14802, ICML), Agents-K1 (2606.13669),
   Trellis/experience-graphs (2606.29823).

**The landmarks:** GraphRAG (2404.16130) · LightRAG (2410.05779) · HippoRAG (2405.14831) · GNN-RAG
(2405.20139) · Graph-of-Thoughts (2308.09687) · AGoT (2502.05078) · KGoT (2504.02670) · GAP (2510.25320).

**The honesty checkpoints (read before building):**
- **"Is GraphRAG Needed?"** (2606.25656) — retrieval gains don't proportionally improve generation;
  retrieval metrics overstate benefit.
- **Graph RAG survey** (2408.08921) — the field's formalization: Graph-Based Indexing → Graph-Guided
  Retrieval → Graph-Enhanced Generation.
- **Graph RAG for Customized LLMs** survey (2501.13958, `DEEP-PolyU/Awesome-GraphRAG`) — living index.

---

## 8. THE "GRAPH AGENT GENIUS" MOVE (the thesis)

The **epistemic-ceiling invariant** is the moat and it's **absent from the entire published landscape**.
Everyone builds graph-RAG that retrieves fluently; nobody structurally prevents the graph from overclaiming.

**The three concrete builds (highest-leverage first):**
1. **`graph_retrieval` product** — lift `fuck-off/lib/retrieval.py` into Pāṭala and **thread the
   `epistemic_ceiling` through the PathRAG flow** so a retrieved answer's authority ceiling is *computed by
   the graph*, not asserted. Fuses both repos' strengths into something the frontier hasn't done.
2. **Lift `lib/retrieval.py`** (PathRAG + HippoRAG + ToG-2) into `research_packet` — direct adoption per
   "reuse, don't rebuild."
3. **Make the runtime graphs durable** — Pāṭala builds `nx.Graph` per-call with no edge store; the
   hash-chained `object_registry` + `graph_stable.py` is the foundation to persist them.

---

## 9. NEXT ACTIONS

- [ ] Fix smellycock stale counts (26 products / 152 PASS / 63 tools) + repo paths.
- [ ] Build `graph_retrieval` product (epistemic-ceiling-aware PathRAG) — the genius move.
- [ ] Wire translation_studio UI page + register in smellycock docs.
- [ ] ROTATE the GitHub token.
- [ ] Push this context review to smellycock.
