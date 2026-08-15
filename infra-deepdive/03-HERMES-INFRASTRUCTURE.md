# INFRA DEEP-DIVE 03 — THE HERMES INFRASTRUCTURE

*2026-08-15 · a full-context audit of the Hermes agent install and configuration on this machine. How to
actually use Hermes properly: the binary, config, the active `patala` profile, kanban, skills, MCP, docs,
and sessions. The single most important operational fact: **Hermes can read the whole filebase itself —
pass file PATHS, not contents.***

---

## 1. INSTALL + BINARY
- **Binary:** `/usr/local/bin/hermes` (pinned to the pip venv at
  `/usr/local/lib/hermes-agent/venv/lib/python3.11/site-packages`).
- **Version:** `Hermes Agent v0.18.2 (2026.7.7.2)`, Python 3.11.2, OpenAI SDK 2.24.0.
- **Config home:** `~/.hermes` (there is NO `~/.config/hermes/`).
- **Top-level subcommands:** `chat, model, moa, fallback, secrets, migrate, gateway, proxy, lsp, setup,
  postinstall, whatsapp, whatsapp-cloud, slack, send, login, logout, auth, status, cron, webhook, portal,
  kanban, project, hooks, doctor, security, dump, debug, backup, checkpoints, import, config, console,
  pairing, skills, bundles, plugins, curator, pets, journey, learning, memory-graph, memory, tools,
  computer-use, mcp, sessions, insights, claw, version, update, uninstall, acp, profile, completion,
  dashboard, serve, desktop, gui, logs, prompt-size`.
- **No dedicated `goals` or `delegate` subcommand** — goals = the `/goal` slash command (Ralph loop);
  delegation = the `delegate_task` tool.

## 2. CONFIG (`~/.hermes/config.yaml`, 22 lines)
```yaml
model: deepseek-v4-flash
provider: opencode-go
kanban:
  auto_decompose: true
  auto_decompose_per_tick: 3
  orchestrator_profile: patala
  default_assignee: patala
  auto_subscribe_on_create: true
delegation:
  max_iterations: 50
  max_concurrent_children: 3
  model: deepseek-v4-flash
  provider: opencode-go
  worktree_isolation: false
goals:
  max_turns: 20
```
- **Provider/model everywhere:** `opencode-go` / `deepseek-v4-flash`. Resolves via `OPENCODE_GO_API_KEY` →
  base URL `https://opencode.ai/zen/go/v1`.
- **⚠️ RATE-LIMIT (critical):** `~/.hermes/profiles/patala/auth.json` shows the opencode-go credential
  `last_status: 'exhausted'`, error `429 GoUsageLimitError` — *"Weekly usage limit reached. Resets in 2
  days."* `last_error_reset_at: 1786924800` (~Aug 15-16 2026). **Expect Hermes model calls to fail until
  reset.** MEMORY.md notes: if `hermes -z` returns "Model not supported", pass `-m deepseek-v4-flash` or set `HERMES_MODEL`.
- **No MCP servers registered** (`hermes mcp list` → "No MCP servers configured."). See §6.

## 3. THE `patala` PROFILE (the ACTIVE profile)
- **Active:** `cat ~/.hermes/active_profile` → `patala`. Location `~/.hermes/profiles/patala/` (isolated
  state: own config, sessions, skills, state.db, auth.json, gateway).
- **`config.yaml` (profile):** pins `model: deepseek-v4-flash`, `provider: opencode-go`.
- **`profile.yaml`:** `description: 'ip-graph (agentgraph) frontier agent: builds + proves epistemic-graph
  kernels, derives enquiry/essay/translation structure from real sources via deepseek-v4-flash, wires
  clones into lib/, reconciles the record, drives the read plane + organism.'`
- **`SOUL.md`:** default Nous Hermes boilerplate (generic — the real doctrine is in `MEMORY.md`).
- **`MEMORY.md`:** the Pāṭala operator doctrine — THE ONE RULE, operating axioms (never `sleep`-wait, use
  `nohup`, kill by PID, external sources → R2, reuse not rebuild, respect CC BY-NC-SA), navigation order
  (SPINE.md → docs/process/README.md), the A0–A7 agent model, and **"Hermes task DONE ≠ Pāṭala object ACCEPTED."**
