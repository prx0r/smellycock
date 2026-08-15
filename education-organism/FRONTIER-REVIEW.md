# FRONTIER REVIEW — current implementation vs. what it could be

*2026-08-15 · a comprehensive gap analysis of the education-serving organism against (a) the cloned
frontier ecosystem at `/root/fuck-off/ecosystem/`, (b) the **FoJin 佛津** sibling (now cloned at
`/root/fuck-off/ecosystem/translation/fojin`, 1220 files), and (c) the graph-RAG / agent-memory arxiv
landscape. The goal: what we ALREADY have, what the frontier has that we're MISSING, and the concrete
adoption path divided between the two work-agents from `HANDOVER-DEVPLAN.md`.*

---

## 0. THE ONE-LINE VERDICT

**Our moat is the *editorial provenance + authority invariant* (we derive readings through recorded
decisions; we enforce `authority(projection) ≤ authority(parent)`). Our gap is the *surface verification
enforcement* (we designed the "UNANCHORED → reject" rule but have no working verbatim-quote / citation
guard at serve-time) and the *measured-learning signal* (no clone, nor we, has a falsifiable
learner-mastery evaluation). FoJin proves the enforcement is buildable; the ecosystem proves the
provenance is portable.**

---

## 1. WHAT WE CURRENTLY HAVE (the honest baseline — verified this session)

### 1.1 The provenance moat (STRONG — keep, don't touch)
- **`kernels/object_registry.py`** — versioned, hash-chained, append+supersede registry. The real
  gold, verified:
  - `input_hash` + `derivation_hash` (anchors an object to *inputs*, red-team HIGH-5);
  - **keyed (HMAC) + payload-digested event ledger** (`append_event`/`verify_event_chain`, HIGH-6);
  - **authority invariant** `assert_authority_invariant` / `parent_ceiling` (CRITICAL-3);
  - multi-parent **deterministic eligibility** `eligible()` (CRITICAL-4) from `CANONICAL-DAG.yaml`;
  - atomic writes, stdlib-only, streams (never bulk-loads).
- **`kernels/misconception.py` + `staleness.py` + `reconciliation.py` + `pedagogy.py` (BKT) +
  `organism_loop.py`** — the flywheel + learning kernels, all deterministic.
- **The audit trail**: an education claim resolves SOURCE→…→EDUCATION (e2e 5/5).
- **Gates**: `check.py` PASS, `check_epistemic.py` PASS, `run-tests.py` 22/22.

### 1.2 The serving surface (PRESENT but thin)
- Astro site (11 pages) + `serve-education.py` (:8787) with a **`/resolve/{id}`** audit endpoint.
- Scholar workbench API (:8788), Ed25519 `scholar_identity` (via the other lane), SQLite learner store.

### 1.3 What verification do we run at SERVE time? → essentially none on the surface.
`serve-education.py` resolves provenance but does **not** run a verbatim-quote check or a citation
whitelist on generated answers. Our anti-hallucination rule is **designed, not enforced.** This is the
single biggest gap vs. FoJin.

---

## 2. THE FRONTIER — WHAT THE CLONED ECOSYSTEM GIVES US (adoption-ready, verified by subagent deep-dives)

