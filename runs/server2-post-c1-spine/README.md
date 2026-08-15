# RUN — SERVER2 POST-C1 SPINE (official, logged)

*2026-08-15 · the full C1→EDUCATION derivational spine validated end-to-end via the Hermes kanban
orchestrator, plus the server3 grounded-IPVV integration. Evidence: all gates below + the kanban
board + the registries.*

---

## The run

| Card | Layer | Status | Result |
|---|---|---|---|
| t_78b7e5d3 | THEME | ✅ done | theme committed (patala_ml.cluster, theme_validator) |
| t_152888dd | ARGUMENT | ✅ done | ENGINEERING_VALIDATED (kanban worker, model-derived) |
| t_f17e323e | SYNTHESIS | ✅ done | ENGINEERING_VALIDATED |
| t_3a309094 | ESSAY | ✅ done | ENGINEERING_VALIDATED (reactive docs, depends_on) |
| t_37a91061 | EDUCATION | ✅ done | ENGINEERING_VALIDATED |

## Registry (after the run + server3 integration)

```
C1:        42 (39 grounded IPVV + 3 kramasadbhava)
THEME:      1
ARGUMENT:   8 (5 grounded IPVV + 3 kramasadbhava)
SYNTHESIS:  3 (ENGINEERING_VALIDATED)
ESSAY:      3 (ENGINEERING_VALIDATED)
EDUCATION:  3 (ENGINEERING_VALIDATED)
```

## Gates (all real, recorded)

- **Chain gate** (`validate-scholarship-chain.py`): PASS — every POST-C1 object resolves to the C1 floor.
- **Cite contract** (`validate_cite_contract.py`): PASS — 22/22 premises carry a citation/evidence_quote.
- **Event tamper** (`validate-event-tamper.py`): 3/3 tamper types detected.
- **Signed attestation** (`validate-signed-attestation.py`): Ed25519 sign + verify + tamper-detect.
- **Grounded args** (`validate-ipvv-grounded-arg.py`): 3/3 premises fully cited (P2/P3 on real IPVV).

## Integration evidence

- 39 real IPVV C1s ingested as a grounded floor (fixes G1).
- 5 grounded arguments committed (from server3 `claim` engine — verbatim evidence_quote).
- openpatala-native entities emitted (PTPROP/PTARG/PTPASS) in `openpatala/emitted/entities.json`.
- `patalaorg check.py --status` PASS (after path compatibility map).

## What this proves

The production-grade spine (commentary→theme/argument→synthesis→essay→lesson) is **validated
end-to-end** — mechanically sound (all gates) and now **contentually grounded** via the real IPVV
floor (G1 addressed at the data level). See `server2/handover/` for full docs.