- **`profile list`:** two profiles — `default` (gateway stopped) and `◆patala` (gateway **running**, alias `patala`).
- **`project list`:** one project — `patala`, anchored to `[1 folder]` = `/root/projects/patala`.

### patala profile skills on disk
`~/.hermes/profiles/patala/skills/` — 12 direct skill dirs:
`assemble-stack, canonical-translate, extract-argmap, patala-translate, push-text, raw-l0,
translate-passage, translate-reading, translate-work, use-api, validate-passage, write-commentary`
PLUS the `autonomous-layer/` bundle (`patala-autonomous-layer-skills`, v1.1.0) with 9 skills:
`patala-{autonomy-controller,l0,l1,l2,l200,c1,theme,essay,education}` + `AUTONOMY_CONTRACT.md`,
`LAYER_MATRIX.md`, `README.md`.

## 4. KANBAN — current state
**Kanban verbs:** `init, boards, create, swarm, list, show, assign, reclaim, reassign, diagnostics, link,
unlink, claim, comment, complete, edit, block, schedule, unblock, promote, archive, tail, dispatch,
daemon, watch, stats, notify-*, log, runs, heartbeat, assignees, context, specify, decompose, gc`.

**Three boards:**
| Board | State |
|---|---|
| `default` | empty |
| `ip-graph` | blocked=3, done=3, ready=3, todo=2 |
| `translation` (● current) | **ready=6** |

**Current board = `translation`** (`~/.hermes/kanban/current`). Its 6 ready, all unassigned:
```
t_b5ebdcac  ready  BUILD_L0: kramasadbhava
t_c7f7c024  ready  BUILD_L0: tantraloka
t_9207607c  ready  BUILD_L2: ipvv
t_a94fd44c  ready  BUILD_ARGMAP: cidgagana
t_ffd53ab1  ready  BUILD_ARGMAP: brahmayamala
t_e932554e  ready  BUILD_ARGMAP: malinivijayottara
```
`hermes kanban stats` on translation: ready 6, running 0, done 0. **No running worker** — the dispatcher
(gateway PID 983, `... -m hermes_cli.main gateway run`) has not spawned workers, consistent with the provider rate-limit.

**Usage notes:** use `--board <slug>` BEFORE the subcommand (e.g. `hermes kanban --board ip-graph list`).
Workers drive the board via the **tools** (`kanban_show, kanban_list, kanban_complete, kanban_block,
kanban_heartbeat, kanban_comment, kanban_create, kanban_link, kanban_unblock`), not the CLI.

## 5. SKILLS — full list (22, all enabled)
```
assemble-stack, canonical-translate, extract-argmap, patala-translate, push-text, raw-l0, translate-passage,
translate-reading, translate-work, use-api, validate-passage, write-commentary,
+ Pāṭala Autonomous Layer Auditor, Controller, C1 Producer, Education Projection Producer, Essay Producer,
  L0 Producer, L1 Producer, L2 Producer, L200 Producer, Theme Synthesis Producer
```
**SKILL.md paths** all under `~/.hermes/profiles/patala/skills/` (listed in 02-PATALA-PIPELINE §3 for the
translation skills). Skill `.hub` metadata at `.../skills/.hub/`. The skill-load snapshot:
`~/.hermes/profiles/patala/.skills_prompt_snapshot.json` (22 skills with conditions).

## 6. MCP — the patala verbs (⚠️ NOT registered in Hermes)
**`hermes mcp list` → "No MCP servers configured."** The four verbs exist only in a **standalone MCP stdio
server**, NOT in Hermes' config:
- **Server:** `/root/projects/patala/mcp/index.mjs` (516 lines, name `patala`, v0.1.0; package.json name
  `patala-mcp`, `npm start` → `node index.mjs`). Transport: `StdioServerTransport`. Proxies the Pāṭala site
  HTTP API (`TANTRA_API_BASE` default `http://localhost:3000`) + the Atlas API (`ATLAS_API_BASE` default `http://localhost:8787`).
- **The four verbs** (468-513): `patala_next_action`, `patala_get_work_state`,
  `patala_get_translation_progress`, `patala_get_ops_status` — all call
  `pipeline/patala_orchestration.py` under `cwd=/root/projects/patala`, PROPOSE-only. Plus
  `get_translation_status`/`get_translation_status_for_work` hit Atlas.
