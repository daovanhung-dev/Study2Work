# PLAN — Implement QA decisions for Study APIs #21–#25

## Metadata and approval

- Task: `2026-11-15-study-api-21-25-qa-implementation`
- Base SPEC: [`SPEC.md`](./SPEC.md), approved SHA256 `589C723AD1697BFB13E37F46136D64564D8F2C3B8E6DD169483B960E77838FE0`.
- PLAN revision SHA256: pending calculation after file creation.
- Approval: `PENDING_APPROVAL`; approval authorizes implementation and the listed focused tests only after this exact PLAN revision is approved.
- Live DDL: excluded; migration source only. Any future application must target `nguyen_anh_duc` and be separately authorized.

## Dependency and deployment order

1. Recheck that migration preconditions still hold. The read-only audit returned 0 duplicate non-NULL `(user_id, lesson_id)` pairs. The migration itself must check duplicates again and raise without deleting rows if any now exist.
2. Add schema-qualified migration `019_lesson_progress_user_lesson_unique.sql`.
3. Change #23 SQL to use the unique conflict target and UPSERT. The migration must be applied to `nguyen_anh_duc` before deploying this application code; applying it is outside this PLAN.
4. Implement #22/#25 behavior, align affected DD/context, then run approved focused tests and inspect the scoped diff.

## Implementation steps

| Step | Weight | Requirements | Files/functions | Change and acceptance |
|---|---:|---|---|---|
| P01 — #22 publication gate | 15% | REQ-22-01 | `app/modules/student/api_22_lessons_access/query.py:FIND_LESSON_BY_ID`; `view.py:check_lesson_access`; `tests/modules/student/api_22_lessons_access/test_lessons_access.py` | Join Course and return `course_status`; return the existing 404 branch unless Course is `PUBLISHED`; retain `ACTIVE`/`COMPLETED` enrollment filtering and no prerequisite query. |
| P02 — #23 unique and UPSERT | 25% | REQ-23-01, REQ-23-02 | New `infra/postgres/study-server/migrations/019_lesson_progress_user_lesson_unique.sql`; `app/modules/student/api_23_lessons_start/query.py`; `view.py:start_lesson`; `tests/modules/student/api_23_lessons_start/test_lessons_start.py`; Study DB context | Migration checks target schema and duplicate pairs, then creates only `nguyen_anh_duc.lesson_progress(user_id, lesson_id)` uniqueness. Replace SELECT-then-write race with one `INSERT ... ON CONFLICT ... DO UPDATE`, preserving `COMPLETED` as current #23 does. Keep response 201/envelope unchanged. |
| P03 — #25 request and state update | 25% | REQ-25-01, REQ-25-02, REQ-25-03 | `app/modules/student/api_25_lessons_progress/models.py`; `validate.py:validate_lesson_progress_request`; `query.py:INSERT_LESSON_PROGRESS_STATE`, `UPDATE_LESSON_PROGRESS_STATE`; `view.py:update_lesson_progress`; `tests/modules/student/api_25_lessons_progress/test_lessons_progress.py` | Remove declared `position`; validate percent 0..100 through existing 422 response convention. Latest request controls status; `completed=false` writes `IN_PROGRESS` and clears `completed_at`; true writes `COMPLETED` and sets timestamp if absent. Submitted percent is stored as supplied and is not coupled to completed. |
| P04 — #21/#24 contract alignment | 10% | REQ-21-01, REQ-24-01 | `docs/dd/21_users_me_progress/04_Response.md`; affected #24 `OPEN_QUESTIONS.md`/data mapping only if stale | Remove #21 `data.bio` from DD; leave current source/model unchanged. Record #24 current verified published Course + Lesson and enrollment behavior; no new #24 source logic unless exact audit finds a mismatch. |
| P05 — DD and context reconciliation | 10% | REQ-21-01 through REQ-25-03 | Affected DD #22/#23/#25 request, mapping, table/open-question pages; `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `modules/README.md`, `database.md` only where a direct contradiction exists | Update only impacted statements; retain remaining unresolved DD claims. Correct stale context that currently says #21-25 were reverted. No broad DD rewrite. |
| P06 — focused verification and diff audit | 15% | All | Focused tests for APIs #21-25; `node scripts/validate-agent-context.mjs`; scoped `git diff --check`; final source/DD/migration diff | Run listed focused tests only (not the full Study suite); report each TC as PASS/FAIL/NOT_RUN/BLOCKED. Run context validator because context pages change. Confirm the migration references no schema outside `nguyen_anh_duc`, DB has not been mutated, and unrelated dirty files remain untouched. |

