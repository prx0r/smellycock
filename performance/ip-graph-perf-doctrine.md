# IP-GRAPH — PERFORMANCE DOCTRINE (serving the knowledge graph fast)

*Adapted from patala's `atlas-performance.md` + `atlas-cloudflare-edge-layer.md`. This is the rulebook
for serving the info-philosophy graph to humans and AI agents with near-zero latency.*

## The obsession

```text
SCHOLARLY WORK happens asynchronously once.
READING that scholarly work should be nearly free forever.
```

```text
request arrives → cache hit → bytes
```

(Not: request → query 11 tables → graph traversal → normalize → serialize giant JSON → send.)

---

## The 10 rules

1. **Compute on write, not read.** Precompute projections once; readers get static bytes. When a
   concept/edge changes, rebuild only the affected projections.
2. **Exact versions are static files conceptually.** Immutable versioned URLs
   (`/concepts/free_will/v3`, `/assets/sha256/...`). `Cache-Control: public, max-age=31536000,
   immutable`. Latest pointers (`/concepts/free_will`) get short cache lifetimes.
3. **One agent question = one request.** Materialized context bundles: `/context/{id}`,
   `/bundle/{id}`, `/trace/{id}`, `/compare/{id1}/{id2}`. Bounded `depth=` (0/1/2 with node/byte/token
   budgets) to prevent graph explosion.
4. **Never ship JS where HTML is enough.** Astro islands: reading pages = 0 JS; only interactive
   islands (graph explorer, search) get client JS.
5. **Rust owns hot deterministic kernels only** (transliteration, search indexing, graph
   serialization). Not the whole app.
6. **Measure before adding infrastructure.** No Neo4j/Kafka/Elasticsearch unless measurements demand.
   Postgres first; Tantivy (Rust) if search hurts.
7. **Language split:** TypeScript at the edge/UI, Python for scholarly/factory work, Rust for hot
   kernels, SQL for the canonical graph.
8. **CDN is the practical read layer.** Postgres + R2 are canonical; Cloudflare Cache serves most
   reads. Static assets bypass the Worker entirely.
9. **ETags from object hashes** (`ETag: "sha256-…"`), `If-None-Match` → 304. Stream big files, never
   buffer. Token-efficient agent responses (`?select=`, `?depth=`, `format=compact`).
10. **Cache aggressively, this domain is cache-friendly:** exact source forever, translations forever,
    work metadata minutes/hours, latest pointer seconds.

## Reference stack

```text
FRONTEND        Astro + React/Preact islands
EDGE            Cloudflare Workers (TypeScript) + CDN + Hyperdrive + Queues + Early Hints
CANONICAL DB    Neon PostgreSQL (pg_trgm, FTS, JSONB)
BLOBS           Cloudflare R2 (SHA-256 content addressing)
FACTORY         Python / Hermes
SEARCH v1       Postgres;  v2 Tantivy if measured
MEDIA           Cloudflare Images / Stream
OPEN DATA       Parquet / TEI / PROV-O / nanopubs
TRUST           hash-chain / signed manifests / Sigstore
BLOCKCHAIN      no
```

## Source (in patala, full text)

- `patala/docs/vision/atlas/atlas-performance.md`
- `patala/docs/vision/atlas/atlas-cloudflare-edge-layer.md`
- `patala/docs/atlas-contracts/read-api.md` (the read API grammar)
