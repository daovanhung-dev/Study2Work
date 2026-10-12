---
task_id: "2026-10-11-create-study-api23-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #23

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available: 36; selected: 3; status: READY`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách expected/current behavior; giữ persistence thiếu bằng chứng ở `SOURCE_REQUIRED`; contract thiết kế không chứng minh runtime.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Ghi discrepancy và nguồn chưa xác nhận trong draft; không tự chọn semantics nghiệp vụ/schema.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Giữ `UNWIRED / NOT_FOUND`, không suy diễn runtime; DD Study theo Markdown folder, tests không chạy khi endpoint chưa wired.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo Draft API DD #23 `POST /api/v1/lessons/{lesson_id}/start` với 8 sheet template và 3 report; không ZIP.
- Contract: Student Bearer JWT; `path{lesson_id:int64!}`; `ApiEnvelope<Lesson>`; HTTP/business codes 201/401/403/404/422/500 theo `docs/lists/list_api.md`.
- AC-14 sequence ghi API #23 upsert lesson progress thành `IN_PROGRESS`; chi tiết khóa upsert và cột được cập nhật chưa được xác nhận.
- Phạm vi: Chỉ thêm DD và worklog; không sửa runtime, catalog, diagram, DDL hoặc migration.

## CURRENT_BEHAVIOR

- API catalog row #23 được kiểm tra lại; AC-14 diagram ghi `UPSERT lesson progress = IN_PROGRESS`.
- Checked-in `infra/postgres/study-server/DB.sql` có `lesson_progress` với `id`, `user_id`, `lesson_id`, `status`, `progress_percent`, `last_accessed_at`, `completed_at`; DDL không khai báo unique key cho cặp user/lesson. Đây là thiết kế checked-in, không xác nhận live schema.
- Current source/test scan không tìm thấy route/module/query/focused test API #23 hoặc implementation `lesson_progress`; trạng thái `UNWIRED / NOT_FOUND`.

- Runnable tests: Không có focused test API #23 trong inventory; application tests không chạy vì task chỉ tạo tài liệu và endpoint chưa wired.

## SOURCE_TRACE

```text
Student -> API #23 contract in list_api.md -> AC-14 API sequence
-> design UPSERT lesson_progress.status=IN_PROGRESS
-> no API #23 runtime route/module/query/test found
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| UPSERT key/updates | AC-14 says UPSERT; checked-in DDL declares no unique `(user_id, lesson_id)` key or update rules | `SOURCE_REQUIRED` | Record without choosing conflict target, timestamp updates, or preservation behavior. |
| Response and creation semantics | Catalog says `ApiEnvelope<Lesson>` and 201 resource created; diagram says `ApiEnvelope` and follows upsert | `DISCREPANCY` | Preserve catalog contract; record payload/201 semantics for confirmation. |
| Access/404 rules | Catalog lists 403/404; AC-14 routes through API #22 access check but gives no #23-specific predicate/resource condition | `SOURCE_REQUIRED` | Preserve status codes; do not invent authorization or 404 mapping. |
| Runtime | No API #23 route/module/query/test in current source inventory | `UNWIRED` / `NOT_FOUND` | DD documents expected design only. |

## CHANGES

- Files changed: Tạo thư mục DD với 8 template sheets + OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md; hoàn tất worklog này.
- Context pages changed: None.

- Planned files: `apps/study-server/docs/dd/23_lessons_start/` (8 sheets + 3 reports) and this worklog.
- CONTEXT_UPDATES: None.
- Assumptions: Keep status `Draft — Needs Confirmation`; record unsupported mutation/authorization details as open questions; no ZIP per Study workflow.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Node worklog selector for docs, limit 3 | Selected API #16–#18 docs worklogs; all three read; shortage none. | VERIFIED |
| Current catalog/AC/schema and Study source/test inventory | API #23 contract and AC-14 UPSERT confirmed; no API #23 route/module/query/focused test found; checked-in schema remains design-only. | VERIFIED |
| Inline static Markdown/JSON/table/link checker | 11 documents; 8 sheets ordered; 2 JSON examples valid; table widths, local links/anchors, front matter, fences and whitespace pass. | VERIFIED |
| API catalog code comparison | API #23 codes exactly match 201/401/403/404/422/500 contract codes. | VERIFIED |
| Template SHA-256 check | All eight template fingerprints recorded in VERIFICATION_REPORT.md. | VERIFIED |
| git diff --check and authored-file whitespace scan | No whitespace errors. | VERIFIED |
| Study Server application tests | Not run; documentation-only scope and API #23 is not wired. | NOT_RUN |
| Context validator | Not run because no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Resolve OPEN_QUESTIONS.md before marking the DD Ready/Final or using it as an implementation contract.
- Next owner/action: Contract/schema owner confirms UPSERT key and state rules, repeated-start/201 semantics, response payload, access/error conditions, transaction/failure behavior and live schema baseline.
