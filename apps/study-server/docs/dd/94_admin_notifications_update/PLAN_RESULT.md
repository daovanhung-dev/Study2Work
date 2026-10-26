# Plan result — API #94 Admin cập nhật notification

## Status

- Result: IMPLEMENTED WITH DERIVED FALLBACK; owner/design decisions remain open.
- DD status: Draft — Needs Confirmation.
- Runtime status: Wired in Study source; fake-DB HTTP verification only.
- AC-36 macro-review: `VERIFIED_WITH_OPEN_QUESTIONS`; APIs #95/#96 remain outside this implementation.

## Direct API requirement

- API #94: `PUT /api/v1/admin/notifications/{notification_id}`.
- Auth: Bearer JWT/Admin; AC-36 additionally names notification-management permission.
- Direct request: `notification_id:int64!`; no body/query is declared.
- Direct response: `ApiEnvelope<Notification>`.
- Success: HTTP 200 `DESIGN_RESOURCE_UPDATED`.
- Errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`.
- AC-36 branch: UPDATE Notification, then reload management.

## Local fallback implemented

- Strict `{title, content}` body; nonblank strings; title maximum 200 based on legacy DDL candidate.
- Shared ADMIN role guard runs before path/body parsing and database access.
- Lock one recipient-level BIGINT notification row and its delivery rows. Only rows with at least one delivery and all delivery statuses `QUEUED` can be updated.
- Update only `notifications.title/content`; preserve recipient, sender, type, read state, channel/delivery rows and `created_at`.
- Return one `AdminNotificationResponse`; derive channels/status from locked outbox rows. Do not call scheduler/provider or add migration.
- These request/lifecycle/mapping choices are DERIVED, not approved contract and not proof of live schema.

## Changed areas

- New API #94 models, SQL-only query constants, validator, view and PUT route.
- Dynamic notification path added to middleware contract paths; linked API #92/#93 OpenAPI counts updated.
- Focused HTTP tests use fake sessions and query doubles.
- DD #94, AC-36 macro-review and server-study context updated.

## Verification

- Focused API #94 HTTP tests: 20 passed.
- Linked #92–#94 regression: 66 passed.
- Full Study Server suite: 1263 passed; one upstream Starlette/httpx TestClient deprecation warning.
- Ruff check and scoped format checks pass; OpenAPI exposes 55 paths / 65 operations.
- Static DD package contains 12 Markdown files and preserves the existing template appendix suffixes. These checks do not verify runtime DB behavior.

## Remaining decisions

- Approve/replace body and title/content validation.
- Confirm Admin target grain/schema and delivery editability policy.
- Define audience/channels/schedule mutation and fine-grained notification-management permission.
- Resolve shared #93 Operation bridge and #95/#96 semantics.
- No PostgreSQL, live schema, production deployment or provider delivery verification was performed.
