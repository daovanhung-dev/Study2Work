# OPEN_QUESTIONS — Study API #40

**Status:** Draft — Needs Confirmation
**Endpoint:** `POST /api/v1/discussions`

## Q-01 — Request content type and representation

**Evidence:** API #40 catalog row and AC-19 declare `content:int64!`. The reusable `Discussion` schema declares `content:string`; `DB_UNICA_TABLES.md` and checked-in `DB.sql` declare `discussions.content TEXT`.

**Impact:** Request validation, storage representation, and response mapping need an approved meaning/conversion rule. This DD proposes a base-10 decimal string as DERIVED.

**Decision needed:** Confirm the intended meaning/type or approve the DERIVED base-10 decimal-string conversion. Keep catalog `int64`, reusable `string`, and DDL `TEXT` discrepancy explicit until decided.

## Q-02 — Physical storage for required title

**Evidence:** API #40 request and reusable `Discussion` require `title:string`. The discussion ERD and checked-in DDL have no `discussions.title` column; API #39 DD records the same gap.

**Impact:** A required request field cannot be persisted or read back from the documented physical schema.

**Decision needed:** Identify an approved physical source or update the schema contract. Do not derive title from content.

## Q-03 — Create response uses `Page<Discussion>`

**Evidence:** API #40 declares HTTP 201 with `ApiEnvelope<Page<Discussion>>`, while request has no page input. `PageMeta` requires `page`, `size`, `total`, and `total_pages`.

**Impact:** The response still needs a defined item and PageMeta policy.

**Decision needed:** Confirm the DERIVED proposal to return one created root with page=1, size=1, total=1, total_pages=1; otherwise update the approved contract or define its intended page shape.

## Q-04 — Course participation/access predicate

**Evidence:** AC-19 precondition requires a logged-in Student with permission to participate in the course discussion. API #40 declares 403; DDL defines enrollment user/course/status fields. API #39/#41/#42 use the same provisional ACTIVE enrollment proposal.

**Impact:** Authorization cannot be implemented consistently; course existence and access failure mapping are not distinguished.

**Decision needed:** Confirm or replace the DERIVED proposal requiring enrollment status ACTIVE for this principal and course_id. Define behavior for missing or inaccessible courses; no ownership or publication rule is proposed.

## Q-05 — Discussion status and visibility for new topics

**Evidence:** `Discussion` requires `DiscussionStatus`; the DB guide describes status as visibility/moderation. Checked-in DDL defaults `status` to `ACTIVE`, but the enum and creation policy are absent.

**Impact:** The insert status and whether a new topic is public, hidden, or moderated cannot be determined.

**Decision needed:** Confirm or replace the DERIVED proposal to create a new topic with status ACTIVE; define the complete enum and visibility policy. The DDL default alone is not approval.

## Q-06 — Required timestamps and transaction behavior

**Evidence:** Checked-in DDL marks `created_at` and `updated_at` NOT NULL without defaults. No API #40 source or approved mapping specifies timestamp values or transaction ownership.

**Impact:** The candidate insert has required columns without an approved value source, and failure rollback behavior is unknown.

**Decision needed:** Confirm or replace the DERIVED proposal to set created_at and updated_at from one server timestamp; separately define transaction/rollback behavior.

## Q-07 — `course_id` and `user_id` nullability

**Evidence:** DB guide/ERD describe course and author relations as required, while checked-in DDL permits both columns to be NULL. Live schema was not checked.

**Impact:** Candidate insert and required response relations may behave differently across design documents and the physical schema.

**Decision needed:** Confirm the canonical nullability and whether live schema matches the checked-in DDL.

## Q-08 — Author and comments in create response

**Evidence:** `Discussion` requires `author:UserSummary` and `comments:DiscussionComment[]`. Current JWT claims expose principal ID/roles, not profile fields. AC-19 routes reloading topic plus comments to API #42.

**Impact:** The author lookup is undefined; comments and page semantics are provisional.

**Decision needed:** Confirm the proposal to resolve author from `users`, return `comments: []` for a new root and keep API #42 as the thread reload. Do not assume the access token contains profile data.
