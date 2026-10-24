# OPEN_QUESTIONS — Study API #98

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/discussions/{discussion_id}`

## Q-98-01 — Discussion report relation and identity

**Evidence:** AC-37 diagram node n5 reads discussion/comments/reports. Legacy DDL has only `discussions`; there is no report table/key.

**Impact:** The service cannot resolve which report records belong to the path Discussion or load report details without inventing schema.

**Decision needed:** Identify approved report relation, keys, report state, timestamps, uniqueness and linkage to root/reply discussions.

## Q-98-02 — Report detail in the response

**Evidence:** AC-37 asks for report detail; catalog returns `Page<Discussion>`, whose reusable schema has no reason, severity, reporter, report count or report timestamp. The generic `Report` schema is analytics for AC-38.

**Impact:** Required report data cannot be returned to the moderation UI under the current response contract.

**Decision needed:** Approve a DiscussionReport response/extension in catalog or identify an explicitly supported consumer outside this API response before implementation.

## Q-98-03 — Is path ID always a thread root?

**Evidence:** API #42 DD proposes root-only `discussion_id` plus direct children. AC-37 and #97 catalog do not specify whether reports can target replies.

**Impact:** A report on a reply may require parent/root context, while a root-only lookup may return 404 or incomplete thread.

**Decision needed:** Confirm root-only IDs, target row IDs with parent context, or another policy; coordinate with #97 queue grain.

## Q-98-04 — Comment scope and moderation visibility

**Evidence:** `Discussion.comments[]` is in response; #42 proposes direct ACTIVE children for Student visibility. AC-37 is Admin moderation and may need hidden/locked items.

**Impact:** Copying Student visibility could hide evidence needed for moderation; nested replies, ordering and missing-author behavior are not specified.

**Decision needed:** Confirm direct/all nested comments, status inclusion, stable order and required-author integrity policy. Do not inherit the Student ACTIVE filter by default.

## Q-98-05 — Discussion title and nullable relations

**Evidence:** Reusable Discussion requires `title`; legacy DDL has no title. Legacy `course_id` and `user_id` are nullable although response fields are required.

**Impact:** Complete Discussion projection may be impossible or require an unapproved schema/serialization rule.

**Decision needed:** Identify title source and canonical FK/null-integrity policy; do not derive title from content.

## Q-98-06 — Page metadata for detail

**Evidence:** Response is `Page<Discussion>` with required PageMeta; request has only path `discussion_id`.

**Impact:** The catalog does not define item cardinality or page metadata values.

**Decision needed:** Confirm the DERIVED one-item wrapper used by #42: page=1, size=1, total=1, total_pages=1.

## Q-98-07 — Admin authentication and scope

**Evidence:** Catalog requires Admin. Study shared current-user guard accepts Student only; no Admin guard/claim policy is source-backed.

**Impact:** Authentication, authorization scope and 403/404 concealment cannot be implemented from current helper.

**Decision needed:** Identify approved Admin token/claims, role spelling, and any permission or tenant restriction.

## Q-98-08 — Path parsing and error mapping

**Evidence:** Catalog includes 404 but omits 422. Current middleware allowlist excludes #98; generic fallback business codes differ from catalog.

**Impact:** Invalid/overflow path values or unhandled exceptions may produce undocumented codes if wired without integration changes.

**Decision needed:** Confirm malformed path behavior and update approved error integration without silently adding catalog codes.
