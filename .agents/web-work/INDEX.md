# Web context index

Top-level scope: `apps/study-client/`, `apps/work-client/web/`

## Subcontexts

| App | Entry | Index |
|---|---|---|
| Study Web / app source absent | `study/AGENTS.md` | `study/INDEX.md` |
| Work Web / React | `AGENTS.md` | `INDEX.md` |

| Task | Page |
|---|---|
| Architecture/deployable boundary | `architecture.md` |
| Shared UI/design | `../project/design.md`, `conventions.md` |
| API/auth/dependencies | `dependencies.md` |
| Feature/module routing | `modules/README.md` |
| Coding/test workflow | `workflows/README.md` |
| Web/API DD | `createDD-markdown` trong `context-manifest.json` |
| Code review | `code-review` skill from the global skill registry |

Study Web has no editable application source or package manifest. The current
ignored `dist` bundle contains only a compiled `/` home route; it does not
establish Student screen routes or serving/deployment behavior. Inspect the
exact app entrypoint before editing; its current documentation/design context
is in the `study/` subcontext. Work Web uses React.
