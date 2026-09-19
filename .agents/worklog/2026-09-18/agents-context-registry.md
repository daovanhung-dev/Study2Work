---
task_id: "2026-09-18-agents-context-registry"
date: "2026-09-18"
primary_task_type: "docs"
secondary_task_types: ["coding", "test"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: [".agents/context-manifest.json", "contracts/", "scripts/validate-agent-context.mjs"]
status: "VERIFIED"
---

# Worklog: Agent context, skill và workflow registry

## EXPECTED_BEHAVIOR

- Agent load order phải là root router → project context khi cần → scope/subcontext → exact source/contract/test.
- Skill, workflow, contract và worklog phải có registry entry, trigger/scope/status và verification rule.
- Expected behavior và current behavior phải được ghi riêng; conflict không được tự reconcile.

## CURRENT_BEHAVIOR

- Context cũ chỉ đăng ký scope/page; `.agents/skills/create_dd/` chưa được registry hóa.
- Study Web được gom trong Web scope nhưng chưa có Vue subcontext riêng.
- DB Admin có page graph chưa đầy đủ trong manifest.
- Context validator trước đây không kiểm tra skill/resource/workflow/contract/worklog registry.
- Study test collection bị stale import; `docs/BD` không tồn tại nên BD validator/DD generator bị block.

## SOURCE_TRACE

```text
AGENTS.md
-> .agents/AGENTS.md
-> context-manifest.json
-> project/scope/subcontext page graph
-> exact source + contract + test command
-> validator/worklog status
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study register tests | `apps/study-server/tests/modules/auth/test_register.py` imports removed `app.modules.auth.models/view` | `DECLARED_NOT_RUNNABLE` | Full Study pytest collection remains blocked |
| Root Basic Design | `docs/BD/` is absent | `NOT_FOUND` | `validate-bd.mjs` and DD generator cannot run |
| DD generator | `scripts/generate_v1_pilot_dd.py` references absent `.agent/` template path and `docs/BD` | `DECLARED_NOT_RUNNABLE` | Not enabled as active workflow |
| Work OpenAPI | legacy route-aligned file differs from target health contract | `DISCREPANCY` | Context retains both producer/status facts |
| Study → Work events | schemas exist, consumer wiring absent | `DECLARED_NOT_RUNNABLE` | No runtime event behavior inferred |
| DB Admin audit | SQL/bootstrap and durable audit path exist; live apply not verified | `VERIFIED_WITH_TARGET_DEPENDENCY` | Context separates checked-in bootstrap from live state |

## CHANGES

- Added manifest schema v3 registries for skills, workflows, contracts,
  worklog and Web subcontexts.
- Added Study Web Vue context and DB Admin architecture/API/security/database/test/workflow pages.
- Added shared workflow registry, worklog contract/template and this task entry.
- Corrected Study DD/business-code paths and DB Admin audit/control-plane facts.
- Updated `createDD-markdown` with repository expected/current precedence.
- Extended `validate-agent-context.mjs` for subcontexts, registries, resources,
  statuses, worklog fields, source paths and drift.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_OK` | `VERIFIED` |
| `deno run --allow-read --allow-env --allow-run scripts/validate-contracts.mjs` | Contract validation passed | `VERIFIED` |
| `apps/db-admin-server/.venv/bin/pytest -q` | 45 passed | `VERIFIED` |
| `PYTHONPATH=apps/study-server apps/study-server/.venv/bin/pytest --collect-only -q apps/study-server/tests` | 28 collected, stale register import error | `DECLARED_NOT_RUNNABLE` |
| `deno run ... scripts/validate-bd.mjs` | `docs/BD` missing | `DECLARED_NOT_RUNNABLE` |
| `python3 scripts/generate_v1_pilot_dd.py --validate-only` | `docs/BD/04_DAC_TA_API.md` missing | `DECLARED_NOT_RUNNABLE` |

## HANDOFF

- No business code, API, schema or runtime source was changed.
- Node/PNPM, Flutter and Dart are unavailable in the current shell; frontend/mobile commands remain unrun.
- Future context changes must update the affected manifest entry, page and this worklog format, then rerun the context validator.
