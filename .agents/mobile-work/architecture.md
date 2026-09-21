# Mobile architecture

`CONTEXT_STATUS: SOURCE_BACKED`

Deep context pages:

- [`file-inventory.md`](file-inventory.md): every tracked file and current status.
- [`flutter-student.md`](flutter-student.md): student runtime graph and modules.
- [`flutter-business.md`](flutter-business.md): business runtime graph and modules.
- [`data-flow.md`](data-flow.md): Neon/SQLite/Gemini and feature data flows.

## Project and flavors

`apps/work-client/mobile/` is one Flutter application package named
`study2work_mobile`. Android product flavors `student` and `business` preserve
the existing application IDs and install as two separate apps. Role-specific
source is temporarily kept under `lib/features/student/legacy/` and
`lib/features/business/legacy/` while active flows move behind new feature and
repository boundaries.

## Startup and dependency direction

`lib/main.dart` đọc Android `appFlavor`, tạo `AppConfig`, khởi tạo
`ProviderScope` và `MaterialApp.router`. `app/router/app_router.dart` chọn
Student/Business login và shell theo flavor, đồng thời áp dụng auth redirect và
named routes. Legacy screens vẫn còn một số `MaterialPageRoute` nội bộ trong
giai đoạn migrate; top-level auth/shell đã đi qua go_router.

```text
new presentation -> Riverpod provider -> repository contract -> role adapter
  -> legacy controller/helper -> NeonDatabase/SQLite helper
legacy presentation -> controller/helper (transitional compatibility path)
shared chat polling/model -> role chat repository adapters
```

`features/auth/presentation/role_login_page.dart` receives the role-specific
`AuthRepository` from Riverpod. The current adapter delegates to the existing
login controller so SQL and local-session behavior remain unchanged. Logout
updates `AuthNavigationState` after the existing local clear completes. The
Student and Business `SessionStore` adapters expose the current SQLite helpers
without changing their database names or schemas.

Screens that are still transitional use
`features/student/application/student_legacy_data.dart` or
`features/business/application/business_legacy_data.dart` as a compatibility
facade. This removes direct database-helper imports from those views while the
typed Job/CV/Candidate repositories are migrated slice by slice.

`lib/core/data/neon/neon_client.dart` is the shared remote data boundary. It owns
lazy singleton pool creation, SSL URL validation/normalization, parameterized
execution, `BIGINT` row normalization, and pool shutdown. Existing helper class
names containing `Supabase` remain as compatibility interfaces for current UI
callers; their implementation is now Neon SQL.

Login reads credentials from Neon, stores the current student/business record
and major lookup in SQLite, and logout clears the local account row. This is a
local cache/session flow, not a JWT or Work HTTP API flow.

## Remote data contract

The mobile clients query the quoted PostgreSQL tables currently present in the
work-server schema: `"SinhVien"`, `"DoanhNghiep"`, `"Chat"`, `"Cv"`,
`"DoanChat"`, `"JD"`, `"TopCV"`, `"TopJD"`, and `"UngVien"`. The lowercase
`bannganh` lookup is maintained by the work-server migration. Student and
business helpers also expose CV, job, candidate/application and conversation
operations directly against those tables.

Chat does not use realtime channels. Each chat screen owns a `Timer` polling
every three seconds, deduplicates by message `id`, and cancels it in
`dispose()`.

The shared `core/data/gemini/gemini_client.dart` sends prompt text directly to
the Gemini HTTP API; it is independent of `apps/ai-server` and `apps/work-server`.

The inventory includes one Android host, flavor resources, shared infrastructure,
role-specific migration source and tests, but excludes generated `build/`,
`.dart_tool/` and cache directories. Several legacy or placeholder screens
remain beside active page variants; their wiring status is recorded in the role
pages instead of being inferred from filenames.

## Presentation foundation

Theme dùng chung tại `lib/app/theme/` gồm `design_tokens.dart`, `app_theme.dart`
và `app_components.dart`. `main.dart` khởi tạo Material 3 theme; menu/login/helper UI tiêu thụ `ColorScheme`, token
và primitive nội bộ thay cho palette mặc định `deepPurple`. Thay đổi này chỉ
ở presentation; không chạm vào MaterialPageRoute, session/cache, Neon,
Gemini hoặc chat polling.

## Security boundary

This direct connection and the embedded Gemini/Neon configuration are
prototype/development-only. Credentials are compiled into each APK. Production
architecture must move database/AI access behind backend boundaries and use
least-privilege, rotated credentials.
