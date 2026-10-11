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
-> models.py: declarative model classes, fields/types/defaults and data conversion
-> app/utils/validate.py: shared input validation/normalization helpers
-> app/utils/auth.py: shared authentication and token helpers
-> API-specific validate.py when request input rules exist; invalid input returns `error_response(...)`
-> query.py when SQL is needed: SQL statement constants only
-> view.py: main API flow, DB/provider calls, business checks, side effects, transaction and response orchestration
-> api/v1.py: route and dependency injection
-> focused tests
```

`app/utils/validate.py` contains shared input normalization helpers.
`app/utils/auth.py` owns shared Bearer/JWT/refresh-token helpers and the Student
current-user guard used by API #3, API #4 and API #14. An API has a module-local
`validate.py` when it has request-specific rules; API #4 calls the shared guard
directly. Validators return normalized input or `error_response(...)` for
invalid input. They do not raise response errors, construct alternate errors,
query DB or perform side effects. Shared pure helpers may raise validation
exceptions internally for the caller to map. API #2 does not have `query.py`
because it dispatches through a provider without DB access.

`models.py` contains model classes, field declarations, types, defaults,
configuration and data conversion only. It does not own runtime validation,
normalization or business rules. If a module needs SQL, `query.py` contains SQL
string constants only; parameter binding and `query_one`/`query_many` calls
belong in `view.py`.

`view.py` owns the main API flow: DB/provider operations, business checks,
transaction boundaries, failure mapping and response construction. Add a short
Vietnamese comment for each meaningful operation in every handler/helper;
consecutive statements that form one operation may share a comment, while
simple assignments do not need individual comments. Keep the API header
comment immediately before each API-facing handler and omit it for internal
helpers.

The current register source normalizes email/password/full_name in
`api_01_auth_register/validate.py`; its model only declares the body fields.
Route OpenAPI metadata retains the prior email and length constraints without
executing them during model parsing.

For API source comments, explain each meaningful operation in `view.py` and
place a short API header immediately before each API-facing handler. Comments
may group consecutive statements in one operation and may use concise DD step
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
