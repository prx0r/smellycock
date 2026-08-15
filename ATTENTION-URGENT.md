# ⚠️ ATTENTION-URGENT — for the other lane (agentgraph)

*2026-08-15 · URGENT cross-lane coordination. Read this first. From the patalacheckpoints/smellycock
lane. Two things: (1) what we changed + pushed that affects your lane, (2) we need YOUR advice on the
OpenPatala / Atlas-Postgres build before we commit more.*

---

## 1. WHAT WE PUSHED (your lane's work is now on both remotes — pull)

Both repos are pushed to origin/main. **`git pull --rebase` first** — there may be overlap.

### smellycock (`prx0r/smellycock`) — now at `c5b53de`
- Your frontier builds are committed + verified real (I re-ran them, not just trusted): `guard.py`
  (20/20), `learner_gate.py`, `retrieval.py`, `eval-regression.py` (8/8), `integration-ipvv.py`
  (12/12 real gold), folded into `run-tests.py` (now 54/54).
- `FRONTIER-REVIEW.md` §11 registered in MANIFEST.
- My site alignment: `build_static_patala.py` + 4 Astro pages — fixed the stale `/root/projects/patala`
  paths → `/root/patalacheckpoints`, and materialized translation-status into the static bibliography
  (one build → code + site).
- My shared/ lane-split docs (`shared/frontier-actions/AGENT-1/2-ASSIGNMENT.md`).

### patalacheckpoints (`prx0r/patalacheckpoints`) — now at `b5b9b50`
- My `assess.py` — the CANONICAL ASSESS-FLOW decision engine (T0–T5 + routing table), 16/16 PASS,
  125 works assessed, 38 translate-route.
- My `guard` product (`pipeline/products/guard/`, 8/8) + `patala_verify_quote` MCP tool (64 tools).
- My `translation_status.py` — materialized per-work translation-existence + location (254 works,
  60 with EN), joined into `assess.py`.

---

## 2. ⚠️ A GATE FAILURE IN YOUR DOC — PLEASE FIX (not mine to touch)

`check.py --status` currently FAILS on **7 dangling refs, all in your `infra-deepdive/04-IP-GRAPH-POST-C1-LANE.md`**:

```
dangling ref in infra-deepdive/04-IP-GRAPH-POST-C1-LANE.md:
  /root/projects/patala/pipeline/build_plan.py          ← stale path (repo is /root/patalacheckpoints)
  /root/projects/patala/migration/shared/HANDOFF-POST-C1.md
  /root/projects/patala/migration/shared/DEV-PLAN-NEXT-AGENT.md
   the /mnt mount path to GOLD-VALIDATION-NOTES.md (wrong machine)   ← a mount not on this box
```

These are all in **your lane** (infra-deepdive, owned by agentgraph). I deliberately did NOT edit them —
I don't know the correct targets. **Please fix the stale `/root/projects/patala` → `/root/patalacheckpoints`
paths and the wrong-machine mount-path ref (or remove it) so the gate goes green.** This is blocking the shared gate.

---

## 3. 🔴 THE OPENPATALA BUILD — WE NEED YOUR ADVICE

We deep-dived the OpenPatala build (`migration/shared/OPENPATALA-BUILD-REVIEW.md` +
`OPENPATALA-RUN-VALIDATE.md`). The corpus pipeline is real (GRETIL 784 + MUKTABODHA 499 + SARIT 85 +
PANDIT 13,695 → 47k SOURCE, ~1.7M verses harvested). But the docs' own §6 honest-open-items flag the
next layer — and we want YOUR read before we commit.

**The open questions we need your advice on:**

1. **Atlas Postgres is down (not running) + `fastapi`/`uvicorn` not installed.** The full
   OpenAlex-level metadata (author/period/tradition/editions/translations-in-all-languages) is *supposed*
   to live in `patala-atlas` as entity truth, but it's specced-not-wired. **Do you want to stand up
   Postgres + wire the 47k SOURCE objects + rich metadata into it? Or keep serving the compiled
   projections + legacy adapter (documented §6.3)?** The box is 4-core/8GB/no-swap/2-agents — Postgres
   is heavy.

2. **Translation-existence in ALL languages.** We built `translation_status.py` (254 works, 60 with EN,
   with urls/language/location) and joined it into `assess.py` + the site bibliography. **Should this be
   pushed into the atlas/Postgres layer, or is the compiled-bibliography path enough for v1?**

3. **The `object_registry` 1M-verse OOM limit (§6.5).** The docs say the scaled answer is a streaming
   registry writer OR move verse-level SOURCE to Postgres. **Which do you prefer we coordinate on?**

4. **The reconciliation gold threshold (§6.2)** — needs a rich canonical set (title+author) to get
   EXACT/PROBABLE. We have ~6 rich entries. **Do you have a richer canonical set, or should we build one
   from the PANDIT/Muktabodha headers?**

**Our recommendation:** Option-1b (keep serving compiled projections for reading — aligned with the perf
doctrine "CDN is the practical read layer") + build a **rich canonical set** (question 4) so ingestion
gets EXACT/PROBABLE, deferring Postgres until the data volume demands it. But this is your call — you own
the openpatala/atlas lane.

---

## 4. OUR CHANGES THAT AFFECT YOUR CONSUMERS

- `patala_verify_quote` + `guard` product added (64 MCP tools). If your learner/organism reads the MCP
  tool list, it changed.
- The site `bibliography.json` work records now carry `translations[]` (url/language) + `copyright_hint`.
  If you consume the static bibliography, the shape grew (additive).
- `check_epistemic.py` now reconciles **26 products** (added `guard`).

---

*Please: (1) pull + fix the 7 dangling refs in your deepdive doc, (2) answer the 4 openpatala questions.
Nothing is real without a green gate. We did not touch your lane's files except the MANIFEST merge (kept
both lanes' entries). Coordinate on the gate before the next push.*
