# DEVLPLAN HANDOVER v2 — the education-serving organism (REAL state, justified, checkpointed)

*2026-08-15 18:50 UTC · v2 corrects v1's two flaws: (1) the scholar engines ALREADY EXIST in
`/root/patalacheckpoints/pipeline/products/` (v1 implied Agent A builds them — it does NOT), and
(2) the kernel path is `kernels/`, not `lib/`. Every claim below was verified against the live code
2026-08-15. Checkpoints are concrete, falsifiable, and reference real gates. Split = 2 non-overlapping
agents (A: scholar/serving, B: organism/flywheel).*

---

## 0. THE STATE (verified, not aspirational)

| Claim | Verified? | Evidence (ran 2026-08-15) |
|---|---|---|
| 16 kernels | ✅ | `education-organism/kernels/` (16 `.py`) — note: path is `kernels/`, NOT `lib/` (v1 error) |
| 20 scripts | ✅ | `scripts/` (20 `.py`) |
| product engines 9 | ✅ | `pipeline/products/education_organism/engines/` (education, memory, misconception, organism, organism_loop, pedagogy, reconciliation, segment_key, staleness) |
| run-tests 22/22 | ✅ | `scripts/run-tests.py` → `SUMMARY: 22/22 passed` |
| test-e2e 5/5 | ✅ | `scripts/test-e2e.py` → `E2E: 5/5 passed` (audit trail) |
| audit-resolve | ✅ | `scripts/audit-resolve.py` → `RESOLVES TO SOURCE` (7 layers) |
| **scholar engines exist** | ✅ | `/root/patalacheckpoints/pipeline/products/scholar_identity/` etc. (scholar_identity, review_policy, scholar_vertical, scholar_publication, review_queue, review_workbench, scholar_review) — all present + tested |
| **serve-scholar already reaches into patalacheckpoints** | ✅ | `serve-scholar.py:22` → `PATA = "/root/patalacheckpoints"`, imports `review_queue.next_for` + `scholar_publication.profile_record/publish_all` |

**THE key correction to v1:** v1's Agent A tasks (A1–A3: "wire `scholar_identity`, `review_policy`, `scholar_vertical`, `scholar_publication`") read as *build-from-scratch*. They are **NOT** — the engines already exist and pass:
`scholar_identity 7/7 · review_policy 7/7 · scholar_vertical 5/5 · scholar_publication 5/5 ·
review_queue 6/6 · review_workbench 6/6 · scholar_review 11/11` (all in patalacheckpoints, all exposed
as `patala_*` MCP tools).

**Agent A's job is VERIFY-AND-WIRE (not build):** confirm the already-proven engines behave, then connect
the bits `serve-scholar.py` doesn't yet call.

---

## 1. THE ARCHITECTURE (the one organism, three layers — unchanged, correct)

```
PUBLIC SITE (0-JS, audited): /education /learning /bibliography /themes /scholars /scholar/workbench
  ▲  serves immutable bytes (compute-on-write, ETag/304)
PRODUCT ENGINES (deterministic, real data): education_organism + patalacheckpoints' scholar/review/
  manuscript engines
  ▲  feeds
THE ORGANISM (derivational chain + audit): SOURCE→…→C1→THEME→ARG→SYNTH→ESSAY→EDUCATION, audited via /resolve
```

**The one cross-repo fact that anchors everything:** the serving surface (`education-organism`) imports
its engines from `/root/patalacheckpoints`. The two repos are *joined at the product layer* — do not
duplicate the scholar engines into smellycock. **Reuse, don't rebuild.**

---

## 2. THE SEAM (revised, concrete — where the two agents meet)

