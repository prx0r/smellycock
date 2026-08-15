# epistemic — MODEL (object contracts + authority)

*2026-08-15. The object contracts for the epistemic layer: what each product's output IS, its authority
vector, and the invariant. Mirrors `OBJECT-MODEL.md` (the production object model) + `AXIOMS.md` §4
(status ladders, authority). Semantics here; wire mechanics in `reference.md`.*

---

## 1. The authority model (identical to the canonical model)

Every product output carries the **4-axis authority vector** (`generation · evidence · review ·
publication`), a **partial order** (`A ⪯ B ⟺ ∀i A_i ≤ B_i`), **never** a scalar max.

```text
authority(projection) ≤ authority(parent)     ← the invariant, on every edge
object TYPE ≠ epistemic STATE                ← a real Source is not SCHOLARLY_CORROBORATED by type
```

**The epistemic_ceiling ladder** (never inflate): `MACHINE_PROPOSED → ENGINEERING_VALIDATED →
SCHOLARLY_CORROBORATED → INDEPENDENT_REVIEWED → ADJUDICATED`.

---

## 2. The object shapes (canonical-named)

### 2.1 Proposition (product #2, `claim`) — PTPROP
```json
{
  "object_id": "PTPROP_...",
  "version_id": "PTPROP_...@v1",
  "claim": "<thesis from the real C1>",
  "scope": "PASSAGE_LOCAL | GENERAL",
  "modality": "ACTUALITY | NECESSITY | POSSIBILITY",
  "epistemic_status": "SOURCE-SAYS | SCHOLAR-RECONSTRUCTS | PĀṬALA-INFERS",
  "epistemic_ceiling": "MACHINE_PROPOSED | SCHOLARLY_CORROBORATED",
  "authority": { "generation": "MACHINE_PROPOSED", "evidence": "NONE",
                 "review": "NOT_REVIEWED", "publication": "PRIVATE" },
  "evidence_quote": "<verbatim from the C1>",
  "source_refs": ["<immutable id>"],
  "gated_ok": true
}
```
Rule: a `PĀṬALA-INFERS` claim **stays `MACHINE_PROPOSED`** — only a `SOURCE-SAYS` status + real source
raises it. Never inflate.

### 2.2 Argument (product #3) — PTARG
```json
{ "object_id": "PTARG_...", "thesis": "...", "premises": ["P0","P1"],
  "inference": { "premise_ids": ["P0","P1"], "conclusion_id": "C0", "type": "abduction" },
  "defeaters": ["..."], "source_refs": ["<immutable>"], "status": "MACHINE_PROPOSED" }
```
Gate: inference type is a **closed vocabulary** (borrowed darshana-graph discipline) — an invented type
is dropped, never kept.

### 2.3 Crux (product #4) — PTCRUX
```json
{ "position_a": "PTARG_...", "position_b": "PTARG_...", "crux_count": 6,
  "crux_a_asserts": ["..."], "crux_b_asserts": ["..."], "shared_premises": [] }
```

### 2.4 Review / Attestation (product #8) — PTREV
- **Review:** `{target, reviewer, decision (ACCEPT/REVISE/REJECT/ABSTAIN), scope, rationale, evidence_refs}`
  — append-only, never mutates the target.
- **Attestation:** content-addressed + **Ed25519 signed** (cosign-style); verify with the public key only.
  Tamper → verification FAIL.
- **Boundary:** a `machine` actor may PROPOSE but never submit a state-changing review (executable).

### 2.5 Bundle (product #9) — PTPACK
Token-budgeted: `micro 2k / standard 8k / deep 32k`. Sections ordered by priority, dropped when the
budget binds (deterministic). Content-addressed `bundle_hash`.

### 2.6 Passage (product #10) — PTPASS
`{passage_id, immutable_id, work_id, source_sanskrit, l2_translation, c1_commentary, status}` — the
philology primitive; the read-plane anchor.

---

## 3. The registry / commit contract

The epistemic products READ the canonical registries (`data/corpus/registries/*-registry.jsonl`) and
produce DERIVED objects. When they commit (e.g. attestations, review-gate decisions), they follow the
same contract as the production model:
- **Append + versioned** (never in-place edit; supersession creates a new version).
- **Idempotent** (dedup by `input_hash`).
- **Content-addressed** where identity matters.

---

## 4. The live truth (what the products read — verified 2026-08-15)

| Layer | Registry count | Product reads |
|---|---|---|
| C1 | 43 | `claim`, `argument`, `evidence_independence` |
| argument | 23 | `crux`, `comparison` |
| synthesis | 7 | `crux`/`comparison`/`research_packet` inputs |
| essay | 8 | `scholar_review`, `context_bundle` |
| education | 6 | `context_bundle` |
| assertion / corroboration | 6 / 6 | `evidence_independence` |

---

*This is the object model for the epistemic layer. It honors the canonical authority model, identity
rule, and status ladders exactly — no 5th taxonomy, no scalar authority, no banned words.*
