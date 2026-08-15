# SPEC-13 — STALENESS & PERFORMANCE ENGINEERING for the Pāṭala futures

*2026-08-14. For each of the 7 futures in `docs/vision/VISION-PATALA-FUTURES.md`, this spec adds the
concrete **staleness mechanisms** (borrowed from the cloned repos) and the **performance optimizations**
(from `docs/05-performance.md` + SPEC-00), each with a **justification** grounded in the source repo's
actual code we've read.*

---

## The staleness toolbox (borrowed mechanisms, verified in clones)

| Mechanism | Source clone (verified) | What it gives us |
|-----------|------------------------|------------------|
| **`review_queue` with flags** `stale_dependency`, `stale_theme`, `unsupported_link`, `potential_contradiction`, priority + status | RKA (`rka/models/review_queue.py`) | a machine-fileable queue of things gone stale, each priority-scored |
| **Blast-radius propagation** (walk upstream→downstream on change) | RKA (`experiment-rka-staleness.py` proven) | one retraction flags every downstream dependent |
| **Reducer state machine** `AWAITING→REVIEWING→CORRECTION→ALIGNED` + `FindingStatus` (Open/Fixed/Closed/Superseded) | herdr (`adversarial_review.rs` + spec) | deterministic promotion gating; nothing promotes without evidence |
| **`invalidation_rules` + `recovery_policy`** per stage, `component_digest` SHA-256 | herdr (stage contract) | exact-object invalidation; digest-verified recovery |
| **Event-sourced append-only state** (never mutate; replay to reconstruct) | arcan (`state.rs`, event sourcing) | staleness computed by replay, not mutation |
| **KV JSON / GraphML content-addressed persistence** | nano-graphrag (`kv_json.py`, `gdb_networkx.py`) | stable, deterministic, restart-safe storage |
| **`superseded` status + supersession chain** | RKA decision model + herdr `FindingStatus::Superseded` | versioned truth; old versions never silently deleted |

---

# FUTURE 1 — THE ARGUMENT MAP (flagship product)

## Staleness mechanisms
- Every argument node carries the **epistemic envelope**; when a supporting `evidence` node's ceiling
  drops (e.g. a retraction), **RKA blast-radius** walks to every argument that used it, flagging
  `stale_dependency` in the **review_queue**.
- The **herdr reducer** gates each objection/position: a position with a stale premise goes
  `ALIGNED → CORRECTION_REQUIRED` until re-grounded.
- **herdr `FindingStatus::Superseded`** — when a position is reframed, the old one is superseded
  (never deleted), preserving the map's history.

## Performance optimization
- **PathRAG flow-pruning** for the per-question view: retrieve only the key relational paths (not all
  evidence), bounded to `token_budget`. *Proven: `experiment-pathrag.py`.*
- **Immutable versioned URLs** (SPEC-00): `/arguments/ARG5/v3` cache forever; the `/free-will` latest
  pointer short-lived. `ETag: sha256-…`.

## Justification
The map must never present a stale position as current. RKA+herdr give the honest lifecycle; PathRAG
keeps each page token-cheap. Both are proven on our data.

---

# FUTURE 2 — THE GENERAL EPISTEMIC ENGINE

## Staleness mechanisms
- **herdr stage contract** per domain: each domain (Sanskrit/Western/Science) is a **registered stage**
  with `component_digest` + `invalidation_rules` — a change in the Sanskrit corpus invalidates only its
  projections, not the whole engine.
- **arcan event-sourcing**: the engine's canonical state is an append-only event log; replay reconstructs
  any domain's view. Staleness = divergence from the log.
- **RKA review_queue scoped per project** (`project_id`) — each domain has its own queue.

## Performance optimization
- **nano-graphrag stable-LCC + GraphML**: deterministic serialization so the engine's output is
  byte-reproducible. *Proven: `experiment-nano-stable-graph.py`.*
- **Compiler model** (SPEC-00): compile each domain once → immutable projections; readers get static
  bytes. The engine is a compiler, not a request-time reconstructor.

## Justification
Domain-agnostic must not mean globally-fragile. herdr's stage isolation + arcan's replayability make
staleness **local and deterministic**; nano-graphrag's determinism makes the engine testable.

---

# FUTURE 3 — SELF-MAINTAINING EPISTEMIC GRAPH

## Staleness mechanisms (the core of this future)
- **Blast-radius propagation** (RKA) on every mutation: `retract(PHYSICS)` → 8 downstream layers stale
  → review_queue. *Proven.*
- **herdr reducer** as the promotion gate: `CORROBORATED→ALIGNED`, `CONTESTED→REVIEWING`,
  `CONTRADICTED→CORRECTION`. *Proven: `experiment-herdr-review.py`.*
- **`invalidation_rules`** per edge: `candidate_changed`, `requirements_changed`, `reviewer_set_changed`
  (herdr) — edges declare what invalidates them.
- **`FindingStatus::Superseded` + `ConcernRecorded`** — disagreements and supersessions are retained as
  first-class, never collapsed.

## Performance optimization
- **Incremental over full-rebuild** (SPEC-00 §4): hash each object; on change, only rebuild the
  affected subtree (the staleness walk IS the dependency graph — same structure).
- **Content-addressed** (SPEC-00 §5): SHA-256 per object → staleness = hash mismatch, O(1) check.

## Justification
The staleness walk and the dependency graph are the **same traversal** — so performance (incremental
rebuild) and correctness (blast-radius) are one mechanism. This is the highest-leverage future: it
makes the whole engine self-maintaining with almost no new machinery.

---

# FUTURE 4 — EXECUTABLE KNOWLEDGE (KG2Code)

