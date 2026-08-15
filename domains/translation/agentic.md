# translation — AGENTIC (how an agent drives this layer)

*How an LLM/agent operates the translation layer: Hermes calling, the skills, the JSONL output contract,
safety, and tracking. This is the agent's operating page.*

---

## 1. The two rules that make it work
1. **Hermes for GENERATION, .py for REDUCTION.** Hermes reads files and derives; `.py` validates,
   aggregates, commits. Never hand-feed a validator; never fabricate both sides of a comparison.
2. **Eligibility is deterministic Python, never an LLM judgment.** The scheduler decides what's next.

## 2. How to call Hermes (correct, agentic)
```bash
hermes chat -Q -q "<system>\n\n<user>" --yolo --max-turns 6 \
  -m deepseek-v4-flash --provider opencode-go -p patala
```
- **Profile `patala`** loads the skills + MCP.
- **Hermes has full filebase access — pass FILE PATHS**, let Hermes read them itself (never stuff contents;
  that is the blind-`-z` mistake, ~3.8% yield).
- Wrapper: `pipeline/model.py` `chat_agentic` (used by the factory).

## 3. The JSONL output contract (why batches don't fail)
**Never ask Hermes to emit one giant `{"verses":[...]}` JSON — it truncates.**
1. Hermes READS the work's Sanskrit from a file path (whole file = its 1M context, loaded once).
2. Hermes emits **one JSONL record per verse per line** (no enclosing array).
3. Python commits every complete line; a truncated tail is dropped and only its verses retried.
4. A zero-recovery call **halves the chunk** and retries (adaptive convergence).

**Throughput:** batch the input (whole file's Sanskrit in context once), chunk the output (small JSONL
records). One call per verse is too slow; one 50-verse JSON is too fragile.

## 4. The skills (installed + enabled in the `patala` profile)
| Skill | What it tells Hermes |
|---|---|
| `canonical-translate` | the canonical T1 flow (read file → JSONL → adaptive chunk → gate) |
| `patala-translate` | the A3 loop (ledger → batch → validate → commit) |
| `raw-l0` | RAW→L0 (MODE_B): read companion guides BEFORE glossing; self-challenge |
| `translate-passage` | the three-version flow (T1→R1→T2→R2→T3→C1) + MEGA-CHUNK rule |
| `validate-passage` / `write-commentary` | the gates + C1 |

## 5. Safety (never break these)
- **MACHINE_PROPOSED ≠ ACCEPTED.** Machine output never self-promotes; promotion is a scoped human action.
- **Abstain, don't invent.** Empty gloss / `AMBIGUOUS` is correct; false-certainty is the failure metric.
- **Wrong is worse than none.** A validator gate is the definition of done, not "looks good".
- **One owner at a time** for the model API; **RAM is scarce** (stream, don't bulk-load).

## 6. Tracking (what to log)
Per-verse: `t1-stream.jsonl` · per-commit: `factory-audit.jsonl` · per-pass: `factory-loop.log` · served:
`translation.json` (now live via compile-on-commit). Idempotency: `factory_certificate.py` → 0 dup.

## 7. Driving the factory as an agent (the orchestration surface — clean + gated)
Instead of touching files, an agent drives translation through the deterministic brain:
```python
from patala_orchestration import progress_summary, work_state, next_action, eligible_next
s = eligible_next(10)          # the works an agent can legally advance, DERIVED from committed counts
                               #   (ranked by potential; not a stale ledger flag) — PROPOSE-only
w = work_state("kramasadbhava") # committed counts + next_action + blocked reason + source
na = next_action("ipvv")        # the deterministic next step (never an LLM judgment)
```
Or over MCP: `patala_next_action`, `patala_get_work_state`, `patala_get_translation_progress`.
**PROPOSE-only:** these verbs report what should happen; the factory + a human do the advancing. An agent
never accepts/promotes. Progress is live to all agents (compile-on-commit).

*This is the agent's operating page. Wire: `reference.md`. Semantics: `model.md`. How-to: `recipes.md`.*
