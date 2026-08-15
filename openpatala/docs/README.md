# OpenPāṭala Documentation

Native documentation for the OpenAlex-grammar API over the Sanskrit record. These are Pāṭala-native
docs (the imported OpenAlex reference lives in `../reference/openalex/` for direct comparison).

## Read in this order

| Doc | What it is | Read when |
|---|---|---|
| `api-reference.md` | the wire grammar — filter/search/sort/group/select/cursor/autocomplete, response envelope, caching, endpoints | you're calling the API |
| `entity-model.md` | the semantics — the `PT*` identity scheme, textual-transmission chain, per-dimension authority, the Work object, external-ID crosswalks, rights | you need to know what an entity/field means |
| `errors.md` | the failure modes — status codes, exact error JSON, retryability | your request failed / you're writing a client |
| `llm-guide.md` | one page for agents — fastest answers, token efficiency, identity rules | you're an LLM/agent using the API |
| `../openapi.yaml` | the machine-readable OpenAPI 3.1 spec of the Atlas API (wire grammar + envelope + error bodies) | your client/agent tooling consumes the API directly |

## OpenAPI

The machine-readable contract is **`../openapi.yaml`** (OpenAPI 3.1). It documents the 17 Atlas
endpoints, the OpenAlex query grammar (`filter`/`search`/`sort`/`group_by`/`select`/`cursor`/
`autocomplete`), the response envelope, the external-identifier crosswalk, and the error body. Agents
and SDKs can load it directly instead of re-reading this prose.

## The reference/model/recipes split (why it's structured this way)

- **wire** (`api-reference.md`) — mechanics only. Never re-explains what a Work is; links out.
- **semantics** (`entity-model.md`) — meaning only. Never repeats URL syntax.
- **recipes** (this index + the how-to examples) — tasks.

This mirrors OpenAlex's own docs structure (reference/model/recipes), so the two are directly
comparable and OpenAlex users feel at home.

## The three truths (recap)

`Postgres` = entity truth · `R2` = artifact truth (SHA-256) · event log = history truth. Everything
else is a rebuildable projection. Compute on write, read from bytes.