## Staleness mechanisms
- **Verifiable traces** (KG2Code): every query returns its resolution path; if an object in the path is
  stale (RKA flag), the trace is **rejected** or marked — never silently served.
- **herdr `FindingStatus::Superseded`**: `resolve("Free Will")` returns the latest version; superseded
  versions resolve only with an explicit version hint.

## Performance optimization
- **Executable queries are deterministic code** (KG2Code, *proven*): the engine precompiles query
  plans; no LLM at request time for structured queries.
- **Compiled agent bundles** (SPEC-00): `/bundle/{id}` precomputed per object; `depth=` bounded.
- **MCP as a thin adapter** over `lib/query.py` — the agent gets a tiny language, not 40 tools.

## Justification
Executable queries give verifiable, cacheable, deterministic access. Staleness rejection on traces
makes the language truth-preserving (the whole point of KG2Code).

---

# FUTURE 5 — THE VERIFIED CORPUS ENGINE (science)

## Staleness mechanisms
- **`review_queue` flags**: `stale_dependency` (a claim rests on a retracted paper), `unsupported_link`
  (provenance link but unsupported content) — RKA's exact science-relevant flags.
- **Replication tracking**: a claim's evidence set includes replications; a failed replication raises
  `potential_contradiction` in the queue.
- **herdr reducer** gates claim↔evidence: a claim is `ALIGNED` only when its evidence bundle is
  corroborated, not just cited.

## Performance optimization
- **PathRAG for evidence retrieval** (proven): retrieve the claim→evidence→experiment paths, not paper
  piles — the "strongest evidence for X" query becomes a bounded path set.
- **HippoRAG PPR** with **hub-correction** (the bias we found): reweight PPR by query relevance to avoid
  hub domination. *Proven + finding documented.*
- **Parquet bulk exports** (SPEC-00 §14) for research downloads.

## Justification
Science needs replication/retraction awareness above all. RKA's `stale_dependency` + `unsupported_link`
flags map exactly onto scientific claim integrity; PathRAG/HippoRAG keep evidence retrieval cheap.

---

# FUTURE 6 — CROSS-TRADITION COMPARATIVE PHILOSOPHY

## Staleness mechanisms
- **KORAL-style two graphs** (reality vs literature): keep primary evidence and interpretation in
  separate graphs so a doctrinal reinterpretation doesn't corrupt the primary text. Staleness flags the
  interpretation, not the source.
- **RKA review_queue per tradition**: a change in Utpaladeva's reading flags only the comparative
  claims built on it.

## Performance optimization
- **KG2Code `compare(question, [traditions])`** (proven DSL): one deterministic query pulls the claims
  from each tradition, compared structurally.
- **Compiled comparison bundles** (SPEC-00): precomputed per question; edge-cached.

## Justification
The `analogy ≠ identity` discipline is enforced by the **two-graph separation** (KORAL): structural
comparison never merges source and interpretation. Deterministic compare-queries make it fast.

---

# FUTURE 7 — THE AUTONOMOUS REVIEW INSTITUTE

## Staleness mechanisms (the end-state)
- **Universal schema lifecycle** (SPEC-09): `Task→Run→Agent→Artifact→Proposal→Review→Decision→Supersede`.
  Every agent-run is immutable; a new run supersedes, never mutates.
- **herdr reducer** gates every promotion: agent output is `AWAITING_CANDIDATE`; only a human-authorize
  gate reaches publication. The `PublicationGate` is mandatory.
- **RKA blast-radius** on the whole system: a corrected fact re-queues every derived claim institute-wide.
- **arcan event-sourcing**: the institute's entire history is an append-only ledger; "what did we know
  and when" is always replayable.

## Performance optimization
- **Self-improvement as PR, not mutation** (SPEC-12): changes are diffs reviewed by the reducer, merged
  atomically — no in-place writes.
- **Incremental + content-addressed** (SPEC-00): each proposal's artifacts hashed; only changed artifacts
  rebuild. Deterministic reducers make the whole flow testable.
- **Compiled projection** of the institute's state (SPEC-00): "current accepted truth" is a materialized
  view, edge-cached.

## Justification
The institute is where every mechanism converges. herdr gives the reducer/gate, RKA the propagation,
arcan the immutable ledger, SPEC-00 the performance. The result is an **autonomous, self-correcting,
high-performance research institute** where verified state accumulates as durable intelligence.

---

## THE UNIFYING JUSTIFICATION

Every future uses the SAME two mechanisms:
1. **Staleness = the dependency graph walked** (RKA blast-radius + herdr invalidation) — correctness.
2. **Performance = compile-once + content-address + incremental** (SPEC-00) — speed.

They're the same structure: the DAG that encodes "what depends on what" is simultaneously the staleness
propagator, the incremental-rebuild scheduler, and the retrieval index. **Correctness and performance
are not two systems — they are one graph.**

## Implementation order (each already has a proven experiment)
| Future | First build | Proven by |
|--------|------------|-----------|
| 3 Self-Maintaining | `lib/staleness.py` + `lib/review.py` | experiment-rka + herdr |
| 4 Executable Knowledge | `lib/query.py` | experiment-kg2code |
| 1 Argument Map | bounded-context per argument | experiment-bounded-context |
| 5 Verified Corpus | `import_scifact` + evidence retrieval | PathRAG/HippoRAG experiments |
| 2 General Engine | 5 import adapters | (extension) |
| 6 Comparative | `compare()` query | KG2Code DSL |
| 7 Review Institute | reducer + event ledger | herdr + arcan |

See `docs/ALGORITHMS.md` + `docs/EXPERIMENT-REPORT.md` for the underlying proofs.
