# Study tests status

```text
TEST_SUITE_PRESENT: YES
TEST_STATUS: VERIFIED (1315 tests passed in the current full Study suite)
```

Tests under `apps/study-server/tests/` cover config, DB helpers, responses and
exception handlers, security tokens, health/security behavior, API #1 register,
API #2 verify-email dispatch, API #3 login/refresh, API #4 current-user profile
access, API #12 resource detail, API #13 avatar upload, API #14 profile update,
API #5 category retrieval, API #6 public course retrieval, API #7 course search,
API #34 upload, Mentor APIs #46–#67, and Admin APIs #68–#97. APIs #4,
#13 and #14 share the auth guard in
`app/utils/auth.py`; security primitive tests remain under `tests/core`.
The API #08 course-detail and API #09 curriculum tests passed in the current
full suite after merge.
The API-specific tests are grouped under
`api_01_auth_register`, `api_02_auth_verify_email_send`, `api_03_auth_login`,
`api_04_users_me`, `api_05_categories`, `api_06_courses`,
`api_07_courses_search`, `api_08_courses_detail`,
`api_09_courses_curriculum`, `api_12_resources_detail`,
`api_13_users_me_avatar`, `api_14_users_me_profile`,
`mentor/api_46_mentor_courses`, `mentor/api_47_mentor_lectures_create`,
`mentor/api_48_mentor_lecture_detail`, `mentor/api_49_mentor_content_list`,
`mentor/api_50_mentor_content_create`, `mentor/api_51_mentor_content_update`,
`mentor/api_52_mentor_content_publish`,
`mentor/api_53_mentor_content_delete`, `mentor/api_54_mentor_submissions_list`,
`mentor/api_55_mentor_submissions_detail`, `mentor/api_56_mentor_submissions_grade`, `mentor/api_57_mentor_submissions_feedback`, `mentor/api_58_mentor_support_requests`, `mentor/api_59_mentor_support_request_detail`, `mentor/api_60_mentor_support_reply`, `mentor/api_61_mentor_support_resolve`, `mentor/api_62_mentor_course_students`, `mentor/api_63_mentor_notifications_create`, `mentor/api_64_mentor_notification_status`, `mentor/api_65_mentor_course_progress`, `mentor/api_66_mentor_course_analytics`, `mentor/api_67_mentor_student_progress`, `admin/api_68_admin_users_list`, `admin/api_69_admin_user_detail`, `admin/api_70_admin_user_update`, `admin/api_71_admin_user_status`, `admin/api_72_admin_user_delete`, `admin/api_73_admin_courses_list`, `admin/api_74_admin_course_detail`, `admin/api_75_admin_course_update`, `admin/api_76_admin_course_status`, `admin/api_77_admin_course_delete`, `admin/api_78_admin_content_pending`, `admin/api_79_admin_content_detail`, `admin/api_80_admin_content_approve`, `admin/api_81_admin_content_reject`, `admin/api_82_admin_lessons_list`, `admin/api_83_admin_lesson_detail`, `admin/api_84_admin_lesson_update`, `admin/api_85_admin_lesson_status`, `admin/api_86_admin_lesson_delete`, `admin/api_87_admin_quizzes_list`, `admin/api_88_admin_quizzes_create`,
`admin/api_89_admin_quizzes_update`, `admin/api_90_admin_quizzes_delete`,
`admin/api_91_admin_quizzes_statistics`, `admin/api_92_admin_notifications_list`,
`admin/api_93_admin_notifications_create`, `admin/api_94_admin_notifications_update`,
`admin/api_95_admin_notifications_delete`,
`admin/api_96_admin_notifications_status` and `student/api_34_uploads`; full
collection is available.

Important remaining scope boundaries include:
- health tests expect standard envelope and trace header;
- health readiness expects labels, not a real DB probe;
- API #1 validation tests post to `/api/v1/auth/register`;
- current-user route uses the API#3 `sub`/`roles` JWT shape and passes `STUDENT` to the shared role-aware guard;
- categories route is public, uses exact locale filtering with default `vi-VN`, and returns an implicit single page;
- courses route is public, filters `PUBLISHED`, uses page/size defaults `1/20`,
  allow-listed sort and rejects category until a course-category relation exists;
- course-search route is public, normalizes optional `q`, uses fixed size `20`,
  applies the same published/search predicates to page/count, and rejects
  category until a course-category relation exists;
