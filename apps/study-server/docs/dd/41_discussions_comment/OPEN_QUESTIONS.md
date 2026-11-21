# OPEN_QUESTIONS — Study API #41

**Status:** Draft — Needs Confirmation
**Endpoint:** POST /api/v1/discussions/{discussion_id}/comments

## Q-41-01 — content request/storage/response type

**Evidence:** API catalog and AC-19 declare request content:int64!; reusable DiscussionComment.content is string; checked-in DDL declares discussions.content TEXT.

**Impact:** The request value cannot be stored and returned as text without a conversion rule. This DD proposes decimal-string conversion as DERIVED.

**Decision needed:** Confirm the request type or approve integer-to-decimal-text conversion. Keep the catalog unchanged until the contract owner decides.

## Q-41-02 — Parent topic and nested replies

**Evidence:** The route uses {discussion_id}; the ERD/DB guide model replies with nullable self-referencing parent_id; AC-19 then reloads a topic plus comments through API #42.

**Impact:** The parent ID could refer to a root topic or another comment. Nested replies change thread reconstruction and API #42 behavior.

**Decision needed:** Confirm that #41 accepts only root topic IDs and inserts direct children (parent_id = discussion_id), or define nested-reply behavior.

## Q-41-03 — Course participation and topic visibility

**Evidence:** AC-19 precondition requires a Student permitted to participate in a course discussion. The checked-in DDL has enrollments.user_id/course_id/status with default ACTIVE and discussions.status with default ACTIVE, but the #41 contract/AC-19 do not define the access predicate or status policy.

**Impact:** The server cannot consistently decide access or whether a hidden/inaccessible topic returns 403 or 404.

**Decision needed:** Confirm or replace this DD's DERIVED proposal: require an ACTIVE enrollment for the parent course and an ACTIVE parent topic; also decide whether inaccessible topics are concealed as 404.

## Q-41-04 — Meaning of “update counters”

**Evidence:** AC-19 says INSERT Comment + update counters; DB guide, ERD, and checked-in DDL expose no counter field/table, and reusable Discussion/DiscussionComment schemas expose no count field.

**Impact:** There is no physical target or response field for a counter update.

**Decision needed:** Confirm that counters are calculated from child rows when reading the thread, or supply an approved counter field/table and update rule. This DD makes no persistent counter write.

## Q-41-05 — Success page and item semantics

**Evidence:** Catalog declares ApiEnvelope<Page<Discussion>>; the request has no page input. AC-19 calls API #42 after the comment is created, and #42 also returns Page<Discussion>.

**Impact:** Page size/count, item contents, comment inclusion, author projection and the purpose of the follow-up GET are not fully defined.

**Decision needed:** Confirm the proposal to return one root thread with all direct ACTIVE comments (including the new child, ordered created_at ASC then id ASC) and metadata 1/1/1/1; keep API #42 as the authoritative refresh, or specify the intended page/item shape.

## Q-41-06 — Required title and physical discussion fields

**Evidence:** Reusable Discussion requires title:string; DB guide, ERD, and checked-in DDL have no discussions.title. Checked-in DDL also permits nullable course_id/user_id, while the logical guide/ERD marks them required.

**Impact:** API #41's proposed updated-thread response cannot provide a complete Discussion from the checked-in table alone; insert behavior can vary with schema nullability.

**Decision needed:** Identify the approved title source and confirm canonical nullability/live schema. Do not derive title from content.

## Q-41-07 — Status and timestamps

**Evidence:** Checked-in DDL defaults status to ACTIVE, while created_at and updated_at are NOT NULL without defaults. Enum and timestamp source are not specified for API #41.

**Impact:** Insert defaults and response serialization need a defined policy.

**Decision needed:** Confirm use of ACTIVE and server-clock timestamps (with updated_at = created_at) for new replies.

## Q-41-08 — Comment ordering after insert

**Evidence:** AC-19 requires API #42 to reload the latest thread but does not define comment ordering or tie-break. API #42 DD proposes created_at ASC, id ASC.

**Impact:** UI ordering may differ for comments with equal or missing timestamps.

**Decision needed:** Confirm that API #41 response and API #42 reload both order comments by created_at ASC, id ASC.
