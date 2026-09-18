# Work server tests

There is no checked-in server test runner or server integration test suite for
the current Express application. Use these source-level checks when the Node
toolchain is available:

```bash
./node_modules/.bin/tsc --noEmit
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

When Node/npm is unavailable, record the commands as
`DECLARED_NOT_RUNNABLE`; source/static checks do not constitute integration
coverage.

The Work Web tests live under `apps/work-client/web/src/` and cover role access,
Bearer header/credential behavior and local token clearing. The mobile tests
cover Neon URL/row/model normalization and polling; their network smoke tests
are opt-in. Never print tokens, passwords, API keys or connection strings.