- API #73 requires shared `ADMIN` auth before query validation/DB, count/page use
  identical exact status/mentor predicates and `id ASC`, and category int64 is
  rejected before DB because no relation is source-backed. Tests cover bounds,
  empty/out-of-range pages, safe mapping/query failures, read-only behavior,
  trace/envelope and OpenAPI; fake DB rows do not verify live schema/deployment.
- API #46 uses the shared role-aware guard with numeric JWT subject and `MENTOR` role before DB access,
  scopes count/page queries to directly owned courses, and uses optional
  `DRAFT`/`PUBLISHED` status with API #6 pagination bounds;
- API #34 tests cover multi-role auth, purpose mismatch, enrollment/direct owner,
  multipart field errors, streamed bytes/metadata fallbacks, 503 storage failure,
  DB rollback and object cleanup;
- API #47 tests cover shared Mentor auth, signed integer/title bounds, asset_refs
  JSON shape/uniqueness/ranges, missing/non-owned course behavior, no course
  status filter, scoped asset resolution with generic 404, request-order
  restoration, PUBLISHED response/insert, decimal-string content, OpenAPI,
  atomic asset-link persistence and insert/link/commit rollback paths;
- API #48 tests cover Mentor auth, direct-owner checks, invalid/missing IDs,
  parent/link integrity, ordered UploadAsset projection, nullable content,
  safe DB errors, catalog mappings and OpenAPI int64 path schema;
