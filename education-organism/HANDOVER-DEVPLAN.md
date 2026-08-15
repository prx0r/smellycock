# DEVLPLAN HANDOVER — the education-serving organism (timestamped)

*2026-08-15 18:33 UTC · updated 18:40 UTC after reading `contextreviewcock.md` (the other lane's
consolidated view). This handover is for the next agent(s) who continue work on the education-serving
organism. It records the FULL state, what's live, the dependencies, and how the next work divides into 2
parallel agents. Everything lives in `/root/smellycock` (the canonical, pullable project).*

---

## 0.5 CROSS-LANE CONTEXT (from `contextreviewcock.md`, verified 18:40 UTC)

**The other lane's view of the SAME stack — read this before building anything in the handover below.**

1. **The scholar stack I wanted to build (Agent A) is ALREADY BUILT by the other lane.** Verified live:
   `scholar_identity` (real ORCID + Ed25519 `signing_key()/public_key()`), `scholar_vertical`,
   `review_policy`, `review_queue`, `review_workbench`, `scholar_profile`, `scholar_review`,
   `scholar_publication` — all in `/root/patalacheckpoints/pipeline/products/`. **ADOPT, do NOT rebuild.**
   → Agent A's A1/A2 become *integration* work, not green-field.
2. **The moat is the `epistemic_ceiling` invariant in `/root/fuck-off/lib/epistemic.py`** —
   `authority(projection) ≤ authority(parent)` + 4-axis authority. Absent from the published graph-RAG
   landscape. **Thread it into my organism** (Agent B), not just the graph. → B2/B4 become ceiling-aware.
3. **Hermes must be used agentic (`hermes chat`), never blind (`hermes -z`).** The ~3.8% translation
   yield was a `-z` bug. This is the generation half of the generation/reduction split.
4. **smellycock is SHARED by BOTH lanes — always `pull --rebase` before push.** (commits 13a0232,
   51fcf42 are the other lane's reconciliation; don't clobber them.)
5. **Fuck-off's `lib/retrieval.py`** (PathRAG + HippoRAG + ToG-2, dependency-light) is the mature version
   of my one-off research_packet flow. Lift it into the organism's retrieval path (reuse, don't rebuild).
6. **Known stale facts to fix:** repo paths in docs point to `/root/projects/patala` +
   `/mnt/HC_Volume_106427611/ip-graph` (old layout; real = `/root/patalacheckpoints` + `/root/fuck-off`);
   test counts say "25 products / 134 PASS / 61 tools" but reality is **26 products / 152 PASS / 63
   tools** (translation_studio added). These are checked-in; my gates tolerate via alias, but the docs
   should be corrected.

---

## 0. THE STATE (what exists, all verified)

- **Project**: `/root/smellycock` — the canonical smellycock/patalaorg project (git repo, branch main,
  up to date with origin/main).
- **The education-serving organism**: `smellycock/education-organism/` (16 kernels, 20 scripts, 9
  domain docs, 7 logged runs) + the product `smellycock/pipeline/products/education_organism/`
  (README/AGENT-GUIDE/VISION/DEPENDENCIES + 9 engines).
- **Live surfaces** (all HTTP 200): Astro site (`/root/smellycock/web` → 11 pages) + education API
  (:8787) + scholar workbench API (:8788) + SQLite learner store.
- **Gates**: `check.py` PASS, `check_epistemic.py` PASS (25 products, 8 layers reconciled).
- **The audit trail**: an education claim resolves to source (e2e 5/5) —
  `EDUCATION → ESSAY → SYNTHESIS → ARGUMENT → C1 → L200 → L2 → L1 → L0 → T1 → SOURCE`.
- **Tests**: `run-tests.py` 22/22.

## 1. THE ARCHITECTURE (the one organism, three layers)

```
PUBLIC SITE (0-JS, audited): /education /learning /bibliography /themes /scholars /scholar/workbench
  ▲  serves immutable bytes (compute-on-write, ETag/304)
PRODUCT ENGINES (deterministic, real data): education_organism + agent3's passage/claim/argument/
  crux/scholar_*/review_*/collation/manuscript_*/tension_finder
  ▲  feeds
THE ORGANISM (derivational chain + audit): SOURCE→…→C1→THEME→ARG→SYNTH→ESSAY→EDUCATION, audited via /resolve
```

