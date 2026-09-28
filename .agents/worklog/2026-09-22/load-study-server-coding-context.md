---
task_id: "2026-09-22-load-study-server-coding-context"
date: "2026-09-22"
primary_task_type: "coding"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Nạp context Study Server và workflow coding

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-22/implement-study-api4-users-me.md`
    - carry_forward: Giữ JWT claims `sub`/`roles`, transaction ownership trong view, query parameterized và không expose secret; live DB chưa được xác minh.
  - path: `.agents/worklog/2026-09-20/implement-study-auth-login-refresh.md`
    - carry_forward: Giữ namespace `app.modules.guest`, shared validation boundary và không suy diễn runtime từ schema/migration chưa apply.
  - path: `.agents/worklog/2026-09-20/merge-mobile-flavors.md`
    - carry_forward: Bảo toàn thay đổi ngoài phạm vi và ghi rõ toolchain không runnable khi chưa có executable.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp context dự án `server-study` và workflow coding cho các task tiếp theo.
- Canonical contract/approved DD: Root router → `.agents/AGENTS.md` → `.agents/context-map.md` → worklog preflight → `.agents/server-study/AGENTS.md`/`INDEX.md` → page theo task → source/test.

## CURRENT_BEHAVIOR

- Source/config: Study Server là `SOURCE_BACKED`; current composition là `app/main.py` → `app/api/v1.py` → core dependencies/routes; register, auth login/refresh và users/me đang được wire trong source.
- Runnable tests: Test source hiện nằm dưới `apps/study-server/tests/`; chưa chạy pytest vì root `.venv/bin/pytest` không tồn tại trong môi trường này.
- Runtime wiring: Workflow `coding` được registry xác nhận `VERIFIED`; không có standalone coding skill file trong skill registry. Scope skill API hiện có là `createDD-markdown`, chỉ dùng cho API DD.

## SOURCE_TRACE

```text
active register_account/models.py
-> app.utils.validate.strip_email/reject_blank_password
-> register_account/view.py
-> register_account/query.py + core.database
-> users insert/transaction ownership
-> tests/modules/auth/test_register.py and current Study test suite
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Standalone `coding` skill | `.agents/skills/INDEX.md` lists only DD skills; `.agents/project/workflows.md` registers coding workflow | VERIFIED_WORKFLOW / NOT_FOUND_SKILL_FILE | Use workflow coding, not an invented skill resource |
| Node selector runtime | `node` executable is unavailable; Deno compatibility invocation succeeded | DECLARED_NOT_RUNNABLE / VERIFIED_SELECTOR | Use Deno selector and record it in future worklogs |
| Test context page vs current source | Some page text still describes stale register import, while current test source imports `app.modules.guest` | DISCREPANCY / CONTEXT_STALE | Prefer current source and runnable test evidence |
| Pytest command | `.venv/bin/pytest` is absent at repository root | DECLARED_NOT_RUNNABLE | Do not claim test collection or execution from this context load |

## CHANGES

- Files changed: Added this context-load worklog only; no application source or tests changed.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: “skill coding” means the registry-backed `coding` workflow because no standalone coding skill is registered.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected 3/9 coding worklogs; all 3 were read | VERIFIED |
| Read `.agents/context-map.md`, `.agents/context-manifest.json`, `.agents/server-study/{AGENTS,INDEX}.md` and relevant Study pages | Scope, workflow, module boundary and status loaded | VERIFIED |
| Read current register route/model/view/query/utility/test source | Current source trace loaded; no source edit | VERIFIED |
| `.venv/bin/pytest --collect-only -q apps/study-server/tests` | Executable not found | DECLARED_NOT_RUNNABLE |

## HANDOFF

- Remaining blockers: Pytest executable location/toolchain must be resolved before claiming runtime test verification; context pages contain at least one stale statement about register test collection.
- Next owner/action: For a coding task in Study Server, load the affected page from `.agents/server-study/`, trace current callers/callees/side effects, then run focused tests and the context validator when the toolchain is available.
