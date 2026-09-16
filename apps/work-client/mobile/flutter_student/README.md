# Study2Work Flutter Student

This module is the Flutter client for student-facing Study2Work workflows. It keeps the existing `work_server` package name and current navigation logic so the app behavior remains unchanged after the repository restructure.

## Features

- Student login and password recovery screens.
- Home, job search, job detail, and application flows.
- CV management and Top CV views.
- Chat, interview schedule, support, courses, news, notifications, and settings screens.
- Direct Neon PostgreSQL synchronization and local SQLite helpers.

## Stack

- Flutter SDK `>=3.9.0 <4.0.0`
- `postgres` (Neon pooler connection)
- `sqflite`, `path`
- `intl`, `shimmer`

## Structure

```text
.
+-- lib/
|   +-- controllers/  # Student app controllers
|   +-- helper_db/    # Local SQLite and direct Neon helper code
|   +-- models/       # Student and external metadata models
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
