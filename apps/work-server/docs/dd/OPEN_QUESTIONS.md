# OPEN_QUESTIONS

## Q-001 — Legacy plaintext account migration

- Current source still accepts legacy plaintext password rows and best-effort rehashes them after successful login.
- Operational question: define the rehash/reset window before disabling fallback.

## Q-002 — Target OpenAPI catalog

- `contracts/openapi/work/openapi.json` contains target domains not registered by current Work Server routers.
- Create a separate DD batch only after those endpoints are implemented.

## Resolved in this DD rewrite

- Transaction documentation now follows actual `$transaction` boundaries in CV, application and business-job mutations.
- System routes are included because they are currently wired.

## Resolved — API naming

- Compatibility API IDs and folder names remain unchanged.
- Source runtime names are now used in `api_name` and documented separately from contract IDs.
- No API route, OpenAPI operation ID or runtime behavior is changed by this documentation update.
