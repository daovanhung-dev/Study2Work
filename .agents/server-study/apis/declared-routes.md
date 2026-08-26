# Study declared API surface

Global status: `DECLARED_NOT_RUNNABLE` because `app.api.v1` imports missing modules and `app.main` has core symbol mismatches.

## Composition-root routes

### `GET /`
Source: `app/main.py:create_app -> root`.
Intended result: `SYSTEM_ROOT_LOADED`, message `Welcome to Study2Work.`, data `{service: study-api}` through missing `success_response`.

### `GET /health/live`
Intended result: `SYSTEM_HEALTH_LIVE`, service/environment. No dependency probe.

### `GET /health/ready`
Intended result: `SYSTEM_HEALTH_READY`, service/environment and labels `{database: configured, redis: configured|not_configured}`. **Database is not probed.**

## `/api/v1` declarations in `app/api/v1.py`

### `GET /api/v1/hello`
Body declaration: `{"message":"hello world!"}`. No auth dependency. Still unreachable through normal app import because module-level missing imports execute first.

### `GET /api/v1/test/db`
Calls `get_engine().connect()` then `SELECT NOW()` with SQLAlchemy `text`; returns list of first-column values. No standard envelope. Import-blocked.

### `POST /api/v1/register`
Declared input `RegisterRequest`; dependencies `get_db`; calls missing `create_user(...)` with trace ID. Request fields, DB tables, validation and business errors are **not source-available**.

### `POST /api/v1/auth/login`
Declared input `LoginRequest`; dependencies `get_db`; calls missing `login_user(...)`. Detailed behavior `SOURCE_REQUIRED`.

### `POST /api/v1/auth/refresh`
Declared input `RefreshTokenRequest`; dependencies `get_db`; calls missing `refresh_access_token(...)`. Detailed persistence/rotation behavior `SOURCE_REQUIRED`.

### `GET /api/v1/auth/me`
Depends on missing `get_current_user`. If dependency existed, handler itself returns standard-looking envelope with `AUTH_CURRENT_USER_FOUND`; auth semantics remain `SOURCE_REQUIRED`.

### `POST /api/v1/chat_log_ai`
Declared query/function parameter `prompt: str`; calls missing `app.module.ai.log.view.chat_log_ai(prompt=...)`. This is **not** the same runtime implementation as AI Server's `ChatLogRequest` route.

## Editing rule

Before implementing/fixing any declared route, inspect current `app/api/v1.py`, then require source/contract for every missing request model/use-case/table. Do not copy AI Server chat implementation or legacy Study auth code unless explicitly approved.
