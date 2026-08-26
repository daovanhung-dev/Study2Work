# Study database + security core

## Database — `app/core/database.py`

### `build_database_url(config)`
Builds SQLAlchemy `URL` for `postgresql+psycopg`; password stays a `SecretStr` until URL construction.

### `build_engine(config)`
- `pool_pre_ping=True`.
- pool size/max overflow from settings.
- PostgreSQL `search_path=<db_schema>,public` via connect options.

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

`Settings` validates app env, docs, CORS, DB host/port/name/user/password/schema/pool, optional Redis, JWT keys/algorithm/expiry/issuer/audience and refresh pepper.

Important validators:
- CORS accepts list or comma-separated string.
- DB schema only alphanumeric/underscore.
- HS256 requires secret; ES256 requires public key at settings validation time.
- `get_settings()` is cached/lazy; `_LazySettings` preserves legacy uppercase-style access.

## Password — `app/core/security/password.py`

- `hash_password`: Argon2id (`time_cost=3`, 64 MiB, parallelism 1).
- `verify_password`: Argon2 hashes or legacy bcrypt `$2a/$2b/$2y`; unknown formats false.
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

These helpers do not establish user/session table schemas or register/login/refresh orchestration. Current `app/module/auth` is `NOT_FOUND`; do not infer its queries/commit behavior from helper names.
