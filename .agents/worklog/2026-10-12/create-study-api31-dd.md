---
task_id: "2026-10-12-create-study-api31-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #31 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Giữ nguyên các DD draft và source gaps; không gộp thao tác Git với nội dung DD mới.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Dùng Draft — Needs Confirmation, open questions, không ZIP; tách contract thiết kế khỏi current runtime.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Giữ các business rule chưa chốt trong OPEN_QUESTIONS; không tự thêm error code hoặc schema.
- shortage: none
- Additional recent precedent reviewed: .agents/worklog/2026-10-12/create-study-api29-dd.md and create-study-api30-dd.md.

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design draft cho API #31 POST /api/v1/attempts/{attempt_id}/submit theo template Markdown, kèm PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog.
- Canonical contract/approved DD: docs/lists/list_api.md là APPROVED_DESIGN_CONTRACT. API #31 yêu cầu Student Bearer JWT; path attempt_id:int64!; ApiEnvelope<QuizAttempt>; HTTP 200 DESIGN_RESOURCE_UPDATED; errors 401/403/404/422/409/500. AC-16 ghi submit attempt, chấm auto và nhánh PENDING_GRADE/GRADED.

## CURRENT_BEHAVIOR

- Source/config: Current Study router/module scan does not find API #31; DB table design/ERD/checked-in DDL are design evidence and do not confirm live schema.
- Runnable tests: No API #31 test found; runtime tests are not applicable to the documentation-only scope.
- Runtime wiring: UNWIRED / NOT_FOUND.

## SOURCE_TRACE

~~~text
Student Bearer -> POST /api/v1/attempts/{attempt_id}/submit (design contract)
-> AC-16 SUBMITTED + automatic grading -> PENDING_GRADE or GRADED
-> candidate read quiz_attempts/quiz_answers/quiz_questions/quiz_choices
-> candidate update quiz_answers grading fields and quiz_attempts result/state
-> ApiEnvelope<QuizAttempt>
Current Study route/module/test: UNWIRED / NOT_FOUND
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #31 runtime | Current router/modules/tests contain no API #31 implementation. | UNWIRED / NOT_FOUND | DD documents expected design only. |
| Grading rules | AC-16 names automatic grading/manual grading but no formula or question-type predicate. | SOURCE_REQUIRED | No score or grading algorithm is invented. |
| API #30 answer storage | Logical answer schema allows choice_ids/text_answer; physical design stores one choice_id; DDL requires is_correct before submit. | DISCREPANCY / SOURCE_REQUIRED | Preserve upstream storage/grade gap; no schema changes. |
| Attempt access/state | Owner predicate, allowed statuses, repeat-submit behavior and 403/404/409 mapping are unspecified. | SOURCE_REQUIRED | Keep decision in OPEN_QUESTIONS.md. |
| Live schema | DB table design and checked-in DDL are design evidence; live metadata not verified. | NOT_VERIFIED | Physical mapping remains candidate only. |

## CHANGES

- Files changed: New API #31 DD folder with eight base template sheets plus a separate quiz_answers mapping sheet, three reports and this worklog.
- CONTEXT_UPDATES: None; no runtime, contract, diagram or schema changed.
- Context pages changed: None.
- Assumptions: Follow the #27–#30 Draft — Needs Confirmation policy; no ZIP; preserve all existing untracked #27–#30 artifacts; document unresolved rules instead of deciding them.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected and read the three listed worklogs. | VERIFIED |
| Source review | API catalog, AC-16 diagram, DB table map, ERD/DDL, guidelines and current router/module/test scan reviewed. | VERIFIED |
| DD structure/content validation | Eight canonical template sheets in order plus the `quiz_answers` mutation mapping and three reports; front matter/status, 2 JSON examples, 399 Markdown table data rows, 19 relative links, six question anchors, contract/error catalog, AC-16 branches, DDL discrepancy, whitespace and conflict markers checked. | VERIFIED |
| Runtime tests | Not run; API #31 is not wired and task scope is documentation-only. | NOT_RUN |
| Context validator | Not required because no context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Product/API owner decisions listed in OPEN_QUESTIONS.md.
- Next owner/action: Review the open questions before marking the DD Final or implementing API #31.
