---
task_id: "2026-10-12-create-study-api32-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #32 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Giữ các DD hiện có ở trạng thái draft; task này không gồm commit/push.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Study DD không tạo ZIP; ghi source gaps và không suy luận runtime từ design.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Giữ nguyên contract/error set; không để lộ answer key trong quiz detail; phân biệt design với runtime.
- shortage: none
- Additional recent precedent reviewed: .agents/worklog/2026-10-12/create-study-api29-dd.md, create-study-api30-dd.md, and create-study-api31-dd.md. Carry forward unresolved eligibility, answer-storage and result-disclosure questions; keep API #32 as a read-only design draft.

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design draft cho API #32 GET /api/v1/attempts/{attempt_id}/result theo template Markdown của Study Server; gồm 8 sheet, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog. Không tạo ZIP, không sửa runtime, catalog, diagrams hoặc schema.
- Canonical contract/approved DD: docs/lists/list_api.md đánh dấu API catalog APPROVED_DESIGN_CONTRACT. API #32 dùng Student Bearer JWT, path attempt_id:int64!, response ApiEnvelope<QuizAttempt>, HTTP 200 DESIGN_RESOURCE_RETRIEVED và lỗi 401/403/404/500. AC-16 mô tả cả nhánh AUTO GRADED và PENDING GRADE gọi API #32.

## CURRENT_BEHAVIOR

- Source/config: apps/study-server/app/api/v1.py không đăng ký API #32; source scan không tìm thấy quiz/attempt runtime module. app/utils/auth.py có helper xác thực Student Bearer/JWT hiện dùng bởi API khác. DB_UNICA_TABLES.md, ERD và infra/postgres/study-server/DB.sql chỉ là design evidence, không xác nhận live schema.
- Runnable tests: Không tìm thấy test API #32; không chạy runtime tests cho tài liệu design-only.
- Runtime wiring: API #32 là UNWIRED / NOT_FOUND.

## SOURCE_TRACE

~~~text
Student Bearer -> API catalog #32 -> AC-16 submit/grading branches (GRADED or PENDING_GRADE) -> candidate read quiz_attempts and quiz_answers -> ApiEnvelope<QuizAttempt>
Current Study route/module/test: UNWIRED / NOT_FOUND
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #32 runtime | Current Study router/module/test scan has no quiz result endpoint. | UNWIRED / NOT_FOUND | DD remains design-only. |
| Result visibility | AC-16 sends both grading branches to API #32; exact eligibility states and pending-grade projection are unspecified. | SOURCE_REQUIRED | Do not invent 403/409 or score/null/omit policy. |
| Feedback field | AC-16 says read score + feedback/status; QuizAttempt schema and candidate DB tables do not define feedback. | DISCREPANCY / SOURCE_REQUIRED | Do not add feedback to the approved response schema. |
| Answer representation/disclosure | Logical QuizAnswer allows choice_ids/text_answer/correct/score; physical quiz_answers has one choice_id/is_correct/score_received. | DISCREPANCY / SOURCE_REQUIRED | Keep selected-answer, correctness and per-answer score projection open. |
| Ownership masking | Candidate quiz_attempts has user_id and current auth helper yields Student user_id; exact owner predicate and 403-versus-404 policy are not specified. | SOURCE_REQUIRED | Do not claim final authorization query or error mapping. |

## CHANGES

- Files changed: Created 8 template sheets and PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md under apps/study-server/docs/dd/32_attempts_result/; finalized this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Follow the user-approved API #32 DD plan and Study Server no-ZIP workflow; preserve all pre-existing untracked DD #27–#31 artifacts.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected and read commit-push-study-dds.md, create-study-api27-dd.md and create-study-api28-dd.md; no shortage. | VERIFIED |
| Source and contract review | Read API #32 catalog row, AC-16 index/activity diagram, quiz_attempts/quiz_answers design, checked-in DDL, current router/auth/module/test surface and API #31 result-related open questions. | VERIFIED |
| Template review | Used all 8 canonical Markdown sheets; preserved template Excel comparison appendices and recorded the 8 input SHA-256 fingerprints and output sheet fingerprints in VERIFICATION_REPORT.md. | VERIFIED |
| Inline DD static validation | 11 Markdown files; 8 sheets in order with metadata; 3 JSON examples parsed; 22 relative links/anchors resolved; tables, exact error-code set, placeholders, whitespace and conflict markers passed. | VERIFIED |
| Existing DD/worklog preservation | SHA-256 checks matched the captured baseline for 56 existing #27–#31 DD files and 5 preceding worklogs. | VERIFIED |
| git diff --check | No tracked-diff whitespace errors. New/untracked DD files were checked by the inline whitespace scan above. | VERIFIED |
| Study runtime tests | Not run; API #32 is UNWIRED / NOT_FOUND and scope is documentation-only. | NOT_RUN |
| Context validator | Not run; no context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Product/API owner decisions about ownership masking, result availability during PENDING_GRADE, answer disclosure, feedback shape, and logical-to-physical answer mapping.
- Next owner/action: Review OPEN_QUESTIONS.md before approving the DD or implementing API #32.
