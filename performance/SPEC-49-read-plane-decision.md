# SPEC-49 PERFORMANCE-BUILD-DECISION — the read-plane stack, Rust policy, agent SEO

**Status:** LIVE (decision recorded). **Layer:** L06 (retrieval-compiler) + L07 (surfaces) + L12 (live).
**Governing docs:** `SPEC-00-INFRA-BUILD.md`, `docs/05-performance.md`, `docs/performanceagent.md`,
`migration/v3/V3-BUILD-SPEC.md`, `migration/v3/PRODUCTS.md`.

*This spec records the definitive build decision for the read plane — what the final build is, why
Python stays the factory, when (and when not) to reach for Rust, and how agent SEO unifies with the
human/search-engine graph. It answers the recurring question "why do the cloned repos use Rust and why
don't we?"*

---

## 1. THE ONE-LINE BUILD DECISION

> **The final build is a knowledge compiler** (Python + DuckDB) that turns the canonical graph into
> globally cached immutable artifacts (R2 + Cloudflare CDN), served to humans via **Astro** (0-JS,
> JSON-LD), to agents via **compiled context bundles + MCP**, and to search via **Postgres FTS first —
> Tantivy only if profiled hot.** Python stays the factory; Rust is used as a *compiled wheel* only when
> measurements show a hot kernel.

This is not a framework choice — it is **"compute on write, read from bytes"** (the founding perf
doctrine) applied to the whole stack.

---

## 2. THE FROZEN STACK (SPEC-00 §24 + v3 build spec)

| Concern | Choice | Why |
|---|---|---|
| Factory/kernel | **Python** (18 kernels) + DuckDB + Polars | I/O + LLM-bound, not CPU-bound |
| Canonical DB | PostgreSQL (Neon) | transactional canonical state |
| Blobs + immutable projections | Cloudflare R2 (SHA-256) | content-addressed, no egress |
| Human site | **Astro** (0-JS reading, Preact islands) + JSON-LD | islands = no unnecessary JS |
| Edge/API | Cloudflare Workers + TypeScript | ms cold start, global |
| MCP | thin Streamable-HTTP adapter over the API | ~8 verbs, stateless |
| Search v1 | **Postgres FTS** (`tsvector`/`pg_trgm`) | free, consistent, no second index |
| Search v2 | **Tantivy** (only if profiled hot) | Rust wheel, BM25 |
| Bulk export | Parquet + Zstd | analytical publication |
| Rust | only measured, stabilized hot kernels | see §3 |

---

## 3. THE RUST POLICY — "Postgres FTS first; Tantivy only if profiled hot" (the question answered)

### 3.1 What the rule means
It is a **decision rule about where to spend engineering effort**, not a ban on Rust. Three parts:
1. **Postgres FTS first** = use Postgres's built-in full-text search (`tsvector`/`tsquery` + `pg_trgm`).
   Free, lives in the canonical DB, transactional-consistent, no second index to sync. Fast enough for
   thousands–millions of rows.
2. **Tantivy only if profiled hot** = switch to Tantivy (a Rust search library) **only after measuring**
   that Postgres FTS is the bottleneck (SPEC-00 §25 step 16, perf rule 6).
3. **Why defer:** Tantivy adds a **second index** you must keep in sync with the canonical DB — the
   classic "two sources of truth" failure v2's review flagged. You trade consistency for speed; pay that
   cost only when measurements justify it. At our scale (490 nodes / 6k edges today; even a full IPVV is
   thousands of passages) Postgres FTS is effectively instant.

### 3.2 Why the cloned repos "use Rust" — and why that doesn't mean we write Rust
There are **two different things** called "Rust" in the ecosystem:

**(A) Rust-compiled Python WHEELS** — what `paper-qa`, `EverOS`, `evolving-memory` actually use.
`tantivy`, `hnswlib`, `faiss-cpu`, `lancedb`, `usearch` are **Python libraries whose heavy kernels are
compiled to Rust/C++**. You `import` them in Python; they are dependency decisions, NOT language
decisions. We clone those repos for *patterns*, not to rewrite our factory in Rust.
- `paper-qa` → `tantivy>=0.22.2` + `usearch` (Rust wheels) for BM25 + vector, because paper-qa IS a
  search-heavy app over huge PDF corpora — search is its product.
- `EverOS` → `lancedb` (Rust core) for "Vector + BM25 + scalar filter" — it's a memory/retrieval engine.
- `evolving-memory` → `faiss-cpu` for vector similarity.

