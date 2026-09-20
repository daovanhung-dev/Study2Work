# Study database + security core

## Database — `app/core/database.py`

### `build_database_url(config)`
Parses `Settings.database_url` from `constants.URL_DATABASE`, converts the
driver to `postgresql+psycopg`, and preserves Neon query options such as SSL
and channel binding. The URL stays a `SecretStr` until URL construction.

### `build_engine(config)`
- `pool_pre_ping=True`.
- pool size/max overflow from settings.
- Does not send `search_path` through startup options because Neon pooler rejects it.
- The current engine path does not send `search_path`; do not infer the active
  schema from a configuration field alone.

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
Verifies configured algorithm, issuer/audience and required claims; wrong/expired/invalid token becomes `TokenError`; also requires `type=access` and nonempty string `sub`.

Signing/verification key selection:
- ES256: private key signs, public key verifies.
- HS256: shared secret.

## Refresh token — `security/refresh_token.py`

- `generate_refresh_token`: `secrets.token_urlsafe(48)` opaque token.
- `hash_refresh_token`: HMAC-SHA256 with configured pepper before DB storage.
- `compare_refresh_token`: constant-time `hmac.compare_digest`.

## Critical absence

Current register and auth SQL reference `users`; login/refresh also reference
`refresh_tokens`, but source inspection alone does not verify live schema/table
metadata. `DB.sql`, migration artifacts and DD pages are not sufficient runtime
evidence when they conflict with live metadata. Register and auth views own
their lookup, security, token persistence and commit/rollback behavior. Current
user orchestration remains unwired; do not infer it from helper names.
