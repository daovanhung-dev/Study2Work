# Work workflow

```text
scope AGENTS
-> module/API/core page
-> controller/service/provider exact source
-> DTO/guard/interceptor/filter/database dependencies
-> Work OpenAPI when public contract changes
-> focused Vitest + typecheck
-> Prisma migration/generate only for approved schema changes
-> update affected context
-> context validator
```

Keep NodeNext `.js` import suffixes and Nest DI boundaries. Do not introduce raw SQL helpers/four-file Python module structure merely for consistency with Study.
