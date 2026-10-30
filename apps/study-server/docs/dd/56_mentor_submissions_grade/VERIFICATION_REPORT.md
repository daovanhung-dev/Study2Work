---
title: "Verification Report — Study API #56 Lưu điểm"
order: 11
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
source_sheet: "Verification Report"
status: "Draft — Needs Confirmation"
---

# Verification Report — Study API #56

## Kết quả

PARTIALLY COMPLETED — API route, focused tests, full local suite and documentation checks pass. Rubric persistence is unresolved because the checked-in legacy schema has no supported target. Direct-owner access, score range and rubric_items wire spelling remain DERIVED fallbacks.

## Evidence reviewed

| Source | Result |
|---|---|
| API catalog #56 | POST path, request descriptors, ApiEnvelope<Submission>, 200 code and exact 401/403/404/422/500 error set retained |
| AC-23 index/activity diagram | Flow #54 list → #55 detail → #56 grade/status → #57 feedback retained |
| Legacy Study DDL/table guide | assignment_submissions score/status, assignments.max_score and nullable relation candidates reviewed |
| V1-PILOT DDL | UUID assessment/rubric model has no supported join to legacy BIGINT submissions |
| Current API #56 source | Module, POST route, score/path validation, lock/update SQL, response projection and rollback/commit flow are present |
| Current middleware | Dynamic API #56 route template is registered for DESIGN_* mapping |
| Focused TestClient tests | 27 passed; fake DB only |
| Full Study suite | 510 passed |
| Ruff | app and tests passed |
| OpenAPI/import | app imports; 27 operations / 26 unique API path templates; request fields required and score format int32 |
| Linked API #57 notes | Stale claims that API #56 is unwired or has no file resolver were updated |
| Context validator | Deno run reports pre-existing db-admin missing-context/source errors and broad dirty-source drift; --skip-drift leaves only db-admin errors |

## Contract and implementation checks

- Request: signed int64 submission_id path; strict int32 score; required strict string rubric_items under a DERIVED wire key.
- Success: HTTP 200 DESIGN_RESOURCE_UPDATED with the reusable Submission response.
- Errors: exactly 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR.
- Score fallback: 0 <= score <= assignments.max_score; exact integer-to-Decimal mapping into candidate NUMERIC(6,2).
- Mutation: score and status=GRADED only; existing feedback is preserved and API #57 remains separate.
- Access: explicit MENTOR guard and direct courses.mentor_id ownership fallback.
- Files: at most one UploadAsset via exact URL, owner, SUBMISSION purpose and course; no match gives files=[].
- Transaction: submission row lock; rollback on failed lookup/update/projection/commit; commit after response projection validation.
- rubric_items is accepted but not interpreted, persisted or echoed. No rubric table, column or join is invented.
- No 400, 409, 503 or extra business code was added.

## DD artifact checks

| Check | Result |
|---|---|
| Expected API #56 Markdown files | PASS — exactly 11 files |
| Front matter | PASS — present on all eight template-sheet files |
| Excel comparison appendices | PASS — all eight appendix suffixes were retained while replacing only main DD content |
| Request/response JSON examples | PASS — parsed |
| Local Markdown links | PASS — targets exist |
| Code fences and trailing whitespace | PASS |
| git diff --check | PASS |
| Context registry | API #56 source/test paths present; full validator has the baseline errors listed above |

## Output SHA-256

Hashes cover all DD artifacts except this report to avoid a self-referential value.

| File | SHA-256 |
|---|---|
| 00_Cover.md | 61d17885c5b7aeb71e967f203cb8aa61e46f3d2d5f6877131d37f3c02d8c8b5b |
| 01_Lich_su.md | 97b81e32514b4b06ccb68d43440dfe1b04f00a82a16ab51a7caf188f3e0ede12 |
| 02_Overview.md | c092c06f54cd462d51a43e0db0043dbd7af28d7bd0a5848d9c32185b660db980 |
| 03_Request.md | 1eea0f9f04ee5229ef79f5fa32cafc9437568aedb8bf92a07e783df564cd4b5e |
| 04_Response.md | 1864d76dd2b8e9334ced26863dffad1af08215853141e2e2cd9032aac2d9c8dd |
| 05_Data_Mapping.md | 2e8d9078c5cf42a05baf99da9a47450e1f475378e7efd62eafb1a9323571e07f |
| 06_Error.md | a69ab61aca20a96caf8619310e2ddc42f5cec9dc4b786af59a4a2035c1fbd095 |
| 07_assignment_submissions_update.md | bec79523e797cd989d8fa17c88d720eaa44236659c8b9cf287ade28768b32be9 |
| OPEN_QUESTIONS.md | 419f8bb367e117f5f8711a13b43b8b00e861f8dc09208a684718c90dc61b0462 |
| PLAN_RESULT.md | 9c97cfb9c4af3212aae26130fc26a6ea8492fb230547162219ec475d3a9ba275 |

## Remaining gaps

- No approved rubric item schema, canonical wire key or persistence relation.
- Direct-owner versus assigned-Mentor policy and JWT-to-user mapping require owner confirmation.
- Score range [0, max_score] and regrading from any status are DERIVED.
- API #35 file URL compatibility and live assignment/upload schema are unverified.
- Checked-in DDL and fake DB tests do not prove live database state or deployment.
- Keep this DD status Draft — Needs Confirmation.

## AC-23 macro-review #54–#57

API #54 list, #55 detail, #56 grade/status and #57 feedback remain separate in the diagram sequence. API #54 uses Page<Submission>, fixed size 20, page 1 default and submitted_at DESC/id DESC order under the current fallback. APIs #54–#56 use a DERIVED constrained UploadAsset lookup. API #56 preserves feedback and has no rubric persistence target. API #57 attachment storage and rubric exposure remain unresolved.
