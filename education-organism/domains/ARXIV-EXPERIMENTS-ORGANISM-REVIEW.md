# ARXIV + EXPERIMENTS REVIEW — organism-related (2026-08-15)

*Review of the arxiv papers + experiments in fuck-off related to the organism/education/memory work I
just built into serveragent3. What's adapted, what's proven, what's missing.*

---

## 1. ARXIV PAPERS ADAPTED INTO KERNELS (real, validated — reuse, don't rebuild)

| arXiv | Paper | Kernel | What it gives |
|---|---|---|---|
| 2605.12061 | SAGE | `structure_recall.py` | self-evolving agentic graph-memory engine |
| 2505.22954 | Darwin Godel Machine | `open_ended_evolve.py` | open-ended evolution of self-improving agents |
| 2512.23760 | Audited Skill-Graph Self-Improvement | `skill_graph.py` | self-improvement under VERIFIABLE reward |
| 2606.01416 | Self-Healing Orchestrators | `self_healing.py` | diagnose-and-recover |
| 2502.14902 | PathRAG | `retrieval.py` | flow-pruned path retrieval |
| 2407.10805 | ToG-2 | `retrieval.py` | alternating text↔graph search |

**These are already built + validated.** My organism should reuse them, not re-derive.

## 2. EXPERIMENTS RELATED TO THE ORGANISM (36 total)

| Experiment | Status | Proves | My organism |
|---|---|---|---|
| `validate-education-organism.py` | 9/9 PASS | LearningClaims + misconception graph | ✅ integrated |
| `validate-organism-loop.py` | 8/8 PASS | consumer→research: probe→gap→intervention→proposal→human gate | ✅ integrated |
| `validate-pedagogy.py` | 7/7 PASS | MasteryEvidence→reducer→LearnerState | ✅ integrated |
| `validate-misconception.py` | 9/9 PASS | the repair cascade (flag→propagate→dissolve) | ✅ integrated |
| `experiment-bkt-mastery.py` | RUN | calibrated P(mastered) per learner per concept | ✅ pedagogy has BKT |
| `experiment-evolving-memory.py` | **PASS** | **dream-cycle consolidation → procedural memory** | ❌ **MISSING** |
| `experiment-self-improve.py` | PASS | PR-style safe self-improvement | the evolution loop |
| `validate-evolve.py` | RUN | MAP-Elites evolution loop (6 niches, gen2 improves) | the organism's growth |
| `experiment-signed-statement.py` | RUN | sign+verify+tamper-detect | the signing layer |
| `experiment-signed-corpus.py` | PASS | signed corpus root | Vision F |

## 3. THE KEY FINDING — what my organism is missing

**The procedural memory (evolving-memory dream-cycle consolidation).** The organism "improves across
sessions" by consolidating episodic agent traces:
```
traces → dream cycle (curator + compactor + connector) → topological memory graph that persists
```
- **verbose + low-access** nodes → compacted (preserve goal/outcome/constraints)
- **high-access** nodes → persist
- **related** traces → linked into a stable memory graph

Without it, my organism is a closed flywheel but **stateless across sessions** — it forgets what it
learned. This is the "durable memory the Verified Epistemic OS builds on."

**Also worth wiring:**
- `self_healing.py` (arxiv 2606.01416) — the organism recovers from failures (memory/JSON/timeout)
- `open_ended_evolve.py` / `validate-evolve.py` — the organism's growth loop (MAP-Elites niches)
- `skill_graph.py` — safe self-improvement under verifiable reward (the PR-not-mutation discipline)

## 4. RECOMMENDED NEXT

1. **Integrate the procedural memory** (evolving-memory dream-cycle) into serveragent3 as
   `kernels/memory.py` — so the organism persists + consolidates what it learns across sessions.
2. **Wire self-healing** (recover from failures under a budget) into the organism loop.
3. **Add the evolution loop** (MAP-Elites) as the organism's growth mechanism.
4. Test each + add to the suite (per AXIOMS: deterministic, on real data).

*This completes the organism: a closed flywheel (learners→misconception→repair→dissolve) + durable
procedural memory + self-healing + evolution.*
