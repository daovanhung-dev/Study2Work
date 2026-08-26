# Work foundation modules

## System

`SystemController` is `@Public()` and controller root path.

### `root()`
Route after global prefix: `GET /api/v1`.
Returns `{service:"work-api"}`; global interceptor supplies `SYSTEM_ROOT_LOADED`, message `Welcome to Study2Work.` and trace envelope through `@ApiSuccess`.

## Health

`HealthController` is `@Public()` with controller path `health`. Health paths are excluded from global `/api/v1` prefix.

### `live()`
`GET /health/live` -> `HealthService.live()` -> `{service:"work-api", environment}`. No DB/Redis call.

### `ready()`
`GET /health/ready` -> `HealthService.ready()`.

`HealthService.ready()`:
1. executes Prisma `$queryRaw` `SELECT 1`;
2. DB failure -> `ApiException` 503 `DEPENDENCY_UNAVAILABLE`, `Work API is not ready.`;
3. success -> service/environment + dependency labels;
4. database label is `configured` after successful probe;
5. Redis label only reflects `environment.redisUrl`, with **no Redis probe**.

No current service reads/writes `SystemRecord`.
