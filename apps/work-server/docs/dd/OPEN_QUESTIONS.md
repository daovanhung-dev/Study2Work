# OPEN_QUESTIONS

## Q-001 — Password request alias and validation drift

- Source: `api_routes.ts:loginStudent/loginBusiness` accepts `matkhau ?? password` and only checks presence.
- Contract/client: `legacy-web.openapi.json` and Work Web send `password` and describe email/password constraints.
- Impact: Request DD documents both current accepted keys and marks the contract drift.
- Decision needed: standardize on `password` and add source-level format/length validation, or preserve alias behavior.

## Q-002 — Sensitive fields in full Prisma responses

- Source: student registration, `getMe`, applications and related service calls can return full Prisma records containing `matkhau`.
- Impact: response contract may expose credential material.
- Decision needed: introduce explicit public select projections and update the API contract. This DD batch records the current behavior and does not alter runtime code.

## Q-003 — Mutation transaction boundary

- Source: each current route calls one Prisma mutation without an explicit transaction.
- Impact: DD marks transaction as source-level `N/A`, not as a stronger atomicity guarantee.
- Decision needed: define transaction/idempotency policy if multi-step flows are added.

## Q-004 — Target OpenAPI catalog

- Source: `contracts/openapi/work/openapi.json` contains target endpoints not registered by `api_routes.ts`.
- Impact: those endpoints are not included in this source-backed runtime DD batch.
- Decision needed: create a separate target-contract DD batch only after route/source implementation exists.
