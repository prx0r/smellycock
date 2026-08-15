# epistemic — GENIUS-PINCHES (processes worth adopting from live docs + similar repos)

*2026-08-15. The "genius" processes observed in the real OpenAlex docs + similar scholarly-graph /
identity products (cloned in `source-evidence/repos/`), and which of our products they should upgrade.
Each: what the process is, the source, and the concrete upgrade to our epistemic layer. License-safe
(MIT/Apache/BSD) unless flagged.*

> **Reference, don't copy.** These are patterns to pinch — re-express against Pāṭala's objects, never
> copy wholesale.

---

## 1. Temporal validity windows (facts invalidated, not deleted) — Graphiti

**The process:** a fact/edge carries a **validity window** (`valid_at` / `invalid_at`). When the world
changes, the old fact is **invalidated — not deleted** — so you can query "what was true now" vs "what
was true at time T." Full temporal history preserved.

**Source:** `getzep/graphiti` — "Facts have validity windows. When information changes, old facts are
invalidated — not deleted. Query what's true now, or what was true at any point in time."

**Upgrade for our layer:**
- **`evidence_independence`**: a corroboration/independence classification should carry `valid_at`
  (the OpenCitations fetch time) + be **invalidatable** when the source changes — not re-inserted. This
  closes the "5× duplicate corroboration" finding with a real temporal model.
- **`scholar_review` (gate)**: a review decision supersedes — never deletes — the prior review; the
  `superseded`/`superseded_by` already exists; make the *validity window* explicit so "what was the
  effective state at revision N" is queryable.

## 2. Compile-on-write + zero-LLM second compile — sage-wiki (already core, verify)

**The process:** `sage-wiki compile` skips unchanged docs on the second run — "zero LLM calls — unchanged
docs are skipped." The graph is a **compile output, not a second database**.

**Status in our layer:** this is already the stack's doctrine (AXIOMS §12: compute on write, read from
bytes; content-addressing). **Verified present** — nothing to add, but worth asserting in the docs.

## 3. Closed-vocabulary + verbatim `evidence_quote` — darshana-graph (already pinched)

**The process:** the model may only emit relations from a FIXED vocabulary, each with a verbatim
`evidence_quote` from the source; anything outside is dropped + counted (never silently kept).

**Status:** already integrated into `_shared/closed_vocabulary.py` + `argument.gated_argument()` + the
`claim` honesty gate. **Done** — this is the backbone of "every claim resolves to source."

## 4. The OpenAlex DO/DON'T + common-mistakes LLM guide — OpenAlex (the doc-structure genius)

**The process:** the OpenAlex `api-guide-for-llms.md` is a **DO/DON'T + 10-common-mistakes** reference
for agents: don't sample by random page (use `?sample=`), don't filter by name (two-step ID lookup),
don't loop sequential ID calls (batch with `|`), implement exponential backoff, `per-page=200`,
`select=` only needed fields.

**Upgrade for our docs:** our `openpatala/llm-guide.md` has the fastest-answers table + token efficiency
but **lacks the DO/DON'T + common-mistakes layer**. Add it (see the enhanced llm-guide).

## 5. Two-step ID lookup, never name-filter — OpenAlex (identity genius)

**The process:** never `filter=author_name:Einstein`; first `search` → get the ID → then filter by ID.
Names are ambiguous; IDs are unique.

**Upgrade for our layer:** our `canonical_id.py` already resolves aliases → canonical IDs
(`canonical_or_self`). **Make the docs teach the two-step pattern** explicitly: resolve → filter by
canonical id, never by display name.

## 6. Per-dimension authority + eligibility predicates, never a scalar — OpenAlex/entity-model (already core)

**The process:** authority is a vector of independent dimensions; eligibility is an explicit predicate,
never `ceiling >= N`.

**Status:** already the stack's model (AXIOMS §4, entity-model). **Verified present.**

---

## The build order (which pinch to wire first)

1. **Temporal validity windows** into `evidence_independence` + `scholar_review` (the highest-value
   genuine addition — closes the SOURCE_ECHO/duplication finding with a real time model).
2. **The DO/DON'T + common-mistakes layer** into the openpatala LLM guide (doc-structure alignment with
   OpenAlex — the thing the user asked for).
3. **Two-step ID lookup** as an explicit documented pattern (canonical_id is ready; teach it).

The rest (compile-on-write, closed-vocab, authority vector) are already integrated — the docs should
say so, not pretend they're new.

---

*This is the pinch list for the epistemic layer. It records what to adopt (temporal validity, DO/DON'T
doc layer, two-step lookup) vs. what's already integrated (compile-on-write, closed-vocab, authority
vector) so nothing is re-invented.*