- API #49 tests cover Mentor auth, direct-owner checks, signed-int64 path parsing, missing course, empty tree, flat parent-linked Content[] ordering, soft-delete filter, all-status visibility, projection/tree integrity failures, rollback, trace/envelope and OpenAPI; focused suite: 20 passed.
- API #50 tests cover Mentor auth, strict request shape, direct-owner/missing-course mapping, root order allocation, Content projection, DB/commit rollback, trace/envelope and OpenAPI; focused suite: 25 passed.
- API #51 tests cover Mentor auth, strict body shape, signed-int64 path parsing, missing/deleted Content, direct-owner access, version snapshot bindings, pending-review response, query/projection/commit rollback, trace and OpenAPI; focused suite: 23 passed. Fake DB tests do not verify migrations/live schema.
- API #52 tests cover Mentor auth, strict target body, signed-int64 path parsing, direct-owner access, APPROVED/PUBLISHED transitions, same-target idempotency, unsupported-state readiness, safe lookup/commit failures, trace, middleware validation code and OpenAPI; focused suite: 27 passed. Fake DB tests do not verify live schema/deployment.
- API #53 tests cover Mentor auth, signed-int64 path parsing, direct-owner access, missing/deleted Content, active-child and PUBLISHED guards, DeleteResult/deleted_at mapping, DB/commit rollback and OpenAPI body/path contract; focused suite: 18 passed. Fake DB tests do not verify live schema/deployment.
- API #54 tests cover Mentor auth, exact status/course filters, fixed-size pagination and stable order, direct-owner denial, empty results, constrained API #34 upload matching, malformed projections, safe DB errors, query bounds and OpenAPI; focused suite: 12 passed. Fake DB results do not verify live assignment/upload relations or deployed schema.
- API #55 tests cover Mentor auth, malformed/missing signed-int64 IDs, direct-owner denial before response mapping, null/orphan parent integrity, constrained 0/1 UploadAsset mapping, optional-field omission, safe DB errors, trace, read-only behavior and OpenAPI; focused suite: 22 passed. Fake DB rows do not verify rubric mapping, live assignment/upload relations or deployed schema.
- API #56 tests cover Mentor auth, signed-int64 path handling, strict score/rubric string body, DERIVED score range, direct-owner denial, missing/orphan relations, row lock/update bindings, feedback preservation, constrained upload lookup, response projection, commit/rollback, trace, error codes and OpenAPI; focused suite: 27 passed. Fake DB tests do not verify rubric persistence, live assignment/upload relations or deployed schema.
- API #57 tests cover Mentor auth before queries, signed-int64 path validation, strict `feedback_text`/`attachments` string body, opaque attachments not persisted/echoed, direct-owner denial, missing/broken parent relations, feedback-only update bindings, preserved score/status, no GRADED precondition, constrained UploadAsset lookup, response projection, commit/rollback, trace, error codes and OpenAPI; focused suite: 28 passed. Fake DB tests do not verify live assignment/upload relations, attachment persistence or deployed schema.
- API #58 tests cover Mentor auth, collection/thread/asset mapping, empty results, exact AND filters and stable ordering, direct-owner denial, malformed int64 query handling, safe DB/projection errors, read-only transaction behavior and OpenAPI; focused suite: 12 passed. Fake DB tests do not verify live support tables, constraints or migration deployment.
- API #59 tests cover Mentor auth before DB access, invalid/missing int64 IDs, direct-owner denial, singleton detail/thread/ordered assets, empty thread, broken parent/link and query errors, read-only behavior and OpenAPI; focused suite: 13 passed. Fake DB results do not verify live support tables, constraints or migration deployment.
- API #62 tests cover Mentor auth, signed-int64 path parsing, direct-owner denial before roster reads, missing/empty course, distinct Student summaries, ACTIVE/role filters, stable order, safe query/projection errors, read-only behavior, trace and OpenAPI; focused suite: 18 passed. Fake DB results do not verify live enrollment/user schema or deployment.
- API #63 tests cover strict direct body/OpenAPI, CSV parsing and duplicate collapse, Mentor auth before DB access, common-course scope denial, notification and channel-outbox bindings/order, trace/Operation/meta mapping, and rollback/safe errors for query, projection, outbox, and commit failures; focused suite: 23 passed. Fake DB results do not verify live schema, migration deployment, or worker/provider delivery.
- API #64 tests cover channel-state aggregation, Operation field/trace mapping, Mentor auth and sender scope, malformed/missing status paths/resources, invalid projections, safe DB errors, read-only behavior, and exact OpenAPI errors/int64/no-body contract; focused suite: 22 passed. Fake DB results do not verify live schema, migration deployment, or worker/provider delivery.
- API #65 tests cover Mentor auth, signed-int64 path, direct-owner scope before aggregate reads, ACTIVE Student roster, PUBLISHED lesson progress aggregation, latest duplicate-row selection, floor-percent/empty handling, invalid projections, safe DB errors, read-only behavior, trace and OpenAPI; focused suite: 20 passed. Fake DB results do not verify live schema/deployment, and runtime `Page<MentorStudentProgress>` remains inconsistent with catalog `Page<Course>`.
- API #66 tests cover Mentor auth before DB access, signed-int64 path handling, direct-owner scope, PUBLISHED lesson/Student filters, distinct Student/lesson proxy aggregation, empty count/null timestamp, invalid projections, safe query errors, read-only behavior, trace and exact OpenAPI error set; focused suite: 18 passed. The proxy is not an event count; fake DB results do not verify live schema/deployment, and the summary response remains inconsistent with catalog `Page<Course>`.
- API #67 tests cover Mentor auth before DB access, both signed-int64 paths, direct-owner scope before roster access, ACTIVE Student eligibility, PUBLISHED lesson order, absent progress defaults, latest-row SQL rule, summary floor average/empty behavior, invalid projection and duplicate rejection, safe query errors, read-only behavior, trace and exact OpenAPI error set; focused suite: 25 passed. Fake DB results do not verify live schema/deployment, and singular runtime `StudentCourseProgress` remains inconsistent with diagram/catalog `Page<Course>`.
- verify-email route is public, uses an injectable stub provider, does not access the database and does not claim real email delivery;
- API #13 requires Student auth, validates Data URL images, injects the lazy S3 provider, and does not access the database; tests use a S3 client stub only;
- response/security unit tests may exercise helpers independently, but do not prove the full API starts.
- Historical API #73 verification: `830 passed`; at that checkpoint OpenAPI exposed 41 unique /api/v1 path templates and 44 operations. API #76 checkpoint was 890 tests / 43 templates / 47 operations; API #77 checkpoint was 910 tests / 43 templates / 48 operations. API #78 checkpoint: 933 tests / 44 templates / 49 operations. API #79 checkpoint: 946 tests / 45 templates / 50 operations. API #80 checkpoint: 968 tests / 46 templates / 51 operations. Current API #81 checkpoint: 997 tests / 47 templates / 52 operations.
  The focused API #54 suite is 12 passed; one upstream Starlette/httpx deprecation warning
  is emitted by TestClient.
  The focused API #55 suite is 22 passed with the same upstream warning; its
  response does not expose rubric because no linked field/relation is source-backed.
  The focused API #56 suite is 27 passed with the same upstream warning; tests use fake DB data.
  The focused API #57 suite is 28 passed with the same upstream warning; tests use fake DB data.
  The focused API #58 suite is 12 passed with the same upstream warning; tests use fake DB data.
  The focused API #59 suite is 13 passed with the same upstream warning; tests use fake DB data.
  The focused API #62 suite is 18 passed with the same upstream warning; tests use fake DB data.
  The focused API #64 suite is 22 passed with the same upstream warning; tests use fake DB data.
  The focused API #65 suite is 20 passed with the same upstream warning; tests use fake DB data.
  The focused API #66 suite is 18 passed with the same upstream warning; tests use fake DB data.
  The focused API #67 suite is 25 passed with the same upstream warning; tests use fake DB data.
  The focused API #68 suite is 15 passed with the same upstream warning; tests use fake DB data.
  The focused API #69 suite is 13 passed with the same upstream warning; tests use fake DB data.
  The focused API #70 suite is 19 passed with the same upstream warning; tests use fake DB data.
  The focused API #73 suite is 24 passed with the same upstream warning; linked #06/#68/#73 regression is 60 passed. Full Study suite: 845 passed.

