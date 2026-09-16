# Mobile architecture

`CONTEXT_STATUS: SOURCE_BACKED`

## Applications

`apps/work-client/mobile/flutter_student/` and
`apps/work-client/mobile/flutter_business/` are separate Flutter applications.
Both intentionally retain the package name `work_server`, so imports must be
resolved relative to the individual app rather than treated as a shared Dart
package.

## Dependency direction

```text
views -> controllers -> helper_db -> NeonDatabase -> Neon PostgreSQL
views -> controllers -> SQLite helpers (session/cache)
views -> models
```

`lib/helper_db/neon_db.dart` is the remote data boundary in each app. It owns
lazy pool creation, connection URL normalization, parameterized execution,
row normalization, and pool shutdown. Existing helper class names containing
`Supabase` remain as compatibility interfaces for current UI callers; their
implementation is now Neon SQL.

## Remote data contract

The mobile clients query the quoted PostgreSQL tables currently present in the
work-server schema: `"SinhVien"`, `"DoanhNghiep"`, `"Chat"`, `"Cv"`,
`"DoanChat"`, `"JD"`, `"TopCV"`, `"TopJD"`, and `"UngVien"`. The lowercase
`bannganh` lookup is maintained by the work-server migration.

Chat does not use realtime channels. Each chat screen owns a `Timer` polling
every three seconds, deduplicates by message `id`, and cancels it in
`dispose()`.

## Security boundary

This direct connection is prototype/development-only. The Neon credential is
compiled into each APK. Production architecture must move database access to a
backend API and use a least-privilege, rotated database credential.
