# Mobile source inventory

`CONTEXT_STATUS: SOURCE_BACKED`

Source root: `apps/work-client/mobile/`. This is one Flutter project with two
Android flavors, `student` and `business`. Generated `build/`, `.dart_tool/`,
Gradle caches and other generated artifacts are excluded.

## Runtime boundaries

| Path | Kind | Responsibility | Status |
|---|---|---|---|
| `pubspec.yaml` | Config | Unified package and superset dependencies | WIRED |
| `lib/main.dart` | Entrypoint | Flavor detection, ProviderScope and bootstrap | WIRED |
| `lib/app/` | App layer | Config, router and shared Material theme | WIRED |
| `lib/core/data/neon/neon_client.dart` | Data boundary | SSL validation, parameterized SQL, row normalization and pool lifecycle | WIRED |
| `lib/core/data/gemini/gemini_client.dart` | Data boundary | Direct Gemini HTTP client compatibility boundary | WIRED |
| `lib/core/data/sqlite/session_store.dart` | Contract | Local session store interface | WIRED |
| `lib/shared/providers/` | DI | Flavor/config, auth, chat, Neon and Gemini providers | WIRED |
| `lib/shared/chat/message_polling.dart` | Shared behavior | Three-second polling, initial seeding and id deduplication | WIRED |
| `lib/shared/models/` | Shared model | Cross-role chat message normalization | WIRED |
| `lib/shared/domain/` | Contracts | Repository interfaces for role adapters | DECLARED_NOT_RUNNABLE |
| `lib/features/auth/` | Shared feature | Auth repository contract and role login adapter | WIRED |
| `lib/features/student/legacy/` | Role migration source | Student controllers, helpers, models and screens | WIRED/LEGACY MIXED |
| `lib/features/business/legacy/` | Role migration source | Business controllers, helpers, models and screens | WIRED/LEGACY MIXED |
| `lib/features/student/{auth,chat,presentation}/` | Role feature boundary | Student auth/session/chat adapters and shell wrapper | WIRED |
| `lib/features/business/{auth,chat,presentation}/` | Role feature boundary | Business auth/session/chat adapters and shell wrapper | WIRED |
| `test/student/` | Tests | Student Neon/model/polling tests | WIRED |
| `test/business/` | Tests | Business Neon/model/polling tests | WIRED |
| `test/shared/` | Tests | Flavor config and shared model tests | WIRED |

## Android flavor boundary

| Path | Responsibility | Status |
|---|---|---|
| `android/app/build.gradle.kts` | `student`/`business` product flavors and application IDs | WIRED |
| `android/app/src/main/` | Shared Flutter Android host and fallback resources | WIRED |
| `android/app/src/student/` | Student app name and launcher resources | WIRED |
| `android/app/src/business/` | Business app name and launcher resources | WIRED |
| `assets/student/` | Student role assets | WIRED/LEGACY_ASSET_MIXED |
| `assets/business/` | Business role assets | WIRED/LEGACY_ASSET_MIXED |

## Migration status

- `work_server` imports have been migrated to the unified `study2work_mobile`
  package.
- Top-level login and role shell use go_router; some legacy child screens still
  use `MaterialPageRoute` until their vertical-slice migration is complete.
- Legacy screens/helpers without current route evidence remain under the role
  legacy directories and are not imported by the new top-level router.
- Exact source ownership still wins over this inventory when a feature task
  changes a legacy file.
