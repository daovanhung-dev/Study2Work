# Mobile context index

Source roots: `apps/work-client/mobile/flutter_student/` and
`apps/work-client/mobile/flutter_business/`

| Task | Page |
|---|---|
| Architecture | `architecture.md` |
| Dependencies | `dependencies.md` |
| Conventions/theme | `conventions.md` |
| Feature/module ownership | `modules/README.md` |
| Workflow/tests | `workflows/README.md` |
| Mobile DD từ BD/BRD | `create-dd-from-bd-mobile` trong `context-manifest.json` |

The two Flutter apps remain independent packages. Read only the affected app's
source and tests unless a cross-app contract is involved.
