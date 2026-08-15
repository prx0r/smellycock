# RUN 5 — the analog gems (GEM-A segment keying + GEM-C reconciliation)

*2026-08-15 · integrated the two highest-value analog steals into the organism pipeline.*

## GEM-A — segment-anchor provenance keying (from Bilara)
- `kernels/segment_key.py`: a stable `segmentId:field` address every layer anchors to.
- The whole chain (SOURCE..EDUCATION) anchors to one atomic segment (`kramasadbhava:v1`) with a
  distinct field per layer (`root`/`translation`/`commentary`/`lesson`/...).
- This is the provenance spine the audit resolver traverses.

## GEM-C — reconciliation gate (from Ambuda)
- `kernels/reconciliation.py`: proves an LLM-derived layer "preserved source while adding structure."
- Source-preserving derivation PASSes; source-dropping derivation BLOCKs (drift > threshold).
- The anti-theatre gate for the tutor/essay generation.

## Tests
- `run-tests.py`: **22/22** (incl. 5 new GEM tests)
- `test-gems-integration.py`: **5/5** (education claims anchor to segments; reconciliation wired)
- `check.py`: PASS
- Performance: 0.07s, ~22MB RSS
