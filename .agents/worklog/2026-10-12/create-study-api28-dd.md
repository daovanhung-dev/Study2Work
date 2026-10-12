---
task_id: "2026-10-12-create-study-api28-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #28 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Các DD Study #16–#26 là design drafts; giữ riêng expected/current và không suy ra runtime từ tài liệu.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Tiếp tục trạng thái Draft + open questions, không tạo ZIP cho Study, giữ nguyên artifacts #27 và không tự chốt business rule.
  - path: .agents/worklog/2026-10-11/create-study-api16-dd.md
    - carry_forward: Dùng createDD-markdown, giữ SOURCE_REQUIRED/DISCREPANCY/UNWIRED rõ ràng; không invent schema hoặc runtime.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design draft cho API #28 GET /api/v1/quizzes/{quiz_id} theo template Markdown, gồm 8 sheet, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog.
- Canonical contract/approved DD: docs/lists/list_api.md đánh dấu API catalog là APPROVED_DESIGN_CONTRACT; API #28 yêu cầu Student Bearer JWT, quiz_id:int64!, ApiEnvelope<Quiz>, HTTP 200/401/403/404/500 với business code tương ứng. AC-16 mô tả Student có quyền làm quiz, quiz đang mở và flow đọc Quiz/rules/question set. Không thêm 409 vào API #28 khi catalog chưa có.

## CURRENT_BEHAVIOR

- Source/config: apps/study-server/app/api/v1.py cùng module scan không có quiz route/module; infra/postgres/study-server/DB.sql có quizzes, quiz_questions, quiz_choices nhưng là checked-in design DDL, không xác nhận live schema.
- Runnable tests: Source scan apps/study-server/tests/ không tìm thấy quiz/API #28 tests; runtime tests không chạy vì task chỉ tạo DD.
- Runtime wiring: API #28 hiện UNWIRED / NOT_FOUND trong Study Server.

## SOURCE_TRACE

~~~text
Student client -> GET /api/v1/quizzes/{quiz_id} (approved design contract)
-> candidate reads quizzes -> quiz_questions -> quiz_choices
-> ApiEnvelope<Quiz> on success / catalog error envelope on failure
Current Study route/module/test: UNWIRED / NOT_FOUND
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Eligibility / quiz state | AC-16 requires eligible Student and open quiz; exact predicate/status values absent. | SOURCE_REQUIRED | Do not invent enrollment or status policy. |
| 403/409 branch | AC-16 activity diagram says 403/409 for ineligible/limit/expiry; API #28 catalog lacks 409. | DISCREPANCY | Preserve catalog error set; ask owner whether branch belongs to API #29 or contract needs change. |
| QuizChoice / QuestionType | Catalog omits QuizChoice field definition and QuestionType values; DB has no question type column. | SOURCE_REQUIRED | Keep response subshape open; exclude is_correct from Student response. |
| Physical nullability | DB table design says quiz FKs required; checked-in DDL permits NULL. | DISCREPANCY / DESIGN_ONLY | Candidate mappings only; live schema not verified. |
| API #28 runtime | Current router/modules/tests contain no quiz implementation. | UNWIRED / NOT_FOUND | DD documents expected design only. |

## CHANGES

- Files changed: New apps/study-server/docs/dd/28_quizzes_detail/ with eight template sheets and three reports; this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Continue API #27 Draft — Needs Confirmation policy; no ZIP per Study workflow; exclude quiz_choices.is_correct per user direction; preserve all existing API #27 files.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected and read the three listed docs worklogs. | VERIFIED |
| API catalog, diagram, DB design and current source review | Đã đối chiếu contract API #28, AC-16, candidate schema và trạng thái runtime UNWIRED. | VERIFIED |
| Inline Python static checks: 8 sheet/order/front matter, tables, JSON, relative links/anchors, catalog row and `is_correct` exclusion | Tất cả assertions đạt; 2 JSON examples parse được và response examples không có `is_correct`. | VERIFIED |
| `git diff --check` and new-file whitespace/conflict scan | Không phát hiện lỗi whitespace hoặc conflict marker. | VERIFIED |
| Study runtime tests | Not run; documentation-only task and API #28 is not wired. | NOT_RUN |
| Context validator | Not run; no agent context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Owner decisions in OPEN_QUESTIONS.md; no runtime/API implementation included.
- Next owner/action: Review the open questions before approving DD or implementing API #28.
