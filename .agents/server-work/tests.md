# Work tests

Runner: Vitest. Commands from `apps/work-server/package.json`:

```bash
pnpm --filter work-api typecheck
pnpm --filter work-api test
# or from apps/work-server: pnpm typecheck && pnpm test
```

`test/config.spec.ts` validates Work env parsing/security constraints.

`test/health.e2e.spec.ts` builds the Nest app with test environment and verifies:
- canonical live envelope + trace response header;
- valid caller trace ID preserved;
- browser CORS preflight includes mutation headers such as If-Match/X-Client-Request-Id;
- readiness service result with mocked successful Prisma probe;
- unknown route is safe `HTTP_ERROR` envelope.

For new protected endpoints, add auth/JWKS tests rather than assuming global guard wiring is sufficient. For readiness changes, distinguish DB probe behavior from Redis configuration label.
