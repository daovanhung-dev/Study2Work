# PLAN_RESULT — API #90 Xóa quiz

- Status: `Draft — Needs Confirmation`.
- Output folder: `apps/study-server/docs/dd/90_admin_quizzes_delete/`.
- Basis: catalog API #90; AC-35 full page/flow; AC-16 #29–#32 dependency; DeleteResult; legacy DB guide/ERD/DDL; V1-PILOT comparison; current Study source; prior DD #87–#89, #86 and #29–#32.
- Primary task: `coding`; secondary: `test`, `docs`; scope: `server-study`; no cross-scope dependencies.
- Runtime: route/module/test wired locally; no live database/deployment verification.

## Plan and result

1. Giữ exact path-only contract, ApiEnvelope<DeleteResult>, HTTP 200 và 5 catalog errors — DONE.
2. AC-35 soft-delete with attempt history and retain answer/history — wired; `DELETED`/`updated_at` remain DERIVED.
3. No-attempt/answer-reference branch hard delete choices → questions → quiz — wired DERIVED proposal; not explicitly stated in diagram.
4. Raw DELETE route, ADMIN-first validation, locks, mapping and rollback — wired and covered by focused HTTP tests.
5. Map API #29 race, tombstone/timestamp and AC-35 group visibility dependencies — OPEN in `OPEN_QUESTIONS.md`.
6. Update DD/context and run linked/full Study verification — see worklog and `VERIFICATION_REPORT.md`.

## Tables read/write

- Read candidate: `quizzes`, `quiz_attempts`; relation review: `quiz_questions`, `quiz_choices`, `quiz_answers`.
- Write candidate: UPDATE `quizzes`; conditional hard DELETE `quiz_choices`, `quiz_questions`, `quizzes`.
- No attempt/answer DELETE is allowed in the soft-delete branch.
- Legacy DDL is not live schema proof; V1-PILOT UUID model is incompatible and not selected.

## Assumptions and conflicts

- AC-35 “soft delete nếu đã có attempts” is treated as direct logical intent.
- No-attempt hard delete is the simplest candidate branch and uses child-first order because checked-in legacy DDL has FK relationships and no cascade clause.
- Runtime uses `status='DELETED'`, `updated_at` for soft-delete time and `CURRENT_TIMESTAMP` for hard-delete result; these mappings remain `DERIVED` proposals.
- Legacy `quizzes` has no `deleted_at` and no canonical status enum; DeleteResult timestamp and physical tombstone remain unresolved.
- API #29 has no approved shared concurrency/status rule. The AC-35 macro-review exists in #90/#91 DDs but does not grant owner approval.