## 2. THE 7 RUNS (the evidence trail)

| Run | What it proved |
|---|---|
| run-1 | the initial spine + build status |
| run-2 | post-red-team rebuild (gates on real data, honest statuses) |
| run-3 | the organism flywheel + ingestion refinery + memory |
| run-4 | the education-serving organism e2e (audit trail 5/5) |
| run-5 | the GEM integrations (segment-key + reconciliation) |
| run-6 | the audited endgame site (live) |
| run-7 | the scholar workbench (the human gate, live) |

---

## 3. THE NEXT WORK — DIVIDED INTO 2 AGENTS

Two parallel agents, non-overlapping. Agent A owns the **product/serving depth**; Agent B owns the
**organism/flywheel depth**. They meet on the audit trail + the site.

### AGENT A — SCHOLAR + SERVING (the human gate + surface depth)
*Owner: the serving surface + the scholar workbench + the live product.*

**A1 — Adopt the existing scholar identity (HIGH) — REVISED, not green-field**
- The other lane's `scholar_identity` ALREADY does ORCID + domain scope + Ed25519 signing. INTEGRATE it
  into the workbench API (`/root/patalacheckpoints/pipeline/products/scholar_identity/engine.py`), don't
  write a new one.
- Replace the demo `scholar-A` with a real keyed identity; `/scholar/login` returns the signed token.
- Gate: an adjudication is Ed25519-signed (via `scholar_identity.signing_key()`), not a plain string.

**A2 — Review-queue + adjudicate persistence via the existing products (HIGH) — REVISED**
- Persist the review queue + adjudications to SQLite (currently in-memory `ADJUDICATIONS` list).
- Wire the other lane's `review_policy` (ACCEPT/REVISE/REJECT) + `scholar_vertical` into the adjudicate
  endpoint (both already exist — adopt their authority semantics).
- Gate: an ACCEPT promotes the object's registry status MACHINE_PROPOSED → ADJUDICATED, signed.

**A3 — Scholar publication → site (MEDIUM)**
- Auto-run `scholar_publication.publish_all` after an adjudication → recompile the `/scholars/` JSON-LD.
- Add a per-scholar page (`/scholar/{id}/`) with their contributions + attestations.

**A4 — The scholar workbench UX (MEDIUM)**
- Flesh out `/scholar/workbench.astro`: login form, queue list, review screen (one object full context
  via `review_workbench`), decision buttons.

**A5 — Site/API hardening (MEDIUM)**
- Move the site build into `web/dist` (already gitignored) + a deploy script (Cloudflare Workers per
  the perf doctrine). Add ETag/304 + immutable caching headers to the API.

### AGENT B — ORGANISM + FLYWHEEL (the data depth)
*Owner: the learner data, the misconception flywheel, the derivation chain, the memory.*

**B1 — Real learner data flow (HIGH)**
- Wire the tutor (`serve-education /answer`) to record EVERY interaction (not just the first claim) to
  SQLite: question, answer, blind grade, failure_type.
