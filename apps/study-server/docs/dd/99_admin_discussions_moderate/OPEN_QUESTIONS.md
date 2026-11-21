# OPEN_QUESTIONS — Study API #99

**Status:** Draft — Needs Confirmation
**Endpoint:** `PATCH /api/v1/admin/discussions/{discussion_id}/moderate`

## Q-99-01 — Action tokens and casing

**Evidence:** Catalog declares `action:string!`; AC-37 names the logical choices ẩn/khóa/cảnh báo but gives no request tokens or casing.

**Impact:** Request validation and stable client contract cannot be implemented.

**Decision needed:** Approve the exact action enum/token values, casing, compatibility policy and behavior for unknown values. `hide|lock|warn` are only `DERIVED` examples.

## Q-99-02 — State transitions and warning behavior

**Evidence:** AC-37 says “UPDATE moderation state + audit”; legacy `discussions.status` is `VARCHAR(20)` with default `ACTIVE`, but no moderation enum or transition table is defined.

**Impact:** The service cannot determine the stored state for each action or whether the discussion remains visible/usable.

**Decision needed:** Define the before-state eligibility and after-state for hide/lock; clarify whether warn changes state, emits a separate notice, or only records a warning audit.

## Q-99-03 — Audit persistence and transaction boundary

**Evidence:** AC-37 requires audit. Legacy Study DDL has no audit relation. Pilot `admin_adjustments` and `audit_events` use UUID/versioned subject/resource identifiers and are not mapped to the legacy BIGINT Discussion model.

**Impact:** Actor, action, reason, before/after state, trace, retention and atomicity cannot be persisted from current evidence.

**Decision needed:** Select the deployed schema/table and required audit fields; decide whether state update and audit append must commit atomically and how audit failure affects the response.

## Q-99-04 — Admin identity and authorization

**Evidence:** Catalog requires Admin Bearer JWT. Current Study helper `validate_current_user_request` enforces Student; no Admin guard/claim policy is present.

**Impact:** Authentication, role checks and audit actor mapping lack a source-backed implementation path.

**Decision needed:** Define trusted Admin token/role claims, subject-to-actor mapping and any permission or tenant scope.

## Q-99-05 — Discussion target grain

**Evidence:** API #97 queue and #98 detail do not establish whether a report targets a root discussion or reply. Legacy `parent_id` is nullable.

**Impact:** The path ID could identify a reply or a root; response/thread scope and not-found behavior may differ.

**Decision needed:** Confirm which Discussion IDs #99 accepts and how moderation of a reply affects its root/thread.

## Q-99-06 — Page response semantics

**Evidence:** Catalog requires `Page<Discussion>` but the #99 request has no page/size. API #42 and #98 use a one-item Page only as a design proposal.

**Impact:** `items` membership and `pagination` values are not determined by the request or mutation result.

**Decision needed:** Confirm whether the response contains exactly the updated Discussion and approve `page=1`, `size=1`, `total=1`, `total_pages=1`, or define another mapping.

## Q-99-07 — Complete Discussion projection

**Evidence:** Reusable `Discussion` requires `title`, `course_id`, `author` and `comments`. Legacy DDL has no title and allows nullable `course_id`/`user_id`; report details also have no relation.

**Impact:** The required response cannot be built safely from legacy DDL alone. The action reason/audit data is not present in `Discussion` schema.

**Decision needed:** Select the authoritative schema/projection for title, nullable references and Admin comment visibility; do not add report, reason or audit fields without a catalog change.

## Q-99-08 — Input validation and error mapping

**Evidence:** Catalog includes 422 `DESIGN_VALIDATION_ERROR` but gives no action/reason constraints; malformed path behavior is not stated. Current middleware design-code allowlist excludes #99.

**Impact:** Exact validation errors and future business-code mapping remain unknown.

**Decision needed:** Define only approved action/reason constraints and malformed int64 mapping; wire #99 into the current design-code path handling when implementation is approved, without adding codes.

## Q-99-09 — Optional delete transition

**Evidence:** AC-37 places “Cần xóa nội dung?” after #99 and routes YES to API #100.

**Impact:** Combining delete into #99 would violate the documented flow and make the action contract ambiguous.

**Decision needed:** Keep delete as a separate #100 request; coordinate moderation state and audit policy with #100 before implementation. The #97–#100 macro-review is complete and records the remaining gaps in [API #100 plan result](../100_admin_discussions_delete/PLAN_RESULT.md).
