# Web context index

Top-level scope: `apps/study-client/`, `apps/work-client/web/`

## Subcontexts

| App | Entry | Index |
|---|---|---|
| Study Web / Angular 22 scaffold | `study/AGENTS.md` | `study/INDEX.md` |
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

Study Web uses Angular 22 standalone components, strict TypeScript, and CSS.
The root placeholder is the only current view; feature routes, auth, and API
integration remain unwired. See `study/` for its architecture and design
context. Work Web uses React; do not apply its React patterns to Study Web.
