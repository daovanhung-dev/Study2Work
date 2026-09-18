# DB Admin context index

Source roots: `apps/db-admin-web/` and `apps/db-admin-server/`

The complete ownership, API safety boundary and verified commands are in
`AGENTS.md`. Before editing, inspect the Angular entrypoint plus the FastAPI
routes/core/services named by the task. This deployable is separate from
Study, Work and AI and must not import their business modules or schemas.