| Repo | Asset | Adopt? | For |
|---|---|---|---|
| `learner-modeling/pyBKT` | **Production BKT**: `Model.fit/partial_fit/predict/evaluate/crossvalidate` + `Roster.update_state()` (live per-learner mastery). MIT, numpy/sklearn. | **YES** | Replace hand-rolled BKT fit/predict in `pedagogy.py` |
| `agent-memory/evolving-memory` | **Dream cycle** (SWS→REM→Consolidation→Compaction), `ParentNode.success_rate`, `FailureClass` negative constraints, Agentic ISA opcodes | **YES** | Our `ProceduralMemory` + `organism_loop.py` flywheel, pre-built |
| `agent-runtime/EverOS` | Markdown-versionable procedural **skill files** + offline `ReflectionOrchestrator` (merge/deprecate episodes) | **YES** | Durable, git-diffable procedural skills |
| `retrieval/PathRAG` | **`bfs_weighted_paths` + `find_paths_and_edges_with_stats`** — token-budgeted, networkx-only path pruning | **YES** | Replace our one-off `research_packet` PathRAG |
| `OSU-NLP-Group_HippoRAG` | PPR math (port to `nx.pagerank`), passage-node weighting | **PARTIAL** | Upgrade `hipporag()` |
| `infinitywings_rka` | **Weighted cascade** `_propagate`: `child = parent * edge_weight` + durable cursor `change_events` | **YES** | Make `misconception.blast_radius` weighted |
| `replay/deterministic-memory-layer` | **Event-sourced replay**: `replay_to/compare_states/replay_excluding`, `FactProjection.supersedes_seq` | **YES** | Our `reconciliation.py` — deterministic source-preservation proof |
| `eigenius_eigenius` | **JustificationTerm ADT** + `Verified⊂Derived⊂Observed⊂Declared` subclass ladder | **CONCEPT** | Output format of `reconciliation.py` + enforcement of the ceiling |
| `aaronsb_knowledge-graph-system` | **Disagreement-aware grounding scores** | **YES** | Citation-guard / misconception grounding |
| `science/scifact` | SUPPORT/CONTRADICT/NEI gold | **YES** | Test data for review/quote verifier |
| `vouchdev_vouch` | SHA-256 content-hash + append-only audit log | **PARTIAL** | Our `scholar_review` reducer (we already have better) |
| `signing/` (cosign) | OCI container signing + Rekor transparency | **NO** | Our Ed25519 `scholar_review/signing.py` already exists + is lighter |

### 2.1 What the ecosystem does NOT give us (must build ourselves)
1. **A falsifiable learner-mastery eval** — every memory/graph repo gives storage + recall; none gives a
   measured "did the learner actually learn" signal for BKT + misconception repair. **This is the
   anti-theatre gap.** We must build a gold set of "this learner had misconception X, did/didn't repair."
2. **fojin** was an empty dir until we cloned it — the actual domain substrate (Buddhist canon RAG with
   citation guards) was missing entirely.

---

## 3. FOJIN 佛津 — THE SIBLING (cloned; 1220 files; what it does GOLD that we lack)

**FoJin = RAG over the Buddhist canon with deterministic anti-hallucination guards.** Its three gold
pieces, all buildable and all missing from our surface:

### 3.1 `quote_verifier.py` (602 lines — the crown jewel) ⭐⭐⭐
Catches the *second* hallucination class: a **real citation with invented quoted text**.
- Detects `【《X》第N卷】`-bound quotes (inline 「」/『』/“”/‘’/"" + Markdown `> ` blockquotes), across a
  bounded `MAX_QUOTE_CITATION_GAP_CHARS=80` gap.
- **`_normalise`**: NFKC + **繁→简 fold (OpenCC)** + strip-punct + lowercase, then substring-test.
- On a miss, **downgrades** (strips quote marks → reads as honest prose, still cites) — it never *serves*
  a false verbatim quote. Records a `QuoteMutation` (reason, similarity, bucket) for telemetry.
- **`_windowed_ratio` + `_classify_failure`** buckets `near_miss` (≥0.85 — likely-correct, retriever
  missed) vs `absent` (paraphrase/fabrication) — **measurement, not just pass/fail**.
- **`count_checked_quotes`** — fixes the metric bug where "cited but quoted nothing" scored as
  "verified." (Anti-theatre discipline at the metric level.)

**Our gap:** we have no verbatim-quote verifier. This is the enforcement of our `UNANCHORED → reject`
rule at serve time. **ADOPT the mechanism.**

### 3.2 `citation_guard.py` (313 lines — the whitelist backstop) ⭐⭐⭐
- **Hallucinated title** → `【《X》第N卷】` stripped to bare `《X》` (no false click-through).
- **Wrong fascicle** → rewritten to the closest real `juan_num`.
- Whitelist = retrieved sources' `(title, juan)` + aligned parallels; `text_id<=0` excluded.

**Our gap:** no served citation is whitelisted against retrieved context. **ADOPT.**

### 3.3 The MCP server (`mcp-server/fojin_mcp/`) ⭐⭐
URN-addressable read-only tools: `search_corpus · read_passage · get_parallels · lookup_dictionary ·
lookup_entity · resolve_urn · verify_quote · commentaries` + `healthz`. We have `resolve_ref`; FoJin
adds `verify_quote` as an MCP verb. **ADOPT the tool surface.**

