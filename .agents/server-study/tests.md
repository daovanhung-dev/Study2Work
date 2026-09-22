# Study tests status

```text
TEST_SUITE_PRESENT: YES
COLLECTION_STATUS: VERIFIED (74 tests)
```

Tests under `apps/study-server/tests/` cover config, DB helpers, responses,
security tokens, health/security behavior, API #1 register and API #3
login/refresh and API #4 current-user profile access. The register test imports the current
`app.modules.guest.register_account.*` namespace; full collection is available.

Important remaining scope boundaries include:
- health tests expect standard envelope and trace header;
- health readiness expects labels, not a real DB probe;
- API #1 validation tests post to `/api/v1/auth/register`;
- current-user route uses the API#3 `sub`/`roles` JWT shape and Student-only authorization;
- response/security unit tests may exercise helpers independently, but do not prove the full API starts.

For a fix task:
1. distinguish unit-testable core helper from app-level route test;
2. run the smallest unit set then full Study tests;
3. do not weaken assertions merely to match broken source.
