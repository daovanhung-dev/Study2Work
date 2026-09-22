# Study tests status

```text
TEST_SUITE_PRESENT: YES
COLLECTION_STATUS: VERIFIED (134 tests)
```

Tests under `apps/study-server/tests/` cover config, DB helpers, responses,
security tokens, health/security behavior, API #1 register, API #2 verify-email
dispatch, API #3 login/refresh, API #4 current-user profile access, API #5
category retrieval, API #6 public course retrieval and API #7 course search.
The register, verification, category, course and course-search tests use the
current `app.modules.guest.*` namespace; full collection is available.

Important remaining scope boundaries include:
- health tests expect standard envelope and trace header;
- health readiness expects labels, not a real DB probe;
- API #1 validation tests post to `/api/v1/auth/register`;
- current-user route uses the API#3 `sub`/`roles` JWT shape and Student-only authorization;
- categories route is public, uses exact locale filtering with default `vi-VN`, and returns an implicit single page;
- courses route is public, filters `PUBLISHED`, uses page/size defaults `1/20`,
  allow-listed sort and rejects category until a course-category relation exists;
- course-search route is public, normalizes optional `q`, uses fixed size `20`,
  applies the same published/search predicates to page/count, and rejects
  category until a course-category relation exists;
- verify-email route is public, uses an injectable stub provider, does not access the database and does not claim real email delivery;
- response/security unit tests may exercise helpers independently, but do not prove the full API starts.

For a fix task:
1. distinguish unit-testable core helper from app-level route test;
2. run the smallest unit set then full Study tests;
3. do not weaken assertions merely to match broken source.