They chose Rust wheels because search/vector is their **hot path**. Our hot path is different: the
**epistemic gate + derivation graph + staleness** — pure Python (networkx + kernels), not search-bound.

**(B) Real Rust projects** — `maestro` is the one true Rust repo we cloned (clap/git2/rusqlite binary).
It's the agent runtime. But v3's build spec says: Hermes/maestro is a **replaceable runtime behind a
`RuntimeRouter`** — we don't write our own Rust; we *route to* a runtime if needed.

### 3.3 Why WE don't write Rust (the doctrine, verbatim from SPEC-00 §18)
1. Our factory (Python) does filesystem, JSON, regex, LLM orchestration, data transforms — Rust does
   not meaningfully speed these up (I/O + LLM-bound).
2. The 18 kernels are dependency-light by design (stdlib + networkx + yaml). A Rust rewrite = huge
   effort, ~no measured gain.
3. The rule is "Rust only when objectively hot": Tantivy indexing, special parsers, massive
   serialization, tokenization, high-volume graph kernels. None are hot for us YET.
4. SPEC-00 §25 step 16: "**Only then** decide whether any Python kernel deserves Rust" — benchmark the
   compiled projection first, let the numbers decide.

### 3.4 The resolution
We DO use Rust — the Rust that ships as `tantivy`/`faiss`/`lancedb` **wheels**, exactly like the repos
we cloned — **when and only when** profiling shows Postgres FTS or pure Python is the bottleneck. We
DON'T write our own Rust from scratch, because the perf doctrine + SPEC-00 explicitly defer it until
measurement, and our hot paths aren't search/CPU-bound.

---

## 4. AGENT SEO — one canonical identifier, four graphs (§17)

Every entity gets ONE canonical public URL + one stable ID (`ip:concept:free_will`). All
representations share it:

```text
https://example.org/concept/free-will       (human HTML)
/concept/free-will.json                     (machine read)
/concept/free-will.md                       (agent/prose)
/api/v1/concepts/free-will                  (API)
```

HTML carries `<link rel="canonical">` + `<script type="application/ld+json">` (schema.org). This unifies
the **human graph, search-engine graph, agent graph, and API graph** from ONE entity model (SPEC-00 §17).

---

## 5. COMPILED AGENT VIEWS + MCP (§15, §16) — the agent-cache-line

The highest-value read-plane feature: compile per-entity **context bundles** so an agent does ONE
request, not seven:

```text
GET /bundle/concept/free-will?v=17
  → { entity, definition, positions, relations, primary_evidence,
      important_works, disagreements, neighbors, provenance }
GET /api/v1/concepts/free-will?view=compact|evidence|context&budget=2000|8000|32000&depth=0|1|2
```

MCP = thin Streamable-HTTP adapter over that API, ~8 tools (`resolve search get context trace compare
neighbors evidence`), NOT 70 micro-tools. One tool call per agent question (perf rule 3 + SPEC-00 §15).

---

## 6. PERFORMANCE BUDGETS (SPEC-00 §23) — the contract to build against

```text
Website   reading-route JS < 10KB (ideally 0) · compressed HTML < 100KB · LCP < 1s · CLS ~0
Agent     lookup = 1 HTTP request · context bundle = 1 request · MCP = 1 tool call
          default response < 4k tokens · depth ≤ 2 by default
Build     a new document must NOT rebuild the entire corpus   (hard requirement)
```

---

## 7. TRACEABILITY (everything above resolves)

| Artifact | Path | Layer |
|---|---|---|
| Perf doctrine | `docs/05-performance.md` | L12 |
| Agent/human speed deep-dive | `docs/performanceagent.md` | L12 |
| The exact build spec | `specs/SPEC-00-INFRA-BUILD.md` (§24, §25) | L00/L06/L07 |
| v3 build spec (the exact stack) | `migration/v3/V3-BUILD-SPEC.md` | ALL |
| Surfaces layer | `layers/07-surfaces.md` (NOT_STARTED) | L07 |
| Retrieval-compiler layer | `layers/06-retrieval-compiler.md` (NOT_STARTED) | L06 |
| Repos that use Rust wheels | `ecosystem/retrieval/`, `ecosystem/science/paper-qa/`, `ecosystem/agent-runtime/EverOS/` | L10 |
| Real Rust repo | `ecosystem/agent-runtime/maestro/` (Cargo.toml) | L09/L12 |

**Status:** L06 + L07 are NOT_STARTED — the read plane is the remaining build. The machine side is done
(55/55 tests, IPVV graduation real). Next: the projection compiler → R2 → Astro + Workers + MCP +
JSON-LD/SEO.
