---
task_id: "2026-10-12-create-study-api30-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #30 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Giữ các DD hiện có; không gộp nội dung DD mới với thao tác Git.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Dùng trạng thái Draft — Needs Confirmation, ghi rõ source gaps và không tạo ZIP cho Study DD.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Giữ riêng contract với design/runtime behavior; không tự chốt các câu hỏi nghiệp vụ của AC-16.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown cho API #30 gồm 8 sheet theo template, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog. Không tạo ZIP hoặc sửa runtime, API catalog, diagram hay schema.
- Canonical contract/approved DD: docs/lists/list_api.md ghi PUT /api/v1/attempts/{attempt_id}/answers, Student Bearer JWT, attempt_id:int64!, body question_id:int64! và answer(s):string!, response ApiEnvelope<QuizAttempt>, HTTP 200 DESIGN_RESOURCE_UPDATED và các error code 401/403/404/422/500.

## CURRENT_BEHAVIOR

- Source/config: AC-16 đặt thao tác UPSERT AttemptAnswer; quiz_answers là candidate design table. Logical schema có choice_ids/text_answer; physical DDL chỉ có choice_id, yêu cầu is_correct NOT NULL, và không có unique key cho (attempt_id, question_id).
- Runnable tests: Không tìm thấy test API #30 trong current scan; không chạy runtime tests vì scope là DD-only.
- Runtime wiring: Không tìm thấy route, module hoặc query API #30 trong Study Server; UNWIRED / NOT_FOUND.

## SOURCE_TRACE

~~~text
Student Bearer JWT -> PUT /api/v1/attempts/{attempt_id}/answers -> candidate attempt/question checks -> candidate UPSERT quiz_answers -> ApiEnvelope<QuizAttempt>
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #30 runtime | Current Study router/modules/tests scan không thấy implementation. | UNWIRED / NOT_FOUND | DD chỉ mô tả design, chưa phải runtime behavior. |
| Request answer shape | Catalog ghi answer(s):string!; logical QuizAnswer có choice_ids hoặc text_answer; physical table có choice_id. | SOURCE_REQUIRED / DISCREPANCY | Giữ notation catalog; chưa chốt JSON property, encoding hay persistence mapping. |
| Upsert key | AC-16 ghi UPSERT; ERD/DDL không khai báo unique key cho (attempt_id, question_id). | SOURCE_REQUIRED / DISCREPANCY | Không thể khẳng định lookup/update hoặc concurrency semantics. |
| Correctness and score | DDL yêu cầu is_correct NOT NULL; AC-16 đặt submit/grading sau autosave ở API #31. | SOURCE_REQUIRED / DISCREPANCY | Cần owner quyết định giá trị/schema/flow trước khi triển khai. |
| Ownership and attempt state | Catalog xác định Student; attempt có user/status candidate columns; AC-16 không chốt predicate hay error mapping. | SOURCE_REQUIRED | Ghi câu hỏi về owner, state, 403/404 và question membership. |
| QuizAttempt response | Catalog yêu cầu ApiEnvelope<QuizAttempt>; response projection và answer disclosure không được chi tiết hóa. | SOURCE_REQUIRED | Giữ dữ liệu trả về và optional fields ở mức candidate. |
| Foreign-key nullability | DB table notes và checked-in DDL khác nhau về nullability của answer references. | DISCREPANCY / DESIGN_ONLY | Không khẳng định schema live hoặc sửa DDL. |

## CHANGES

- Files changed: Tạo 8 sheet, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md tại apps/study-server/docs/dd/30_attempts_answers/ và worklog này.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Giữ draft precedent #27–#29; không ZIP; không sửa runtime/catalog/diagram/schema; không tự giải quyết xung đột contract/schema.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Chọn và review 3 worklog được liệt kê tại PRIOR_WORKLOG_REVIEW. | VERIFIED |
| Source review | Đối chiếu API catalog, AC-16/index, DB tables/ERD/DDL, current auth helper/router/modules/tests, canonical template và DD precedent. | VERIFIED |
| Inline Python DD validation | 8 sheet đúng thứ tự/metadata/template appendix; 392 table rows, 3 JSON examples và 23 relative links/anchors hợp lệ; contract/error set và hygiene đạt. | VERIFIED |
| git diff --check | Không phát hiện whitespace errors. | VERIFIED |
| Runtime tests | Không chạy; API #30 UNWIRED / NOT_FOUND và task documentation-only. | NOT_RUN |
| Context validator | Không chạy vì không thay đổi context page/manifest. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Các quyết định trong OPEN_QUESTIONS.md cần Product/API owner xác nhận trước khi nâng trạng thái DD hoặc wire API.
- Next owner/action: Chốt answer representation/storage, khóa upsert và concurrency, ownership/status policy, response projection/disclosure, cùng quy tắc message/trace.