### 3.4 `fojin-eval-regression.sh` + `backend/eval/` ⭐⭐⭐
Daily answer-quality **regression gate** (Recall@5, faithfulness) against a baseline with CI/cron. We've
been building toward this; FoJin runs it. **ADOPT as a gated harness.**

---

## 4. THE SYNTHESIS — what the combined model must be

```
                    ┌─ retrieval (FoJin's strength): find passages, rank, rerank (PathRAG/HippoRAG)
  query/prompt ────►├─ editorial (OUR moat): resolve, show decisions, C1, authority invariant, depth
                    └─ guard (FoJin's): citation whitelist + verbatim-quote verify → any unanchored
                                        claim REJECTED / DEGRADED at serve-time
                                        (plus our /resolve provenance, signed by Ed25519)
```
- **FoJin proves the answer is *real* (in the corpus). We prove the reading is *justified* (derived
  through recorded decisions). Both, combined, are what a scholar trusts.**
- FoJin's citation-guard + quote-verifier are the **enforcement** of our UNANCHORED→reject rule. We
  designed the rule; FoJin has it working. **Borrow the mechanism, keep our provenance.**

---

## 5. THE GAP-TO-ACTION MAP (current → could-be), divided between the 2 agents

### AGENT A (scholar + serving surface)
| Current | Could-be (adopt from) | Priority |
|---|---|---|
| No quote verification at serve | `quote_verifier.py` ported to our L2/essay/education answers (downgrade + `QuoteMutation` telemetry) | **HIGH** |
| No citation whitelist | `citation_guard.py` ported (title whitelist + fascicle-correct) over served citations | **HIGH** |
| No eval regression gate | `fojin-eval-regression.sh` → our QA toolchain becomes a gated harness with baselines | **MEDIUM** |
| `resolve_ref` only | add `verify_quote` + `resolve_urn` as MCP verbs (fojin-mcp surface) | **MEDIUM** |
| Workbench API | already-strong `scholar_identity`/`review_policy`/`scholar_vertical` (other lane) — wire + persist | HIGH (in HANDOVER) |
| Disagreement grounding | `aaronsb` grounding-score model | **MEDIUM** |
| Review verification gold | `science/scifact` as test data | **LOW** |

### AGENT B (organism + flywheel + data)
| Current | Could-be (adopt from) | Priority |
|---|---|---|
| Hand-rolled BKT | `pyBKT Model/Roster` (fit/evaluate/crossvalidate + live mastery pacing) | **HIGH** |
| Unweighted `blast_radius` | RKA weighted `_propagate` (derived_from=1.0, contradicts=1.1, cites=0.7…) | **HIGH** |
| `reconciliation.py` (custom) | DML event-sourced `replay_to/compare_states/replay_excluding` + eigenius `JustificationTerm` shape | **HIGH** |
| `organism_loop.py` flywheel | evolving-memory dream cycle (curator/compactor/connector) + EverOS skill files | **MEDIUM** |
| One-off `research_packet` PathRAG | PathRAG `bfs_weighted_paths` (networkx-only) + HippoRAG PPR port | **MEDIUM** |
| **No measured-learning signal** | **BUILD: a falsifiable learner-mastery gold set + blind eval (the anti-theatre gap)** | **HIGH (must build)** |
| Derivation chain (1 work only) | link IPVV gold chain + enforce input_refs at commit | MEDIUM (in HANDOVER) |

---

## 6. THE #1 THING WE'RE MISSING (nothing in the frontier covers it)

**A learner-centered, pedagogy-aware evaluation signal** — a ground-truth "did the learner actually
learn" measurement for the BKT + misconception-repair flywheel. Every clone gives us storage + recall
(write path, provenance, consolidation); **none gives us mastery dynamics** (a falsifiable BKT mastery
prediction testable against real learning outcomes, a misconception-repair loop that optimizes toward
measured mastery, and an eval that is not theatre). This is domain-specific to Pāṭala pedagogy; we must
build it. It is exactly the anti-theatre doctrine: *"the clones can store the learner's state; the
prediction + evaluation of learning is the piece no cloned repo supplies."*

---

## 7. WHAT TO DO NEXT (ordered)