Current error contract:
- `error_response(...)` returns a `JSONResponse` with the standard envelope, HTTP
  status and `X-Trace-Id`; omitted error `data` is JSON `null`; no custom API
  exception class is used. Field errors are constructed as `ErrorDetail` values
  and retain the `meta.fieldErrors` contract.
- Module validators for APIs #1–#9 return `error_response(...)` responses for
  contract rules; framework type/parse failures use the registered request
  validation handler and `meta.fieldErrors`.
- Tests cover direct response shape, field errors, validator normalization,
  status/business mappings, trace headers and rollback on DB failures.
- API #46 tests cover missing/malformed Bearer headers, invalid JWT/claims,
  Mentor role enforcement, status/page/size validation, owner-scoped query
  predicates, malformed integer mapping, orphaned Mentor projections, DB
  failure rollback, invalid aggregate count mapping and successful response/trace
  mapping.
- Password tests cover legacy bcrypt verification, malformed hash rejection
  and safe rejection of passwords longer than the bcrypt limit.

For a fix task:
1. distinguish unit-testable core helper from app-level route test;
2. run the smallest unit set then full Study tests;
3. do not weaken assertions merely to match broken source.

- API #60 tests cover Mentor auth before DB access, invalid/overflow int64 path and strict body parsing, blank-message and ordered unique JSON-array ref validation, missing/broken/other-owner requests, scoped asset resolution, message/link persistence and order, full updated SupportRequest hydration, unchanged status, trace/OpenAPI, and DB/projection/link/commit rollback. Focused #59/#60 regression set: 34 passed. Fake DB tests do not verify live support schema, migration deployment, concurrency or storage URL reachability.
- Verification captured at API #60 completion: 584 passed; one upstream Starlette/httpx TestClient deprecation warning. The API #60 suite uses fake DB rows.
- API #61 tests cover Mentor auth before DB access, signed-int64 path parsing, 404/403 scope mapping, active-state transition, resolved retry, cancelled-state 422, concurrent update recheck, full thread response, trace/OpenAPI, and query/projection/commit rollback. Focused #59–#61 regression set: 47 passed. Fake DB tests do not verify live support schema, constraints, migration deployment or PostgreSQL concurrency.
- Historical snapshots: 597 passed at API #61, 615 after API #62, and 638 after API #63; the latest total is recorded at the top of this page.

- API #68 tests cover ADMIN auth before DB access, role/status/keyword filters, fixed-size pagination and stable order, empty results, invalid int32 page, nullable UserProfile fields, password-hash exclusion, malformed count/rows, SQL rollback, trace/envelope and OpenAPI; focused suite: 15 passed. Fake DB data does not verify live schema/deployment.

- API #69 tests cover ADMIN auth before lookup, safe single-profile mapping/null fields, omitted bio/password hash, catalog 404 for invalid int64/no row, safe SQL/projection 500 with rollback, read-only behavior, trace and exact OpenAPI path/error contract; focused suite: 13 passed. Fake DB data does not verify live schema/deployment.

- API #70 tests cover ADMIN auth before DB access, strict replacement body and role allowlist, API #14 normalization, signed-int64 422 handling, no-row 404, safe profile projection, trace, and query/projection/commit rollback; focused suite: 19 passed. Fake DB sessions do not verify live schema/deployment or authorization policy.

