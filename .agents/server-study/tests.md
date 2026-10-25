# Study tests status

```text
TEST_SUITE_PRESENT: YES
TEST_STATUS: SOURCE_BACKED (276 tests passed in the current full Study suite)
```

Tests under `apps/study-server/tests/` cover config, DB helpers, responses and
exception handlers, security tokens, health/security behavior, API #1 register, API #2 verify-email
dispatch, API #3 login/refresh, API #4 current-user profile access, API #12
resource detail, API #13 avatar upload, API #14 profile update, API #5 category
retrieval, API #6 public course retrieval and API #7 course search. APIs #4,
#13 and #14 share the auth guard in
`app/utils/auth.py`; security primitive tests remain under `tests/core`.
The API #08 course-detail and API #09 curriculum tests passed in the current
full suite after merge.
The API-specific tests are grouped under
`api_01_auth_register`, `api_02_auth_verify_email_send`, `api_03_auth_login`,
`api_04_users_me`, `api_05_categories`, `api_06_courses`,
`api_07_courses_search`, `api_08_courses_detail`,
`api_09_courses_curriculum`, `api_12_resources_detail`,
`api_13_users_me_avatar`, `api_14_users_me_profile` and
`mentor/api_46_mentor_courses`; full collection is available.

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
- API #46 uses the shared role-aware guard with numeric JWT subject and `MENTOR` role before DB access,
  scopes count/page queries to directly owned courses, and uses optional
  `DRAFT`/`PUBLISHED` status with API #6 pagination bounds;
- verify-email route is public, uses an injectable stub provider, does not access the database and does not claim real email delivery;
- API #13 requires Student auth, validates Data URL images, injects the lazy S3 provider, and does not access the database; tests use a S3 client stub only;
- response/security unit tests may exercise helpers independently, but do not prove the full API starts.
- Full current verification: `276 passed` in the Study virtual environment;
  route composition exposes 16 `/api/v1` paths, including API #46.

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
