---
task_id: "2026-10-12-create-study-api35-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #35 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-12/commit-push-study-dds.md
    - carry_forward: Giữ nguyên các DD hiện có; không commit/push trong task này; DD và worklog #27–#34 đang untracked.
  - path: .agents/worklog/2026-10-12/create-study-api27-dd.md
    - carry_forward: Dùng Draft — Needs Confirmation, ghi open questions, không ZIP và không suy luận runtime từ contract thiết kế.
  - path: .agents/worklog/2026-10-12/create-study-api28-dd.md
    - carry_forward: Bảo toàn contract/error set, phân biệt EXPECTED_BEHAVIOR với CURRENT_BEHAVIOR, để source gaps ở trạng thái SOURCE_REQUIRED/DISCREPANCY.
- shortage: none
- Additional recent precedent reviewed: create-study-api29-dd.md through create-study-api34-dd.md and review-study-api27-32-dds.md; preserve prior artifacts and use exact catalog field notation when its wire shape is unresolved.

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown draft API #35 POST /api/v1/assignments/{assignment_id}/submissions theo canonical template; kèm PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md và worklog. Không sửa runtime, API catalog, diagrams, schema hoặc DD #27–#34; không tạo ZIP.
- Canonical contract/approved DD: docs/lists/list_api.md là APPROVED_DESIGN_CONTRACT. API #35 yêu cầu Student Bearer JWT, path assignment_id:int64!, body text:string! và file refs:string!, response ApiEnvelope<Submission>, HTTP 201 DESIGN_RESOURCE_CREATED, errors 401/403/404/409/422/500.

## CURRENT_BEHAVIOR

- Source/config: API #35 không có route/module/query runtime. DB_UNICA_TABLES.md mô tả candidate assignment_submissions fields; checked-in DB.sql là design evidence, không xác nhận live schema.
- Runnable tests: Không tìm thấy test API #35; runtime tests không chạy theo phạm vi documentation-only.
- Runtime wiring: UNWIRED / NOT_FOUND; scan v1.py, modules và tests chỉ tìm thấy API #13 avatar upload khi dò từ khóa upload.

## SOURCE_TRACE

Student Bearer -> API #35 approved design contract -> AC-17 assignment access/deadline -> candidate assignment lookup and assignment_submissions mutation -> ApiEnvelope<Submission>. API #34 upload/Object Storage is a preceding design flow. Current API #35 route/module/test: UNWIRED / NOT_FOUND.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request file reference | Catalog notation file refs:string! does not define a concrete JSON key, representation, cardinality or relation to API #34 UploadAsset. | SOURCE_REQUIRED | Preserve exact catalog notation; do not invent a normalized request shape. |
| Request/response text | Request requires text:string!, while Submission.content is optional and physical content is nullable. | DISCREPANCY / SOURCE_REQUIRED | Keep request contract and candidate storage separate; record empty/null and mapping policy as open. |
| File cardinality/storage | Logical Submission has files:UploadAsset[]; candidate assignment_submissions has a single nullable file_url. | DISCREPANCY / DESIGN_ONLY | Do not claim multi-file persistence or invent an association table. |
| Insert/update semantics | AC-17 says INSERT/UPDATE Submission=SUBMITTED, but no upsert key, resubmission limit or unique assignment/user constraint is defined. | SOURCE_REQUIRED | Do not choose create-versus-replace behavior or concurrency policy. |
| Eligibility/deadline | AC-17 requires Student permission and unexpired assignment; exact predicates and 403-versus-409 branch ownership are unspecified. | SOURCE_REQUIRED | Preserve only API #35 catalog statuses and document policy gaps. |
| Physical schema | Table notes describe assignment_id/user_id as required; checked-in DDL permits nullable foreign keys. | DISCREPANCY / DESIGN_ONLY | Candidate mapping only; live schema is unverified. |

## CHANGES

- Files changed: Added eight template-based sheets, PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md under apps/study-server/docs/dd/35_assignments_submissions/; this worklog. Final static verification passed.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Continue the established Study API Draft — Needs Confirmation policy. Preserve existing untracked #27–#34 files. Keep source gaps explicit and do not alter canonical inputs.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected commit-push-study-dds.md, create-study-api27-dd.md and create-study-api28-dd.md; all three were read. | VERIFIED |
| API catalog, AC-17, DB table notes/ERD, checked-in DDL, API #33/#34 DD and runtime source scan | Sources reviewed; discrepancies above recorded. | VERIFIED |
| DD structural/content verification | 11-file inventory; all eight front matters and template appendix suffixes; request and response JSON; local links/anchors; Markdown table widths; exact catalog error-code set; whitespace/conflict scan; output SHA-256 fingerprints. | VERIFIED |
| git diff --check | No whitespace errors. | VERIFIED |
| Existing untracked DD/worklog #27–#34 | Final worktree review confirmed prior paths were not edited. | VERIFIED |
| Runtime tests / live DB | Not run or queried; outside documentation-only scope. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #35 design details listed above remain SOURCE_REQUIRED; they do not block this draft.
- Next owner/action: Product/API/Architecture owners resolve OPEN_QUESTIONS.md before the DD is approved or implementation-ready.
