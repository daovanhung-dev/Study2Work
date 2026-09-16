# Study2Work Work Web

React + TypeScript + Vite frontend for the Work application. The package is a
separate deployable from `apps/work-server`, which remains the Express API and
EJS compatibility server.

```bash
corepack pnpm --filter work-web dev
corepack pnpm --filter work-web typecheck
corepack pnpm --filter work-web test
corepack pnpm --filter work-web build
```

Development runs on port `5174`. Vite proxies `/api`, `/uploads`, and `/img` to
the Work server on port `3000`; production should provide the same paths through
a same-origin reverse proxy. The client uses `/api/v1`, stores the JWT under
`access_token`, and sends it as `Authorization: Bearer <token>`. It does not
load `.env`, use cookies/session auth, or connect to Neon directly.
