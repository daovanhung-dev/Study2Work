# SPEC — Chuyển quyết định QA vào code cho Study APIs #21–#25

## Metadata

- Task: `2026-11-15-study-api-21-25-qa-implementation`
- Scope owner: Study Server
- Input: developer request in chat to implement QA decisions for APIs #21–#25, followed by explicit decisions recorded in the conversation on 2026-11-15.
- Related QA evidence: `.agents/worklog/2026-11-15/study-api-21-25-qa-verification.md`.
- Live DB evidence: `.agents/worklog/2026-11-15/study-api-21-25-live-schema-audit.md`; schema `nguyen_anh_duc`; metadata query read-only; duplicate-pair aggregate query returned 0 non-NULL duplicate `(user_id, lesson_id)` pairs.
- Current source and tests: `apps/study-server/app/modules/guest/api_21_users_me_progress` through `api_25_lessons_progress`, `apps/study-server/app/api/v1.py`, matching test modules, and `apps/study-server/docs/dd/21_*` through `25_*`.
- Approval: `PENDING`; approver and exact SHA256 to be recorded after review.

## Scope and exclusions

### In scope

- API #21: align the response contract with the existing model/SQL by omitting `bio`; retain the current profile-shaped response and current handling of `course_id`/`aggregate`.
- API #22: require the parent course to have `courses.status = 'PUBLISHED'`; preserve the current enrollment eligibility of `ACTIVE` or `COMPLETED`; do not add prerequisite checks.
- API #23: enforce at most one non-NULL `(user_id, lesson_id)` progress row with a unique database key and make start-progress writes use PostgreSQL UPSERT. Preserve the current behavior of not demoting an existing `COMPLETED` progress row when a lesson is started again.
- API #24: retain its current checks requiring both Lesson and Course to be `PUBLISHED`, plus enrollment status `ACTIVE` or `COMPLETED`; do not add prerequisite checks.
- API #25: remove `position` from the request model/contract; do not add a database column. Validate `percent` within 0..100. Treat each valid request as the new progress state: `completed=true` sets `COMPLETED`; `completed=false` sets `IN_PROGRESS` and clears `completed_at`.
- Update only the affected DD sections and Study Server context needed to reflect implemented behavior.
- Add a schema-qualified migration source for the unique key. All DDL in that source must explicitly target `nguyen_anh_duc`.

### Out of scope

- No change to API #21's overall profile-shaped response, aggregation semantics, selectors, or `users` lifecycle filtering.
- No prerequisite model/table/query.
- No enrollment unique key.
- No `position` storage/resume feature and no new column for it.
- No cleanup or deletion of application rows. The observed duplicate count is zero, but the migration must fail safely if a duplicate pair appears before migration application.
- No live DB DDL/migration application or data mutation in this task; deliver migration source only.
- No edits to unrelated dirty files. No push, merge, or PR actions.

## Expected behavior and current behavior

| API | Expected behavior from developer decisions | Current source behavior | Discrepancy |
|---:|---|---|---|
| #21 | `bio` is not part of this response because the live `users` table has no such column; retain current response shape. | Current local model and SQL already omit `bio`; DD response still lists `data.bio`. | DD-only stale field; no runtime code change needed for `bio`. |
| #22 | Allow access only when parent Course is `PUBLISHED` and the learner has `ACTIVE` or `COMPLETED` enrollment. No prerequisite check. | Checks enrollment states, but does not read/check Course publication. | Add Course status lookup/check. |
| #23 | A learner/lesson pair has one progress row; concurrent starts are race-safe. | SELECT-then-INSERT/UPDATE; live DB has no pair unique key; observed current non-NULL duplicate pair count is 0. | Add unique key in a target-schema migration and use `INSERT ... ON CONFLICT ... DO UPDATE`. |
| #24 | Preserve checks for published Lesson and published Course, enrollment `ACTIVE`/`COMPLETED`; no prerequisite check. | Current source already implements these checks. | Behavior already matches; update only stale DD/context if necessary. |
| #25 | Request contains `percent` and `completed`, no `position`; percent 0..100; latest request controls active/completed state and completion timestamp remains consistent. | `position` is required but unused; percent is unbounded; status follows `completed`, but a false request leaves the old `completed_at`. | Remove field, add range validation, clear timestamp on reset. |

## Requirements and acceptance criteria

### REQ-21-01 — No nonexistent `bio` in #21 response contract

- Evidence: developer decision in chat; live schema audit confirms `users` has no `bio`; current #21 model and query omit it.
- Acceptance: #21's relevant DD response no longer advertises `data.bio`. No profile aggregate behavior or selector semantics are changed.

