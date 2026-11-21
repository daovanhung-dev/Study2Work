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
It routes `/` to Shared SH-01 (#05/#06), includes SH-02/SH-03 routes, partial Guest GS-01–GS-03
routes/callers, Student ST-11–ST-26 routes, and Admin AD-01–AD-25 routes with
selected Admin GET callers. Mentor routes/callers remain absent; auth and API
wiring are screen-specific, so consult `study/` and current source. Work Web
uses React; do not apply its React patterns to Study Web.