| Shared thing | Who owns | Who reads | The contract |
|---|---|---|---|
| The audit trail (`/resolve`) | Agent B feeds, Agent A serves | both | `scripts/audit-resolve.py` must stay green |
| Learner DB (SQLite) | Agent B | Agent B | `kernels/memory.py`, `learner-log.py` |
| Scholar DB (adjudications) | Agent A | Agent A | currently in-memory `ADJUDICATIONS` in `serve-scholar.py` → to SQLite |
| **The product engines** | **patalacheckpoints lane** | both | read-only; import via `PATA` sys.path — never copy into smellycock |
| The site | Agent A | Agent B's data | rebuild after B commits education objects (compute-on-write) |

---

## 3. AGENT A — SCHOLAR + SERVING (verify-and-wire the human gate)

*Job: connect the ALREADY-BUILT engines to the live workbench. Not build-from-scratch.*

### A1 — Real scholar identity + Ed25519 auth (HIGH)
**What's real now:** `serve-scholar.py:31` → `SCHOLARS = {"scholar-A": ...}` (hardcoded demo). Engine
`scholar_identity` (7/7) + Ed25519 signing already exist in patalacheckpoints; `serve-scholar.py` does
**NOT** yet import them.
**The change:** import `scholar_identity` (ORCID + domain scope + Ed25519 keypair) into `serve-scholar.py`;
`/scholar/login` returns a signed token instead of the hardcoded dict.
**CHECKPOINT (falsifiable):** `/scholar/login` returns a token whose signature verifies with the embedded
public key (`scholar_identity` 7/7 proof pattern); the demo `scholar-A` is gone.

### A2 — Review-queue + adjudicate persistence (HIGH)
**What's real now:** `serve-scholar.py:24` already calls `review_queue.next_for` (queue) ✓. But
`serve-scholar.py:32` → `ADJUDICATIONS = []` is in-memory (lost on restart).
**The change:** (a) persist adjudications to SQLite (new table), (b) import `review_policy` (7/7) for
ACCEPT/REVISE/REJECT authority semantics + `scholar_vertical` (5/5) for the attestation vertical into the
adjudicate endpoint.
**CHECKPOINT (falsifiable):** an ACCEPT actually promotes the object's registry status
`MACHINE_PROPOSED → ADJUDICATED` in the patalacheckpoints registry (check the layer registry file);
adjudications survive a server restart (SQLite, not the in-memory list).

### A3 — Scholar publication → site (MEDIUM)
**What's real now:** `serve-scholar.py:25` already imports `scholar_publication.profile_record/publish_all` ✓.
**The change:** auto-run `publish_all` after an ACCEPT → recompile `/scholars/` JSON-LD; add a per-scholar
page `/scholar/{id}/`.
**CHECKPOINT (falsifiable):** after an adjudication, the `/scholars/` JSON-LD reflects the new
contribution; `/scholar/{id}/` serves it (HTTP 200).

### A4 — Scholar workbench UX (MEDIUM)
**The change:** flesh out `/scholar/workbench.astro`: login form, queue list, review screen (one object
full context via `review_workbench` 6/6), decision buttons.
**CHECKPOINT (falsifiable):** the workbench page loads the review context for a real object (not a stub)
and a decision button fires the `/adjudicate` POST.

### A5 — Site/API hardening (MEDIUM)
**The change:** build into `web/dist` (already gitignored) + a deploy script (Cloudflare Workers per the
perf doctrine); ETag/304 + immutable caching on the API.
**CHECKPOINT (falsifiable):** a rebuild emits into `web/dist/`; the API returns `ETag`/304 on repeat GETs.

---

## 4. AGENT B — ORGANISM + FLYWHEEL (the data depth)

### B1 — Real learner data flow (HIGH)
**What's real now:** `kernels/memory.py` + `learner-log.py` exist; `serve-education /answer` records
interactions.
**The change:** record EVERY interaction to SQLite (question, answer, blind grade, failure_type), not just
the first claim.
**CHECKPOINT (falsifiable):** N tutor interactions → N rows in the learner SQLite table (each with a
failure_type); a wrong answer is persisted, not dropped.

