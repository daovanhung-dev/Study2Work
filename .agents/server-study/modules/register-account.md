# Register account module

## Source

```text
app/api/v1.py
→ app/modules/auth/register_account/models.py
→ app/modules/auth/register_account/view.py
   ├─ query.py
   ├─ core/security/password.py
   └─ core/responses.py
```

Current endpoint: `POST /api/v1/auth/register`.

`RegisterRequest` contains `email`, `password` and `full_name`. The model strips
`email`/`full_name`, rejects blank password input and validates the email type.
`validate.py` currently exists but is empty and is not called.

## Current runtime flow

```text
request
→ TraceIdMiddleware
→ RegisterRequest parse/normalize
→ create_user()
→ duplicate email lookup
→ Argon2id password hash
→ INSERT users
→ commit
→ safe success response
```

`view.py` owns duplicate handling, password hashing, commit/rollback and safe
error mapping. `query.py` owns parameterized SQL and does not commit. Password
plaintext/hash is not returned or logged.

## Validation boundary

Future special rules go in `validate.py` and are called by `view.py` after model
parse/normalization and before the duplicate query. Examples are illustrative;
the module must not add a domain rule without current contract/source evidence.

## Current discrepancy

`tests/modules/auth/test_register.py` imports removed paths
`app.modules.auth.models/view`, so pytest collection is currently blocked. This
context records the mismatch; it does not treat the stale test as runtime
evidence and does not invent a compatibility package.
