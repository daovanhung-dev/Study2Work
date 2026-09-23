# DB Admin workflow

```text
classify task -> worklog preflight/read same-type logs
->
db-admin/AGENTS.md
-> architecture/API/security/database page
-> exact Angular/FastAPI source and local contract
-> permission + confirmation + transaction side effects
-> focused backend/frontend tests
-> build/typecheck when available
-> update context + global worklog
-> context validator
```

Never import Study/Work schemas or business modules into DB Admin. Treat live
bootstrap and live SQL as external-state operations; local unit tests do not
verify that a configured Neon target contains the control-plane schema.
