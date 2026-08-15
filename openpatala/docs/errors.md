# OpenPāṭala API Errors — what can go wrong, and the exact JSON

*Status: v1.0 (live). Every error is machine-readable (`code`), agent-actionable (`message` +
`suggestion`), and signals retryability. This page documents the exact shapes so clients and agents
can handle them deterministically.*

---

## 1. The error envelope

Errors return a non-2xx status with a `detail` body:

```json
{
  "detail": {
    "error": {
      "code": "OBJECT_NOT_FOUND",
      "message": "no work does-not-exist-zzz",
      "suggestion": "use /search?search=...",
      "retryable": false
    }
  }
}
```

---

## 2. Status codes

| Status | Code(s) | Meaning |
|---|---|---|
| 200 | — | success |
| 304 | — | `If-None-Match` matched — send nothing (immutable bytes already cached) |
| 400 | `INVALID_CURSOR` | malformed cursor token |
| 404 | `OBJECT_NOT_FOUND` | entity doesn't exist (has `suggestion`) |
| 404 | `LAYER_NOT_FOUND` | no compiled layer at `/openpatala/{layer}` |
| 500 | `CROSSWALK_UNAVAILABLE` | `/resolve` backend not importable |
| 503 | `PROJECTIONS_NOT_BUILT` | run `build-static-site.py` first (compiled registry absent) |
| 503 | `INDEX_NOT_BUILT` | `search-index.json` absent |

---

## 3. Failure classes

### 3.1 Not found (404)
An entity id that doesn't resolve. Always carries a `suggestion`:
```json
{"error": {"code": "OBJECT_NOT_FOUND", "message": "no work <id>",
           "suggestion": "use /search?search=...", "retryable": false}}
```

### 3.2 Bad request (400)
A malformed cursor:
```json
{"detail": "invalid cursor"}
```

### 3.3 Projection not built (503, retryable)
The compiled registry / search index is absent (compute-on-write artifacts not produced yet):
```json
{"error": {"code": "PROJECTIONS_NOT_BUILT",
           "message": "run scripts/build-static-site.py first", "retryable": true}}
```
Retry after the builder runs. This is **retryable** — the operator must build the projections.

### 3.4 Crosswalk unavailable (500, not retryable as-is)
The identity resolver isn't importable:
```json
{"error": {"code": "CROSSWALK_UNAVAILABLE",
           "message": "metadata_resolver not importable: <err>", "retryable": false}}
```

---

## 4. Client guidance

- **On 304**: use the cached bytes — do not re-serialize/re-send. This is the normal, desired path.
- **On 503 retryable**: back off and retry after the projection builder has run.
- **On 404**: follow the `suggestion` (e.g. use `/search`). Do not retry blindly.
- **On 500**: not retryable as-is; it's a deployment/import problem to fix.

---

*All errors are machine-readable + agent-actionable by design. For the grammar see
`docs/api-reference.md`; for semantics `docs/entity-model.md`.*
