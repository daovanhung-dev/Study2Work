# Work server tests

The checked-in server integration suite is `test/app.test.ts`. It uses Supertest
against `createApp({ config, dependencies })` with an injected fake Prisma
dependency, so it does not connect Neon or require Docker. It covers system
routes, readiness failure, trace propagation, safe errors, auth/password alias,
role boundaries, registration, jobs and duplicate applications.

Use these checks when the Node toolchain is available:

```bash
./node_modules/.bin/tsc --noEmit
npm test
npm run prisma:validate
npm run prisma:generate
```

`npm run s2w` is the development server command, not an automated test. If an
integration harness is added later, it must cover successful student/business
login, JSON `401` for missing/invalid/expired Bearer tokens, JSON `403` for a
wrong role, owner checks, multipart upload behavior, logout without
`Set-Cookie`, absence of server-side session state, legacy plaintext rehash,
duplicate registration/CV/application, invalid IDs/pagination, and the absence
of `matkhau` in responses. Do not claim these scenarios are currently
automated.

When Node/npm is unavailable, the equivalent Deno fallback can execute the
workspace-installed TypeScript/Vitest CLIs for static and focused checks; the
normal npm/pnpm scripts remain the canonical CI commands.

The Work Web tests live under `apps/work-client/web/src/` and cover role access,
Bearer header/credential behavior and local token clearing. The mobile tests
cover Neon URL/row/model normalization and polling; their network smoke tests
are opt-in. Never print tokens, passwords, API keys or connection strings.
