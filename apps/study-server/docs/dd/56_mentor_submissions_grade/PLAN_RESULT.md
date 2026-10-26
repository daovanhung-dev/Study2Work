---
title: "Plan — Study API #56 Lưu điểm"
order: 8
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
source_sheet: "Plan Result"
status: "Draft — Needs Confirmation"
---

# PLAN_RESULT — API #56 Lưu điểm

## Status

PARTIALLY COMPLETED. The endpoint is wired and locally verified. The required rubric_items string is accepted but not persisted because the checked-in legacy schema has no supported rubric target. Keep Draft — Needs Confirmation until the API/schema owner resolves that contract gap and the derived business fallbacks.

## API contract

| Item | Value | Basis |
|---|---|---|
| API ID | #56 | API catalog |
| Method/path | POST /api/v1/mentor/submissions/{submission_id}/grade | API catalog |
| Authentication/actor | Bearer JWT; explicit MENTOR role | API catalog and current shared guard |
| Request | submission_id:int64; score:int32; rubric_items:string | catalog descriptor; snake-case wire key is DERIVED |
| Success | HTTP 200 DESIGN_RESOURCE_UPDATED | API catalog |
| Response | ApiEnvelope<Submission> | API catalog; reusable API #54 response model |
| Errors | 401/403/404/422/500 with catalog DESIGN_* codes | exact catalog set |

## Decisions and current behavior

1. rubric_items is the simple snake-case wire-key fallback, required as a strict string and treated as opaque. It is neither persisted nor echoed because no supported schema target exists.
2. Legacy assignment_submissions.score/status are the mutation candidates. Only score and status=GRADED are changed; existing feedback is preserved for API #57.
3. Score is converted exactly from int to Decimal and validated against DERIVED range 0 <= score <= assignments.max_score. Out-of-range score returns catalog 422.
4. Regrading from any current status is allowed; the catalog does not define a 409 trigger.
5. MENTOR access uses numeric JWT subject and direct courses.mentor_id ownership, consistent with APIs #54/#55. Assigned-Mentor access remains unsupported/unverified.
6. Submission.files uses the same DERIVED constrained lookup as APIs #54/#55: exact file URL, owner, SUBMISSION purpose and course; at most one result; no result gives an empty list.
7. The row is locked while access and score are checked. The endpoint validates the updated Submission projection before commit and rolls back failures.
8. API #57 remains the separate feedback mutation.

## Changes

- Added API #56 request/response models, score/path validation, SQL constants and view orchestration.
- Wired the POST route and dynamic route-template business-code mapping.
- Added focused TestClient coverage and synchronized this DD plus linked API #57 notes.
- Updated server-study context pages and manifest required source paths.
- No migration or live database operation was performed.

## Verification

- Focused API #56 TestClient suite: 27 passed.
- Full Study Server suite: 510 passed.
- Ruff over app and tests: passed.
- OpenAPI import/route checks: passed; API #56 body fields are required and score is int32.
- DD content/link/example checks and context validation are recorded in VERIFICATION_REPORT.md and the task worklog.

## Boundaries

Fake-DB tests verify application behavior and SQL bindings only. Checked-in legacy DDL does not prove live schema or deployment. Rubric persistence and its item format remain unresolved; score range, direct-owner policy and file URL matching are DERIVED fallbacks.