- API #71 tests cover ADMIN auth before DB access, strict body and signed-int64 path validation, unsupported current-state rejection, status lock/update, conditional refresh-token revoke, safe profile response, exact errors/trace/OpenAPI and rollback on query/projection/revoke/commit failures; focused suite: 21 passed. The linked API #03 and Admin #68–#71 regression set passed 80 tests. Fake DB sessions do not verify live schema/deployment or authorization policy.


- API #72 tests cover ADMIN auth before DB access, signed-int64 path bounds, success projection, missing/already-DELETED 404, malformed result safety, query/commit rollback, trace/envelope and OpenAPI; focused suite: 11 passed. Linked API #03 + Admin #68–#72 regression: 95 passed. Full Study suite: 806 passed. Fake DB sessions do not verify live user schema, policy approval, migration deployment or access-token revocation.


- API #74 tests cover shared ADMIN auth before parsing/query, malformed and out-of-range int64 paths, missing rows, singleton CoursePage mapping, nullable fields, decimal status projection, no status/category/counter query, safe query/projection errors, rollback/no-commit, trace and OpenAPI; focused suite: 15 passed. Linked #06/#08/#69/#73/#74 regression: 80 passed; full Study suite: 845 passed; Ruff: all checks passed. One upstream Starlette/httpx TestClient deprecation warning appears. Fake DB tests do not establish live schema/deployment or a dedicated course-management permission.

- API #75 tests cover shared ADMIN auth, strict full-replacement body, raw signed-int64 validation, title/decimal candidate bounds, metadata-only SQL bindings, preserved status/mentor, missing-row 404, safe UPDATE/readback/projection/commit failures, rollback, trace and OpenAPI. Focused suite: 27 passed; linked #06/#08/#70/#73/#74/#75 regression: 113 passed; full Study suite: 872 passed; Ruff passes. Fake DB sessions do not establish live schema/deployment or dedicated course-management permission; DD remains Draft.

- API #76 tests cover ADMIN auth, strict target-status body, raw signed-int64 validation, bound row-lock/update/audit parameters, same-status no-op, missing course, safe query/audit/projection/commit failures, rollback, error envelope, trace and OpenAPI. Focused suite: 18 passed; linked #06/#08/#71/#73–#76 regression: 134 passed; full Study suite: 890 passed; Ruff passes. Migration 010 and audit table are DERIVED candidates; fake DB sessions do not verify PostgreSQL/live schema, deployment or dedicated course-management permission. DD remains Draft.

- API #77 tests cover shared ADMIN auth before DB access, raw signed-int64 bounds, missing/already-DELETED 404, enrollment/content blockers, status marker and DB timestamp mapping, malformed lock/dependency/RETURNING projections, query/commit rollback, safe errors, trace and exact OpenAPI body/error set. Focused suite: 20 passed; linked #06/#08/#72–#77 regression: 143 passed; full Study suite: 910 passed; Ruff passes. Fake DB sessions do not verify live PostgreSQL/schema/deployment or dedicated permission; DD remains Draft.

- API #78 tests cover shared ADMIN auth before query parsing/DB access, exact type/course filters, default/page-2 pagination, empty/out-of-range pages, query bounds, malformed count/rows/payload, safe DB errors/rollback, read-only behavior, trace/envelope and OpenAPI. Focused suite: 23 passed; linked #49–#53/#73/#78 regression: 160 passed; full Study suite: 933 passed; Ruff and OpenAPI checks pass. Fake DB sessions do not verify live schema/deployment or dedicated moderation permission; response cardinality/pagination/filter/deletion rules are DERIVED and DD remains Draft.


- API #79 tests cover ADMIN auth before path/DB access, signed-int64 parsing, active Content projection and stored status, missing/deleted rows, query/projection failures with rollback, read-only behavior, route precedence, trace/envelope and OpenAPI. Focused suite: 13 passed; full Study suite: 946 passed; Ruff: pass. Fake DB sessions do not verify live schema/deployment or moderation permission; version/author metadata and revision identity remain open in the Draft DD.

- API #80 tests cover ADMIN auth before path/DB access, malformed/overflow int64 paths, missing/soft-deleted rows, PENDING_REVIEW eligibility, atomic APPROVED update/audit actor bindings, safe query/projection/audit/commit rollback, direct Content envelope, trace/OpenAPI and #78/#79 route reachability. Focused suite: 22 passed; linked #49–#53/#76/#78–#80 regression: 189 passed; full Study suite: 968 passed; Ruff passes. Fake DB sessions do not prove PostgreSQL schema/migration deployment, dedicated moderation permission or exact revision continuity with #79. Migration 011 and approval-state choice remain DERIVED; DD stays Draft.

