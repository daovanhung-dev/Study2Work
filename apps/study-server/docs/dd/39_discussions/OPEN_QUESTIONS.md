# OPEN_QUESTIONS — API #39

**Status:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/discussions

## Q-01 — Student access and omitted course_id

**Evidence:** API catalog requires Student Bearer JWT. AC-19 precondition says Student has permission to participate in a course discussion; API #39 allows course_id to be omitted.
**Impact:** The response scope and access predicate are unknown when one course is not specified. A broad list could expose discussions outside the Student's course access.
**Decision needed:** Define the course participation predicate and whether omitted course_id lists all accessible courses, requires a course context, or follows another bounded scope.

## Q-02 — Pagination and sort policy

**Evidence:** Request declares optional page and sort; response is Page<Discussion> with PageMeta.page, size, total, and total_pages. No request size, sort allowlist, default or range is defined.
**Impact:** Page boundaries, ordering, size, total count and stable pagination cannot be implemented consistently.
**Decision needed:** Define page default/range, fixed or configured page size, sort syntax/allowlist/direction/default/tie-break, and empty/out-of-range behavior. If a size input is required, update the approved catalog first.

## Q-03 — List item and comments boundary

**Evidence:** Reusable Discussion schema contains comments[]. AC-19 activity labels API #39 as the discussion list, while API #42 reads “topic + comments”.
**Impact:** Loading all child rows in the list can change payload size and pagination cost; omitting them may not satisfy the reusable response schema as written.
**Decision needed:** Confirm whether API #39 returns root threads only with empty/summary comments or embeds full child comments, and align the shared schema or API #42 contract.

## Q-04 — Public visibility and status values

**Evidence:** AC-19 says to read public discussions. DB guide describes discussions.status as a visibility/moderation field and checked-in DDL defaults it to ACTIVE; allowed status values and public filter are absent.
**Impact:** The list could include hidden/locked content or exclude valid threads if ACTIVE is assumed without approval.
**Decision needed:** Define public visibility statuses and whether locked, hidden, deleted, or reported rows appear to a Student.

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