1. **Agent A: port `quote_verifier.py` + `citation_guard.py`** (fojin) into `smellycock` as a
   `guard.py` kernel wired into `serve-education.py`/`tutor-agent.py` — the enforcement our rule lacked.
2. **Agent B: adopt `pyBKT` + RKA weighted propagation + DML replay** for the flywheel; **build the
   learner-mastery gold eval** (the gap nothing covers).
3. Both: keep the provenance moat untouched; keep the gates green (`check.py`, `check_epistemic.py`,
   `run-tests.py` 22/22, `test-e2e.py` 5/5).

---

## 8. SECOND ROUND — WHAT MAKES US NEXT-LEVEL **AND LEGIT** (the "genius" filter)

*This section is the deep-dive beyond fojin: the remaining cloned repos assessed through the two tests
that matter — (a) does it make our products genuinely **better**, and (b) does it make them
**legitimate** (real, measurable, not marketing)? "Bigger" is not a goal. Below: the assets that pass
both, with the honest caveat that training-heavy / graph-DB-bound / GPU-only research code does NOT fit
an 8GB/2-agent box and is marked accordingly.*

### 8.1 The learner-store legitimacy stack (buildable NOW on our Postgres/DuckDB read-plane) ⭐⭐⭐
Three repos converge on the SAME correct design for a *time-bounded, authority-gated, correction-safe*
learner store. All three are liftable **without** a graph DB or a heavy LLM pipeline, and each preserves
tombstones + provenance rather than mutating in place — which is exactly our anti-theatre discipline:

| Principle | Adopt from | Exact asset | Why it makes us legit |
|---|---|---|---|
| **A misconception correction is TIME-BOUNDED** | `getzep_graphiti` | `graphiti_core/edges.py` — `valid_at`/`invalid_at` + `episode_id` provenance on every fact | A corrected misconception invalidates the old fact (`invalid_at=now`) WITHOUT deleting it — "what was believed" and "what is true now" are both queryable. This is the graphiti paper (arXiv 2501.13956), the strongest temporal-memory reference of all. Schema-only, lifts onto our store. |
| **Authority-GATED memory (2-tier)** | `neo4j-labs_meta-knowledge-graph` | `hooks/consistency_gate.py` (auto gate) + `server.py:1197/1258` (human `project_review_queue`/`project_resolve_learning`) | The closest thing in the whole ecosystem to an authority-gated memory. Auto-gate judges `GENUINELY CONTRADICTS?`/`ALREADY LEARNED?` with a conservative precedence (existing-veto > merge > new-win > unclear); genuine ambiguity is punted to a HUMAN with the machine's rationale attached, stamped `reviewed_by='human'`. Liftable (pure Python + LLM judge + retrieval). |
| **Corrections SUPERSEDE, never pile up** | `MemTensor_MemOS` | `src/memos/mem_feedback/feedback.py` `standard_operations`/`_single_update_operation` + `utils.py` `should_keep_update` | The anti-hallucination guard for memory writes: LLM-emitted ids are mapped back to REAL ids (`correct_item`), UPDATE takes precedence over ADD, a change-ratio guard downgrades update→add rather than clobbering, and the old node is ARCHIVED with a `covered_history` link (never deleted). Exactly our `authority(projection)≤authority(parent)` tombstone move, proven at production scale. |