### B2 — The closed flywheel with real data (HIGH)
**What's real now:** `kernels/misconception.py` (MisconceptionRepairCascade) + `kernels/staleness.py`
(RKA) exist.
**The change:** run the repair cascade over the ACTUAL learner events from B1: cluster real confusions →
flag the source → RKA propagate → measure dissolution.
**CHECKPOINT (falsifiable):** a run-8 log shows flagged / stale / dissolved metrics computed from REAL
learner rows (not a synthetic fixture); at least one real confusion resolves to a source.

### B3 — Procedural memory integration (MEDIUM)
**The change:** wire `kernels/memory.py` ProceduralMemory into the tutor so past sessions consolidate +
persist (dream-cycle), targeting the weakest skill from history.
**CHECKPOINT (falsifiable):** after ≥2 sessions, the tutor targets the skill the learner failed most
(proven from the learner DB, not a hardcode).

### B4 — Reconciliation gate on generation (MEDIUM)
**The change:** apply `kernels/reconciliation.py` to the ESSAY/EDUCATION generation path (prove the model
preserved source while adding structure).
**CHECKPOINT (falsifiable):** a source-preserving derivation PASSES; a source-dropping derivation BLOCKS
(the run-tests.py pattern, already 22/22 — extend it to the live path).

### B5 — Derivation-chain completeness (MEDIUM)
**The change:** extend the lower-chain linker beyond the kramasadbhava customer path; link the IPVV gold
chain; enforce `input_refs` at commit (reject empty on lower layers).
**CHECKPOINT (falsifiable):** ≥1 new work links SOURCE→C1 (resolves via `audit-resolve.py`); a commit with
empty `input_refs` on a lower layer is rejected.

---

## 5. THE GATES (never skip — per the axioms)

```bash
# both agents, before claiming anything
cd /root/smellycock/education-organism
python3 scripts/run-tests.py     # 22/22 (must stay green)
python3 scripts/test-e2e.py      # 5/5 (the audit trail)
python3 scripts/audit-resolve.py # claim → source (must resolve)

# Agent A, after touching the workbench
cd /root/patalacheckpoints && for p in scholar_identity review_policy scholar_vertical \
     scholar_publication review_queue review_workbench scholar_review; do
     PYTHONPATH=pipeline python3 pipeline/products/$p/test.py | grep SUMMARY; done

# Agent B, after touching kernels
cd /root/smellycock/education-organism && python3 scripts/run-tests.py
```

**Banned words:** PROVED · TRUTH · CORRECT · BEST · WINS. **Use:** SUPPORTED BY · PASSED CHECK X ·
MACHINE-PROPOSED · REVIEWED BY.

---

## 6. THE DEFINITION OF DONE (next milestone — falsifiable)

1. A scholar logs in with a **real Ed25519 identity** (A1 checkpoint) → sees the prioritized queue
   (`review_queue`) → adjudicates **ACCEPT** → the object promotes **MACHINE_PROPOSED → ADJUDICATED** in
   the registry (A2 checkpoint) → `scholar_publication` recompiles → the public site serves the citable
   record (A3 checkpoint).
2. Real learner interactions flow into **SQLite** (B1) → the MisconceptionGraph → the repair cascade (B2)
   → run-8 flywheel metrics (flagged / stale / dissolved) from **REAL data**.
3. Both agents' gates stay green; every new object resolves to source.

---

## 7. THE PROVENANCE RULE (the fix v1 missed)

- **The scholar engines live in `/root/patalacheckpoints/pipeline/products/`** — do NOT copy them into
  smellycock. `serve-scholar.py` already reaches across via `PATA = "/root/patalacheckpoints"`.
- **The organism kernels live in `/root/smellycock/education-organism/kernels/`** (NOT `lib/`).
- If you need a capability the engines already provide, call it — don't rebuild it.

---

*This is the v2 handover. Agent A verifies + wires the existing scholar engines; Agent B builds the data +
flywheel depth. Both meet on the audit trail. Checkpoints are real, gates are green, provenance is exact.*
