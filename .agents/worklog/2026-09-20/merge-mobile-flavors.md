---
task_id: "2026-09-20-merge-mobile-flavors"
date: "2026-09-20"
primary_task_type: "coding"
secondary_task_types: ["test", "context-maintenance"]
project_scopes: ["mobile-work"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Hợp nhất mobile thành một Flutter project và hai Android flavors

## PRIOR_WORKLOG_REVIEW

- primary_task_type: coding
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-20/implement-study-auth-login-refresh.md`
    - carry_forward: Giữ thay đổi hiện có; ghi rõ toolchain không runnable và không claim verification chưa chạy.
  - path: `.agents/worklog/2026-09-20/publish-develop-to-github.md`
    - carry_forward: Không overwrite hoặc commit thay đổi ngoài phạm vi task.
  - path: `.agents/worklog/2026-09-19/extract-strip-email-utility.md`
    - carry_forward: Giữ source-backed boundary, cập nhật context khi contract/path thay đổi và xác minh bằng validator.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Hợp nhất `flutter_student` và `flutter_business` thành một Flutter project tại `apps/work-client/mobile/`, build hai Android app bằng flavors `student` và `business`, giữ application IDs, đổi Dart package thành `study2work_mobile`, thêm feature-first/core/shared boundary, Riverpod, go_router và repository interfaces mà không đổi DB/schema/direct Neon-Gemini behavior.
- Approved plan: Migrate theo phase; active flows trước, legacy/placeholder archive; giữ Android là target phase đầu.

## CURRENT_BEHAVIOR

- Source/config: Hai package độc lập, package Dart `work_server`, 210 tracked source files; chỉ có Android host cho từng app; Student/Business có 12 Dart file chung hoàn toàn và 17 file cùng path nhưng khác logic.
- Runtime wiring: `main.dart` của mỗi app tự tạo `MaterialApp`; login/menu dùng `MaterialPageRoute`; controllers/helpers gọi trực tiếp Neon/SQLite/Gemini; chưa có flavor, Riverpod hoặc go_router.
- Runnable tests: Chỉ có `neon_test.dart` và opt-in `neon_connection_test.dart` ở mỗi app; `flutter`/`dart` không có executable trong shell.

## SOURCE_TRACE

```text
mobile root -> old flutter_student/flutter_business package roots
-> main.dart -> DangNhap -> controller -> helper -> Neon/SQLite/Gemini
-> Menu -> role-specific views/controllers
-> neon_test.dart + neon_connection_test.dart
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Flutter SDK | `command -v flutter` and `command -v dart` absent | DECLARED_NOT_RUNNABLE | Static checks only; build/analyze/test deferred |
| Existing source snapshot | Mobile context is source-backed at 210 files; merge will intentionally change paths | SOURCE_CHANGED_EXPECTED | Must update mobile context pages after migration |
| Direct client credentials | Current constants are duplicated in both apps | PROTOTYPE_SECURITY_BOUNDARY | Centralize config; backend/security migration remains out of scope |
| Legacy screens/helpers | Inventory marks multiple `UNWIRED`, `LEGACY`, `PLACEHOLDER` items | UNWIRED/LEGACY/PLACEHOLDER | Keep outside new runtime until active flows pass |

## CHANGES

- Hợp nhất hai package vào `apps/work-client/mobile/`: một `pubspec.yaml`, một
  Android host, một `lib/`, `assets/` và `test/`; source role cũ được giữ dưới
  `features/student/legacy/` và `features/business/legacy/` để rollback/migrate
  theo slice.
- Đổi Dart package thành `study2work_mobile`, cập nhật package imports và asset
  paths; giữ nguyên database/table/SQL/direct Neon-Gemini behavior.
- Thêm Android product flavors `student`/`business`, application IDs cũ,
  flavor app name bằng `resValue`, launcher resources riêng và `appFlavor` /
  `AppConfig` tập trung.
- Thêm app bootstrap, Riverpod providers, go_router auth/role routes,
  `AuthNavigationState`, shared `NeonClient`, `GeminiClient`, `SessionStore`,
  repository contracts/adapters, Student/Business SQLite session adapters,
  shared `ChatMessage` và polling implementation.
- Nối login chính qua `authRepositoryProvider`; logout chờ local clear rồi cập
  nhật router auth state. Các view legacy còn lại được đặt sau role application
  facade để không import trực tiếp database/Gemini implementation.
- Thêm README root và shared/auth/config tests. Neon network smoke tests vẫn
  opt-in như trước.
- Generated/cache directories không được đưa vào migration; một số thư mục
  generated cũ đã được di chuyển tạm thời, có thể phục hồi tại
  `/tmp/study2work-mobile-old.op7pVA`.
- CONTEXT_UPDATES: cập nhật `context-manifest.json`, context-map, toàn bộ
  mobile-work architecture/dependencies/data-flow/inventory/deep role pages,
  module/workflow/convention pages và source-status.
- Assumptions: Preserve current SQL/table/SQLite contracts and user-visible
  behavior; use a root superset pubspec; keep Flutter-generated/build/cache
  artifacts out of tracked migration; defer full typed Job/CV/Candidate vertical
  slices until the Flutter runtime is available.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type coding --limit 3` | Selected and read 3 coding worklogs | VERIFIED |
| Current source inventory and import/config inspection | Baseline recorded above | VERIFIED |
| Deno package/relative import resolver | 137 Dart files; 0 unresolved imports; 0 old `work_server` imports | VERIFIED |
| Direct infrastructure import scan for legacy views | No direct Neon/SQLite/Gemini implementation imports remain in role legacy views/AI test screens | VERIFIED |
| Asset reference scan | 34 references found; 10 missing references already present in the source before merge | DISCREPANCY_PRE_EXISTING |
| `git diff --check` | No whitespace errors | VERIFIED |
| Flavor/config assertions | Package name, default flavor, flavor IDs, app names and resource wiring present | VERIFIED |
| `validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| Full `validate-agent-context.mjs` | Existing stale snapshots in server-study, server-work, web-work, db-admin and intentional mobile source migration | CONTEXT_STALE_OUT_OF_SCOPE/EXPECTED |
| `flutter pub get` | Flutter executable unavailable; lockfile was not regenerated for new Riverpod/go_router dependencies | DECLARED_NOT_RUNNABLE |
| `flutter analyze` | Flutter executable unavailable | DECLARED_NOT_RUNNABLE |
| `flutter test` | Flutter executable unavailable | DECLARED_NOT_RUNNABLE |
| `flutter build apk/appbundle --flavor student/business` | Flutter executable unavailable | DECLARED_NOT_RUNNABLE |

## HANDOFF

- Implemented foundation: one project, two Android flavors, shared app/core/
  shared boundaries, top-level auth routing and transitional role adapters.
- Remaining blocker: Flutter/Dart runtime unavailable, so `pub get`, analyzer,
  widget/unit tests and all APK/AAB builds are not verified here. `pubspec.lock`
  must be regenerated by `flutter pub get` on a Flutter SDK environment.
- Remaining migration work: move active Student/Business home/jobs/CV/
  candidate/report slices from `legacy` into typed feature repositories,
  controllers/providers and go_router child routes; resolve the 10 pre-existing
  missing asset references; then run the full acceptance matrix.
