# translation — EXTENSION (how to extend + the roadmap + patterns to borrow)

*How to extend the translation layer, the NOT-IMPLEMENTED roadmap, and the concrete patterns to borrow
from the cloned agentic repos (`ip-graph/ecosystem/`: maestro, herdr-workflow, self-improving-agent, dgm,
graphiti). Each extension cites the real source pattern + how it applies here.*

---

## 1. PATTERNS TO BORROW (from the agentic clones — high signal)

### 1.1 Sealed council + adversarial review (herdr, adversarial-review, AgentReview)
**Source:** herdr's design-council — independent agents propose from a frozen brief; proposals are
**sealed** until all slots submit (prevents anchoring); cross-critique against a rubric; an editor
synthesizes; unanimity; escalate to `HUMAN_DECISION`. Reviewer evidence alone never closes a finding.
**Apply here:** T1/L2 production → a **translation council** (3 independent translations from the same
frozen verse + term packet) → sealed → cross-critique → adjudicate → the agreement is the hard core, the
divergence is the crux. This is the **three-version flow (R1/T2/R2)** made mechanical.
**Value:** the anti-cheat scholarship; "three independent translations cannot be wrong in the same way."

### 1.2 State as typed reducer core (herdr, maestro)
**Source:** workflow state advances by **deterministic reducers over committed events**; the LLM only
proposes artifacts. Lifecycle `PENDING→…→COMPLETED|FAILED→INVALIDATED`. "State is never inferred by
matching natural-language output."
**Apply here:** model each passage's translation as a typed state machine
(`SOURCE_LOCKED → DRAFT → REVIEWED → ANNOTATED → PUBLISHED`) advanced by reducers — the registry already
does versioned commits; make the transitions typed + gated.

### 1.3 Verifiable-reward self-improvement (dgm, Audited Skill-Graph)
**Source:** dgm evaluates each generation on a **deterministic harness**; patches that don't beat it are
dropped; fitness is empirical. "Unverifiable changes are discarded."
**Apply here:** a translation-quality loop — score output by **deterministic checks** (morphological
round-trip, term-consistency vs the glossary, alignment to source segments, agreement vs Dyczkowski gold);
a proposed improvement that doesn't beat the score is discarded; promotion requires the score + human
approval. **This is the live validation gate + self-improvement.**

### 1.4 Self-healing orchestration (Self-Healing Orchestrators paper; the factory's retry queue)
**Source:** map observable failure → failure class → targeted recovery under a budget → verify → trace.
Verifier-guided healing reduces silent failures to ~0%.
**Apply here:** the factory already has a retry queue; make it **failure-class-aware** (truncated-JSON vs
timeout vs validator-reject → different recovery) with an explicit budget, and **verify the recovered
trajectory** before commit.

### 1.5 Graph memory (graphiti, SAGE)
**Source:** raw episodes → extracted typed entities/facts → retrievable graph, with temporal validity;
a reader-writer loop that self-evolves from feedback.
**Apply here:** the term/context packet is the memory — make it a **typed graph** (lemma dossiers as
SAGE-style memory the translator reads + updates), with `valid_at/invalid_at` for semantic-shift.

---

## 2. NOT-IMPLEMENTED ROADMAP (exact gaps, in dependency order)

| # | Extension | Pattern | Gap to close |
|---|---|---|---|
| 1 | **Compile-on-commit** | compute-on-write | ✅ **DONE** — `compile-translation-status.py` + `PATALA_COMPILE_ON_COMMIT=1` |
| 2 | **Live validation gate (verifiable reward)** | dgm / TranslationProof | ✅ **DONE** — `pipeline/translation_gate.py`, env-gated in `factory_batch` (`PATALA_T1_GATE=1`), tested 6/6 |
| 3 | **Translation-content surface** | read plane | ✅ **DONE** — `GET /openpatala/translation/{work_id}/content` serves the committed T1/L2/L200/C1 reading (ETag/304 + immutable) |
| 4 | **Three-version flow (R1/T2/R2)** | sealed council (§1.1) | the anti-cheat translations → hard core + crux |
| 5 | **Typed state machine** | reducer core (§1.2) | per-passage typed lifecycle + gates |
| 6 | **Self-healing recovery** | §1.4 | failure-class-aware recovery with budget + verify |
| 7 | **Term-packet as graph memory** | §1.5 | lemma dossiers with temporal validity |

---

## 3. HOW TO ADD AN EXTENSION (the protocol)
1. Write the extension as a **new artifact in this layer** (a kernel + a gate + a skill entry-point).
2. Prove it with a **deterministic test** (mock + real where possible) — the verifiable reward.
3. Document it in `reference.md`/`model.md`/`agentic.md` + a new section here (move from NOT-IMPLEMENTED
   to WORKS).
4. Run `check.py` + the layer proofs. **A layer advances only when its 7 artifacts all hold** (README §0).

*This is the extension spec. Borrow the council, the typed-reducer core, the verifiable reward, the
self-healing recovery, and the graph memory — in that order of value. Each is a real pattern from the
cloned agentic repos, not invented here.*
