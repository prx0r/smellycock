# shared/ — the seam between the two lanes

*Read this FIRST if you are either lane. This folder is the single coordination point: who owns what,
the shared gates, and the frontier-action plan. No lane builds the other's scope; both lanes keep the
shared gates green.*

| File | What |
|---|---|
| `frontier-actions/SHARED-PLAN.md` | **the plan**: Agent A = surface guards (FoJin port), Agent B = learning kernels + measured-learning eval, with checkpoints + gates |
| `AGENTS-SPLIT.md` | the lane ownership map (who builds what) — see below |

## The lane ownership (from HANDOVER-DEVPLAN v2 + FRONTIER-REVIEW)

| Lane | Repo | Owns | Do NOT build |
|---|---|---|---|
| **Agent A** (scholar + serving) | `patalacheckpoints/pipeline/products/` (the `scholar_*`, `review_*`, `manuscript_*`, `collation` engines) + MCP + UI | the surface guards (`guard.py` from FoJin), `verify_quote` MCP, answer-quality regression | the learning kernels / eval |
| **Agent B** (organism + flywheel) | `smellycock/education-organism/kernels/` + `pipeline/products/education_organism/` | pyBKT mastery, RKA weighted propagation, DML replay, dream-cycle, the learner-mastery eval | the surface guards / scholar engines |

## The shared gates (both lanes)

```bash
cd /root/smellycock
python3 check.py --status            # refs resolve
python3 check_epistemic.py           # products reconcile
cd education-organism
python3 scripts/run-tests.py         # 22/22
python3 scripts/test-e2e.py          # 5/5
python3 scripts/audit-resolve.py     # claim → source
```

**Banned words:** PROVED · TRUTH · CORRECT · BEST · WINS. **Use:** SUPPORTED BY · PASSED CHECK X ·
MACHINE-PROPOSED · REVIEWED BY.