### REQ-22-01 — Course publication gate

- Evidence: developer decision in chat.
- Acceptance: #22 returns its existing not-found response when the Lesson is missing/unattached or its parent Course is not `PUBLISHED`; a published Course proceeds to the existing enrollment check. Enrollment `ACTIVE` and `COMPLETED` remain accepted. No prerequisite check is added.
- Failure/side effects: read-only endpoint; no write/transaction is introduced.

### REQ-23-01 — Unique learner/lesson progress row

- Evidence: developer decision in chat; live schema audit shows no unique pair key and 0 duplicate non-NULL pairs at audit time.
- Acceptance: migration source creates a unique key on `lesson_progress(user_id, lesson_id)` explicitly inside `nguyen_anh_duc`. No other schema is modified. Do not include row cleanup.

### REQ-23-02 — Race-safe start progress

- Evidence: developer decision in chat; AC-14 says UPSERT; current source performs SELECT then INSERT.
- Acceptance: #23's write uses PostgreSQL `INSERT ... ON CONFLICT (user_id, lesson_id) DO UPDATE`; only the status behavior already established by current source is retained, including preserving `COMPLETED`. Existing HTTP response/status behavior remains unchanged.

### REQ-24-01 — Preserve confirmed publication and enrollment rules

- Evidence: developer decision in chat and current #24 source.
- Acceptance: #24 continues to require Lesson and Course `PUBLISHED` and enrollment `ACTIVE` or `COMPLETED`. No prerequisite logic is introduced.

### REQ-25-01 — Remove unused position

- Evidence: developer decision in chat; live schema has no position column; current code ignores the field.
- Acceptance: `position` is absent from the declared #25 request model and updated DD request. No DB column or position-related persistence is added. Other extra fields follow the request model's existing extra-field behavior.

### REQ-25-02 — Validate progress percent

- Evidence: developer decision in chat and meaning of the `percent` field.
- Acceptance: values below 0 or above 100 receive the existing 422 validation envelope/business code. Values 0 and 100 are accepted. No database CHECK constraint is added by this task.

### REQ-25-03 — Latest request controls completion state

- Evidence: explicit developer decision in chat: a completed lesson is handled like active progress on a new update.
- Acceptance: on each valid update, `completed=true` sets status `COMPLETED` and sets `completed_at` if absent; `completed=false` sets status `IN_PROGRESS` and clears `completed_at`. The submitted percent is stored as supplied after range validation; it is not coupled to the boolean.

## Data and compatibility effects

- Runtime DB changes are not applied by this task. A schema-qualified migration is delivered for later application only in `nguyen_anh_duc`.
- The live duplicate check was read-only and returned zero non-NULL duplicate pairs. Recheck at migration application if the data can change before deployment; do not resolve any duplicates automatically.
- #25 request contract drops the unused required `position` field. Clients may still send it as an unknown field according to current `extra='ignore'` model behavior; it is no longer declared or persisted.
- All existing routes and response envelope/business codes remain in place. #22 adds a publication gate using its existing not-found branch.

## Impact map

- Direct code: `app/modules/guest/api_21_users_me_progress` contract docs; `api_22_lessons_access/query.py`, `view.py`; `api_23_lessons_start/query.py`, `view.py`; `api_25_lessons_progress/models.py`, `validate.py`, `query.py`; `app/api/v1.py` only if route metadata must reflect the request change.
- Schema artifact: new migration under `infra/postgres/study-server/migrations/`, explicitly schema-qualified to `nguyen_anh_duc`.
- DD: narrowly update the affected response/request/data-mapping/table and open-question sections for #21–25.
- Consumers: #22/#23/#24/#25 are routed through `app/api/v1.py`; update API #25 tests that send `position`; #23 focused tests must cover insert/conflict path via query contract or fake-session behavior.
- Context: update stale Study Server route/module/database summaries only where they contradict current behavior.
- Tests: focused existing modules are under `apps/study-server/tests/modules/guest/api_21_users_me_progress` through `api_25_lessons_progress`; planned cases belong in PLAN. Actual test edits/runs require the approved PLAN and remain pending at SPEC stage.

## Known limitations

- The five DD packages remain Draft; this SPEC records the developer's direct decisions for the selected behavior and does not claim the rest of each DD is complete.
- The live schema metadata and duplicate aggregate are point-in-time evidence; no migration application or runtime integration test has been performed.
- API #21 remains profile-shaped and still ignores selectors; this is preserved by explicit decision, not asserted to implement course aggregation.

## Approval

- Status: `PENDING_APPROVAL`
- Approver: pending
- Approved revision SHA256: pending
- Decision date: pending
