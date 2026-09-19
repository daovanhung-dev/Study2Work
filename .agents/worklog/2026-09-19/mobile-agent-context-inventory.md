---
task_id: "2026-09-19-mobile-agent-context-inventory"
date: "2026-09-19"
primary_task_type: "docs"
secondary_task_types:
  - context-maintenance
  - architecture-inventory
project_scopes:
  - mobile-work
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Mobile deep-context inventory

## EXPECTED_BEHAVIOR

- Requirement: Nạp deep-context cho toàn bộ `apps/work-client/mobile`, gồm hai
  Flutter app, từng file tracked, views, controllers, models, helper/data flow,
  wiring status và discrepancy.
- Canonical contract/approved DD: Root `AGENTS.md`, `.agents/mobile-work/`
  router and `.agents/context-manifest.json`; no runtime code or API contract
  change authorized.

## CURRENT_BEHAVIOR

- Source/config: `flutter_student` và `flutter_business` là hai package độc lập,
  cùng Dart package name `work_server`, direct Neon/SQLite/Gemini clients,
  MaterialPageRoute navigation và local Cobalt theme.
- Runnable tests: two unit-test files per app exist; Neon connection smoke tests
  are opt-in. Flutter/Dart/Node executables are not installed in this environment.
- Runtime wiring: login, home, job/CV/application, chat and settings flows are
  source-backed; legacy/placeholder/unwired files are marked in the mobile pages
  and inventory.

## SOURCE_TRACE

```text
main.dart -> DangNhap -> login controller -> Neon helper -> NeonDatabase -> Neon
                         -> SQLite account/major cache -> Menu
Menu -> role home/search/chat/settings/candidate views
View -> controller/helper -> model mapping -> Neon SQL or SQLite side effect
ChatView -> getChat/guiTinNhan -> Chat -> Timer.periodic(3s) -> dispose cancel
AI view/helper -> AIService -> Gemini HTTP API
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Context was previously summary-level | Existing mobile pages had no exhaustive file inventory or per-app deep page. | SOURCE_CHANGED | Added inventory and app/data-flow pages. |
| Source inventory boundary | `git ls-files apps/work-client/mobile` returns 210 files; generated dirs are excluded. | VERIFIED | Inventory covers all tracked files and excludes generated output. |
| Supabase naming | Helpers/classes contain Supabase in names but import/use `postgres` and `NeonDatabase`. | DISCREPANCY | Context documents compatibility naming, not Supabase runtime. |
| Direct credentials | Both `lib/constants.dart` files contain Neon/Gemini constants. | SOURCE_BACKED | Context redacts literals and records prototype-only security boundary. |
| README platform claim | READMEs mention `web/`, but current tracked source has no tracked web directory. | DISCREPANCY | Source wins; no missing runtime file was invented. |
| Validation toolchain | `node`, `flutter`, and `dart` are unavailable. | DECLARED_NOT_RUNNABLE | Validator/analyzer/test commands could not be executed. |
| Runtime stubs/legacy copies | Source contains placeholder screens and active/legacy duplicate view/helper/model shapes. | UNWIRED / EMPTY_PLACEHOLDER | Status recorded per app page and inventory; no runtime wiring changed. |

## CHANGES

- Files changed:
  - `.agents/mobile-work/file-inventory.md`
  - `.agents/mobile-work/flutter-student.md`
  - `.agents/mobile-work/flutter-business.md`
  - `.agents/mobile-work/data-flow.md`
  - `.agents/mobile-work/AGENTS.md`, `INDEX.md`, architecture/dependencies/
    conventions/modules/workflows pages
  - `.agents/AGENTS.md`, `.agents/context-manifest.json`
  - This worklog
- CONTEXT_UPDATES: Registered all four new mobile pages in the manifest and
  page graph; documented file purpose, route/controller/helper/model links,
  database/external side effects, wiring states and security boundary.
- Context pages changed: mobile scope only; no cross-scope contract page was
  changed because no runtime cross-scope dependency was found.
- Assumptions: tracked source is canonical; generated/cache directories are
  intentionally excluded; context contains no secret values.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git ls-files apps/work-client/mobile \| wc -l` | 210 tracked files; inventory has 210 file rows plus table header. | VERIFIED |
| `git diff --check` | Passed with no whitespace errors. | VERIFIED |
| `python3 -m json.tool .agents/context-manifest.json` | Manifest parsed successfully. | VERIFIED |
| Read-only inventory reconciliation | 210 tracked paths = 210 inventory rows; no missing/extra paths. | VERIFIED |
| Read-only context-link check | 13 changed/created context/worklog files checked; no broken local links. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | `node: command not found`. | DECLARED_NOT_RUNNABLE |
| `flutter analyze` / `flutter test` for both apps | `flutter`/`dart` not installed. | DECLARED_NOT_RUNNABLE |

## HANDOFF

- Remaining blockers: Install Node for context validation and Flutter/Dart for
  analyzer/tests.
- Next owner/action: Run the unavailable verification commands, then update
  this worklog status to `VERIFIED` if they pass. Do not run Neon smoke tests
  unless explicitly supplying `--dart-define=RUN_NEON_SMOKE=true`.
