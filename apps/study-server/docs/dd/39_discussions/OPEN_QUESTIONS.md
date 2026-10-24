# OPEN_QUESTIONS — API #39

**Status:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/discussions

## Q-01 — Student access and omitted course_id

**Evidence:** API catalog requires Student Bearer JWT. AC-19 requires permission to participate in the course discussion; API #39 allows course_id to be omitted. The DB design includes enrollments with status.
**Impact:** The access predicate and omitted-course scope are not approved.
**Decision needed:** Confirm or replace the DERIVED proposal: require enrollment status ACTIVE for each returned course; when course_id is omitted, list only courses where the principal has an ACTIVE enrollment.

## Q-02 — Pagination and sort policy

**Evidence:** Request declares optional page and sort; response is Page<Discussion>. API #10 uses page=1 and fixed size=20, but API #39 does not define its own pagination or sort rules.
**Impact:** Page boundaries, ordering, size, total count and stable pagination cannot be implemented consistently.
**Decision needed:** Confirm the DERIVED proposal: page defaults to 1, fixed size=20, total_pages=ceil(total/20) (0 for empty), and sort accepts created_at_desc (default) or created_at_asc with id tie-break in the same direction. Define malformed/out-of-range handling; update the catalog before adding a size input or new error code.

## Q-03 — List item and comments boundary

**Evidence:** Reusable Discussion requires comments[]. AC-19 assigns the list to API #39 and separately reloads “topic + comments” through API #42.
**Impact:** Returning comments in every list item can increase payload size and query cost.
**Decision needed:** Confirm the DERIVED proposal that #39 returns each root with all direct ACTIVE comments, ordered created_at ASC then id ASC, matching #42. Otherwise revise the shared schema or API #42 contract.

## Q-04 — Public visibility and status values

**Evidence:** AC-19 says to read public discussions. DB guide describes discussions.status as a visibility/moderation field and checked-in DDL defaults it to ACTIVE; allowed status values and public filter are absent.
**Impact:** The list could include hidden/locked content or exclude valid threads if ACTIVE is assumed without approval.
**Decision needed:** Confirm or replace the DERIVED proposal that only root discussions and direct comments with status ACTIVE are visible; define whether locked, hidden, deleted, or reported rows appear to a Student.

## Q-05 — Discussion title source

**Evidence:** Catalog requires Discussion.title:string; DB_UNICA_TABLES, DB_UNICA_ERD and checked-in DB.sql define no discussions.title column.
**Impact:** The response field cannot be populated from the documented physical schema.
**Decision needed:** Identify an approved source or update the schema/contract. Do not derive title from content without an explicit decision.

## Q-06 — Query parse and validation behavior

**Evidence:** course_id, page, and sort have typed/optional declarations, but API #39 catalog errors are only 401, 403 and 500 in addition to 200.
**Impact:** Malformed or out-of-range query values have no specified client error response.
**Decision needed:** Define parse/range handling. If 400/422 or another code is required, update the approved catalog before adding it to this DD.

## Q-07 — Discussion foreign-key nullability

**Evidence:** DB guide/ERD describe course_id and user_id as required relations; checked-in DB.sql permits NULL for both. Live database metadata has not been verified.
**Impact:** Candidate author/course joins may omit rows or conflict with required response fields.
**Decision needed:** Confirm canonical physical nullability and whether live schema differs from checked-in DDL.
