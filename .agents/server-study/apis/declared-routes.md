# Study declared API surface

Global status: current route source is `SOURCE_BACKED`; `app.main` import and
the register/auth/category/course test modules use the current `guest` internal
namespace. Current auth login/refresh, verify-email dispatch, current-user,
category, course, course-search, resource-detail, avatar-upload and profile
update routes are wired; the AI route remains `UNWIRED`.

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
`app.modules.guest.api_01_auth_register.view.create_user(...)` with trace ID.
The flow checks duplicate email, hashes the password with Argon2id, inserts into
the `users` relation referenced by current SQL, commits the transaction and
returns the safe profile envelope. The active schema is not asserted here
without live metadata.
Verification dispatch is not part of the register transaction. Direct API #2
invocation uses the current injectable development stub and does not claim real
email delivery.

### `POST /api/v1/auth/login`
Implemented through `app.modules.guest.api_03_auth_login.view.login(...)`. It looks up
the user by email, verifies the stored password hash, requires `status=ACTIVE`,
creates a JWT access token, stores only the HMAC refresh-token hash, commits the
session and returns the profile plus token fields.
Success is HTTP `200` with `DESIGN_RESOURCE_RETRIEVED`. Unknown/wrong
credentials return `401 DESIGN_AUTHENTICATION_REQUIRED`; inactive accounts
return `403 DESIGN_ACCESS_DENIED`; database/token failures return
`500 DESIGN_INTERNAL_ERROR`.

### `POST /api/v1/auth/refresh`
Implemented through `app.modules.guest.api_03_auth_login.view.refresh(...)`. It hashes
the supplied opaque token, requires an unrevoked and unexpired DB row for an
active user, revokes that row and inserts a new hashed refresh token in the same
transaction, then returns a new access-token pair and profile.
Invalid, expired or already rotated tokens return
`401 DESIGN_AUTHENTICATION_REQUIRED`.

### `POST /api/v1/auth/verify-email/send`

Implemented through `app.modules.guest.api_02_auth_verify_email_send.view.send_verification_email(...)`.
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
Implemented through `app.modules.guest.api_04_users_me.view.get_current_user(...)`.
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

Implemented through `app.modules.guest.api_05_categories.view.get_categories(...)`.
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

Implemented through `app.modules.guest.api_06_courses.view.get_courses(...)`. The route
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

### `GET /api/v1/courses/search`

Implemented through `app.modules.guest.api_07_courses_search.view.search_courses(...)`. The
route is public and accepts optional `q`, `category`, `page` and `sort` query
parameters. `q` is trimmed/lowercased; blank input removes the text predicate.
`page` defaults to `1`, page size is fixed at `20`, and `sort` uses the
allow-listed `field:direction` format over `id`, `name`, `price` and
`created_at`, with default order `created_at DESC, c.id ASC`.

The query selects only `PUBLISHED` courses, searches `LOWER(c.name)` with a
bound `q_pattern`, reads mentor summary fields from `users`, and applies the
same predicates to the count query. A supplied `category` is rejected with
`422 DESIGN_VALIDATION_ERROR` before DB access because no source-backed
course-category relation exists. Missing mentor integrity, query failures and
mapping failures return safe `500 DESIGN_INTERNAL_ERROR`; empty results return
`200 DESIGN_RESOURCE_RETRIEVED` with fixed-size pagination. No schema or live DB
verification is claimed.

### `GET /api/v1/resources/{resource_id}`

Implemented through `app.modules.guest.api_12_resources_detail.view.get_resource_detail(...)`.
The route is public and reads the resource metadata. If a resource has a lesson,
the view also requires a published parent course; invalid, missing or
unpublished-parent resources return `404 DESIGN_RESOURCE_NOT_FOUND`. Success is
`200 DESIGN_RESOURCE_RETRIEVED` with the source-backed resource fields, including
the URL stored on the resource. The route does not inject a storage signer.

### `POST /api/v1/users/me/avatar`

Implemented through `app.modules.guest.api_13_users_me_avatar.view.upload_avatar(...)`.
The route has no database dependency and uses the shared Student Bearer guard.
JSON `{image}` must contain a strict Base64 Data URL for PNG, JPEG or WebP; the
decoded image is limited to 5 MiB and its signature must match the declared MIME.
Extra request fields are rejected.

`app.service.object_storage.avatar.S3AvatarStorageProvider` reads its required
configuration from process environment when upload is requested, so missing
storage configuration does not prevent app startup. It writes
`avatars/{user_id}` with the checked `Content-Type`, then returns a URL derived
from `OBJECT_STORAGE_PUBLIC_BASE_URL`. The client uses a five-second connect
timeout, 30-second read timeout and one attempt. Same-user uploads overwrite the
same key. Failures map to `500 DESIGN_INTERNAL_ERROR` without provider details.

Success is `201 DESIGN_RESOURCE_CREATED` with
`ApiEnvelope<AvatarUploadResult>`; `data` contains only `avatar_url`. API #13
does not update `users.avatar_url`; API #14 remains the profile update step in
AC-11. Route, parser, auth, storage failure and S3 stub behavior have local
tests; no remote storage call or credential check is claimed.

### `PUT /api/v1/users/me/profile`

Implemented through `app.modules.guest.api_14_users_me_profile.view.update_profile(...)`.
The route requires Student Bearer auth and owns the profile database update.
In AC-11 the client sends the URL returned by API #13 as `avatar_url` in this
follow-up request.

### `POST /api/v1/chat_log_ai`
Not currently exposed; implementation remains `UNWIRED`. This is **not** the
same runtime implementation as AI Server's `ChatLogRequest` route.

## Editing rule

Before implementing/fixing any future declared route, inspect current
`app/api/v1.py`, then require source/contract for every missing request
model/use-case/table. Do not copy AI Server chat implementation or legacy Study
auth code unless explicitly approved.
