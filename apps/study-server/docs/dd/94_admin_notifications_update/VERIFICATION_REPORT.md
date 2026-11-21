# Báo cáo kiểm chứng — API #94 Admin cập nhật notification

## Phạm vi

- DD folder: `apps/study-server/docs/dd/94_admin_notifications_update/`.
- DD status: Draft — Needs Confirmation.
- Runtime source: PUT route/module wired locally; no live database or deployment verification.
- AC-36 macro-review: `VERIFIED_WITH_OPEN_QUESTIONS`; #92–#95 are now locally wired and #96 remains unwired (current group status is recorded in the macro-review).

## Nguồn đối chiếu

- Catalog #94, reusable Notification schema, AC/API index and AC-36 UPDATE edge.
- Legacy BIGINT notifications/outbox DDL and separate V1-PILOT UUID DDL.
- APIs #92/#93 response and recipient/delivery grain, current route/middleware, and API #94 source/tests.
- Three selected coding worklogs (#74–#76) were read in the task preflight; no shortage.

## Template and package

- Package count: 12 Markdown files — 8 standard sheets, one supplementary recipient boundary mapping, and 3 reports.
- All nine sheet files retain the original Excel appendix suffix byte-for-byte from the pre-implementation DD package.
- Every sheet remains `Draft — Needs Confirmation`; this implementation does not approve the DERIVED body/editability fallback.

## Verification results

| Check | Result | Status |
|---|---|---|
| Focused API #94 tests | 20 passed | PASS — fake DB HTTP tests |
| Linked #92–#94 regression | 66 passed | PASS — fake DB HTTP tests |
| Full Study Server suite | 1263 passed; one upstream Starlette/httpx TestClient deprecation warning | PASS — local tests |
| Ruff | `ruff check app tests` passed; scoped format check passed | PASS — static |
| OpenAPI | 55 `/api/v1` path templates / 65 operations; #94 has direct success/error set and strict DERIVED body | PASS — local source |
| Transaction branches | Locks parent then deliveries; tests verify bindings, QUEUED eligibility, preserved fields and rollback on query/mapping/commit failures | PASS — fake sessions |
| Live PostgreSQL/schema/deployment | Not run | NOT VERIFIED |
| Owner approval/fine-grained permission | Not available | OPEN |

## Preserved discrepancy and limits

- Catalog and diagram specify a path-only request while the runtime fallback requires `{title, content}`.
- Only checked-in legacy DDL columns are used; checked-in files and fake DB tests do not prove deployed schema.
- Outbox `QUEUED` is used as the local editability gate; it is not a proven Draft/Scheduled Notification state.
- Recipients, channels, schedule, read state and delivery rows are preserved. No provider/scheduler action is performed.
- Shared ADMIN role is enforced; AC-36's finer notification-management permission remains unresolved.
- The DD remains Draft and the macro-review remains `VERIFIED_WITH_OPEN_QUESTIONS`.
