# Mobile context index

Source root: `apps/work-client/mobile/` (one Flutter project, Android flavors
`student` and `business`).

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

The two flavors share one package and core infrastructure. Read only the
affected role feature and tests unless a shared boundary is involved.

The current source keeps role-specific migration files under
`lib/features/student/legacy/` and `lib/features/business/legacy/`; new code
belongs under `app/`, `core/`, `shared/` and role feature subdirectories.
`data-flow.md` is the shared data boundary page.
