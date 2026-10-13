---
task_id: "2026-10-11-create-study-api25-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #25

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available: 38; selected: 3; status: READY`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách expected/current; giữ persistence thiếu bằng chứng ở `SOURCE_REQUIRED`; không biến design contract thành runtime.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Ghi discrepancy và nguồn còn thiếu; không tự chọn semantics nghiệp vụ/schema.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Dùng template 8 sheet; giữ `UNWIRED / NOT_FOUND`; Study DD output là Markdown-only.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo Draft API DD #25 `PATCH /api/v1/lessons/{lesson_id}/progress` với 8 template sheets, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md` và `VERIFICATION_REPORT.md`; không tạo ZIP.
- Canonical contract/approved plan: Student Bearer JWT; path `lesson_id:int64!`; body `position:int32!`, `percent:int32!`, `completed:boolean!`; response `ApiEnvelope<Lesson>`; HTTP/business codes 200/401/403/404/422/500. AC-14 mô tả update lesson progress + course aggregate và nhánh completed.
- Scope: Chỉ tạo DD Markdown và worklog; không sửa runtime, catalog, diagram, DDL, migration hoặc context page.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không đăng ký API #25; module inventory không có module API #25; `DB_UNICA_TABLES.md`/`DB.sql` có candidate `lesson_progress` nhưng không có cột `position` hoặc unique `(user_id, lesson_id)` declaration.
- Runnable tests: Test inventory không có focused test API #25; không chạy application tests trong docs-only scope.
- Runtime wiring: Source/module/query/test scan không tìm thấy API #25; trạng thái `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
Student -> API #25 catalog / AC-14
-> design-only progress update + course aggregate intent
-> candidate lesson_progress schema (position/unique key absent)
-> catalog ApiEnvelope<Lesson> response; payload assembly not defined
Current Study route/module/query/test -> NOT_FOUND / UNWIRED
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #25 runtime | Current router/module/test inventory omits endpoint | `UNWIRED` / `NOT_FOUND` | DD documents expected design only. |
| `position` persistence | Request has `position`; candidate ERD/DDL has no matching column | `SOURCE_REQUIRED` | Do not invent a column or unit. |
| Progress mutation | AC-14 gives completion branch; DDL has no unique user/lesson key or update policy | `SOURCE_REQUIRED` | No SQL/conflict target/state preservation is specified. |
| Course aggregate | Diagram says update aggregate but no source/target/formula is defined | `SOURCE_REQUIRED` | No aggregate calculation, table or transaction is invented. |
| Response | Catalog says `ApiEnvelope<Lesson>`; diagram says generic `ApiEnvelope` | `DISCREPANCY` | Preserve catalog response; payload assembly remains open. |
| Schema constraints | ERD calls user/lesson required; DDL columns are nullable and lack unique pair | `DISCREPANCY` / `DESIGN_ONLY` | Do not claim live schema or uniqueness. |

## CHANGES

- Files changed: Added `apps/study-server/docs/dd/25_lessons_progress/` (8 sheets + 3 reports) and this worklog.
- CONTEXT_UPDATES: None — no canonical context page/manifest changed.
- Context pages changed: None.
- Assumptions: Keep status `Draft — Needs Confirmation`; record missing mapping/rules as open questions; no ZIP; preserve all pre-existing worktree changes.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Docs worklog selector and review | Selected and read API #16–#18 docs worklogs; shortage none. | VERIFIED |
| Contract/AC/schema/runtime comparison | API #25 contract and AC-14 were compared with DB design/DDL and current router/module/test inventory; endpoint remains `UNWIRED / NOT_FOUND`. | VERIFIED |
| Inline static DD checker | 11 deliverables, 8 sheet metadata/order, Markdown tables/fences, three JSON examples, local links/anchors, catalog request/error-code set, four matrices and DB column coverage passed. | VERIFIED |
| `git diff --check` | No whitespace errors in tracked changes. | VERIFIED |
| Authored-file whitespace scan | No trailing whitespace in the 11 DD files and this worklog. | VERIFIED |
| Runtime source scan | No API #25/progress references found in Study Python app/tests. | UNWIRED / NOT_FOUND |
| Study Server application tests | Not run; documentation-only scope and API #25 is not wired. | NOT_RUN |
| Context validator | Not required; no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Q-25-01 through Q-25-08 in `OPEN_QUESTIONS.md` require authoritative decisions before DD can be marked Ready/Final.
- Next owner/action: Review and resolve open questions in canonical contract/schema sources before implementation.
