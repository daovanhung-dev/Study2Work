# Mobile architecture

`CONTEXT_STATUS: SOURCE_BACKED`

## Applications

`apps/work-client/mobile/flutter_student/` and
`apps/work-client/mobile/flutter_business/` are separate Flutter applications.
Both intentionally retain the package name `work_server`, so imports must be
resolved relative to the individual app rather than treated as a shared Dart
package.

## Startup and dependency direction

Student `lib/main.dart` khởi động `MaterialApp` với `DangNhap` làm `home`.
Business `lib/main.dart` cũng khởi động từ `DangNhap` và khởi tạo
`sqflite_common_ffi` trên desktop non-Android/iOS. Navigation hiện dùng các
`MaterialPageRoute` từ view; không có shared router package.

```text
views -> controllers -> helper_db -> NeonDatabase -> Neon PostgreSQL
views -> controllers -> SQLite helpers (session/cache)
views -> models
```

`lib/helper_db/neon_db.dart` is the remote data boundary in each app. It owns
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

Both apps also contain `AIService`, which sends prompt text directly to the
Gemini HTTP API; it is independent of `apps/ai-server` and `apps/work-server`.

## Presentation foundation

Mỗi app có bộ theme độc lập tại `lib/theme/` gồm `design_tokens.dart`,
`app_theme.dart` và `app_components.dart`. Hai bộ dùng cùng giá trị Cobalt
trong design context nhưng không tạo Dart package dùng chung. `main.dart`
khởi tạo Material 3 theme; menu/login/helper UI tiêu thụ `ColorScheme`, token
và primitive nội bộ thay cho palette mặc định `deepPurple`. Thay đổi này chỉ
ở presentation; không chạm vào MaterialPageRoute, session/cache, Neon,
Gemini hoặc chat polling.

## Security boundary

This direct connection and the embedded Gemini/Neon configuration are
prototype/development-only. Credentials are compiled into each APK. Production
architecture must move database/AI access behind backend boundaries and use
least-privilege, rotated credentials.
