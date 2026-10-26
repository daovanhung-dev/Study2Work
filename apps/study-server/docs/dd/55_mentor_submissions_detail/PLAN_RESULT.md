# Plan Result — Study API #55 Lấy bài làm và rubric Mentor

**Trạng thái plan:** `PARTIALLY_COMPLETED — runtime contract implemented; rubric source gap remains`
**API:** `GET /api/v1/mentor/submissions/{submission_id}`
**Output folder:** `apps/study-server/docs/dd/55_mentor_submissions_detail/`
**Phân loại:** `coding` · secondary `test`, `docs` · scope `server-study`
**Basis:** Catalog/AC-23 method, input, envelope and error set `DIRECT`; direct-owner, malformed-path, integrity and UploadAsset behavior `DERIVED`; live schema `NOT_VERIFIED`.
**Deliverable:** Local route/module/tests and updated Markdown DD/context; no schema migration or live database change.

## Source-priority decision

| Priority | Evidence | Decision |
|---|---|---|
| AC-23 activity diagram | #55 action says read `Submission + files + rubric`; node response is `ApiEnvelope<Submission>` | Preserve the action in the discrepancy log; response node does not define a rubric field. |
| Infra/DB artifacts | Legacy BIGINT `assignments`/`assignment_submissions` has no rubric link; separate V1-PILOT uses UUID `assessments`/`rubrics` | Do not join unrelated models or invent a foreign key. |
| API catalog/reusable schema | `ApiEnvelope<Submission>`; `Submission` has `files` but no `rubric` | Implement the catalog shape and keep rubric out of the response pending linked schema/contract. |
| Fallback per task instruction | Current #46/#48/#54 use numeric JWT subject and direct `courses.mentor_id`; #54 has a DERIVED file lookup | Reuse direct-owner and exact URL/owner/`SUBMISSION` purpose/course fallback; preserve `Draft — Needs Confirmation`. |

## Implemented flow

1. `app/api/v1.py` wires the GET route with a raw string path parameter exposed as signed int64 in OpenAPI; middleware registers its route template.
2. The view calls `validate_current_user_request(..., role="MENTOR")` before parsing the path or reading the database.
3. A raw signed-int64 parser maps malformed/overflow paths to catalog 404, following API #48; no new 422 code is added.
4. One SQL constant reads `assignment_submissions` with LEFT JOINs to assignments/courses and a constrained LATERAL lookup of at most one matching upload.
5. Missing submission maps to 404; missing/orphan required relations map to safe 500; a different direct course owner maps to 403.
6. After ownership passes, the view reuses API #54's `SubmissionResponse`, converts stored score with `str(...)`, omits null optional fields, and returns the shared success envelope. It never commits.
7. Rubric is not queried or returned because no response field or legacy assignment-rubric relation is source-backed.

## Linked API review

- API #54 returns the selected IDs through the DERIVED `Page<Submission>` list fallback; API #55 receives one `submission_id` and returns the same reusable Submission fields.
- API #54 and #55 use the same constrained URL/owner/purpose/course file lookup. API #35 producer compatibility is still unverified.
- API #56 remains the separate grade/status mutation and API #57 the separate feedback mutation; #55 does not mutate either field.
- `Submission.score`, `status`, `submitted_at`, and optional-field serialization remain subject to the open DD/schema questions. No rubric item payload is inferred from API #56's unresolved string field.

## Verification

| Check | Result | Status |
|---|---|---|
| API #55 TestClient suite | 22 passed; one upstream Starlette/httpx deprecation warning | VERIFIED_LOCAL |
| Full Study Server suite | 483 passed; one upstream Starlette/httpx deprecation warning | VERIFIED_LOCAL |
| Ruff | All checks passed for API #55 module/route/middleware/tests | VERIFIED_LOCAL |
| OpenAPI | 26 `/api/v1` operation declarations / 25 unique path templates; #55 GET response envelope and signed-int64 path present | VERIFIED_LOCAL |
| DD/context static checks | Eight expected sheets, byte-identical Excel appendix suffixes, JSON examples, local links, fences, whitespace, and `git diff --check` pass. Context validator reports repository-wide db-admin structure gaps and dirty-source drift; details in `VERIFICATION_REPORT.md`. | VERIFIED_STATIC / BLOCKED_BY_REPOSITORY_BASELINE |
| Live PostgreSQL/schema/deployment | Not checked | NOT_VERIFIED |

## Remaining discrepancies

- AC-23 rubric projection cannot be implemented against the catalog `Submission` type and the inspected legacy schema; domain/schema/contract confirmation is required.
- Direct-owner access, malformed-path 404, orphan-integrity 500 and file matching are DERIVED fallbacks, not approved business/schema facts.
- Assigned-Mentor access, API #35 file URL compatibility, live nullability, timestamp zone and score/status semantics remain open.

The API DD stays `Draft — Needs Confirmation`; local source and tests prove only the implemented catalog `Submission` response and the branches listed above.
