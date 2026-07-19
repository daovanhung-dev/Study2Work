# Learn2Earn Flutter Business

This module is the Flutter client for business-facing Learn2Earn workflows. It keeps the existing `learn2earn` package name and current runtime logic so the app behavior remains unchanged after the repository restructure.

## Features

- Business login and account screens.
- Candidate search, applicant list, and CV detail flows.
- Job posting, job management, and job detail/update flows.
- Reports and statistics screens.
- Chat, interview schedule, university linking, notifications, and settings screens.
- Supabase-backed synchronization and local SQLite helpers.

## Stack

- Flutter SDK `>=3.8.1 <4.0.0`
- `supabase_flutter`
- `sqflite`, `sqflite_common_ffi`, `path`
- `fl_chart`, `intl`, `shimmer`
- `http`, `connectivity_plus`

## Structure

```text
.
+-- lib/
|   +-- controllers/  # Business app controllers
|   +-- helper_db/    # Local and Supabase helper code
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

- Keep the package name as `learn2earn` unless imports are migrated deliberately.
- Supabase configuration and desktop SQLite initialization are currently in `lib/main.dart`.
- Android local configuration such as `android/local.properties` is ignored by Git.
