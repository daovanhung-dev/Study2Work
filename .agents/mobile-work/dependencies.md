# Mobile dependencies

`CONTEXT_STATUS: SOURCE_BACKED`

- Both apps target Dart `>=3.9.0 <4.0.0` and use Flutter Material widgets.
- Both apps use `postgres: ^3.5.12` for direct Neon PostgreSQL access and
  `http: ^1.5.0` for the direct Gemini `AIService` call.
- `supabase_flutter` is no longer a dependency or runtime import.
- `sqflite` and `path` remain local session/cache dependencies. The business
  app additionally uses `sqflite_common_ffi` for desktop, `fl_chart` for
  reports, `connectivity_plus` for connectivity UI, and `rename_app`.
- The student app also uses `intl` and `shimmer`; the business app uses those
  packages as well. Neither app uses `supabase_flutter`.
- `lib/helper_db/neon_db.dart` is duplicated intentionally because the two
  standalone Flutter apps both expose the package name `work_server`.
- No `.env` dependency is used. `NEON_POOLER_URL` and `GEMINI_API_KEY` live in
  each app's `lib/constants.dart` for the current prototype requirement.
- The Cobalt theme uses only Flutter Material 3 and existing widgets; no
  package, font, icon library or asset was added for the UI refresh.

## Per-app package and platform details

| App | Runtime-specific dependencies/config |
|---|---|
| `flutter_student` | `postgres`, `http`, `sqflite`, `path`, `intl`, `shimmer`; Android id `com.s2w.work.students`; local DB `sinhvien.db`. |
| `flutter_business` | Student dependencies plus `sqflite_common_ffi`, `fl_chart`, `connectivity_plus`, `rename_app`; Android id `com.s2w.work.business`; local DB `doanhnghiep.db`. |

Both apps retain namespace/package `com.example.work_server` and Dart package
name `work_server`. `supabase_flutter` is absent; names containing Supabase are
compatibility names for Neon-backed helpers. Both `constants.dart` files define
direct Neon/Gemini configuration, but agent context records only symbol names
and security implications, never credential literals.
