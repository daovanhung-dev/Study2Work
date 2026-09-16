# Study2Work Flutter Business

This module is the Flutter client for business-facing Study2Work workflows. It keeps the existing `work_server` package name and current runtime logic so the app behavior remains unchanged after the repository restructure.

## Features

- Business login and account screens.
- Candidate search, applicant list, and CV detail flows.
- Job posting, job management, and job detail/update flows.
- Reports and statistics screens.
- Chat, interview schedule, university linking, notifications, and settings screens.
- Direct Neon PostgreSQL synchronization and local SQLite helpers.

## Stack

- Flutter SDK `>=3.9.0 <4.0.0`
- `postgres` (Neon pooler connection)
- `sqflite`, `sqflite_common_ffi`, `path`
- `fl_chart`, `intl`, `shimmer`
- `http`, `connectivity_plus`

## Structure

```text
.
+-- lib/
|   +-- controllers/  # Business app controllers
|   +-- helper_db/    # Local SQLite and direct Neon helper code
|   +-- models/       # Business, job, CV, chat, and candidate models
|   +-- views/        # Screens and UI flows
+-- assets/           # Images and icons
+-- android/          # Android project
+-- web/              # Flutter web assets
```

## Setup

```bash
flutter pub get
flutter run
```

## Checks

```bash
flutter analyze
flutter test
```

## Notes

- Keep the package name as `work_server` unless imports are migrated deliberately.
- Neon configuration is intentionally stored in `lib/constants.dart`; this is a prototype/development setup and does not use `.env`.
- Chat uses a 3-second polling timer because the Neon pooler runs in transaction mode and is not used for `LISTEN/NOTIFY`.
- The Neon credential is embedded in the APK and can be extracted. The current account has high database privileges and could read, modify, or delete all data.
- Before production release, move database access behind a backend API, use a least-privilege database credential, and rotate the current Neon credential.
- Android local configuration such as `android/local.properties` is ignored by Git.