- API #81 tests cover ADMIN auth before path/DB access, malformed/overflow int64 paths, required strict reason body, empty-string preservation, missing/soft-deleted and non-pending rows, atomic REJECTED/reason decision bindings, safe query/projection/decision/commit rollback, direct Content envelope, trace/OpenAPI and #78/#79/#80 route reachability. Focused suite: 29 passed; linked #49–#53/#78–#81 regression: 200 passed; full Study suite: 997 passed; Ruff passes. Fake DB sessions do not verify PostgreSQL schema/migration deployment, dedicated moderation permission or exact revision continuity with #79. Migration 011 reason mapping and pending gate remain DERIVED; DD stays Draft.

- API #82 tests cover ADMIN auth before validation/query, signed-int64 course bounds, exact course/status bindings, unsupported `type` without DB access, list and empty-array response, nullable optional fields, required projection errors, rollback/no-commit, trace/error envelope, OpenAPI and linked #09/#78/#83 routes; focused suite: 15 passed. Full Study suite after API #82: 1012 passed. Fake DB tests do not verify live schema/deployment or dedicated lesson-management permission.
- API #83 tests cover ADMIN auth before path parsing/query, malformed and overflow int64 paths, singleton Lesson mapping with optional nulls, absent row, mismatched/incomplete projection, safe SQL error rollback, no commit, trace/error envelope and exact OpenAPI errors/int64 parameter. Focused suite: 15 passed; linked #09/#74/#82 regression: 54 passed; full Study suite: 1027 passed; full Ruff passes. Fake DB tests do not verify live schema/deployment or AC-34 fine-grained permission; dependency output and soft-delete visibility remain unresolved.
- API #84 tests cover ADMIN auth, malformed/out-of-range path 422, strict full-replacement body rules, null clearing, bound UPDATE fields, direct Lesson response, no-row 404, safe query/mapping/commit failures with rollback, trace/error envelope and OpenAPI schema. Focused suite: 23 passed; linked #09/#47/#48/#82–#84 regression: 104 passed; full Study suite: 1050 passed; full Ruff passes. Fake DB sessions do not verify live schema/deployment, timestamp triggers or AC-34 fine-grained permission; body and schema remain DERIVED/Draft.


## API #85 Admin lesson status

- Tests cover shared ADMIN auth before query, signed-int64 parsing, strict target body/enum, 200 Lesson projection, same-status no-op without duplicate audit, missing row, safe lock/update/audit/mapping/commit failures with rollback, error envelope, SQL bindings and OpenAPI error/body declaration.
- Focused suite: 28 passed. Linked #09/#47/#48/#82–#85 regression: 132 passed. Full Study suite: 1078 passed; full Ruff: passed; OpenAPI: 50 `/api/v1` paths / 56 operations.
- Fake DB HTTP tests do not verify PostgreSQL execution, migration 012 deployment, live schema or fine-grained lesson-management permission; request enum/audit mapping remain DERIVED and DD stays Draft.

## API #86 Admin lesson delete

- Tests cover ADMIN auth before path/database access, signed-int64 parsing, row locking, progress/resource/upload blockers, status tombstone and DB timestamp mapping, repeated-delete 404, safe query/projection/commit failures with rollback, error envelope, trace and path-only OpenAPI.
- Focused API #86 suite: 15 passed. Linked #09/#12/#47/#48/#77/#82–#86 regression: 180 passed. Full Study suite: 1093 passed; Ruff passes; OpenAPI: 50 route templates / 57 operations.
- Tests use fake DB sessions; they do not verify deployed legacy tables/FKs, migration state, live locking, owner approval or fine-grained AC-34 lesson-management permission. Marker, blocker set and timestamp alias remain DERIVED; DD stays Draft.


## API #87 Admin quiz list

- Tests cover shared ADMIN auth before query/DB access, signed-int64 course and signed-int32 page parsing, raw exact status filtering, default/page-2 pagination, matching count/page filters, DELETED exclusion, empty pages, required Quiz metadata/decimal mapping, malformed count/rows, safe rollback/no-commit, trace/envelope and OpenAPI.
- At the API #87 checkpoint, its focused suite had 20 passed and linked #07/#78/#82/#86/#87 regression had 93 passed; the full suite then had 1113 tests. At the API #88 checkpoint: 1134 full Study tests, Ruff passed, and OpenAPI had 51 `/api/v1` path templates / 59 operations.
- Fake DB tests verify application mapping and error handling only; they do not verify live PostgreSQL schema/query behavior, migration state, deployment or AC-35 fine-grained quiz-management permission. Page cardinality, tombstone behavior, 422 and empty `questions` remain DERIVED; DD stays Draft.

