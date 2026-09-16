# Work auth, config and database core

## Global auth

`AuthModule` is `@Global()` and registers `JwksAuthGuard` as `APP_GUARD`.

### `JwksAuthGuard.canActivate`
1. Reads `@Public()` metadata across handler/class; public => allow.
2. Parses exactly one `Bearer <token>` value.
3. Missing/malformed token -> 401 `AUTHENTICATION_REQUIRED`.
4. Calls `JwksAuthService.verifyAccessToken`.
5. Stores returned principal on `request.user`.

### `JwksAuthService`
Constructor creates remote JWKS only when `jwksUrl` configured, with cache 300s, cooldown 30s, timeout 5s.

`verifyAccessToken`:
- no JWKS config -> 503 `DEPENDENCY_UNAVAILABLE`;
- verifies ES256, configured issuer + audience;
- requires `type=access`, nonempty `sub/jti/sid`, numeric `authVersion`;
- scope can be space-separated string or string array;
- expired -> 401 `ACCESS_TOKEN_EXPIRED`;
- JWKS transport/timeout/invalid dependency family -> 503 `DEPENDENCY_UNAVAILABLE`;
- other JWT failures -> 401 `INVALID_ACCESS_TOKEN`.

## Configuration — `constants.ts` and `config/env.ts`

`apps/work-server/src/constants.ts` is the local-only source of truth. It
provides `local`, `docker`, and `neon` profiles containing the PostgreSQL URL,
host/port, Redis URL, CORS origins, JWKS URL, issuer/audience, docs flag, and
public web projection. `config/env.ts` validates the selected profile before
Nest starts. No Work runtime code reads `.env`, `dotenv`, or `process.env`.

Security constraints:
- CORS `*` forbidden; only http/https origins.
- Redis must use redis/rediss.
- staging/production require JWKS URL.
- JWKS must use HTTPS outside local/test.
- parsed environment is frozen.

## Prisma — `database/prisma.service.ts`

`PrismaService` extends one shared `PrismaClient`, injecting the validated Work
DB URL and logging warnings outside production. `onModuleDestroy()` disconnects
client. CLI commands go through `scripts/prisma-with-constants.ts`, which
renders the selected URL into a temporary schema and removes it afterward.

Domain modules should inject this service, not construct PrismaClient themselves.
