# Performance — the doctrine + references

*The consolidated performance knowledge for the whole stack. **The binding doctrine is
`ip-graph-perf-doctrine.md` (the 10 rules).** The rest are the research/reference + build decisions.*

## Read order

| Doc | What it is | Status |
|---|---|---|
| **`ip-graph-perf-doctrine.md`** | **THE 10-RULE DOCTRINE** (compute-on-write, immutable URLs, one-request, 0-JS Astro, Rust hot-only, measure-before-infra, ETag/304, cache aggressively) | **CANONICAL** |
| `SPEC-49-read-plane-decision.md` | the frozen read-plane stack (Python+DuckDB→R2→Astro+bundles/MCP+Postgres-FTS-first) | CANONICAL |
| `atlas-performance.md` | patala's original performance doctrine (full text) | reference |
| `atlas-cloudflare-edge-layer.md` | the edge/CDN layer design (now deployed — see note) | reference |
| `performanceagent.md` | external best-practices survey (SSG/islands, edge Workers, Protobuf, HTTP/3, vector RAG) | reference |
| `agent-optimization.md` | agent-specific optimization (token efficiency, JSON-LD, materialized bundles) | reference |
| `SPEC-13-staleness-performance.md` | staleness/blast-radius performance | reference |
| `BUILD-OPENPATALA-PERFECTING.md` | the perf audit + gap-closure record | build record |

## The one doctrine (the 10 rules — the only ones you must never violate)

```text
1. Compute on write, not read.        6. Measure before adding infrastructure.
2. Immutable versioned URLs + ETag.   7. TS at edge, Python for factory, Rust hot-only, SQL canonical.
3. One agent question = one request.  8. CDN is the practical read layer (R2 + Postgres canonical).
4. Never ship JS where HTML is enough.9. ETags from hashes → 304; stream; token-efficient (?select=/?depth=).
5. Rust owns hot kernels only.        10. Cache aggressively (source/translations forever).
```

## Performance budgets (SPEC-00 §23 — the contract)

```text
Website   reading-route JS < 10KB (ideally 0) · compressed HTML < 100KB · LCP < 1s · CLS ~0
Agent     lookup = 1 HTTP request · context bundle = 1 request · MCP = 1 tool call
          default response < 4k tokens · depth ≤ 2 by default
API       cached p95 < 50ms · DB-backed p95 < 200ms
Build     a new document must NOT rebuild the entire corpus   (hard requirement)
```

## Edge deploy (as of 2026-08-15)

The read plane is **LIVE**: `https://patala.tradesprior.workers.dev/` (R2 bucket `patala-site`, KV
`patala-aliases`, 4342 site objects, all routes verified 200). Custom domain blocked only because
`patala.org` is not a zone in the CF account.

---

*This folder is the performance reference. The binding doctrine is `ip-graph-perf-doctrine.md`; budgets
are the contract; everything else is reference/decision history.*
