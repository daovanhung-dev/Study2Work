---
task_id: "2026-10-11-create-study-api19-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #19

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Giữ DD ở Draft khi thiếu nguồn; phân biệt Order và Payment; bảo toàn các gap bằng `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Tách contract design khỏi runtime/schema; ghi nhận API #19 là consumer tiếp theo của flow thanh toán nếu API #17 thành công.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Dùng đủ tám sheet template, các ma trận data mapping, status `UNWIRED / NOT_FOUND`, không tự giải quyết discrepancy.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown API #19 `POST /api/v1/courses/{course_id}/enrollments` ở trạng thái `Draft — Needs Confirmation`, kèm reports và ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` là `APPROVED_DESIGN_CONTRACT`; API #19 là Bearer JWT / Student, trả `ApiEnvelope<Enrollment>` với 201 và các lỗi 401/403/404/422/409/500.
- AC-12 yêu cầu tạo Enrollment và khởi tạo Progress trong transaction; luồng gọi API #19 sau nhánh course miễn phí hoặc thanh toán thành công.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py`, route context và module/test inventory hiện không có API #19; DB design có `enrollments` và `lesson_progress`, nhưng chưa xác minh schema live.
- Runnable tests: Không có test API #19; không chạy runtime tests theo phạm vi docs-only.
- Runtime wiring: `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
Student -> API #19 contract / AC-12 -> logical anti-duplicate check
-> transaction: INSERT enrollments + initialize lesson_progress -> ApiEnvelope<Enrollment>
Current Study route/module/query/test -> NOT_FOUND / UNWIRED
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request identity | API row declares `user từ JWT:string!`; Enrollment uses `user_id:int64`; current Study token helper parses numeric `sub` into int | `DISCREPANCY` | Preserve contract wording; do not select a claim or conversion. |
| Duplicate enrollment | AC-12 requests anti-duplicate behavior; DB.sql has no unique `(user_id, course_id)` constraint | `SOURCE_REQUIRED` / `DISCREPANCY` | Concurrency guarantee and exact 409 condition remain unresolved. |
| Progress initialization | AC-12 says `INIT Progress` transaction; `lesson_progress` is keyed by user/lesson but lesson selection and row count are unspecified | `SOURCE_REQUIRED` | Do not assume all lessons or invent initialization values. |
| Nullability | DB_UNICA_TABLES says enrollment/progress FKs are required; DB.sql omits `NOT NULL` on those FKs | `DISCREPANCY` | Preserve both schema sources and their limits. |

## CHANGES

- Files changed: Created apps/study-server/docs/dd/19_courses_enrollments/ with 9 sheets/mappings and 3 reports; created apps/study-server/docs/dd/19_courses_enrollments.zip; completed this worklog.
- CONTEXT_UPDATES: None expected; this is a docs-only deliverable.
- Context pages changed: None.
- Assumptions: Draft treatment and documentation-only scope are approved; no route, catalog, diagram, DB or migration edits.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the three latest docs worklogs (#16–#18); no shortage. | VERIFIED |
| Source/contract/diagram/schema review | Compared API catalog, AC-12/index, Enrollment/Progress design tables and ERD, DB.sql, current auth/route/test context. | VERIFIED |
| Inline DD structural/content validator | 12 Markdown files; 9 ordered sheets/mappings; 3 valid JSON examples; 53 local links; tables, front matter, code fences, anchors, hashes and whitespace passed with zero errors. | VERIFIED |
| unzip -t apps/study-server/docs/dd/19_courses_enrollments.zip | Archive contains all 12 expected Markdown deliverables; no compressed-data errors. | VERIFIED |
| git diff --check | No whitespace errors in tracked diff; authored files also passed explicit trailing-whitespace scan. | VERIFIED |
| Study runtime tests | Not run; API #19 is unwired and task is docs-only. | NOT_RUN |
| Context validator | Not required; no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Contract owner decisions listed in `OPEN_QUESTIONS.md` are needed before this DD can become Ready/Final or guide runtime implementation.
- Next owner/action: Review the Draft and resolve open contract, concurrency, transaction and progress initialization questions.
