# Skill registry

Skills are loaded by task trigger and scope. They are not runtime source and do
not become active merely because a file exists.

| Skill | Target | Entry | Trigger | Scope |
|---|---|---|---|---|
| `create-dd-from-bd-mobile` | Mobile module DD | `create-dd-mobile/SKILL.md` | BD/BRD to Flutter/mobile module DD | Mobile Work |
| `createDD-markdown` | Web/API DD | `create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md` | API DD authoring, conversion or review | Study, Work, AI and cross-scope Web/API work |

Boundary rules:

- `create-dd-from-bd-mobile` creates a module DD from business sources with
  `Overall`, features, functions, views, imports, diagrams, assets and history.
- `createDD-markdown` creates Web/API Detail Design with Request, Response,
  Data Mapping, Error and DB mapping sheets.
- Web UI-only DD has no canonical skill in this repository; do not infer one
  from either skill.

Resources for both skills are registered in `context-manifest.json` and remain
under `.agents/skills` as their canonical source.
