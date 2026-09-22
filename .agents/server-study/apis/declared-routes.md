# Study declared API surface

Global status: current route source is `SOURCE_BACKED`; `app.main` import and
the register/auth/category/course test modules use the current `guest` internal
namespace. Current auth login/refresh, verify-email dispatch, current-user,
category and course routes are wired; the AI route remains `UNWIRED`.

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
Verification dispatch is not part of the register transaction. Direct API #2
invocation uses the current injectable development stub and does not claim real
email delivery.

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

### `POST /api/v1/auth/verify-email/send`

Implemented through `app.modules.guest.verify_email_send.view.send_verification_email(...)`.
The route is public, accepts JSON `{user_id, email}`, ignores any Authorization
header, does not resolve the database dependency and does not verify user
existence or email ownership because DD #2 does not provide that query contract.

The view calls the injectable `app.service.email.provider.VerificationEmailProvider`.
The current default is `StubVerificationEmailProvider`, which accepts the
dispatch without sending a real email. A successful response is HTTP `202` with
`DESIGN_OPERATION_ACCEPTED` and `data: {status: "accepted"}`. Provider failures
before acceptance map to `500 DESIGN_INTERNAL_ERROR`; raw provider details are
not returned or logged. No token/link/expiry/retry field, DB mutation or retry
worker is currently implemented.

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

### `GET /api/v1/categories`

Implemented through `app.modules.guest.categories.view.get_categories(...)`.
The route is public, accepts only optional query `locale` and has no request
body, path parameter, pagination, sort or authorization requirement. Missing
locale resolves to `vi-VN`; a provided locale is matched exactly. The query
selects `id`, `name`, `slug` and nullable `description` from `categories` where
`status = 'ACTIVE'` and `locale = :locale`, ordered by `id`.

Success is HTTP `200` with `DESIGN_RESOURCE_RETRIEVED` and
`data.items` plus implicit pagination `{page: 1, size: total, total,
total_pages: 1}`. An empty result is still a successful empty page. Request
validation maps to `422 DESIGN_VALIDATION_ERROR`; database or mapping failure
maps to `500 DESIGN_INTERNAL_ERROR`. No live schema/migration application is
claimed by source or tests.

### `GET /api/v1/courses`

Implemented through `app.modules.guest.courses.view.get_courses(...)`. The route
is public and accepts optional `category`, `page`, `size` and `sort` query
parameters. `page` defaults to `1`; `size` defaults to `20` and is limited to
`1..100`. `sort` accepts one allow-listed `field:direction` pair over `id`,
`name`, `price` or `created_at`; the default order is `created_at DESC, id ASC`.

The query reads only `courses.status = 'PUBLISHED'`, joins the public mentor
projection from `users`, and returns `CoursePage` items with decimal-string
prices. `category` is parsed but returns `422 DESIGN_VALIDATION_ERROR` until a
course-category relation is source-backed. A published course with a missing
mentor, query/mapping failure or database failure maps to safe
`500 DESIGN_INTERNAL_ERROR`. Empty and out-of-range pages return HTTP `200`;
`total_pages` is zero when `total` is zero. No migration or live schema
verification is claimed.

### `POST /api/v1/chat_log_ai`
Not currently exposed; implementation remains `UNWIRED`. This is **not** the
same runtime implementation as AI Server's `ChatLogRequest` route.

## Editing rule

Before implementing/fixing any future declared route, inspect current
`app/api/v1.py`, then require source/contract for every missing request
model/use-case/table. Do not copy AI Server chat implementation or legacy Study
auth code unless explicitly approved.
