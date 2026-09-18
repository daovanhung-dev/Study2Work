# OPEN_QUESTIONS

## Q-001 — Mutation transaction boundary

- Source: each current route calls one Prisma mutation without an explicit transaction.
- Impact: DD marks transaction as source-level `N/A`, not as a stronger atomicity guarantee.
- Decision needed: define transaction/idempotency policy if multi-step flows are added.

## Q-002 — Legacy plaintext account migration

- Source: login keeps a compatibility fallback for pre-existing plaintext rows and rehashes them best-effort after successful login.
- Impact: rows that never authenticate remain legacy plaintext until seed/reset/migration policy is applied.
- Decision needed: choose an operational rehash/reset window before disabling the fallback.

## Q-003 — Target OpenAPI catalog

- Source: `contracts/openapi/work/openapi.json` contains target endpoints not registered by `api_routes.ts`.
- Impact: those endpoints are not included in this source-backed runtime DD batch.
- Decision needed: create a separate target-contract DD batch only after route/source implementation exists.
