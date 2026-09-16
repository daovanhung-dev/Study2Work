# Work workflow

```text
scope AGENTS
-> module/API/core page
-> route/service exact source
-> middleware/Prisma/upload dependencies
-> legacy-web OpenAPI when JSON contract changes
-> focused frontend tests + TypeScript typecheck
-> Prisma migration/generate only for approved schema changes
-> update affected context
-> context validator
```

Keep NodeNext `.js` import suffixes and Express route composition. Do not apply
Nest/Fastify or Study Python patterns to this server.
