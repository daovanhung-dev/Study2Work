# Work foundation API

Canonical executable contract: `contracts/openapi/work/openapi.json`.

## `GET /api/v1`
- Auth: public.
- Input: optional `X-Trace-Id` UUID header.
- Flow: Fastify trace hook -> global public guard bypass -> `SystemController.root` -> `ApiEnvelopeInterceptor`.
- 200 business code: `SYSTEM_ROOT_LOADED`.
- Data: `{service:"work-api"}`.

## `GET /health/live`
- Auth: public.
- Prefix exception: path is not `/api/v1/health/live`.
- Flow: trace hook -> controller -> `HealthService.live` -> envelope.
- No dependency IO.
- 200 business code: `SYSTEM_HEALTH_LIVE`.

## `GET /health/ready`
- Auth: public.
- Flow: trace hook -> controller -> `HealthService.ready` -> Prisma `SELECT 1` -> envelope/filter.
- 200: `SYSTEM_HEALTH_READY`.
- 503 on DB probe failure: `DEPENDENCY_UNAVAILABLE`, `Work API is not ready.`.
- Redis status in successful response is config label only.

## Shared response behavior

Success keys: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`.
Safe errors: same shape with `success:false`, `data:null`, `meta.fieldErrors`.
`X-Trace-Id` response header must match body `traceId`.

Do not add product endpoints to context or OpenAPI until source/approved requirement introduces them.
