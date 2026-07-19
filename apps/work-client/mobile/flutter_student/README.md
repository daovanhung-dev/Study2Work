# Learn2Earn Flutter Student

This module is the Flutter client for student-facing Learn2Earn workflows. It keeps the existing `learn2earn` package name and current navigation logic so the app behavior remains unchanged after the repository restructure.

## Features

- Student login and password recovery screens.
- Home, job search, job detail, and application flows.
- CV management and Top CV views.
- Chat, interview schedule, support, courses, news, notifications, and settings screens.
- Supabase-backed synchronization and local SQLite helpers.

## Stack

- Flutter SDK `>=3.8.1 <4.0.0`
- `supabase_flutter`
- `sqflite`, `path`
- `intl`, `shimmer`

## Structure

```text
.
+-- lib/
|   +-- controllers/  # Student app controllers
|   +-- helper_db/    # Local and Supabase helper code
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

- Keep the package name as `learn2earn` unless imports are migrated deliberately.
- Supabase configuration is currently initialized in `lib/main.dart`.
- Android local configuration such as `android/local.properties` is ignored by Git.
