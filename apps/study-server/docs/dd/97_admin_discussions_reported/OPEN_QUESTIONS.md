# OPEN_QUESTIONS — Study API #97

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/discussions/reported`

Implementation uses the local `DERIVED` fallbacks below. These choices keep the
catalog response shape and make the route testable; they are not proof of live
schema, deployment, policy approval or report ingestion.

## Resolved locally with `DERIVED` fallbacks

| Topic | Current fallback | Remaining verification |
|---|---|---|
| Report source and join | Study `discussion_reports`; `discussion_id BIGINT` references `discussions.id` with `ON DELETE RESTRICT` | Migration deployment and report writer are not verified; no report-ingest API is in #97 scope; API #100 must preserve/reconcile reports before hard delete |
| Queue grain | One unique Discussion with at least one `OPEN`/`IN_REVIEW` report | Cross-endpoint moderation transition for #99 remains future work |
| Query filters | Exact `reason_code` and `severity`; both combine with AND on the same report | Allowed values/taxonomy are free-form and remain unspecified |
| Pagination | Page defaults to 1, size 20, latest matching report first then Discussion ID descending; total counts unique Discussions | Catalog omits defaults/order; this fallback needs product confirmation |
| Discussion title | Normalized Discussion content clipped to 120 characters | No physical `title` column exists in legacy schema |
| Comments | Queue summary returns `comments=[]`; #98 owns full thread | If Admin list requires previews, response contract/design must be revised |
| Invalid page | 422 `DESIGN_VALIDATION_ERROR` | Catalog lists only 401/403/500; this is a local validation fallback |
| Admin authorization | Shared `validate_current_user_request(..., role="ADMIN")` | Fine-grained AC-37 permission/tenant policy and live issuer remain unverified |

## Q-97-01 — Report ingestion and live persistence

**Evidence:** The local fallback migration adds `discussion_reports`, but Study
has no report-create endpoint in the current catalog/runtime.

**Impact:** The queue can read rows written by a future/approved producer, but
this endpoint alone does not create reports. Checked-in DDL does not prove the
table is present in a deployed database.

**Follow-up:** Identify the approved report producer and verify migration/live
schema before deployment.

## Q-97-02 — Report details in the response

**Evidence:** AC-37 says the Admin reads reports, while catalog #97 returns
`Page<Discussion>` without report reason, severity, count, reporter or report
time fields.

**Impact:** Filters work, but the list response does not expose the report
metadata. #98 currently has the same reusable Discussion response shape.

**Follow-up:** If the UI needs report metadata, revise the catalog/schema for
#97/#98; implementation does not add unlisted fields.

## Q-97-03 — Legacy required-field integrity

**Evidence:** Legacy `discussions.course_id` and `user_id` are nullable although
the reusable `Discussion` requires `course_id` and `author`.

**Impact:** A report linked to a Discussion with missing course/author/status
returns 500 `DESIGN_INTERNAL_ERROR` instead of fabricating response values.

**Follow-up:** Confirm live FK integrity and decide whether these columns should
be made non-null in the authoritative schema.
