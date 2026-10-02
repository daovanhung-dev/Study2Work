# Study workflow

For coding/fix tasks:

```text
classify task -> worklog preflight/read same-type logs
->
scope AGENTS
-> affected API/core page
-> exact source
-> import/caller/callee trace
-> requirement/contract for missing business behavior
-> smallest implementation
-> focused tests
-> full Study tests when app can collect
-> update affected context
-> context validator
```

For API implementation, keep the module flow explicit:

```text
requirement / DD / schema
-> models.py: request fields, types, defaults and type conversion
-> app/utils/validate.py: shared pure normalization helpers
-> each API's validate.py: input rules, normalization and direct ApiError response
-> query.py: parameterized SQL only
-> view.py: business checks, security, transaction and response orchestration
-> api/v1.py: route and dependency injection
-> focused tests
```

`app/utils/validate.py` contains shared pure normalization and claim helpers.
Each API #1–#7 has its own `validate.py` that returns normalized input or an
`ApiError(...)` `JSONResponse`. Validators do not query DB, commit/rollback or
perform side effects; DB-backed duplicate/existence/permission checks stay in
`view.py` with `query.py`.

The current register source normalizes email/password/full_name in
`api_01_auth_register/validate.py`; its model only declares the body fields.
Route OpenAPI metadata retains the prior email and length constraints without
executing them during model parsing.

For API source comments, place a short API header immediately before each
API-facing handler, keep one event per inline comment, and use concise DD step
labels when useful. A comment-only task must not change executable statements;
verify this from the diff, then run focused tests, full scope tests and static
checks as available. Do not use comments to reconcile a DD/current-source
discrepancy.

## Implementation checklist

Before edit:

1. Identify endpoint → module → caller/callee/core/service dependencies.
2. Read current source, tests and authoritative contract/schema evidence.
3. Separate expected behavior from current behavior; record `DISCREPANCY` when
   they differ.

After edit:

1. Recheck imports, router/view signatures and query placeholders.
2. Recheck commit/rollback, response/error/trace and secret safety.
3. Run focused verification, then full scope checks when collection is possible.
4. Update the affected `.agents/<scope>/` page and run the context validator.

Do not declare a test or runtime flow verified from source reading alone.

Special rule: because Study has multiple independent import mismatches, a fix for the first exception is not enough evidence that the app is runnable. Re-import the composition root and continue until the approved task boundary is satisfied.

Mọi task phải tạo/cập nhật worklog theo `.agents/worklog/TEMPLATE.md`, tách
`EXPECTED_BEHAVIOR` khỏi `CURRENT_BEHAVIOR` và ghi blocker collection bằng
`DECLARED_NOT_RUNNABLE` khi chưa chạy được.
