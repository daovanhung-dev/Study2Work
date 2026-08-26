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

## Environment — `config/env.ts`

Required: `WORK_DATABASE_URL` PostgreSQL URL.
Defaults: env local, host `0.0.0.0`, port 8001, issuer `study2work`, audience `work-api`, docs true.
Optional: Redis URL, CORS origins, JWKS URL.

Security constraints:
- CORS `*` forbidden; only http/https origins.
- Redis must use redis/rediss.
- staging/production require JWKS URL.
- JWKS must use HTTPS outside local/test.
- parsed environment is frozen.

## Prisma — `database/prisma.service.ts`

`PrismaService` extends one shared `PrismaClient`, injecting Work DB URL and logging warnings outside production. `onModuleDestroy()` disconnects client.

Domain modules should inject this service, not construct PrismaClient themselves.
