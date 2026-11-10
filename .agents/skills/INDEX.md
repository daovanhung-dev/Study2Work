# Skill registry

Skills are loaded by task trigger and scope. They are not runtime source and do
not become active merely because a file exists.

| Skill | Target | Entry | Trigger | Scope |
|---|---|---|---|---|
| `create-dd-from-bd-mobile` | Mobile module DD | `create-dd-mobile/SKILL.md` | BD/BRD to Flutter/mobile module DD | Mobile Work |
| `createDD-markdown` | Web/API DD | `create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md` | API DD authoring, conversion or review | Study, Work, AI and cross-scope Web/API work |
| `code-review` | Code review | `code-review/SKILL.md` | User-requested diff/PR review or path/module audit | All six code scopes |

Boundary rules:

- `create-dd-from-bd-mobile` creates a module DD from business sources with
  `Overall`, features, functions, views, imports, diagrams, assets and history.
- `createDD-markdown` creates Web/API Detail Design with Request, Response,
  Data Mapping, Error and DB mapping sheets.
- `code-review` checks repository rules, reuse, maintainability, and security
  without modifying reviewed code or running tests; load it only on an explicit
  review request.
- Web UI-only DD has no canonical skill in this repository; do not infer one
  from either skill.

All skill entries and resources are registered in `context-manifest.json` and
remain under `.agents/skills` as their canonical source.