## API #88 Admin quiz create

- Focused API #88 HTTP suite: 21 passed. Linked API #87/#88 quiz regression: 41 passed. Full Study suite: 1134 passed; one upstream Starlette/httpx deprecation warning. Ruff passes; OpenAPI: 51 `/api/v1` path templates / 59 operations.
- Tests cover ADMIN-before-body/query behavior, nested JSON validation and mapping, ordered child inserts, course missing, atomic rollback, response envelope/status and OpenAPI. Fake DB sessions do not verify real PostgreSQL or migration deployment.

## API #89 Admin quiz update

- Focused HTTP suite: 26 passed. Linked #87–#89 quiz regression: 67 passed. Full Study suite: 1160 passed with one upstream Starlette/httpx TestClient deprecation warning. Ruff passes; OpenAPI: 52 `/api/v1` paths / 60 operations.
- Coverage includes ADMIN-before-parse/DB, signed-int64 path bounds, request validation, missing/tombstone, attempt/answer history, course lookup, ordered full replacement, response projection, rollback on mapping/query/commit errors, error envelope and OpenAPI. Fake sessions do not verify PostgreSQL lock/FK behavior or live schema/migration deployment.

## API #90 Admin quiz delete

- Focused HTTP suite: 18 passed. Linked API #86–#90 regression: 100 passed. Full Study suite: 1178 passed with one upstream Starlette/httpx TestClient deprecation warning. Ruff check passes; the five API #90 module/test files and modified route pass Ruff format check. OpenAPI exposes 52 `/api/v1` path templates / 61 operations.
- Coverage includes ADMIN-before-path/DB, positive signed-int64 bounds, missing and existing tombstone, attempt and answer-only soft branches, child-first hard-delete order, exact returned-ID checks, query/projection/commit rollback, error envelope/trace and path-only OpenAPI. Fake DB tests do not verify live schema, PostgreSQL execution/locks/FKs, migration deployment or API #29 race behavior; hard delete, answer-only preservation, marker/timestamp mapping and repeat semantics remain DERIVED, and DD stays Draft.

## API #91 Admin quiz statistics

- Focused HTTP suite: 19 passed. Linked #87–#91 quiz regression: 104 passed. Full Study suite: 1197 passed with one upstream Starlette/httpx TestClient deprecation warning. Ruff check and scoped Ruff format pass; OpenAPI exposes 53 `/api/v1` templates / 62 operations.
- Coverage includes ADMIN-before-path/DB, malformed and overflow ID mapping, zero attempts, submitted-but-ungraded counts, scored average/pass calculations, nullable threshold, missing quiz, malformed aggregate projections, safe query errors, rollback/read-only behavior, trace/envelope and exact OpenAPI errors/path metadata.
- All HTTP tests use fake DB projections; they do not verify PostgreSQL execution, deployed legacy schema/migrations or AC-35 fine-grained permission. `QuizStatistics`, metrics, tombstone visibility and malformed-path-to-404 behavior are DERIVED against diagram/catalog `ApiEnvelope<Quiz>`; DD remains Draft.

## API #92 Admin notification list

- Focused HTTP suite: 20 passed. Linked #63/#64/#87/#92 regression: 85 passed. Full Study suite: 1217 passed with one upstream Starlette/httpx TestClient deprecation warning. Ruff check and scoped Ruff format pass; OpenAPI exposes 54 `/api/v1` path templates / 63 operations.
- Coverage includes ADMIN-before-query/page validation, exact status/channel filters, default/page-offset/empty results, notification and delivery aggregate projection checks, malformed counts, 500/503 mapping, rollback/read-only behavior, trace/envelope and OpenAPI query/error schemas.
- Tests use fake DB rows and do not verify PostgreSQL execution, live legacy schema/migration 009, deployment, delivery worker, notification-management permission or campaign grain. Page cardinality, status aggregation, permission scope and 422 are DERIVED against direct catalog/AC-36 contracts; DD remains Draft.


## API #93 Admin notification create/send

