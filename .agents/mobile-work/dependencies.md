# Mobile dependencies

`CONTEXT_STATUS: SOURCE_BACKED`

- Both apps target Dart `>=3.9.0 <4.0.0` and use Flutter Material widgets.
- Both apps use `postgres: ^3.5.12` for direct Neon PostgreSQL access.
- `supabase_flutter` is no longer a dependency or runtime import.
- `sqflite` and `path` remain local session/cache dependencies. The business
  app additionally uses `sqflite_common_ffi` for desktop, plus its existing
  UI/network packages.
- `lib/helper_db/neon_db.dart` is duplicated intentionally because the two
  standalone Flutter apps both expose the package name `work_server`.
- No `.env` dependency is used. `NEON_POOLER_URL` lives in each app's
  `lib/constants.dart` for the current prototype requirement.
