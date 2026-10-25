# Study database + security core

## Database — `app/core/database.py`

### `build_database_url(config)`
Parses `Settings.database_url` from `constants.URL_DATABASE`, converts the
driver to `postgresql+psycopg`, and preserves Neon query options such as SSL
and channel binding. The URL stays a `SecretStr` until URL construction.

### `build_engine(config)`
- `pool_pre_ping=True`.
- pool size/max overflow from settings.
- PostgreSQL engines register a SQLAlchemy `begin` listener that applies only
  `Settings.db_schema` with `SELECT set_config('search_path', quote_ident(:schema), true)`.
- The setting is transaction-local and is applied at every transaction begin,
  which supports Neon transaction pooling. Schema setup errors propagate and
  prevent the transaction from continuing to business queries.
- Schema is not sent through connection startup options. No `public` fallback
  is appended and the listener does not create or verify the schema.

### `build_session_factory(engine)`
Sync `Session`, `autoflush=False`, `expire_on_commit=False`.

### `get_engine()` / `get_session_factory()`
Process-cached factories (`lru_cache(maxsize=1)`).

### `SessionLocal()`
Legacy compatibility wrapper returning a new Session.

### `get_db_from_factory(factory)` / `get_db()`
Yield request-scoped Session and always close. No implicit commit/rollback policy beyond Session close.

### `execute_query(db, query, params=None)`
Executes `text(query)` with dictionary/named parameters. **Does not commit.**

### `query_one` / `query_many`
Return mapping rows as plain dict(s). Transaction ownership remains with caller.

## Config — `app/core/config.py`

`Settings` lấy default từ `app/core/constants.py`, dùng `URL_DATABASE` làm DB
connection chính và validates app env, docs, CORS, schema/pool, optional Redis,
JWT keys/algorithm/expiry/issuer/audience and refresh pepper. Các field DB rời
được giữ optional để tương thích constructor cũ nhưng không được engine dùng.
Model không tự đọc `.env` hoặc process environment; caller vẫn có thể truyền
override tường minh khi khởi tạo `Settings(...)`.

Important validators:
- CORS accepts list or comma-separated string.
- DB schema only alphanumeric/underscore.
- HS256 requires secret; ES256 requires private and public key at settings validation time.
- `get_settings()` is cached/lazy; `_LazySettings` preserves legacy uppercase-style access.
- Settings field validators use Pydantic's custom validation errors;
  construction sanitizes Pydantic validation failures as a generic
  `RuntimeError`. Configuration is checked outside an HTTP request and does
  not produce an `error_response(...)` or `JSONResponse`.

## Password — `app/core/security/password.py`

- `hash_password`: Argon2id (`time_cost=3`, 64 MiB, parallelism 1).
- `verify_password`: Argon2 hashes or legacy bcrypt `$2a/$2b/$2y`; unknown formats false.
- An optional legacy algorithm argument remains accepted for older callers; new
  password creation always uses Argon2id.
- `needs_password_rehash`: true for non-Argon2 or invalid/outdated Argon2 params.

## Access token — `security/access_token.py`

### `create_access_token`
Creates signed JWT with `sub`, `type=access`, `roles`, `jti`, `iat`, `exp`, `iss`, `aud`; custom claims cannot overwrite reserved claims.

### `decode_access_token`
Verifies configured algorithm, issuer/audience and required claims. Non-ASCII
input is rejected as an authentication 401. PyJWT validation errors are caught
by the decoder and mapped to its existing authentication 401 response. A
`TypeError` from JWT claim decoding propagates to the application auth facade,
which maps it through the existing authentication `error_response(...)` path
with 401. Missing signing/verification configuration remains a safe internal
`error_response`.

Signing/verification key selection:
- ES256: private key signs, public key verifies.
- HS256: shared secret.

## Refresh token — `security/refresh_token.py`

- `generate_refresh_token`: `secrets.token_urlsafe(48)` opaque token.
- `hash_refresh_token`: HMAC-SHA256 with configured pepper before DB storage.
- `compare_refresh_token`: constant-time `hmac.compare_digest`.
- Missing refresh pepper becomes a safe internal `error_response`.

Application-level auth ownership is `app/utils/auth.py`: it parses Bearer
headers, validates access claims, applies the shared
`validate_current_user_request(...)` guard for an explicit required role, and
rejects blank refresh-token input. APIs #4/#13/#14 require `STUDENT`; API #46
requires `MENTOR`. It delegates JWT signing/decoding and
refresh-token generation/hashing to the primitives above. Authentication
failures retain the existing `error_response(...)` mappings. Shared input
helpers return `ErrorDetail` or a typed failure result for their API
validator/view to map through `error_response(...)`. Request parsing and type
failures use FastAPI's registered request-validation handler, which serializes
them through the existing response helpers. Study Server source and tests do
not use built-in `ValueError`; errors outside HTTP retain internal error
handling rather than becoming `JSONResponse`.

## Critical absence

Current register and auth SQL reference `users`; login/refresh also reference
`refresh_tokens`; APIs #08/#09 also query `courses` and `lessons`, but source
inspection alone does not verify live schema/table metadata.
`infra/postgres/02_study_db.sql`, migration artifacts and DD pages are not
sufficient runtime evidence when they conflict with live metadata. Register and auth views own
their lookup, password checks, token persistence and commit/rollback behavior.
API #3, API #4, API #13, API #14 and API #46 use app-level token/auth helpers
from `app/utils/auth.py`; all access-JWT protected APIs use the shared
role-aware guard.
