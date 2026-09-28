# Mobile dependencies

`CONTEXT_STATUS: SOURCE_BACKED`

- The unified project targets Dart `>=3.9.0 <4.0.0` and uses Flutter Material widgets.
- `flutter_riverpod: ^3.3.2` provides flavor/config, repository and session-store
  dependency injection; `go_router: ^18.0.1` provides top-level auth redirect
  and role routes.
- The project uses `postgres: ^3.5.12` for direct Neon PostgreSQL access and
  `http: ^1.5.0` for the direct Gemini `AIService` call.
- `supabase_flutter` is no longer a dependency or runtime import.
- `sqflite` and `path` remain local session/cache dependencies. The business
  app additionally uses `sqflite_common_ffi` for desktop, `fl_chart` for
  reports, `connectivity_plus` for connectivity UI, and `rename_app`.
- The student app also uses `intl` and `shimmer`; the business app uses those
  packages as well. Neither app uses `supabase_flutter`.
- `lib/core/data/neon/neon_client.dart` is shared by both flavors.
- `lib/core/data/sqlite/session_store.dart` is the local-session contract; role
  adapters keep the Student `sinhvien.db` and Business `doanhnghiep.db`
  implementations separate.
- No `.env` dependency is used. `NEON_POOLER_URL` and `GEMINI_API_KEY` live in
  the unified `lib/app/config/app_config.dart` for the current prototype requirement.
- The Cobalt theme uses only Flutter Material 3 and existing widgets; no
  package, font, icon library or asset was added for the UI refresh.

## Per-flavor package and platform details

| Flavor | Runtime-specific dependencies/config |
|---|---|
| `student` | Student features; Android id `com.s2w.work.students`; local DB `sinhvien.db`. |
| `business` | Business features plus `sqflite_common_ffi`, `fl_chart`, `connectivity_plus`, `rename_app`; Android id `com.s2w.work.business`; local DB `doanhnghiep.db`. |

The Android namespace remains `com.example.work_server` for compatibility, while
the Dart package is `study2work_mobile`. `supabase_flutter` is absent; names containing Supabase are
compatibility names for Neon-backed helpers. Both `constants.dart` files define
direct Neon/Gemini configuration, but agent context records only symbol names
and security implications, never credential literals.
