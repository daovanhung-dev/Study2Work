# Study tests status

```text
TEST_SUITE_PRESENT: YES
COLLECTION_STATUS_AT_SOURCE_SNAPSHOT: BLOCKED_BY_IMPORT_CHAIN
```

Tests under `apps/study-server/tests/` cover config, DB helpers, responses, security tokens and intended health/security behavior. However `tests/conftest.py` imports `app.main`; current app import reaches missing `app.module.*` and mismatched response/trace symbols.

Important stale/blocked expectations include:
- health tests expect standard envelope and trace header;
- health readiness expects labels, not a real DB probe;
- validation test posts to `/api/v1/register`, whose request model/module is missing;
- response/security unit tests may exercise helpers independently, but do not prove the full API starts.

For a fix task:
1. reproduce collection/import failure first;
2. distinguish unit-testable core helper from app-level route test;
3. after an approved runtime repair, run the smallest unit set then full Study tests;
4. do not weaken assertions merely to match broken source.
