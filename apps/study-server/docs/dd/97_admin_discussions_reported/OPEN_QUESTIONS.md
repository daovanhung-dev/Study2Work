# OPEN_QUESTIONS — Study API #97

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/discussions/reported`

## Q-97-01 — Report persistence and join key

**Evidence:** AC-37 diagram node n3 reads reports + discussion summary. Legacy Study DDL only defines `discussions`; it has no discussion-report relation or join key.

**Impact:** The queue predicate and physical Q1 cannot be implemented without guessing a table or relationship.

**Decision needed:** Identify the approved report source, primary key, discussion foreign key, state, timestamps, uniqueness/grain and indexes.

## Q-97-02 — Queue grain and duplicate reports

**Evidence:** Catalog returns `Page<Discussion>` while the source diagram reads report records.

**Impact:** It is unknown whether one queue item represents one report or one unique discussion when several users report the same discussion. `pagination.total` changes with that decision.

**Decision needed:** Confirm report-vs-discussion grain, deduplication rule and stable ordering.

## Q-97-03 — Report data in the response

**Evidence:** AC-37 queue reads report information, but reusable `Discussion` has no report reason, severity, count, reporter or report timestamp fields.

**Impact:** Admin cannot see the report data used to filter the queue in the current response contract.

**Decision needed:** Keep `Page<Discussion>` and define a supported source/consumer for report summary, or approve a catalog schema change before implementation.

## Q-97-04 — `reason` and `severity` semantics

**Evidence:** Catalog only declares optional strings.

**Impact:** Allowed values, normalization, comparison, unknown-value behavior and whether both filters combine with AND/OR are not defined.

**Decision needed:** Approve taxonomy and matching/composition rules; do not infer enums from the query names.

## Q-97-05 — Pagination and ordering

**Evidence:** Request declares only `page?:int32`; `PageMeta` requires page, size, total and total_pages.

**Impact:** Default, positive range, page size, out-of-range response, count grain and deterministic order are open.

**Decision needed:** Confirm pagination contract. A page default of 1, fixed size 20 and `ceil(total/size)` are only DERIVED proposals from other Admin list DDs, not approved here.

## Q-97-06 — `Discussion.title` and candidate columns

**Evidence:** Reusable Discussion requires title; legacy `discussions` DDL has content but no title. Legacy course/user foreign keys are nullable although the response requires `course_id` and `author`.

**Impact:** Candidate projection cannot populate every required response field or safely handle missing relations.

**Decision needed:** Identify approved title and null-integrity policy; do not derive title from content.

## Q-97-07 — Comment projection in a queue summary

**Evidence:** Discussion schema requires `comments[]`; AC-37 calls the queue item a summary and API #98 separately reads full thread detail.

**Impact:** Comment inclusion, preview size, nested depth, status filter, order and author-failure behavior are unknown.

**Decision needed:** Confirm whether #97 returns no comments, a bounded summary, all direct children or another approved shape; update contract if needed.

## Q-97-08 — Admin authentication and scope

**Evidence:** Catalog requires Admin. Current Study shared guard only authorizes Student; no Admin guard, claim mapping or policy is source-backed.

**Impact:** Authorization and 401/403 ordering cannot be implemented from current Study helper.

**Decision needed:** Identify approved Admin credential/claims, role spelling and any scope/tenant rule.

## Q-97-09 — Query parse and envelope mapping

**Evidence:** Catalog omits 422. Current middleware allowlist excludes this path; generic fallback uses different business codes. Current error helper serializes absent data as `{}`, while API guidelines describe `null`.

**Impact:** Future route wiring can produce unsupported validation/internal codes or an envelope shape mismatch.

**Decision needed:** Resolve invalid query behavior and include #97 in approved error integration when implemented, without silently adding catalog codes.