- Focused HTTP suite: 26 passed. Linked #63/#64/#87/#92/#93 regression: 111 passed. Full Study suite: 1243 passed with one upstream Starlette/httpx TestClient deprecation warning. Ruff check and scoped Ruff format pass; OpenAPI exposes 54 `/api/v1` path templates / 64 operations.
- Coverage includes ADMIN-before-body/DB, authorization, strict body and recipient/segment/channel/text validation, missing recipients, one row per recipient/channel, batch UUID/ID metadata, full transaction and commit boundary, rollback/error mapping, trace/envelope, and OpenAPI schema/error/count.
- Tests use fake DB projections and do not prove PostgreSQL execution, live `notifications`/outbox schema, migration deployment, provider delivery, fine-grained notification permission, Admin model approval, or Operation bridge. The fallback rules remain DERIVED and DD remains Draft.


## API #94 Admin notification update — 2026-10-26

- Focused #94 HTTP tests: 20 passed.
- Linked #92–#94 regression: 66 passed.
- Full Study Server suite: 1263 passed with one upstream Starlette/httpx TestClient deprecation warning.
- Ruff `check app tests` and scoped `ruff format --check` pass.
- OpenAPI: 55 `/api/v1` path templates / 65 operations; #94 declares direct response/errors and the DERIVED strict body.
- Tests use fake sessions/query doubles; no PostgreSQL/live schema, deployment or fine-grained permission verification.


## API #95 Admin notification delete/cancel — 2026-10-26

- Focused #95 HTTP/OpenAPI tests: 21 passed.
- Linked #92–#95 regression: 87 passed.
- Full Study Server suite: 1284 passed with one upstream Starlette/httpx TestClient deprecation warning.
- Ruff `check app tests` and scoped `ruff format --check` pass; OpenAPI: 55 `/api/v1` paths / 66 operations.
- Coverage includes ADMIN-before-path/DB, role denial, positive-int64 bounds, missing target, no/started delivery rejection, parent/delivery/delete order, exact path binding, DeleteResult timestamp, malformed projection, SQL/commit rollback and no-body OpenAPI.
- Fake sessions/query doubles do not verify live schema, migration deployment, PostgreSQL FK/row locks, worker/provider cancellation or fine-grained notification permission; local lifecycle rules remain DERIVED and DD remains Draft.


## API #96 Admin notification delivery status — 2026-10-26

- Focused #96 HTTP/OpenAPI tests: 16 passed; linked #92–#96 regression: 103 passed.
- Full Study Server suite: 1300 passed with one upstream Starlette/httpx TestClient deprecation warning.
- Ruff `check app tests` and scoped Ruff format check pass; OpenAPI exposes 56 `/api/v1` path templates / 67 operations. #96 declares exactly 200/401/403/404/500, no body/query, and direct `Notification` response.
- Coverage includes ADMIN-before-path/DB, 401/403 auth, malformed/overflow/non-positive int64→404, absent/no-delivery→404, QUEUED/FAILED/SENT projection, channel ordering/duplicate rejection, safe SQL/projection 500, read-only behavior, trace envelope, and OpenAPI contract.
- Tests use fake sessions/query doubles; they do not verify live schema, migration deployment, PostgreSQL aggregation, delivery retry grain, fine-grained permission, enum approval or the #93 Operation bridge. Local schema/projection/error choices remain DERIVED and DD remains Draft.


## API #97 Admin reported discussions — 2026-10-26

- Focused HTTP/OpenAPI tests: 15 passed.
- Linked notification contract regression (#92–#95) plus API #97: 102 passed; full Study Server suite: 1315 passed with one upstream Starlette/httpx TestClient deprecation warning.
- OpenAPI exposes 57 `/api/v1` path templates / 68 operations; #97 declares GET, optional `reason`/`severity`/`page` parameters and 200/401/403/422/500 responses.
- Coverage includes ADMIN-before-page/DB, exact report filters, one Discussion per matching report group, latest-report ordering, page default/offset/empty result, invalid signed-int32 page, required author/course projection, safe query/projection failures and no commit.
- `ruff check app tests` and scoped format check for all touched Python files pass. Repo-wide `ruff format --check app tests` reports 60 files outside this task's Python paths would be reformatted; no formatter was run over those files.
- Fake DB rows do not verify PostgreSQL query execution, migration deployment, live schema or report ingestion. Queue schema and projection rules remain DERIVED; DD remains Draft.