- **NOT wired into Hermes or opencode:** neither `~/.hermes/config.yaml` nor any `opencode.json` registers
  this server. **To use it:** register it in your MCP client config as
  `node /root/projects/patala/mcp/index.mjs`, OR call
  `python3 /root/projects/patala/pipeline/patala_orchestration.py {--next,--state,--summary,--limit}` directly.
- The old `tantrakosa` MCP (planned in PATALA-SETUP.md) was reworked into this `patala`/`index.mjs` tool set.

## 7. DOCS (where to read the real usage)
- **Pāṭala-specific:** `/mnt/HC_Volume_106427611/ip-graph/handover/hermes/` → `CANONICAL.md`,
  `HERMES-CALLING.md`, `PATALA-SETUP.md`, `DEV-PLAN.md`, `AUTOTRANSLATE-NORTHSTAR.md`,
  `TRANSLATION-APPROACH-AND-VALIDATION.md`, `README-PATALA.md`, `PEER-REVIEW.md`,
  `hermespatala-architecture-review.md`.
- **Official Hermes docs:** `/usr/local/lib/hermes-agent/website/docs/user-guide/features/{kanban,goals,delegation}.md`,
  `kanban-tutorial.md`, `kanban-worker-lanes.md`, `/usr/local/lib/hermes-agent/docs/kanban/multi-gateway.md`,
  `/usr/local/lib/hermes-agent/website/docs/user-guide/guides/delegation-patterns.md`.

## 8. HOW TO ACTUALLY CALL HERMES (the correct way)
From `HERMES-CALLING.md` — **do NOT use blind `hermes -z` for real work** (no file tools → ~3.8% yield). Use:
```bash
hermes profile use patala
hermes project use patala
hermes chat -Q -q "<system>\n<user>" --skills <skill> --yolo --max-turns 8 -m deepseek-v4-flash --provider opencode-go
```
- **Pass FILE PATHS, not contents** — Hermes can read the whole filebase itself (it has read+edit access to
  `/root/projects/patala` + `/mnt/HC_Volume_106427611/ip-graph`). Stuffing contents into the prompt hides
  context + risks ARG_MAX blowup.
- **`-Q`** quiet (parseable) · **`--yolo`** no prompts · **`-p patala`** loads the profile's skills + config.

## 9. SESSIONS / PERSISTENCE
- **Store:** per-profile SQLite `~/.hermes/profiles/patala/state.db` (`SessionDB`) + WAL files. Legacy
  `~/.hermes/profiles/patala/sessions/` has **1,951 `request_dump_*.json`** (from a batch run 2026-08-13).
- **Manage:** `hermes sessions list | export | delete | prune | archive | optimize | repair | stats | rename | browse`.
- **Resume flags (top-level AND `hermes chat`):** `--resume <SESSION_ID>` / `-r`; `--continue [NAME]` / `-c`
  (resume by name or most recent); `--checkpoints` enables filesystem checkpoints with `/rollback`.
- **`hermes chat -Q -q`** = quiet programmatic single-query mode (used by the translation pipeline).

## 10. KEY FACTS A NEXT AGENT MUST KNOW
1. **Binary:** `/usr/local/bin/hermes`, v0.18.2; home `~/.hermes`; active profile `patala`.
2. **Model:** `deepseek-v4-flash` / `opencode-go` everywhere. ⚠️ **The opencode-go credential is
   rate-limited/exhausted (429 weekly limit, resets ~Aug 15-16)** — expect model calls to fail until reset.
3. **Gateway is running** (PID 983) — the kanban dispatcher is live, but the `translation` board has 6
   ready tasks with no running workers (consistent with the rate-limit).
4. **MCP:** the patala MCP is a standalone stdio server, NOT registered. Use the direct
   `patala_orchestration.py` calls or register `node /root/projects/patala/mcp/index.mjs`.
5. **Correct invocation:** `hermes chat -Q -q "<ask>" --skills <skill> --yolo --max-turns 8` under `patala` — not `hermes -z`.
6. **Docs:** `/usr/local/lib/hermes-agent/website/docs/user-guide/features/{kanban,goals,delegation}.md` +
   `HERMES-CALLING.md`, `PATALA-SETUP.md`, `CANONICAL.md` (in `/mnt/HC_Volume_106427611/ip-graph/handover/hermes`).
7. **Hermes task DONE ≠ Pāṭala object ACCEPTED** — the deterministic gate decides what's real.
