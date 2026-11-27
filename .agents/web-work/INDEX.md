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
| Study Web UTC/testcase generation | `utc-screen` skill và `utc-screen-generation` workflow trong `context-manifest.json` |
| Code review | `code-review` skill from the global skill registry |

Study Web uses Angular 22 standalone components, strict TypeScript, and CSS.
Its current root route groups cover Shared SH-01–SH-07, Guest GS-01–GS-03 and
GS-07 (GS-04–GS-06 are tabs owned by GS-03), Student ST-01–ST-26, Mentor
ME-01–ME-18, and Admin AD-01–AD-25. Each screen's caller wiring and gate status
are screen-specific; use `study/INDEX.md` and recheck current source. Work Web
uses React; do not apply its React patterns to Study Web.
