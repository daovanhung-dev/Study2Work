---
task_id: "2026-09-21-update-root-readme"
date: "2026-09-21"
primary_task_type: "docs"
secondary_task_types: ["test", "context-loading"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["root package/workspace scripts", "docker-compose.yml", "contracts/"]
status: "VERIFIED"
---

# Worklog: Cập nhật README tổng quan Study2Work

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-20/load-mobile-work-context.md`
    - carry_forward: Mobile hiện là một Flutter project với hai flavor; direct Neon/SQLite/Gemini boundary và Flutter/Dart runtime phải được ghi đúng trạng thái.
  - path: `.agents/worklog/2026-09-20/load-study-server-auth-login-context.md`
    - carry_forward: Tách EXPECTED_BEHAVIOR/CURRENT_BEHAVIOR; không suy diễn runtime từ DD hoặc tên file.
  - path: `.agents/worklog/2026-09-19/2026-09-19-create-mobile-dd.md`
    - carry_forward: Dùng source-backed behavior; đánh dấu NOT_FOUND/UNWIRED/DECLARED_NOT_RUNNABLE thay vì đoán.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Viết lại root `README.md` để mô tả toàn bộ deployable, công nghệ, kiến trúc, lệnh chạy/build/test, lệnh tổng hợp và địa chỉ sau build.
- Canonical contract/approved DD: Root router, `.agents/context-map.md`, `.agents/project/architecture.md`, scope context và current app manifests/configs; không dùng `docs/BD` vì directory hiện không tồn tại.

## CURRENT_BEHAVIOR

- Source/config: Có 8 deployable gồm Study Web/API, Work Web/API/Mobile, AI API và DB Admin Web/API; root package/workspace/compose/config files đang bị deletion chưa commit.
- Runnable tests: Node/corepack, Flutter/Dart và Docker không có trong PATH; `uv` và Deno có sẵn. Không claim runtime build/test pass.
- Runtime wiring: Work Web dùng relative `/api/v1` tới Work API; mobile direct Neon/SQLite/Gemini; AI gọi Ollama; DB Admin Web launcher khởi động DB Admin API riêng.

## SOURCE_TRACE

```text
root README -> app manifests/configs/readmes -> scope architecture/context -> ports/build commands -> links and status notes
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Root orchestration files | `git status` shows deletion of `package.json`, `pnpm-workspace.yaml`, `docker-compose.yml` and related root config | `CURRENT_WORKTREE_INCOMPLETE` | Document commands as intended baseline and warn that root/Compose commands require restoration |
| Study BD links | `docs/BD` is absent; `scripts/validate-bd.mjs` is not runnable against it | `NOT_FOUND` | Remove broken canonical-BD claims from README |
| Study Web Vite config | `apps/study-client/vite.config.ts` begins with malformed `Nêimport` token | `SOURCE_BLOCKER` | Do not claim Study Web build is verified |
| Study OpenAPI | `contracts/openapi/study/README.md` is placeholder only | `NOT_FOUND` | Describe Study Web/API boundary without inventing request/response fields |
| Work target OpenAPI | `contracts/openapi/work/openapi.json` contains target-only surface not mounted by current Express routes | `DISCREPANCY` | Link source-aligned legacy contract and explain target contract status |
| AI copied core/tests | copied core is unwired and no AI test suite is tracked | `UNWIRED` / `NOT_FOUND` | Describe only active chat path and Ollama dependency |
| Mobile backend boundary | Flutter calls Neon/SQLite/Gemini directly and does not consume Work HTTP API | `CURRENT_BEHAVIOR` | Document prototype boundary and security limitation |

## CHANGES

- Files changed: `README.md`, this worklog.
- CONTEXT_UPDATES: none; no runtime, API, schema or architecture change.
- Context pages changed: none.
- Assumptions: “Từng file” means all relevant tracked source/config/README/contract/context files; generated dependencies, caches and binary assets are excluded from README source claims.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | Passed before documentation edit | `VERIFIED` |
| `git diff --check` | Passed | `VERIFIED` |
| Markdown link check | 28 local README links resolved | `VERIFIED` |
| README structure/content check | Required sections, aggregate commands, mobile build command and address evidence found | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | `VERIFIED` |
| Root build/test commands | Node/corepack unavailable and root manifests are missing in working tree | `DECLARED_NOT_RUNNABLE` |

## HANDOFF

- Remaining blockers: Root orchestration files, Node/corepack, Flutter/Dart and Docker are unavailable in the current working tree/environment; Study Web has a malformed source token in `vite.config.ts`.
- Next owner/action: Review README source-backed command/address table and restore root orchestration files before running aggregate commands.
