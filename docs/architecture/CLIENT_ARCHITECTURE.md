# Study2Work Client Architecture

| Field | Value |
|---|---|
| Status | Canonical |
| Updated | 2026-07-02 |
| Client roots | `apps/*`, `packages/*` |
| Web stack | Vue 3, TypeScript, Vite |
| Mobile stack | Flutter |

## 1. Responsibility

The Client side owns user-facing web and mobile experiences. Clients consume the Server API only through `/api/v1` contracts and must not access persistence, Redis, Celery workers or provider SDKs directly.

This pass documents target structure only. Existing app folders may remain skeletons until a separate implementation task creates runnable clients.

## 2. Web Applications

| App | Audience | Modules |
|---|---|---|
| `apps/web-public` | Guest/public | Landing, public content, community events, help and auth entry points. |
| `apps/web-student` | Student | Dashboard, learning, practice, assessment, projects, AI learning help, community, notifications and profile. |
| `apps/web-mentor` | Mentor | Dashboard, assigned learners, review queue, rubric feedback, workshops and notifications. |
| `apps/web-admin` | Admin | User management, mentor scope, content, rubric, settings, analytics, audit and moderation. |

Target web structure:

```text
apps/<web-app>/
|-- src/
|   |-- app/          # app bootstrap, providers, root shell
|   |-- assets/       # static app assets
|   |-- components/   # app-local reusable components
|   |-- modules/      # role-specific feature modules
|   |-- routes/       # Vue Router route records and guards
|   |-- services/     # API clients and integration adapters
|   |-- stores/       # Pinia stores
|   |-- utils/        # app-local utilities
|   `-- main.ts
|-- public/
|-- tests/
|-- package.json
`-- README.md
```

`web-public` may use `pages`, `sections` and `layouts` instead of role modules when it is content-heavy.

## 3. Mobile Application

`apps/mobile-app` is the Flutter mobile client. It should prioritize student-first Study workflows while sharing API contracts and design decisions with web.

Target mobile structure:

```text
apps/mobile-app/
|-- lib/
|   |-- app/          # app bootstrap, shell, providers
|   |-- core/         # config, constants, routing, theme, utilities
|   |-- features/     # auth, dashboard, learning, practice, assessment, projects, community, profile
|   |-- shared/       # reusable widgets, models and adapters
|   `-- main.dart
|-- test/
|-- pubspec.yaml
`-- README.md
```

## 4. Shared Packages

`packages/*` is reserved for future shared client packages:

| Package | Future responsibility |
|---|---|
| `packages/shared-types` | Generated or approved API contract types. |
| `packages/shared-ui` | Framework-appropriate shared UI primitives for web. |
| `packages/shared-utils` | Pure utilities used by clients. |
| `packages/design-system` | Tokens, accessibility rules and visual primitives. |
| `packages/eslint-config` | Shared JavaScript/TypeScript lint configuration. |
| `packages/tsconfig` | Shared TypeScript configuration. |

Do not place business rules in shared client packages. Business rules remain server-owned and are expressed through approved API contracts.

## 5. API Consumption Rules

- Clients call only `/api/v1` endpoints.
- Clients preserve and display `businessCode` only where useful for support/debug.
- Clients propagate `X-Trace-Id` when present and include it in error reports.
- Clients treat AI output as non-authoritative guidance.
- Client-side validation improves UX but never replaces server validation.
- New API client types should come from approved API DD/OpenAPI, not hand-written assumptions.

## 6. Client Verification

When clients become runnable, add per-app scripts for:

```powershell
pnpm install
pnpm --filter <app> lint
pnpm --filter <app> typecheck
pnpm --filter <app> test
```

Do not add these commands as required gates until the corresponding app manifests are real.