**The synthesis (this is the legit learner store):** graphiti's temporal model ("when was this believed")
+ MKG's 2-tier gate ("who approves a correction") + MemOS's guards ("corrections supersede, with
provenance"). All three are logic-only / schema-only lifts onto our existing store — no Neo4j, no GPU.

### 8.2 The evolution-of-content engine (the flywheel's retain-loop) ⭐⭐
| Repo | Asset | Verdict |
|---|---|---|
| `evolution/openevolve` | `openevolve/database.py` — `ProgramDatabase` (`_update_archive`/`_update_best_program`/`_sample_parent` = generate→verify→retain-elite), MAP-Elites island grid + cascade evaluator + checkpoint/resume | **ADOPT the retain-loop as a pattern.** Our `organism_loop.py` is the same generate→verify→repair→retain; OpenEvolve makes it a real algorithm (MAP-Elites over a complexity×diversity grid). Liftable-python, OpenAI-compatible. Replace the code-evaluator with OUR verifier as the fitness. Token-heavy but I/O-bound → fine on 8GB. |
| `science/scifact` | claim↔evidence SUPPORT/CONTRADICT/NEI gold (fetch via `download-data.sh`; gold JSONL not checked in) | **ADOPT as eval gold** for our quote-verifier + scholar_review gate. The cleanest independent gold in the ecosystem. A download step away. |
| `science/knowledge_storm` (`storm_wiki`) | LLM→report synthesis engine with grounded, citable output (`knowledge_storm/lm.py`, provider-agnostic) | **ADOPT as the generation engine** for essay/education synthesis — it emits grounded citations that feed our (future) verifier. Pure Python, pip-installable. |

### 8.3 The retrieval/rankers "genius" (liftable math, not the model) ⭐⭐
| Repo | Asset | Verdict |
|---|---|---|
| `RManLuo_gfm-rag` | `gfmrag/models/gfm_rag_v1/rankers.py` — **sparse entity→doc projection rankers** (Simple/IDF/TopK/IDF-TopK, ~110 lines, dependency-free) | **ADOPT the ranker math.** The "graph foundation model" itself needs torch+checkpoint+GPU (not deployable on our box) — but the insight (project entity-level scores to documents via a sparse entity→doc matrix, IDF-weighted) is exactly what our `research_packet`/graph-retrieval needs to go from "find paths" to "rank documents." Lift the ranker, skip the GNN. |
| `RManLuo_reasoning-on-graphs` | `src/utils/graph_utils.py` — **rule-constrained BFS + random-walk negative-path sampling**, networkx-only | **ADOPT for path/negative sampling** over our epistemic graph. The reasoning-on-graphs paradigm (LLM plans a relation-path → graph retrieves → LLM answers faithfully) maps onto our organism; the path utilities are the liftable core. |
| `airi-institute_arigraph` | `graphs/parent_graph.py` — **TripletGraph + episodic-vertex design** | **BORROW the episodic-memory idea only** ("what happened when" edges). Code is TextWorld-bound research glue; not an eval harness. |

### 8.4 Audited provenance/consolidation (the schema machinery) ⭐
| Repo | Asset | Verdict |
|---|---|---|
| `neo4j-labs_agent-memory` | `src/neo4j_agent_memory/memory/consolidation.py` — `valid_from`/`valid_until` supersession + **dry-run audited `ConsolidationRun`**; `reasoning.py` — `:TOUCHED` audit edges | **ADOPT the patterns** (time-bounded supersession + dry-runnable audited consolidation + reasoning-step→entity provenance). Cypher-bound code; port the pattern to our store. |
| `rhanka_graphify` | reconciliation-as-validated-atomic-patch lifecycle (accept/reject/merge/supersede + decision log) | **BORROW the discipline** (never in-place-edit derived files; reconcile as a reviewable patch). Pattern only (TS/Graphology). |

### 8.5 Explicitly SKIP (research-only / not a fit / marketing — do not adopt)
| Repo | Why |
|---|---|
| `EvoScientist_EvoScientist` | A DeepAgents CLI interface, not a discovery algorithm; verification is a *prompt* not a deterministic gate (anti-theatre violation); heavy dep tree. |
| `evolution/axplorer` | A torch training harness (self-play of a small generative model); off-theme. |
| `broomva_arcan` | A Rust agent-runtime monorepo; unrelated to epistemic/scholarship. Our axiom mandates Rust only as measured hot wheels. |
| `signing/` (cosign) | OCI container signing + Rekor transparency — overkill; our Ed25519 `scholar_review/signing.py` is lighter and already real. |
| `DataArcTech_ToG-2` | Requires local Wikidata SPARQL + embedding + LLM; not liftable. Only the alternating graph↔doc *concept* (which `lib/retrieval.py` already mirrors). |
| `Graph-COM_SubgraphRAG` | Trained GNN retriever weights; research/training code. |
| `MemTensor_MemOS` (full) | Adopt only the feedback-correction *patterns* (§8.1), not the graph/vector-DB+LLM engine. |

---

## 9. THE LEGITIMACY TEST — applying it to the whole adoption list

Every candidate above was screened by the anti-theatre test: **is it a working, independently-grounded
capability, or a repo that merely looks impressive?** The honest verdict:

- **LIFT (real, dependency-light, matches a gap we have):** fojin guards (§3), pyBKT, RKA weighted
  propagation, DML replay, graphiti temporal model, MKG authority gate, MemOS feedback guards,
  OpenEvolve retain-loop, GFM-RAG rankers, RoG path utils, SciFact gold, Storm generation.
- **PATTERN-ONLY (real idea, but code is graph-DB/GPU/training-bound — port the idea, not the import):**
  AriGraph episodic memory, neo4j-agent-memory consolidation + `:TOUCHED`, rhanka reconciliation-patch,
  eigenius justification term, HippoRAG PPR, ToG-2 concept.
- **SKIP (research-only / marketing / off-fit):** EvoScientist, axplorer, broomva_arcan, cosign, GFM-RAG
  full model, SubgraphRAG, MemOS engine.

**The rule we keep:** adopt the *mechanism that enforces an honesty invariant we already designed* (fojin's
guards enforce our UNANCHORED→reject; MemOS/MKG/graphiti enforce our authority+correction discipline).
Never adopt a repo that *asserts* quality — only ones that *enforce* it deterministically. That is the
difference between "bigger" and "legit."

---

## 10. REVISED WHAT-TO-DO (with the second-round additions)

1. **Agent A:** port fojin `quote_verifier.py` + `citation_guard.py` (§3) + SciFact as review-gold (§8.2)
   + GFM-RAG ranker + RoG path-utils into the serving/retrieval path (§8.3).
2. **Agent B:** adopt pyBKT + RKA weighted propagation + DML replay (§1.3) + the **learner-store
   legitimacy stack** — graphiti temporal model + MKG 2-tier gate + MemOS feedback guards (§8.1) +
   OpenEvolve retain-loop as the flywheel's evolutionary core (§8.2); **build the measured-learning eval**
   (§6, the gap nothing covers).
3. Both: never adopt a training-heavy / graph-DB / GPU repo wholesale; keep the provenance moat; keep the
   gates green.

---

*This review is the honest "current vs. could-be." Our strength is editorial provenance + the authority
invariant; our gap is surface verification enforcement + a measured-learning signal. FoJin proves the
enforcement is buildable; the ecosystem proves the provenance is portable. The second round adds the
learner-store legitimacy stack (graphiti + MKG + MemOS), the evolution engine (OpenEvolve), the liftable
retrieval math (GFM-RAG rankers + RoG), and the eval golds (SciFact + Storm) — each screened so we adopt
the *enforcers*, not the *asserters*. A = guards + scholar surface; B = mature learning/flywheel kernels +
the measured-learning eval.*

---

## 11. BUILT SO FAR (this session — the review is now a projection of real code)

*What was adopted and wired into smellycock, verified by the test suite. **39/39 tests PASS**, check.py
PASS, check_epistemic PASS (26 products), e2e 5/5, GEM 5/5.*

| Adoption | File (smellycock) | What it does | Test |
|---|---|---|---|
| **fojin quote_verifier + citation_whitelist** | `kernels/guard.py` + product `engines/guard.py` | verbatim-quote verify (downgrades invented quotes to prose, strips fabricated citations) | `test_guard_kernel` |
| **guard wired into the API** | `scripts/serve-education.py` `/guard` + `/answer` | guards a learner answer against the lesson's resolved source context, deterministic, no LLM | verified live |
| **graphiti temporal + MKG 2-tier + MemOS guards** | `kernels/learner_gate.py` + `engines/learner_gate.py` | time-bounded belief store + machine gate (veto/reinforce/accept) + human review queue | `test_learner_gate_kernel` |
| **RKA weighted propagation** | `kernels/misconception.py` + engine | `weighted_propagate` (derived_from=1.0, contradicts=1.1, cites=0.7, supersedes=0.3) | `test_weighted_propagation` |
| **graphiti temporal provenance + context compiler** | `kernels/staleness.py` + engine | `TemporalFact.episode`, `facts_to_context` (time-aware read-plane bundle) | `test_temporal_context` |

**Not yet built (next session — the genuine remaining gaps):** the measured-learning eval (§6), the
OpenEvolve retain-loop as the flywheel's core (§8.2), GFM-RAG ranker + RoG path-utils in the retrieval
path (§8.3), SciFact gold download + eval regression harness (§8.2).