- Feed the recorded wrong-answers into the MisconceptionGraph + repair cascade (the flywheel's fuel).

**B2 — The closed flywheel with real data, ceiling-aware (HIGH) — REVISED**
- Run `misconception.MisconceptionRepairCascade` over the ACTUAL learner events: cluster real
  confusions → flag the source → RKA propagate → measure dissolution.
- Thread the `epistemic_ceiling` invariant (from `/root/fuck-off/lib/epistemic.py`) into the cascade so
  a dissolution/flag never claims more than its authority(projection) ≤ authority(parent) allows.
- Log the flywheel metrics (run-8): flagged / stale / dissolved from REAL learner data.

**B3 — Procedural memory integration (MEDIUM)**
- Wire `memory.ProceduralMemory` into the tutor so a learner's past sessions consolidate + persist
  (dream-cycle), so the tutor targets the weakest skill from history.

**B4 — Reconciliation + ceiling gate on generation (MEDIUM) — REVISED**
- Apply `reconciliation_check` to the ESSAY/EDUCATION generation path (prove the model preserved
  source while adding structure) — the anti-theatre gate for new content.
- Add the fuck-off `authority(projection) ≤ authority(parent)` check so no generated object overclaims
  its epistemic ceiling (the moat, threaded into the organism).

**B5 — Derivation-chain completeness (MEDIUM)**
- Extend the lower-chain linker to more works (currently only the kramasadbhava customer path is
  linked SOURCE→C1). Link the IPVV gold chain too.
- Enforce input_refs at commit (reject empty on the lower layers) so future objects are always audited.
- Lift `/root/fuck-off/lib/retrieval.py` (PathRAG/HippoRAG/ToG-2) into the organism's retrieval path —
  reuse the mature version rather than the one-off research_packet flow.

---

## 4. THE SEAM (where the two agents meet — coordinate, don't collide)

- **The audit trail** (`/resolve`) is the shared spine. Agent A serves it; Agent B feeds it (more
  objects + learner data). Both must keep `audit-resolve.py` green.
- **The learner DB** (SQLite) is Agent B's; the scholar DB (adjudications) is Agent A's. Separate
  tables, no collision.
- **The site** is Agent A's; the data it serves is Agent B's. A rebuild happens after B commits new
  education objects (compute-on-write).

## 5. THE GATES (never skip — per the axioms)

```bash
cd /root/smellycock
python3 check.py --status        # drift validator
python3 check_epistemic.py       # product engine reconciliation
cd education-organism
python3 scripts/run-tests.py     # 22/22 (must stay green)
python3 scripts/test-e2e.py      # 5/5 (the audit trail)
python3 scripts/audit-resolve.py # claim → source
```

**Banned words**: PROVED · TRUTH · CORRECT · BEST · WINS. **Use**: SUPPORTED BY · PASSED CHECK X ·
MACHINE-PROPOSED · REVIEWED BY.

## 6. THE DEFINITION OF DONE (for the next milestone)

- A scholar logs in with a real Ed25519 identity, sees the prioritized review queue, adjudicates
  ACCEPT → the object promotes to ADJUDICATED → `scholar_publication` recompiles → the public site
  serves the citable record.
- Real learner interactions flow into SQLite → the MisconceptionGraph → the repair cascade → the
  flywheel metrics (run-8) show flagged/stale/dissolved from REAL data.
- Both agents' gates stay green; every new object resolves to source.

---

## 10. BUILT THIS SESSION (the frontier adoptions, live + tested)

*The frontier-review's top adoptions are now REAL CODE in smellycock, verified 39/39 tests + all gates
green. The FRONTIER-REVIEW §11 is the authoritative "what's built."*

- **`kernels/guard.py`** — fojin's quote_verifier + citation_whitelist, Sanskrit-adapted (stdlib, no
  OpenCC), wired into `serve-education.py` `/guard` + `/answer`. The enforcement our UNANCHORED→reject
  rule lacked. Idempotent; invented quotes downgraded to prose, fabricated citations stripped.
- **`kernels/learner_gate.py`** — the learner-store legitimacy stack (graphiti temporal + MKG 2-tier
  authority gate + MemOS correction guards) as one stdlib kernel. Time-bounded beliefs, machine veto/
  reinforce/accept, human review queue stamped `reviewed_by`.
- **`kernels/misconception.py`** — `weighted_propagate` (RKA: derived_from=1.0, contradicts=1.1,
  cites=0.7, supersedes=0.3) replaces the unweighted blast-radius in the repair cascade.
- **`kernels/staleness.py`** — graphiti `TemporalFact.episode` provenance + `facts_to_context` time-aware
  read-plane compiler.
- Product engines mirrored (`engines/guard.py`, `engines/learner_gate.py`, misconception/staleness
  synced), MANIFEST updated, FRONTIER-REVIEW §11 + this HANDOVER record the build.

**Remaining (Agent A/B next):** measured-learning eval (§6 of FRONTIER-REVIEW), OpenEvolve retain-loop,
GFM-RAG rankers + RoG path-utils in retrieval, SciFact gold + eval regression harness.
