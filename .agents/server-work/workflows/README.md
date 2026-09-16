# Work workflow

```text
scope AGENTS
-> module/API/core page
-> route/service exact source
-> middleware/Prisma/upload dependencies
-> legacy-web OpenAPI when JSON contract changes
-> focused Work Web/mobile tests + TypeScript/Flutter checks
-> Prisma migration/generate only for approved schema changes
-> update affected context
-> context validator
```

Keep NodeNext `.js` import suffixes, Express route composition, the shared Prisma
client and existing legacy table names. Do not apply Nest/Fastify, health-route,
HTML-rendering or Study Python patterns to this server. Treat empty services and
contract-only routes as `UNWIRED` until an actual import/registration exists.
