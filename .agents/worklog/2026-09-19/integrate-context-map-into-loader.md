---
task_id: "2026-09-19-integrate-context-map-into-loader"
date: "2026-09-19"
primary_task_type: "docs"
secondary_task_types: ["context-maintenance", "test"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["AGENTS.md", ".agents/AGENTS.md", ".agents/context-map.md", ".agents/context-manifest.json", "scripts/validate-agent-context.mjs"]
status: "PARTIAL"
---

# Worklog: Tích hợp context-map vào logic context agent

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-19/2026-09-19-upgrade-agent-workflow-worklog.md`
    - carry_forward: Context governance phải liên kết router, manifest, workflow, worklog và validator.
  - path: `.agents/worklog/2026-09-19/create-agent-context-map.md`
    - carry_forward: Manifest là machine source of truth; map phải được validator kiểm tra coverage và links.
  - path: `.agents/worklog/2026-09-19/mobile-agent-context-inventory.md`
    - carry_forward: Context map không được thay thế source evidence hoặc suy diễn runtime từ file name.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Sau `.agents/AGENTS.md`, agent phải đọc `.agents/context-map.md` trước khi
  chọn scope/subcontext và đọc source sâu.
- Project load order, workflow registry và map phải biểu diễn cùng một thứ tự.
- Validator phải fail nếu root router hoặc global registry bỏ qua context map.

## CURRENT_BEHAVIOR

- `context-map.md` đã được đăng ký trong manifest và được kiểm tra coverage/link,
  nhưng root load flow chưa coi nó là bước bắt buộc.
- `.agents/AGENTS.md` đã mô tả map nhưng chưa yêu cầu đọc trước scope selection.

## SOURCE_TRACE

```text
AGENTS.md
-> .agents/AGENTS.md
-> .agents/context-map.md
-> primary_task_type + worklog preflight
-> project/INDEX.md when cross-scope
-> scope AGENTS/INDEX
-> exact source/contract/test
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Root load order | `AGENTS.md` skipped `context-map.md` between registry and task routing | RESOLVED | Map is now mandatory in canonical flow |
| Project load order | `project/INDEX.md` did not include the map | RESOLVED | Cross-scope routing now exposes the map |
| Validator wiring | Map coverage existed but root/registry reference was not guarded | RESOLVED | Validator checks both references |
| Application source drift | Existing Study/Work/Web/DB Admin source differs from manifest snapshot | CONTEXT_STALE | Unchanged and outside this context-only task |

## CHANGES

- Files changed: `AGENTS.md`, `.agents/AGENTS.md`,
  `.agents/project/INDEX.md`, `.agents/project/workflows.md`,
  `.agents/context-map.md`, `scripts/validate-agent-context.mjs` and this worklog.
- CONTEXT_UPDATES: Added context-map to mandatory load order and validator guard.
- Context pages changed: root/global/project context governance only.
- Assumptions: context-map remains human-readable documentation while the manifest remains machine-readable source of truth.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `python3 -m json.tool .agents/context-manifest.json` | Manifest parsed successfully | VERIFIED |
| `deno check scripts/validate-agent-context.mjs scripts/select-worklogs.mjs` | Passed | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Only existing source `CONTEXT_STALE` results remain | CONTEXT_STALE |
| `git diff --check` | Passed | VERIFIED |

## HANDOFF

- Remaining blockers: Existing source snapshot drift remains unresolved by design.
- Next owner/action: When the context load order changes again, update
  `AGENTS.md`, `.agents/context-map.md`, project workflow/index and validator
  guard together.
