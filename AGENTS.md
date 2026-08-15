# AGENTS.md — read this FIRST. The governing file for every agent in patalaorg.

*Auto-loaded when an agent works in this project. patalaorg is the **clean canonical reference** for the
Pāṭala stack — it documents + validates, it does not duplicate the working repos. Read this, then
`AXIOMS.md`, then `MANIFEST.json`, then `check.py --status` before doing anything. This project exists to
keep the documentation TRUE and drift-proof (the ONE RULE below).*

---

## 0. THE ONE RULE

> **Nothing is "real" because a file exists. It is real only when an independently defined task,
> human-grounded gold, and a reproducible gate show it does what its name claims. A doc is a projection;
> the truth is `object_registry` + `corpus_state` + ReviewEvents + git.**

patalaorg is the *projection layer*. Every doc here must resolve to a real path in the working repos and
(where possible) reconcile to a live count. If it can't, it doesn't belong here.

---

## 1. WHAT PATALAORG IS (and is NOT)

- **IS:** the clean, authoritative, agent/machine-referenced documentation + contracts for the whole
  Pāṭala stack — rules (`AXIOMS.md`), the object model (`OBJECT-MODEL.md`), the machine pointer
  (`MANIFEST.json`), the drift validator (`check.py`), the performance doctrine (`performance/`), and the
  per-domain references (`domains/`).
- **IS NOT:** a copy of code. It **points at** `patala/` (PRODUCES) and `ip-graph/` (VALIDATES + SERVES)
  via `reference/`, and **validates against them**.

| Repo | Role | Path |
|---|---|---|
| **patala** | PRODUCES — the factory DAG, the atlas surface, the workers, the registry | `/root/projects/patala` |
| **ip-graph** | VALIDATES + SERVES — read plane, organism, validation kernels, OpenAlex surface | `/mnt/HC_Volume_106427611/ip-graph` |

---

## 2. THE READ ORDER (what to read, in what order, before building)

```text
STEP 1  THIS FILE (AGENTS.md)      the one rule + how to behave.        (you are here)
STEP 2  README.md                  the constitution + the three planes.
STEP 3  AXIOMS.md                  the STRICT rules: naming conventions, file organisation,
                                   operating axioms, banned words. The non-negotiables.
STEP 4  OBJECT-MODEL.md            the canonical DAG (from LAYERS.yaml) + object/registry contracts.
STEP 5  MANIFEST.json              the machine pointer (every doc → id + owner + validator).
STEP 6  performance/README.md      the perf doctrine + budgets (if you touch surfaces).
STEP 7  check.py --status          the drift validator (run before/after any doc change).
```

Before writing a domain doc, ALSO read the domain's canonical reference in the working repo (e.g.
`patala/translation/`, `patala/openpatala/docs/`) so this project stays a clean projection, not a 4th
description.

---

## 3. HOW TO UPDATE PATALAORG (the maintenance rules)

1. **Never duplicate a role.** If a doc here already covers a concern, extend it — don't add a sibling.
   `check.py` rejects duplicate roles.
2. **Never invent a 5th status ladder or taxonomy.** `AXIOMS.md` freezes them.
3. **Every new doc gets a MANIFEST entry** (stable id + owner + validator) or `check.py` flags it.
4. **Reference, don't copy.** Point at `patala/` + `ip-graph/` paths; only copy a doc if it is a *contract*
   that must live here (like the perf doctrine).
5. **Archive, don't delete.** A superseded doc gets the `ARCHIVED/SUPERSEDED` marker + a
   `DOCS-AUDIT.json` entry, never silent removal.
6. **Run `check.py` after any change.** A dangling ref, duplicate role, or count mismatch = a failed gate.

---

## 4. THE ENVIRONMENT (the hard reality — respect it)

- **4-core / 8 GB total RAM / NO swap / 2 agents concurrent.** ~2.5 GiB available. Stream, never
  bulk-load a registry; one heavy job at a time; background long jobs (`setsid … &`); kill by PID.
- **Disk:** the `/mnt/HC_Volume_106427611` volume is **100% full** (snapshot cadence blocked). External
  sources → R2. Root fs `/` has ~17G free.
- **Postgres:** `patala-atlas` (port 5433) is the entity-truth layer when up; JSONL is the rebuildable
  export (`PATALA_REGISTRY_PG=0` falls back).
- **R2** is the byte truth; `rclone r2:` remote configured + verified.

---

## 5. THE OPERATING AXIOMS (the hard rules — see `AXIOMS.md` for the full list)

1. **Hermes for GENERATION, .py for REDUCTION.** Hermes reads files and derives; `.py` validates,
   aggregates, commits. Never hand-feed a validator; never fabricate both sides of a comparison.
2. **Eligibility is deterministic Python, never an LLM judgment.**
3. **Fail-closed, validate-first.** Wrong is worse than none; abstain rather than fabricate.
4. **THE ONE RULE** (the gate is done, not a file existing).
5. **RUNNING TESTS IS NOT WORK** — a green suite on unchanged code is noise; run a gate only when you
   changed something or a claim is in doubt.
6. **Compute on write, read from bytes** (ETag/304 + immutable; one question = one request).

---

## 6. THE GATE (before claiming anything here is "done")

```bash
python3 /root/projects/patalaorg/check.py --status   # resolves refs, rejects dup roles, reconciles counts
```

If a doc doesn't pass, it isn't done. **Banned words:** `PROVED · TRUTH · CORRECT · BEST · WINS`.
**Use:** `SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY`.

---

*The spine: patala PRODUCES → ip-graph VALIDATES + SERVES → Hermes is the execution kernel →
patalaorg documents + validates the contracts. Read STEP 1-5; run `check.py`; never present DESIGN as
BUILT.*
