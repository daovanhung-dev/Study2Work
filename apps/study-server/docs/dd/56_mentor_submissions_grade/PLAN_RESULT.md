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

`PARTIALLY COMPLETED` — Plan recorded before DD authoring. The API contract and AC-23 flow are documented; rubric input/storage, score limits/scale and Mentor scope still need owner decisions. Runtime API #56 is `UNWIRED / NOT_FOUND`.

## Output folder

`apps/study-server/docs/dd/56_mentor_submissions_grade/`

## API contract

| Item | Value | Basis |
|---|---|---|
| API ID | `#56` | API catalog |
| Name | `Lưu điểm` | API catalog |
| Method/path | `POST /api/v1/mentor/submissions/{submission_id}/grade` | API catalog |
| Authentication/actor | Bearer JWT; role `Mentor` | API catalog and AC-23 |
| Request | `submission_id:int64!`; `score:int32!`; `rubric items:string!` | API catalog; rubric descriptor needs clarification |
| Success | HTTP `200`, `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Submission>` | API catalog |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Exact catalog set |

## Sources reviewed

- `docs/lists/list_api.md`: API #56 contract and reusable `Submission`, `Assignment`, `UploadAsset`, `ApiEnvelope` field contracts.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`: AC-23 actor, precondition, postcondition and API order.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`: all AC-23 nodes and edges, including #54 → #55 → grade input → #56 → #57 feedback.
- `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md`: design-only `assignments` and `assignment_submissions` tables and fields.
- `infra/postgres/study-server/DB.sql`: legacy candidate `assignment_submissions` DDL and nullable foreign keys.
- `infra/postgres/02_study_db.sql`: V1-PILOT rubric/criterion tables; they are UUID/assessment based and do not link to the legacy assignment submission model.
- `contracts/api-guidelines/README.md`: expected error envelope uses data=null.
- `apps/study-server/app/core/responses.py` and `apps/study-server/app/core/middleware.py`: current helper data default and exact-path design-code dispatch.
- API #35 submission-creation DD and API #36 submission-detail DD: current candidate fields and unresolved schema/asset/score/feedback visibility questions.
- API #54 and #55 DDs/worklogs: current AC-23 group findings, Mentor access candidate, Submission response mapping and files/rubric gap.
- `.agents/server-study/AGENTS.md`, `INDEX.md`, `apis/declared-routes.md`, `database.md`, `core/database-security.md`, `tests.md`, `workflows/README.md`.
- `.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md` and all eight registered Markdown templates.

## Tables read / write

- Candidate read: `assignment_submissions`, `assignments`, `courses` for submission lookup and direct-course-owner access check.
- Candidate write: `assignment_submissions.score`, `assignment_submissions.status` only.
- No rubric table is selected: legacy assignment schema has no rubric persistence relation; V1-PILOT rubric tables belong to UUID assessment records.
- No feedback write is included: AC-23 sequences API #57 as a separate feedback mutation after API #56.

## Planned output and authoring decisions

1. Preserve all eight template sheets and their Excel comparison appendices byte-for-byte.
2. Add one table mapping, `07_assignment_submissions_update.md`, for the candidate score/status update.
3. Add `OPEN_QUESTIONS.md` for contract, schema, authorization and lifecycle gaps.
4. Add `VERIFICATION_REPORT.md` with static-only evidence and exact error-set checks.
5. Keep candidate course ownership explicitly `DERIVED`; no Mentor route/auth code exists.
6. Treat `rubric items:string!` as a required but unresolved descriptor. Do not invent its JSON key, string encoding, item fields or persistence.
7. Treat score bounds, decimal conversion and max-score validation as `SOURCE_REQUIRED`; preserve catalog request `int32` and response `decimal-string?` without silently reconciling them.
8. Preserve `Submission.files[]` as a response-contract gap because the legacy table has only `file_url` and no approved asset resolver.
9. Do not edit application source, tests, DB schema, API catalog, diagrams or client code.
10. Do not create a ZIP; the Study Server workflow explicitly requires Markdown-only DD delivery.

## Assumptions and conflicts

- `courses.mentor_id = authenticated Mentor ID` is only a direct-owner access candidate inferred from AC-23 and legacy relations. Assigned Mentor policy and JWT subject mapping are unconfirmed.
- AC-23 states score and status become graded, but does not define DB transaction, status precondition, repeat-grading behavior, score range, rounding, rubric persistence or history.
- The input type `int32` and response type `decimal-string` differ. No conversion or scale rule is approved.
- AC-23 explicitly makes feedback a later API #57 action. API #56 must not consume or update feedback.
- API #54 is currently a singular `Submission` response while AC-23 needs a list selection. This existing cross-API discrepancy remains in the #54–#57 macro-review.
- API Guidelines expects error data=null, while current error_response(None) emits {}; current exact-path middleware allowlist omits API #56's dynamic path. These are conditional future-wiring discrepancies because the route is absent.

## Verification plan

- Validate exact 11-file set, template appendices, YAML/front matter, API contract and error set.
- Validate each request and response field has a usage/source or explicit `SOURCE_REQUIRED` status.
- Validate JSON examples, relative links, Markdown table widths, code fences and whitespace.
- Run `git diff --check`; do not run application tests for this docs-only task.
- Refresh API DD inventory after authoring; source implementation count should remain unchanged.
