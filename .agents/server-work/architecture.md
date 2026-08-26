# Work Server architecture

## Runtime composition

```text
src/main.ts
  -> bootstrap()
     -> loadWorkEnvironment()
     -> createWorkApplication()
        -> AppModule.forRoot(environment)
           -> WorkConfigModule
           -> DatabaseModule
           -> HttpModule
           -> AuthModule
           -> HealthModule
           -> SystemModule
        -> Fastify trace hook + CORS
        -> global prefix /api/v1 (health excluded)
        -> global ValidationPipe
```

Cross-cutting runtime:

- `AuthModule`: global `APP_GUARD` (`JwksAuthGuard`).
- `HttpModule`: global `APP_INTERCEPTOR` (`ApiEnvelopeInterceptor`) and `APP_FILTER` (`ApiExceptionFilter`).
- Fastify hook creates/normalizes `X-Trace-Id` before Nest handler execution.

Current product surface is foundation-only: system root and health endpoints. No job/CV/company domain module is present in `src/`.
