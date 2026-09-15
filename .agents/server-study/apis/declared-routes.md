# Study declared API surface

Global status: `VERIFIED` for current routes; unimplemented auth/AI routes remain `UNWIRED`.

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
Implemented input `RegisterRequest`; dependency `get_db`; calls `app.modules.auth.view.create_user(...)` with trace ID.
The flow checks duplicate email, hashes the password with Argon2id, inserts into
`public.users`, commits the transaction and returns the safe profile envelope.
Verification dispatch is currently deferred and logged because API #2/provider is
not implemented.

### `POST /api/v1/auth/login`
Not currently exposed; implementation remains `UNWIRED`.

### `POST /api/v1/auth/refresh`
Not currently exposed; implementation remains `UNWIRED`.

### `GET /api/v1/auth/me`
Not currently exposed; implementation remains `UNWIRED`.

### `POST /api/v1/chat_log_ai`
Not currently exposed; implementation remains `UNWIRED`. This is **not** the
same runtime implementation as AI Server's `ChatLogRequest` route.

## Editing rule

Before implementing/fixing any future declared route, inspect current
`app/api/v1.py`, then require source/contract for every missing request
model/use-case/table. Do not copy AI Server chat implementation or legacy Study
auth code unless explicitly approved.
