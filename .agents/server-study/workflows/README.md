# Study workflow

For coding/fix tasks:

```text
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
-> model.py: request type, required, basic length/format/normalization
-> validate.py: named pure special validation, when contract requires it
-> query.py: parameterized SQL only
-> view.py: business checks, security, transaction and response orchestration
-> api/v1.py: route and dependency injection
-> focused tests
```

`validate.py` must state the target field, condition and error message for each
special rule. Examples include no whitespace, a required prefix/suffix or an
allowed email domain such as `@gmail.com`; examples are not automatic rules.
It must not query DB, commit/rollback, return HTTP responses or create side
effects. DB-backed duplicate/existence/permission checks stay in `view.py` with
`query.py`.

The current register source is not fully wired to this target flow:
`register_account/validate.py` is empty and current model validators remain in
`models.py`. The register test module currently has a stale import path and
blocks pytest collection.

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
