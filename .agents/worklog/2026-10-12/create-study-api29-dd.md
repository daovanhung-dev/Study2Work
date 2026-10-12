---
task_id: "2026-10-12-create-study-api29-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #29 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Giữ các DD hiện có và source gaps; không gộp thao tác Git với nội dung DD mới.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Dùng Draft — Needs Confirmation, open questions, không ZIP cho Study; current runtime và design contract phải tách biệt.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Giữ API #28 và các câu hỏi về eligibility; không tự quyết nhánh 403/409 của AC-16.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD draft cho API #29 POST /api/v1/quizzes/{quiz_id}/attempts theo template Markdown, kèm PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog; không tạo ZIP hoặc sửa runtime/catalog/diagram/schema.
- Canonical contract/approved DD: docs/lists/list_api.md đánh dấu catalog APPROVED_DESIGN_CONTRACT. API #29 dùng Student Bearer JWT, quiz_id:int64!, ApiEnvelope<QuizAttempt>, HTTP 201/401/403/404/422/409/500.

## CURRENT_BEHAVIOR

- Source/config: AC-16 là design evidence. API #29 chưa được đăng ký trong apps/study-server/app/api/v1.py; scan modules/tests không tìm thấy route/module/test quiz-attempt. DB_UNICA_TABLES.md/ERD/DB.sql là design/schema artifacts, không xác nhận live schema.
- Runnable tests: Không tìm thấy test API #29; không chạy runtime test cho tài liệu design-only.
- Runtime wiring: UNWIRED / NOT_FOUND.

## SOURCE_TRACE

```text
Student Bearer -> POST /api/v1/quizzes/{quiz_id}/attempts -> candidate eligibility/read checks -> candidate INSERT quiz_attempts as IN_PROGRESS -> ApiEnvelope<QuizAttempt>
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #29 runtime | Current Study router/modules/tests have no quiz-attempt implementation. | UNWIRED / NOT_FOUND | DD remains design-only. |
| Eligibility and 403/409 mapping | AC-16 states permission/open-quiz preconditions and exhausted/expired branch but does not assign exact predicate or response code. | SOURCE_REQUIRED / DISCREPANCY | Preserve catalog codes; record owner questions. |
| Physical FK nullability | DB table design describes quiz_id/user_id as required references; checked-in DB.sql permits NULL references. | DISCREPANCY / DESIGN_ONLY | Mark candidate mapping; do not claim live schema. |
| Initial QuizAttempt response | Logical schema requires answers[]; AC-16 only specifies creating an IN_PROGRESS attempt. | SOURCE_REQUIRED | Mark initial answers and optional fields as open. |

## CHANGES

- Files changed: Created eight template-derived sheets and PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md in apps/study-server/docs/dd/29_quizzes_attempts/; created this worklog. Existing API #27/#28 files were preserved.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Follow the user-approved API #27/#28 draft policy; no ZIP; no runtime/catalog/diagram/schema changes; unresolved business rules remain in OPEN_QUESTIONS.md.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected and read the three worklogs listed under PRIOR_WORKLOG_REVIEW. | VERIFIED |
| Source review | Read API #29 catalog row, AC-16 index/activity page, quiz_attempts design/ERD/DDL, current router/modules/tests scan, canonical template and adjacent API #28 DD. | VERIFIED |
| Inline Python DD validation | 8 sheets in template order; front matter/status, template appendix and SHA-256 fingerprints, API contract codes, 2 JSON examples, 28 Markdown tables, 25 links/anchors, whitespace and conflict markers passed. | VERIFIED |
| Runtime tests | Not run; API #29 is UNWIRED / NOT_FOUND and task scope is documentation-only. | NOT_RUN |
| Context validator | Not run; no agent-context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Product/API owner decisions in OPEN_QUESTIONS.md are needed before marking the DD Final or implementing runtime behavior.
- Next owner/action: Review eligibility ownership, attempt limit/expiry and 403/409 mapping, user identity/schema mapping, and initial QuizAttempt response shape.
