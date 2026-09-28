---
task_id: "2026-09-22-load-project-context"
date: "2026-09-22"
primary_task_type: "docs"
secondary_task_types: ["context-loading"]
project_scopes: []
cross_scope_dependencies: ["all-scope registry and boundary contracts"]
status: "VERIFIED"
---

# Worklog: Nạp context dự án Study2Work

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-21/update-root-readme.md`
    - carry_forward: Root orchestration files đang bị deletion trong working tree; Node/corepack, Flutter/Dart và Docker chưa runnable; Work OpenAPI và Study OpenAPI có discrepancy/not-found cần giữ nguyên trạng thái.
  - path: `.agents/worklog/2026-09-20/load-mobile-work-context.md`
    - carry_forward: Mobile gồm hai Flutter app, direct Neon/SQLite/Gemini boundary; không suy diễn runtime từ file legacy/unwired; Deno là compatibility runner khi Node vắng.
  - path: `.agents/worklog/2026-09-20/load-study-server-auth-login-context.md`
    - carry_forward: Tách EXPECTED_BEHAVIOR/CURRENT_BEHAVIOR; Study auth login DD chưa wired và không được coi DD là runtime proof.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp global project context của Study2Work để làm nền cho task tiếp theo.
- Canonical contract/approved DD: Root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/context-manifest.json`, `.agents/project/*`, và worklog contract.

## CURRENT_BEHAVIOR

- Source/config: Registry, ownership, boundary, contract, workflow và trạng thái source hiện tại đã được đọc.
- Runnable tests: Đây là task read-only; Node và `rg` không có trong PATH, Deno dùng được cho selector/validator; contract validator bị thiếu dependency `ajv`.
- Runtime wiring: Chỉ nạp context/read-only; chưa thay đổi runtime hay business code.

## SOURCE_TRACE

```text
AGENTS.md -> .agents/AGENTS.md -> context-map/manifest -> project pages -> scope registry/contracts -> current worktree status
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Working tree | `git status --short --branch` có deletion/modification/untracked trước task | CURRENT_WORKTREE_DIRTY | Không được ghi đè hoặc suy diễn các thay đổi hiện hữu |
| Node/rg availability | `node` và `rg` không có trong PATH | DECLARED_NOT_RUNNABLE | Dùng Deno/`find`/`sed` cho workflow đọc và validation phù hợp |
| Context drift | Full validator báo `CONTEXT_STALE` ở Study Server, Work Server, Web Work, Mobile Work và DB Admin | CONTEXT_STALE | Task tiếp theo phải ưu tiên current source; không chỉ đổi snapshot commit |
| Contract validator | `scripts/validate-contracts.mjs` không import được `ajv/dist/2020.js` | DECLARED_NOT_RUNNABLE | Chưa kết luận contract pass/fail từ validator này |

## CHANGES

- Files changed: Chỉ thêm worklog này; không sửa source/runtime.
- CONTEXT_UPDATES: Không có; chỉ nạp context đã đăng ký.
- Context pages changed: Chưa có.
- Assumptions: “Nạp context dự án” là global context handoff, chưa chọn scope feature cụ thể và không author implementation.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn 3/19 worklog cùng type và đã đọc đủ | VERIFIED |
| Đọc `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/context-manifest.json` | Registry/page graph/boundary đã nạp | VERIFIED |
| Đọc `.agents/project/{INDEX,architecture,source-status,conventions,dependencies,contracts,workflows,design,business-code,database}.md` | Global project context đã nạp | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Báo `CONTEXT_STALE` ở nhiều deep scope | CONTEXT_STALE |
| `deno run --allow-read --allow-run --allow-env scripts/validate-contracts.mjs` | Thiếu import `ajv/dist/2020.js` | DECLARED_NOT_RUNNABLE |

## HANDOFF

- Remaining blockers: Contract validator cần dependency `ajv`; full context validator còn báo drift đã đăng ký ở các scope. Working tree có thay đổi sẵn có.
- Next owner/action: Khi nhận task cụ thể, chọn đúng scope entry và đọc current source/test trước khi sửa; giữ các status `DISCREPANCY`, `UNWIRED`, `NOT_FOUND`, `DECLARED_NOT_RUNNABLE`.
