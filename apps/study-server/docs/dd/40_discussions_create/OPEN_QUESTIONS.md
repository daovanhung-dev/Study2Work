# OPEN_QUESTIONS — Study API #40

**Status:** Draft — Needs Confirmation
**Endpoint:** `POST /api/v1/discussions`

## Q-01 — Request content type and representation

**Evidence:** API #40 catalog row and AC-19 declare `content:int64!`. The reusable `Discussion` schema declares `content:string`; `DB_UNICA_TABLES.md` and checked-in `DB.sql` declare `discussions.content TEXT`.

**Impact:** Request validation, storage representation, and response mapping cannot be implemented consistently without a conversion rule.

**Decision needed:** Confirm the intended type and meaning of request `content`, and whether the approved catalog, reusable schema, or database design should change. This DD preserves the catalog `int64` value and does not invent a cast.

## Q-02 — Physical storage for required title

**Evidence:** API #40 request and reusable `Discussion` require `title:string`. The discussion ERD and checked-in DDL have no `discussions.title` column; API #39 DD records the same gap.

**Impact:** A required request field cannot be persisted or read back from the documented physical schema.

**Decision needed:** Identify an approved physical source or update the schema contract. Do not derive title from content.

## Q-03 — Create response uses `Page<Discussion>`

**Evidence:** API #40 declares HTTP 201 with `ApiEnvelope<Page<Discussion>>`, while request has no page input. `PageMeta` requires `page`, `size`, `total`, and `total_pages`.

**Impact:** The response cannot be populated without defining the page shape and values for a newly created topic.

**Decision needed:** Confirm whether create returns the `Page<Discussion>` contract as written and define its pagination values, or update the approved contract. This DD preserves the current catalog.

## Q-04 — Course participation/access predicate

**Evidence:** AC-19 precondition requires a logged-in Student with permission to participate in the course discussion. API #40 declares 403 but does not define the access predicate. API #39 open questions also leave Student course access unresolved.

**Impact:** Authorization cannot be implemented consistently; course existence and access failure mapping are not distinguished.

**Decision needed:** Define the eligible Student/course relationship and the behavior for missing, unavailable, or inaccessible courses. Do not assume enrollment, ownership, or publication rules.

## Q-05 — Discussion status and visibility for new topics

**Evidence:** `Discussion` requires `DiscussionStatus`; the DB guide describes status as visibility/moderation. Checked-in DDL defaults `status` to `ACTIVE`, but the enum and creation policy are absent.

**Impact:** The insert status and whether a new topic is public, hidden, or moderated cannot be determined.

**Decision needed:** Confirm the allowed status values and initial state for a new topic. The DDL default is only a candidate, not approved API behavior.

## Q-06 — Required timestamps and transaction behavior

**Evidence:** Checked-in DDL marks `created_at` and `updated_at` NOT NULL without defaults. No API #40 source or approved mapping specifies timestamp values or transaction ownership.

**Impact:** The candidate insert has required columns without an approved value source, and failure rollback behavior is unknown.

**Decision needed:** Define timestamp generation and transaction/rollback behavior before implementation.

## Q-07 — `course_id` and `user_id` nullability

**Evidence:** DB guide/ERD describe course and author relations as required, while checked-in DDL permits both columns to be NULL. Live schema was not checked.

**Impact:** Candidate insert and required response relations may behave differently across design documents and the physical schema.

**Decision needed:** Confirm the canonical nullability and whether live schema matches the checked-in DDL.

## Q-08 — Author and comments in create response

**Evidence:** `Discussion` requires `author:UserSummary` and `comments:DiscussionComment[]`. Current JWT claims expose principal ID/roles, not profile fields. AC-19 routes reloading topic plus comments to API #42.

**Impact:** The author lookup, comments inclusion, and initial comments value in API #40's `Page<Discussion>` response are undefined.

**Decision needed:** Confirm whether API #40 returns the author profile and an empty comments list, or whether the client must call API #42 to load the thread. Do not assume the access token contains profile data.
