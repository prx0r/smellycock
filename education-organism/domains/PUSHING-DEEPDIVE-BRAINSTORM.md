# BRAINSTORM — THE PUSHING / DEEP-DIVE ENGINE (feed essays from any text)

*2026-08-15. Deep-dive of the pushing specs (SPEC-33 PUSHING GUIDE, SPEC-34 AUTONOMOUS PUSHING,
SPEC-35 COMPARATIVE PUSHING, + the LOGICVID series SPEC-36..48). The goal: how to mechanically
deep-dive a text, mine its penetrations/arguments/cruxes, and feed future essays. This is the
"pushing type logic" the user asked about.*

---

## 1. WHAT PUSHING IS (the one-line)

> **Hound the text with "why," and force its OWN reasoning out. Frameworks supply only the
> questioning; the answers must come from the text.**

Pushing is a **graph-growth machine** — two loops compose:
```
SANSKRIT → claims → definitions → dependencies → proof-or-boundary → GRAPH     (decomposition)
graph tension → paradox → hidden premises → branches → research → NEW GRAPH   (question-growth)
```

## 2. THE METHOD (how to deep-dive a text)

### 2.1 The three passes (the anti-cheat)
- **Pass A — Construct:** produce the strongest coherent reconstruction from the quoted passages.
- **Pass B — Destroy:** a SEPARATE agent, FORBIDDEN from improving it, must only find unsupported
  entailments, conflated levels, translation dependence, hidden contradictions. (This is the
  automated penetration-mining engine.)
- **Pass C — Provenance audit:** every explicit claim has a passage; every derived claim lists
  premises; every cross-source claim preserves direction.

### 2.2 The round loop (the question-growth engine)
```
ROUND
  The question        (penetrating, not paraphrase — from the question-DNA)
  The text's answer   (restated EXACTLY as it argues — no strawman)
  > PENETRATION N     (the exact spot where the text asserts but does not prove)
  The next forced question
```
- Push to a natural endpoint, pivot to a new direction, STOP on repeats.

### 2.3 The question-DNA (why the question is the key)
1. Start from the text's own primitive (prakāśa, not "consciousness").
2. Interrogate every would-be-identical word (presence/manifestation/consciousness/experience ≠ same).
3. Find the quantifier/scope problem ("why manifest to me and not everyone?").
4. Push on the load-bearing step's WHY.
5. Expose the hidden premise.
6. Play the strongest opponent (the "relabelling" accusation).
7. Separate licensed from unlicensed (the dog: ontological yes, liberating no).
8. End with "the next forced question is…".
9. Produce branches.

## 3. THE OUTPUT — ARGUMENT TRUTH-PACKETS (the feed-to-essay object)

Treat a logical argument like a translation — an auditable, strength-graded object:
```
pt:argument:<work>:<slug> {
  work_id, title, kind (reductio|analogy|identity|entailment|decomposition),
  premises[{text, passage_ids}], inference, conclusion{text, passage_ids},
  tension_id, provenance (auditable path), proof?, status
}
```
**Claim strength (derived, never hand-waved):**
`PROVED → REVIEWED → WELL_SUPPORTED → PLAUSIBLE → SPECULATIVE`
An essay cites "the text's position (WELL_SUPPORTED, prem A,B,C)" vs "a possible reading
(SPECULATIVE)" — so the reader knows exactly how load-bearing each claim is.

## 4. THE COMPARATIVE MATRIX (the compounding asset)

Ask every text the **same** deep question-shapes (SPEC-35): the agnostic CORE
(MECHANISM-GAP/CRUX/SUBVERSION/QUANTIFIER/REGISTER/ROOT) + the Śaiva Q1–Q25 module organized by the
7-fold frame. Output: `question × text → answer (strength-graded, passage-anchored)`.
**The unanswered is data** — SILENT/OUT_OF_SCOPE maps each text's register. A "one-and-many"
comparative essay is *derived* from a matrix column, not re-researched.

## 5. THE PIPELINE (deep-dive → essay)

```
PUSHING enquiry (finds a tension, quotes the passages)
  → resolve passages (/api/resolve)
  → FORMAL LOGICAL ARGUMENT (truth-packet: premises/inference/conclusion + auditable path)
  → TRUTH ENGINE (nyāya/Lean: PROVED / OUTSIDE_FORMAL / HOLLOW)
  → ESSAY (cites the argument at its correct claim-strength)
  → LEARNING (from the essay)
  → back to PUSHING the next tension
```

## 6. WHAT MAKES THIS VISIONARY (from the spec deep-dive)

1. **Autonomous adversarial deep-dive** (SPEC-42): the double-pass loop run autonomously makes the
   LLM genuinely self-adversarial — penetration-mining at corpus scale without theatre.
2. **Independent-rediscovery-count as epistemology** (SPEC-36/45): score primitives by how many
   independent investigations converged on them; never create a node because it "sounds important."
3. **The merge-attempt Logicvid** (SPEC-36): when branches converge, run "are these the same
   primitive?" — it proves identity or splits into finer kinds (manufactures new theorems).
4. **The five-ontologies matrix with failure tags** (SPEC-48): a reusable comparative template.
5. **The T/R/C/H status key** (SPEC-44): T explicit-text / R reconstruction / C cross-disciplinary /
   H hypothesis — the epistemic envelope for the whole matrix.
6. **The inquiry-artifact + MCP ops as the feed contract** (SPEC-42): `create_inquiry →
   attach_source → extract_claims → reconstruct_argument → prosecute_argument → audit_provenance →
   generate_branches → compile_logicvid` — the deterministic glue between deep-dive and essays.

## 7. RECOMMENDED FIRST BUILD (production-grade, Hermes-driven)

Build the **autonomous pushing loop** as a Hermes skill + `.py` reducer:
1. `skills/pushing-deepdive/` — the Hermes skill that engineers the question-context, runs the round
   loop, and outputs truth-packets (GENERATION).
2. `.py` reducer: validates the truth-packets (every premise resolves, strength derived), commits to
   the argument registry (REDUCTION).
3. Feed the committed arguments into the ESSAY layer (they're the mined content).

*This turns the pushing specs into the actual deep-dive-to-essay engine.*
