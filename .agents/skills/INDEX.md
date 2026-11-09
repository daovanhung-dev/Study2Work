# Skill registry

Skills are loaded by task trigger and scope. They are not runtime source and do
not become active merely because a file exists.

| Skill | Target | Entry | Trigger | Scope |
|---|---|---|---|---|
| `create-dd-from-bd-mobile` | Mobile module DD | `create-dd-mobile/SKILL.md` | BD/BRD to Flutter/mobile module DD | Mobile Work |
| `createDD-markdown` | Web/API DD | `create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md` | API DD authoring, conversion or review | Study, Work, AI and cross-scope Web/API work |
| `dev-superpowers` | BD/DD/description to approved spec, plan, code/tests and PR reminder | `dev-superpowers/SKILL.md` | Developer requests the full staged development workflow | Project scopes selected from approved inputs |

Boundary rules:

- `create-dd-from-bd-mobile` creates a module DD from business sources with
  `Overall`, features, functions, views, imports, diagrams, assets and history.
- `createDD-markdown` creates Web/API Detail Design with Request, Response,
  Data Mapping, Error and DB mapping sheets.
- Web UI-only DD has no canonical skill in this repository; do not infer one
  from either skill.
- `dev-superpowers` accepts BD, DD, a developer description, or a combination.
  It asks about missing decisions, then waits for approval of scope, `SPEC.md`,
  `PLAN.md`, and code/test results before the next step. Each requirement links
  its source -> spec -> plan/test cases -> code/executable tests. Material
  changes invalidate affected approvals. The final step reminds the developer
  to create a PR/MR; the skill does not create one or author a DD. Scope review,
  `SPEC.md`, `PLAN.md`, and approval summaries default to Vietnamese. Open
  decisions and verification gaps stay in their owning artifact and are also
  presented in chat with choices plus free-text input. Lifecycle choices must
  explain who opens, reuses and closes resources, including failure behavior.

Resources for registered skills are listed in `context-manifest.json` and remain
under `.agents/skills` as their canonical source.
