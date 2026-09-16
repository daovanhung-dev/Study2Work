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

Configuration is sourced exclusively from the local-only
`apps/work-server/src/constants.ts`. `config/env.ts` validates the selected
`local`, `docker`, or `neon` profile; Prisma commands use
`scripts/prisma-with-constants.ts` with a temporary schema, so Work runtime and
Prisma do not read `.env`, `dotenv`, or `process.env`.

Work product surface is provided by `src/modules/work/WorkModule` and the shared
runtime. It exposes public jobs/companies/products plus protected identity,
candidate, tenant/enterprise, university, applications, conversations,
interviews, billing and operations routes. Prisma is injected through the
existing `DatabaseModule`; external Identity/JWKS, payment and storage
providers remain dependency boundaries.
