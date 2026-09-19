# Work workflow

```text
classify task -> worklog preflight/read same-type logs
->
scope AGENTS
-> module/API/core page
-> createApp/api/v1 and exact module source
-> middleware/Prisma/upload dependencies
-> legacy-web OpenAPI when JSON contract changes
-> focused Work Web/mobile tests + TypeScript/Flutter checks
-> Prisma migration/generate only for approved schema changes
-> update affected context
-> context validator
```

Keep NodeNext `.js` import suffixes, Express route composition, injected Prisma
dependencies and existing legacy table names. Apply the Study request lifecycle
without copying Study's Python, SQLAlchemy, credentials or ES256. Work runtime
configuration belongs in tracked static `src/utils/constants.ts`; never put
those values in `.env`, context or logs. Treat empty services and target-contract-only
routes as `UNWIRED` until an actual import/registration exists.

Mọi task phải dùng `.agents/worklog/TEMPLATE.md`; khi API contract và route
source khác nhau, ghi `DISCREPANCY` và chạy contract validator/context validator.