## Test-case matrix

| Case | Requirement / step | Scenario and expected result | Test layer / path | Status before code |
|---|---|---|---|---|
| TC-22-01 | REQ-22-01 / P01 | Published Course + ACTIVE enrollment returns 200. | API module test, `tests/modules/student/api_22_lessons_access/test_lessons_access.py` | Existing; update fixture for course status if needed. |
| TC-22-02 | REQ-22-01 / P01 | Unpublished Course returns existing 404 and does not grant access. | API module test, same path | New regression case. |
| TC-22-03 | REQ-22-01 / P01 | Published Course + COMPLETED enrollment remains allowed. | API module test, same path | New boundary case. |
| TC-23-01 | REQ-23-01/02 / P02 | A new start issues one UPSERT with the declared `(user_id, lesson_id)` conflict key. | SQL/view unit test, `tests/modules/student/api_23_lessons_start/test_lessons_start.py` | Update existing new-progress case. |
| TC-23-02 | REQ-23-02 / P02 | Repeated/concurrent conflict path does not demote existing `COMPLETED`; successful route remains HTTP 201. | SQL contract assertion plus API module test, same path | New regression case. |
| TC-23-03 | REQ-23-01 / P02 | Migration guards wrong/missing schema and duplicate pairs; DDL names only target schema. | Static migration-source assertion or reviewed SQL; no live migration | New verification case; DB execution NOT planned. |
| TC-24-01 | REQ-24-01 / P04 | Existing published Lesson/Course + ACTIVE enrollment still returns 200. | API module test, `tests/modules/student/api_24_lessons_detail/test_lessons_detail.py` | Existing regression case. |
| TC-24-02 | REQ-24-01 / P04 | Unpublished Lesson or Course returns existing 404; COMPLETED enrollment remains accepted. | API module test, same path | Existing unpublished cases; add completed enrollment case if absent. |
| TC-25-01 | REQ-25-01 / P03 | Request without `position` succeeds; request model no longer declares it. | API module test, `tests/modules/student/api_25_lessons_progress/test_lessons_progress.py` | Update existing success/body fixtures. |
| TC-25-02 | REQ-25-02 / P03 | `percent < 0` and `percent > 100` return 422 validation envelope; 0 and 100 are accepted. | API module test, same path | Replace existing “no range validation” case; add bounds. |
| TC-25-03 | REQ-25-03 / P03 | Existing COMPLETED row plus `completed=false` stores IN_PROGRESS and clears completion timestamp. | API/query contract test, same path | New regression case. |
| TC-25-04 | REQ-25-03 / P03 | `completed=true` sets COMPLETED and preserves existing completion timestamp or sets it when absent. | API/query contract test, same path | Update existing completion case. |

## Migration and compatibility handling

- New migration source follows the checked-in 018 pattern: require schema `nguyen_anh_duc`, fully qualify every target relation, verify no duplicate non-NULL learner/lesson pairs, then add a named unique constraint only to `nguyen_anh_duc.lesson_progress`.
- If duplicates appear at application time, migration raises and performs no cleanup. Stop and ask for a separate data-resolution decision.
- Do not apply migration in this task. Before application, recheck migration ordering/current schema and live duplicates; deploying #23's UPSERT before applying migration will fail because PostgreSQL lacks the conflict target.
- Keeping the constraint during code rollback is safe; do not automatically drop it because that would re-enable duplicates.
- No backfill, row update, `position` column, or other schema mutation.

## Known risks and uncovered areas

- The SQL migration is not executed in this task; syntax/deployment behavior is reviewed statically only unless PLAN approval explicitly includes local migration simulation. Live DB application is out of scope.
- API module tests use fake DB sessions; they cannot prove PostgreSQL concurrency behavior. The unique constraint plus PostgreSQL UPSERT is the database-level protection; a real concurrent integration test is not in this plan.
- #21 retains a profile-shaped response and ignores progress selectors per explicit decision; this does not claim that the endpoint computes course progress.
- Unrelated pre-existing working-tree changes are numerous; final review must use scoped paths and preserve all other files.

## Approval

- Status: `PENDING_APPROVAL`
- Approver: pending
- Approved revision SHA256: pending
- Decision date: pending
