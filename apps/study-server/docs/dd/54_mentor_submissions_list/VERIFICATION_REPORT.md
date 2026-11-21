# Verification Report — Study API #54 Lấy submissions Mentor

**Result:** VERIFIED_WITH_OPEN_QUESTIONS
**DD status:** Draft — Needs Confirmation
**Runtime status:** Source-backed and HTTP-tested with a fake database session.

## Source coverage

| Source | Result |
|---|---|
| API catalog and reusable schemas | Method, path, filters, success/error codes, `Submission`, `Page`, `Pagination` and `UploadAsset` reviewed. The original singular response conflicts with AC-23 list/select. |
| AC-23 index and diagram | Reviewed the Mentor list → select submission → API #55 detail → #56 grade → #57 feedback flow. Response cardinality was changed to `Page<Submission>` as the user's requested fallback; this remains DERIVED. |
| DB guide, ERD and checked-in legacy DDL | Candidate `assignment_submissions → assignments → courses` path and nullable legacy foreign keys reviewed. DDL is not live-schema evidence. |
| API #34 upload source and migration | `uploads` exposes owner, purpose, course, URL and metadata; `SUBMISSION` is a supported purpose. There is no submission-upload foreign key. |
| API #35/#36 and #55–#57 DDs | File-reference producer ambiguity, Student detail, Mentor detail/rubric, grade and feedback sequence reviewed. API #35 does not guarantee that `file_url` stores the API #34 URL. |
| Current Study runtime | API #54 route, role-aware `MENTOR` guard, design-contract middleware mapping, read-only view orchestration and SQL constants reviewed. |

## Selected fallback behavior

| Item | Behavior | Evidence/status |
|---|---|---|
| Response | `ApiEnvelope<Page<Submission>>` | DERIVED from AC-23 list/select; catalog and diagram now match the implementation. |
| Pagination | `page=1`, fixed size 20, `submitted_at DESC, id DESC`, `data.pagination` | DERIVED from the existing Study pagination shape. |
| Mentor access | Numeric JWT subject must equal `courses.mentor_id` | Follows current Mentor APIs #46/#49; assigned Mentor access is not represented. |
| Submitted files | At most one asset, matched by exact `file_url`, owner, `SUBMISSION` purpose and course | DERIVED; no FK or API #35 producer guarantee. No match returns `files: []`. |
| Missing course | Empty page; an existing course owned by another Mentor returns 403 | Keeps the catalog error set, which has no 404 for this endpoint. |
| 409 | Declared in the diagram/catalog; no runtime trigger | No conflict condition is defined in AC-23. |
| Invalid query | Positive int64 `course_id`, positive int32 `page`, 422 validation error | Added to the catalog/diagram and covered by route tests. |

## Verification

| Check | Result |
|---|---|
| Focused API TestClient suite | 12 passed. Covers authentication/role, owner scope, filters and pagination, empty results, upload matching, malformed projection, safe DB errors, query bounds and OpenAPI. Uses fake DB data. |
| Full Study suite | 461 passed; one upstream Starlette/httpx TestClient deprecation warning. |
| Ruff | Passed for API #54 module, route, middleware and tests. |
| Route/OpenAPI | `GET /api/v1/mentor/submissions` is composed; its query and page response schema are asserted by the focused test. |
| Template appendix preservation | All eight API #54 template sheets retain appendix suffixes identical to the checked-in baseline. Supplemental report files are not template sheets. |
| Context validation | Node is unavailable. `deno run -A scripts/validate-agent-context.mjs` returns `AGENT_CONTEXT_INVALID` for existing missing db-admin context/source paths and links, plus source drift in the dirty worktree. With `--skip-drift`, only the db-admin context/source errors remain; no API #54 path is missing. |
| Documentation links/XML/whitespace | 97 relative DD links resolve; AC-23 draw.io XML parses; `git diff --check` passes. |
| Live PostgreSQL/schema/deployment | Not verified. Fake sessions and checked-in DDL do not prove live behavior. |

## AC-23 macro-review #35/#36 and #54–#57

- API #54 now returns a collection so the UI can select an ID for API #55. The response change is a DERIVED fallback and still needs contract-owner confirmation.
- API #34 stores upload metadata, but API #35's `file_refs` encoding and persistence into `assignment_submissions.file_url` remain unresolved. The URL lookup must not be treated as a confirmed producer contract.
- API #55 now reuses the same constrained file lookup and the reusable `Submission` response shape; rubric remains unresolved because the response schema and legacy assignment tables do not define a usable relation.
- APIs #56 and #57 remain separate mutations. Their future `Submission` responses can follow the #54 file fallback, but no shared resolver or runtime implementation exists yet. Feedback attachments remain separate from student-submitted files.
- Current shared auth supports explicit `MENTOR`; API #55 now uses it with a DERIVED direct-owner fallback. APIs #56/#57 still need their own access checks. Direct-owner policy does not cover assigned Mentors.

## Remaining questions

- Confirm the `Page<Submission>` contract, fixed size/order, and added 422 outcome.
- Confirm how API #35 persists file references and whether it stores the exact API #34 URL.
- Confirm assigned-Mentor access, submission status lifecycle, 409 trigger, null/orphan behavior and timestamp timezone policy.
- Verify the live schema and migrations before claiming deployment readiness.
