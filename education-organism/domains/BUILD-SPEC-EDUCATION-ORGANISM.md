# BUILD SPEC — the education-serving organism (end-to-end, auditable)

*2026-08-15. From the context + performance + derivation-chain audits. This specs the actual
infrastructure that turns the (real, validated) kernels into a working organism that serves education
to a customer with a full source→L0→…→C1→…→EDUCATION audit trail.*

---

## 0. THE HONEST CURRENT STATE (from the audits)

| Half | Linked? | Evidence |
|---|---|---|
| **Upper: C1→THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION** | ✅ REAL | `input_refs` populated; ENGINEERING_VALIDATED; education has real learning claims with `depends_on` resolving down |
| **Lower: SOURCE→T1→L0→L1→L2→L200→C1** | ❌ DISCONNECTED | `input_refs=[]` everywhere; SOURCE/T1/L0 seam has NO edge; L200 dual-superseded bug; stale L1 ref |
| **Site** | ❌ no education | Astro has bibliography/passages/themes/scholars, NO learning pages |
| **Tutor agent** | ❌ missing | kernels exist, nothing serves them |
| **Data logging** | ❌ missing | learner responses/mastery/misconceptions not persisted |
| **Audit resolver** | ❌ missing | no utility walks source→…→EDUCATION |

**The design law:** education is a projection of the graph (never a separate KB). Every LearningClaim
resolves downward to canonical objects.

---

## 1. WHAT TO BUILD (in dependency order)

### BUILD-1: The derivation-edge linker (the audit trail foundation)
Backfill `input_refs` on the lower six layers using the shared `object_id` as the join key:
```
SOURCE.v1 → T1 → L0 → L1 → L2 → L200 → C1
```
- Promote payload refs to `input_refs`: L1 `l0_ref`, L2 `l1_ref`, L200 `l2_ref`, C1 `_l200_version`.
- Fix data defects: L200 dual-superseded, stale L1 ref, missing T1 for v4.
- **Gate:** a layer is only eligible when its parent `input_refs[0]` resolves (the existing
  `DEPENDENCY_BLOCKED` pattern).

### BUILD-2: The audit/resolve resolver
A utility that walks any `object_id` up/down the chain:
```
resolve(object_id) → the full lineage: SOURCE→T1→L0→L1→L2→L200→C1→THEME/ARG→SYNTH→ESSAY→EDUCATION
```
Fails loudly at any seam with no edge. This is the audit trail: any educational claim traces to its
source Sanskrit.

### BUILD-3: The education serving site (Astro, compute-on-write)
New pages compiled at write time (never per-request LLM):
- `/education/` — lesson index (by work/difficulty/ceiling)
- `/education/{lesson_id}/` — the LearningPacket (question, expected, wrong-answer taxonomy, deps)
- `/learn/{work_id}/` — the ordered lesson progression
- `education-index.json` + `education-{lesson}.json` + search index (static bytes, ETag/304)

### BUILD-4: The AI tutor agent
Serves the LearningPackets + interacts:
- presents a question → learner answers → **blind-assessor grade** (recalled/partial/lapsed) →
  next interaction (targets the weakest skill). **No LLM in the cognition path** — deterministic .py.

### BUILD-5: The data logging store
Persist learner responses/mastery/misconceptions (append-only, streamed):
- `learner-events.jsonl` (responses, correctness)
- `mastery-state.json` (per learner per concept, BKT)
- `misconceptions.jsonl` (wrong-answer → known neighbor)
- feeds the misconception graph → the flywheel.

### BUILD-6: The end-to-end pipeline + audit
Wire source→…→EDUCATION→customer with the resolver + serving + logging as ONE tested path.

---

## 2. PERFORMANCE CONSTRAINTS (the 10-rule doctrine)

- **Compute on write, not read** — education pages are static bytes, ETag/304, immutable.
- **One agent question = one request** — `/education/{id}`, bounded depth.
- **0-JS reading pages** — Astro static; islands only for real interaction.
- **Stream, never bulk-load** — registries are big (SOURCE 47k); the resolver streams.
- **RAM budget** — 4-core/8GB/no-swap, 2 agents. Test suite must stay < ~30MB RSS.

---

## 3. ANTI-THEATRE / AXIOMS

- Every LearningClaim `derived_from` a real committed object; ceilings honest (MACHINE_PROPOSED /
  ENGINEERING_VALIDATED).
- The blind-assessor gate proves "did the learner get it" — no inflated claims.
- **Test on real data** — the e2e test traces a REAL education claim back to its REAL source, not a
  fixture.

---

## 4. TEST + LOG

- `run-tests.py` extended: linker (chain resolves), resolver (trace real object), tutor (grade),
  logging (persist), e2e (education claim → source).
- `check.py --status` runs all gates on real data.
- Log the run in `data/runs/run-4/` (honest per-object verdicts + performance).
