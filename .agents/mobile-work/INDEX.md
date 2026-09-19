# Mobile context index

Source roots: `apps/work-client/mobile/flutter_student/` and
`apps/work-client/mobile/flutter_business/`

| Task | Page |
|---|---|
| Architecture | `architecture.md` |
| Complete tracked-file inventory | `file-inventory.md` |
| Student app deep context | `flutter-student.md` |
| Business app deep context | `flutter-business.md` |
| Cross-app data flow and boundaries | `data-flow.md` |
| Dependencies | `dependencies.md` |
| Conventions/theme | `conventions.md` |
| Feature/module ownership | `modules/README.md` |
| Workflow/tests | `workflows/README.md` |
| Mobile DD từ BD/BRD | `create-dd-from-bd-mobile` trong `context-manifest.json` |

The two Flutter apps remain independent packages. Read only the affected app's
source and tests unless a cross-app contract is involved.

Current inventory contains 210 tracked files: 110 in `flutter_student/` and 100
in `flutter_business/`. The app pages contain per-file runtime responsibilities,
controllers, models, views, route composition and known unwired/legacy states;
`data-flow.md` is the cross-app boundary page.
