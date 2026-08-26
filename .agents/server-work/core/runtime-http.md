# Work bootstrap, trace and HTTP pipeline

## `src/bootstrap.ts`

### `configureFastify(app, environment)`
- Decorates Fastify request with `traceId`.
- `onRequest`: read `x-trace-id`, normalize UUID or generate new ID; attach to request and response header.
- Registers CORS with explicit origins; credentials false.
- Allowed headers include Authorization, Content-Type, Idempotency-Key, If-Match, X-Client-Request-Id, X-Trace-Id.

### `createWorkApplication(environment=loadWorkEnvironment())`
- Creates NestFastifyApplication using `AppModule.forRoot`.
- Calls Fastify setup.
- Global prefix `api/v1`; excludes `health/live` and `health/ready`.
- Global `ValidationPipe`: transform, whitelist, forbid non-whitelisted, custom validation exception factory.
- Enables shutdown hooks.

### `bootstrap()`
Loads env, creates app, listens on configured host/port.

## Trace — `common/trace/trace-id.ts`

Contract: `X-Trace-Id` is UUID-based; valid caller value is preserved, invalid/missing gets generated. Response header and envelope trace ID should match.

## `ApiEnvelopeInterceptor.intercept`

- Reads/creates request trace ID.
- Reads `@ApiSuccess` metadata from method/class, fallback `REQUEST_SUCCEEDED`.
- If controller already returns an API envelope, passes it through.
- Else wraps data as `{success:true,businessCode,message,data,meta,traceId}`.

## `ApiExceptionFilter.catch`

- No-op if reply already sent.
- Ensures trace ID.
- Normalizes:
  - `ApiException` -> declared status/business code/safe message/field errors;
  - generic Nest `HttpException` -> `HTTP_ERROR`, safe generic message;
  - status-like unknown error -> 4xx/5xx status when valid, else 500;
  - 503 -> `DEPENDENCY_UNAVAILABLE`; other unknown -> `INTERNAL_SERVER_ERROR`.
- Logs stack only for 5xx.
- Sends `{success:false,businessCode,message,data:null,meta:{fieldErrors},traceId}` and trace header.

## Validation

Global pipe strips/transforms known DTO fields and rejects unknown fields. Custom validation exception should remain the owning mapping for field-level validation errors when DTO endpoints are added.
