---
task_id: "2026-10-11-create-study-api24-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #24

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available: 37; selected: 3; status: READY`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách expected/current behavior; giữ persistence chưa có bằng chứng ở `SOURCE_REQUIRED`; không suy diễn runtime từ contract thiết kế.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Ghi rõ discrepancy và nguồn còn thiếu; không tự chọn semantics nghiệp vụ/schema.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Study API DD là Markdown folder, không tạo ZIP; nếu endpoint chưa wire thì ghi `UNWIRED / NOT_FOUND`, không chạy application tests.
- extra_relevant_worklog: `.agents/worklog/2026-10-11/create-study-api23-dd.md`
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo API DD Markdown #24 `GET /api/v1/lessons/{lesson_id}` gồm 8 template sheets và `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không tạo ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` khai báo Student Bearer JWT, `path{lesson_id:int64!}`, `ApiEnvelope<Lesson>`, HTTP/business codes 200/401/403/404/500. AC-14/AC-15 diagram dùng endpoint này trong luồng học và xem nội dung; AC-15 ghi bước kiểm tra access và trạng thái publish.
- Scope: Chỉ thêm DD #24 và worklog; không sửa runtime, catalog, diagram, DDL hoặc context page.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` không đăng ký route #24; source/module scan không tìm thấy API #24. DDL checked-in có bảng thiết kế `lessons` (`id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status`) nhưng không xác nhận live schema.
- Runnable tests: Không có test riêng cho API #24; application tests không chạy theo phạm vi đã chốt.
- Runtime wiring: `UNWIRED / NOT_FOUND`; API #12 chỉ đọc quan hệ lesson để truy vấn parent course trong resource-detail flow.

## SOURCE_TRACE

```text
Student -> API #24 catalog contract -> AC-14/AC-15 lesson content flow
-> candidate read-only lessons projection (checked-in design DDL only)
-> no API #24 route/module/query/focused test found in current Study source
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #24 runtime | Route/module/focused test absent from current Study source inventory | `UNWIRED` / `NOT_FOUND` | DD documents expected design only. |
| Access and publish predicate | AC-15 says check access and publish status; exact policy is unspecified | `SOURCE_REQUIRED` | Do not invent entitlement, status scope or 403/404 split. |
| Lesson mapping | Catalog `Lesson` fields and checked-in DDL fields have design mapping; no API #24 query exists | `DESIGN_ONLY` / `SOURCE_REQUIRED` | Do not claim SQL, projection behavior or live schema. |

## CHANGES

- Files changed: Created `apps/study-server/docs/dd/24_lessons_detail/` (8 sheets + 3 reports) and this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Status remains `Draft — Needs Confirmation`; preserve access, publish, 403/404 and optional/null serialization questions as open; no ZIP.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Docs worklog selector and review | Selected API #16–#18 worklogs; all read; #23 reviewed as extra relevant context. | VERIFIED |
| Inline static DD validation | 11 Markdown files; sheet front matter/status/order, tables, fences, whitespace, JSON examples, relative links/anchors and API #24 error-code set passed. | VERIFIED |
| Source/catalog/diagram/runtime comparison | Contract and AC-14/15 represented; current source scan found no API #24 route/module/query/focused test; design gaps recorded. | VERIFIED |
| `git diff --check` | No whitespace errors reported for tracked changes; authored files also passed inline trailing-whitespace validation. | VERIFIED |
| Runtime tests | Not run; API #24 is not wired and plan excludes application tests. | NOT_RUN |
| Context validator | Not run; no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Access predicate, JWT-to-enrollment binding, publish scope, 403/404 semantics, response serialization and live schema remain unconfirmed in `OPEN_QUESTIONS.md`.
- Next owner/action: Review `OPEN_QUESTIONS.md` and provide approved rules before using the DD as a final implementation contract.
