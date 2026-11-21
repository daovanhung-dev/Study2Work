---
task_id: "2026-10-12-create-study-api27-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #27 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: DD Study #16–#26 là tài liệu design; giữ nguyên artifacts cũ và không suy ra runtime từ DD.
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách contract thiết kế khỏi current source; ghi `SOURCE_REQUIRED`/`DISCREPANCY`, không lấp gap bằng schema suy đoán.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Ghi riêng expected/current behavior; API chưa wire phải giữ `UNWIRED`/`NOT_FOUND`; không invent provider, persistence hoặc status rules.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design draft cho API #27 `GET /api/v1/lessons/{lesson_id}/next` theo template Markdown của dự án, kèm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` và worklog.
- Canonical contract/approved DD: `docs/lists/list_api.md` đánh dấu catalog là `APPROVED_DESIGN_CONTRACT`; API #27 yêu cầu Student Bearer JWT, path `lesson_id:int64!`, `ApiEnvelope<Lesson>`, HTTP 200/401/403/404/500 với business code tương ứng. AC-15 ghi mục tiêu điều hướng bài tiếp theo.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` không đăng ký route API #27; source scan không tìm thấy module/query API #27. `lessons` chỉ xuất hiện trong query hiện tại của API #12 ở source scan.
- Runnable tests: Không tìm thấy test API #27 trong `apps/study-server/tests/`; runtime tests không chạy vì task chỉ tạo DD.
- Runtime wiring: Study runtime context xác nhận các route hiện wire không bao gồm API #27; runtime status `UNWIRED / NOT_FOUND`.

## SOURCE_TRACE

```text
User requirement -> approved design contract API #27 -> AC-15 lesson-content flow -> candidate lessons schema/order evidence -> current Study router/module/test scan (API #27 absent) -> documentation-only DD draft
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #27 runtime | Current `v1.py`, modules and tests do not contain API #27. | `UNWIRED / NOT_FOUND` | DD documents expected design only. |
| Next-lesson selection | AC-15 says “Đọc thứ tự curriculum”; no predicate, visibility filter, tie-break or terminal behavior is defined. | `SOURCE_REQUIRED` | Keep query semantics and terminal response open. |
| Student entitlement | Catalog requires Student Bearer and AC-15 says user has lesson access, but identity/access/publish predicate is absent. | `SOURCE_REQUIRED` | Do not invent authorization SQL or 403/404 masking. |
| Lesson schema evidence | `DB_UNICA_TABLES.md`/ERD are design evidence; checked-in DDL allows nullable `lessons.course_id`, unlike required logical `Lesson.course_id`. Live schema is unverified. | `DISCREPANCY / DESIGN_ONLY` | Mark candidate mappings and nullability conflict. |

## CHANGES

- Files changed: Created eight template sheets, PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md under `apps/study-server/docs/dd/27_lessons_next/`; this worklog. No runtime or canonical design inputs changed.
- CONTEXT_UPDATES: None; no runtime or canonical source contract changes.
- Context pages changed: None.
- Assumptions: Follow the user's selected `Draft + open questions` policy; no ZIP per `.agents/server-study/workflows/README.md`; do not decide missing business rules.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the three docs worklogs listed above. | VERIFIED |
| Source review | Read API contract, AC-15 activity/index, lesson DB design/DDL, adjacent DDs, and current route/module/test inventory. | VERIFIED |
| DD structural/content validation | 8 sheets/order/front matter passed; 2 JSON examples parsed; 36 Markdown tables and 35 internal/source links passed; response codes match the API #27 catalog row. | VERIFIED |
| Runtime tests | Not run; documentation-only task and API #27 is not wired. | NOT_RUN |
| `git diff --check` + new-file whitespace scan | No whitespace errors or conflict markers in changed documentation/worklog. | VERIFIED |

## HANDOFF

- Remaining decisions before DD approval: Product/API owner confirmation for access/publish predicate, curriculum ordering/tie-break, lesson visibility, path parse behavior, and not-found semantics.
- Next owner/action: Review `OPEN_QUESTIONS.md` and update canonical contract/schema before implementation or final approval.
