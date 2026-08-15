# RUN 7 — the scholar workbench (the human gate, made live)

*2026-08-15 · completed the endgame's third layer: the scholar login + review/adjudicate/publish
surface, wired to agent3's proven engines.*

## What was built
- `scripts/serve-scholar.py` (:8788) — the scholar workbench API:
  `login` · `queue` (review_queue.next_for) · `adjudicate` (the human gate) · `publish` (scholar_publication).
- `web/src/pages/scholar/workbench.astro` — the scholar login + review surface on the site.

## The full endgame, now all live
| Layer | Surface | Status |
|---|---|---|
| Public site | `/education /learning /bibliography /themes /scholars /scholar/workbench` | 6 pages, all 200 |
| Education API | :8787 `/education /resolve /answer` | 200 |
| Scholar workbench | :8788 `/login /queue /adjudicate /publish` | 200 |
| Audit trail | claim → source | RESOLVES TO SOURCE ✅ |

## The human gate
A scholar logs in → sees the prioritized review queue → adjudicates ACCEPT/REVISE/REJECT →
`scholar_publication` compiles the citable JSON-LD record → the public site serves it. This promotes
the organism's MACHINE_PROPOSED → ADJUDICATED, and the flywheel gets real adjudication data.

## Tests
- scholar_review 11/11 · review_queue 6/6 · review_policy 7/7 · scholar_publication 5/5 (agent3 engines)
- test-e2e 5/5 (audit trail) · run-tests 22/22
- site 11 pages built · all surfaces HTTP 200
