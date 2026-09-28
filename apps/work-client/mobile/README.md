# Study2Work Mobile

Unified Flutter client for the Student and Business roles.

## Flavors

The Android project builds two installable apps from the same source tree:

```bash
flutter run --flavor student
flutter run --flavor business

flutter build appbundle --flavor student
flutter build appbundle --flavor business

flutter build apk --flavor student
flutter build apk --flavor business
```

The application IDs remain `com.s2w.work.students` and
`com.s2w.work.business`. The Dart package is `study2work_mobile`.

## Architecture

- `app/`: bootstrap, flavor configuration, router and theme.
- `core/`: direct Neon, Gemini and SQLite infrastructure boundaries.
- `shared/`: reusable providers, models and cross-role behavior.
- `features/`: role-specific features. Existing source is temporarily kept
  under `features/student/legacy` and `features/business/legacy` while each
  active flow is migrated behind repository and provider boundaries.

The mobile client currently keeps the prototype direct Neon/Gemini behavior.
Production must move those credentials and data operations behind a least-
privilege backend boundary.

## Checks

```bash
flutter pub get
flutter analyze
flutter test
```

The Neon network smoke test is opt-in:

```bash
flutter test --dart-define=RUN_NEON_SMOKE=true
```
