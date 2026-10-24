# PLAN_RESULT — API #90 Xóa quiz

- Status: `Draft — Needs Confirmation`.
- Output folder: `apps/study-server/docs/dd/90_admin_quizzes_delete/`.
- Basis: catalog API #90; AC-35 full page/flow; AC-16 #29–#32 dependency; DeleteResult; legacy DB guide/ERD/DDL; V1-PILOT comparison; current Study source; prior DD #87–#89, #86 and #29–#32.
- Primary task: `docs`; scope: `server-study`; no cross-scope dependencies.
- Runtime: `UNWIRED / NOT_FOUND`; no route/module/test API #90.

## Plan and result

1. Giữ exact path-only contract, ApiEnvelope<DeleteResult>, HTTP 200 và 5 catalog errors — DONE.
2. AC-35 soft-delete when attempts exist, retain attempt/answer history — DOCUMENTED; physical marker SOURCE_REQUIRED.
3. No-attempt branch hard delete choices → questions → quiz — DERIVED proposal; not explicitly stated in diagram.
4. Map request/query/mutation/response/error matrices; four operation mapping sheets — DONE.
5. Record API #29 race, tombstone/timestamp and AC-35 group visibility dependencies — OPEN in `OPEN_QUESTIONS.md`.
6. Verify template, contract, examples, links, tables, fences, whitespace and source boundary — see `VERIFICATION_REPORT.md`.

## Tables read/write

- Read candidate: `quizzes`, `quiz_attempts`; relation review: `quiz_questions`, `quiz_choices`, `quiz_answers`.
- Write candidate: UPDATE `quizzes`; conditional hard DELETE `quiz_choices`, `quiz_questions`, `quizzes`.
- No attempt/answer DELETE is allowed in the soft-delete branch.
- Legacy DDL is not live schema proof; V1-PILOT UUID model is incompatible and not selected.

## Assumptions and conflicts

- AC-35 “soft delete nếu đã có attempts” is treated as direct logical intent.
- No-attempt hard delete is the simplest candidate branch and uses child-first order because checked-in legacy DDL has FK relationships and no cascade clause.
- `status='DELETED'`, `updated_at` as soft-delete time and mapping it to DeleteResult.deleted_at are `DERIVED` proposals only.
- Legacy `quizzes` has no `deleted_at` and no canonical status enum; DeleteResult timestamp and physical tombstone remain unresolved.
- API #29 has no approved shared concurrency/status rule. AC-35 macro-review awaits API #91 DD.
