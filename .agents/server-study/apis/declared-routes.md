# Study declared API surface

Global status: current route source is `SOURCE_BACKED`; `app.main` import and
the register/auth test modules use the current `guest` internal namespace.
Current auth login/refresh and current-user routes are wired; the AI route
remains `UNWIRED`.

## Composition-root routes

### `GET /`
Source: `app/main.py:create_app -> root`.
Result: `SYSTEM_ROOT_LOADED`, message `Welcome to Study2Work.`, data
`{service: study-api}` through `success_response`.

### `GET /health/live`
Intended result: `SYSTEM_HEALTH_LIVE`, service/environment. No dependency probe.

### `GET /health/ready`
Intended result: `SYSTEM_HEALTH_READY`, service/environment and labels `{database: configured, redis: configured|not_configured}`. **Database is not probed.**

## `/api/v1` declarations in `app/api/v1.py`

### `GET /api/v1/hello`
Body declaration: `{"message":"hello world!"}`. No auth dependency. Verified
through the current FastAPI composition.

### `GET /api/v1/test/db`
Calls `get_engine().connect()` then `SELECT NOW()` with SQLAlchemy `text`; returns
list of first-column values. No standard envelope. The route is composed, while
the separate health readiness endpoint does not probe the database.

### `POST /api/v1/auth/register`
Implemented input `RegisterRequest`; dependency `get_db`; calls
`app.modules.guest.register_account.view.create_user(...)` with trace ID.
The flow checks duplicate email, hashes the password with Argon2id, inserts into
the `users` relation referenced by current SQL, commits the transaction and
returns the safe profile envelope. The active schema is not asserted here
without live metadata.
Verification dispatch is currently deferred and logged because API #2/provider is
not implemented.

### `POST /api/v1/auth/login`
Implemented through `app.modules.guest.auth_login.view.login(...)`. It looks up
the user by email, verifies the stored password hash, requires `status=ACTIVE`,
creates a JWT access token, stores only the HMAC refresh-token hash, commits the
session and returns the profile plus token fields.
Success is HTTP `200` with `DESIGN_RESOURCE_RETRIEVED`. Unknown/wrong
credentials return `401 DESIGN_AUTHENTICATION_REQUIRED`; inactive accounts
return `403 DESIGN_ACCESS_DENIED`; database/token failures return
`500 DESIGN_INTERNAL_ERROR`.

### `POST /api/v1/auth/refresh`
Implemented through `app.modules.guest.auth_login.view.refresh(...)`. It hashes
the supplied opaque token, requires an unrevoked and unexpired DB row for an
active user, revokes that row and inserts a new hashed refresh token in the same
transaction, then returns a new access-token pair and profile.
Invalid, expired or already rotated tokens return
`401 DESIGN_AUTHENTICATION_REQUIRED`.

### `GET /api/v1/users/me`
Implemented through `app.modules.guest.users_me.view.get_current_user(...)`.
The route requires one `Authorization: Bearer <jwt>` header and no request body,
path parameter or query parameter. It decodes the current API#3 JWT shape
(`sub` + `roles`), requires the normalized `STUDENT` role, then reads the
public profile columns from `users` by the numeric `sub` value. It returns
`DESIGN_RESOURCE_RETRIEVED` with `id`, `full_name`, `email`, `role`,
`avatar_url`, `phone`, `status`, `created_at` and `updated_at`; `bio` is omitted
because no current `users` column is source-backed.

Missing/malformed/invalid claims and a missing user return
`401 DESIGN_AUTHENTICATION_REQUIRED`; a non-Student role returns
`403 DESIGN_ACCESS_DENIED`; query or profile mapping failures return
`500 DESIGN_INTERNAL_ERROR`. The route never selects `password_hash` and does
not mutate the database.

### `POST /api/v1/chat_log_ai`
Not currently exposed; implementation remains `UNWIRED`. This is **not** the
same runtime implementation as AI Server's `ChatLogRequest` route.

## Editing rule

Before implementing/fixing any future declared route, inspect current
`app/api/v1.py`, then require source/contract for every missing request
model/use-case/table. Do not copy AI Server chat implementation or legacy Study
auth code unless explicitly approved.
