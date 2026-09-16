# Work tests

Runner: Vitest. Commands from `apps/work-server/package.json`:

```bash
pnpm --filter work-api typecheck
pnpm --filter work-api test
# or from apps/work-server: pnpm typecheck && pnpm test
```

`test/config.spec.ts` validates constants-profile parsing/security constraints.
`test/constants.spec.ts` checks all local/docker/neon profiles and confirms the
Neon template contains no real credential. `test/prisma-with-constants.spec.ts`
checks temporary-schema rendering, Prisma validation, and cleanup.

`test/health.e2e.spec.ts` builds the Nest app with test environment and verifies:
- canonical live envelope + trace response header;
- valid caller trace ID preserved;
- browser CORS preflight includes mutation headers such as If-Match/X-Client-Request-Id;
- readiness service result with mocked successful Prisma probe;
- unknown route is safe `HTTP_ERROR` envelope.

For new protected endpoints, add auth/JWKS tests rather than assuming global guard wiring is sufficient. For readiness changes, distinguish DB probe behavior from Redis configuration label.

Verified on 2026-09-16 with the temporary Node 22.14.0/pnpm 9.15.4 toolchain:

- `work-api typecheck`, `build` and `test` pass (15 tests, including constants
  and Prisma-wrapper coverage).
- Neon migration deploy and catalog checks pass; the database was left without
  smoke-test fixture rows.
- Authenticated HTTP smoke passed through tenant -> job -> publish -> CV ->
  application -> message -> interview, including 412 `If-Match` conflict and
  idempotent retries. Public, readiness, 401 and generic 404 responses were
  also checked.
- In-app browser automation was `UNWIRED` because no browser session was
  available; Vite HTTP smoke and production build were used instead.
