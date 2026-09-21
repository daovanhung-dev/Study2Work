---
task_id: "2026-09-20-load-mobile-work-context"
date: "2026-09-20"
primary_task_type: "docs"
secondary_task_types: ["context-loading"]
project_scopes: ["mobile-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Nạp context mobile-work

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-20/load-study-server-auth-login-context.md`
    - carry_forward: Context phải tách EXPECTED_BEHAVIOR/CURRENT_BEHAVIOR; không suy diễn runtime từ tài liệu hoặc tên file.
  - path: `.agents/worklog/2026-09-19/2026-09-19-create-mobile-dd.md`
    - carry_forward: Mobile context source-backed; hai app Flutter độc lập; phải phân biệt WIRED/UNWIRED/PLACEHOLDER; Flutter/Dart không runnable trong shell.
  - path: `.agents/worklog/2026-09-19/2026-09-19-upgrade-agent-workflow-worklog.md`
    - carry_forward: Deno là compatibility runner khi Node không có; selector/worklog/validator là workflow bắt buộc.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Nạp context dự án `mobile-work` cho source root `apps/work-client/mobile/`.
- Canonical context: `.agents/mobile-work/AGENTS.md`, `INDEX.md`, architecture, dependencies, conventions, file inventory, hai app pages, data-flow, modules và workflows; `mobile-work` được registry đánh dấu `DEEP`/`SOURCE_BACKED`.

## CURRENT_BEHAVIOR

- Source/config: Có hai package độc lập `flutter_student/` và `flutter_business/`, đều giữ Dart package name `work_server`; current tracked inventory là 210 file, lần lượt 110 và 100.
- Runtime wiring: Cả hai khởi động từ `DangNhap`, dùng `MaterialPageRoute`; remote data đi trực tiếp qua `NeonDatabase` tới Neon PostgreSQL, session/cache qua SQLite; chat polling 3 giây; Gemini gọi trực tiếp từ client.
- Runnable tests: `flutter` và `dart` không có executable trong shell; đã đọc static test contracts `neon_test.dart` và `neon_connection_test.dart`; không claim runtime verification.

## SOURCE_TRACE

```text
mobile-work context
-> flutter_student/lib/main.dart / flutter_business/lib/main.dart
-> DangNhap -> controllers -> helper_db/neon_db.dart -> Neon PostgreSQL
-> SQLite account/major cache; AIService -> Gemini HTTP; chat Timer polling
-> neon_test.dart / neon_connection_test.dart
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Direct client data/AI credentials | `constants.dart` symbols are consumed by Neon/Gemini clients; values intentionally not copied to context | PROTOTYPE_SECURITY_BOUNDARY | Production should move access behind a least-privilege backend and rotate exposed credentials |
| Supabase naming | `helper_supabase.dart`/helper classes use `postgres` and `NeonDatabase`; no `supabase_flutter` dependency | COMPATIBILITY_NAMING | Do not describe current runtime as Supabase |
| Static/legacy/placeholder screens | App pages and inventory mark screens without route/import evidence accordingly | UNWIRED/LEGACY/PLACEHOLDER | Do not infer active behavior from file existence |
| Flutter/Dart runtime | `command -v flutter` and `command -v dart` return no executable | DECLARED_NOT_RUNNABLE | No analyze/test/device claim |
| Node runtime | `node` is absent; Deno 2.9.6 is available | DECLARED_NOT_RUNNABLE | Deno compatibility invocations used for selector/validator |

## CHANGES

- Files changed: `.agents/worklog/2026-09-20/load-mobile-work-context.md` only.
- CONTEXT_UPDATES: none; this is a context-loading handoff, not a source/context-page change.
- Context pages changed: none.
- Assumptions: User requested loading, not implementation; no feature-specific source deep dive beyond canonical mobile context and representative current entrypoints/tests.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected 3/17 matching docs worklogs; all 3 were read | VERIFIED |
| `git ls-files apps/work-client/mobile` count check | Business 100, Student 110, total 210 | VERIFIED |
| Read `.agents/context-map.md` and mobile-work page graph | Canonical route and all mobile pages loaded | VERIFIED |
| Read `pubspec.yaml`, `main.dart`, `neon_db.dart` and both test pairs | Current package/runtime/data-boundary/test contracts checked | VERIFIED |
| `flutter --version` / `dart --version` availability check | Both executables absent | DECLARED_NOT_RUNNABLE |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` reported in server-study, server-work, web-work and db-admin; no mobile drift reported | CONTEXT_STALE_OUT_OF_SCOPE |

## HANDOFF

- Remaining blockers: Flutter/Dart runtime verification unavailable; direct client Neon/Gemini access remains prototype-only; several static/legacy/unwired screens require exact app-page tracing before changes. Full validator still reports pre-existing drift outside `mobile-work`.
- Next owner/action: For a feature task, choose exactly `flutter_student` or `flutter_business`, then trace view -> controller -> helper/model -> Neon/SQLite/external call -> tests and update the mobile worklog.
