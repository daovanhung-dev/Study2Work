# VERIFICATION_REPORT — Study API #64

## Kết quả

- DD status: `Draft — Needs Confirmation`. Catalog contract được giữ nguyên;
  ownership, Operation projection và channel aggregation vẫn là lựa chọn local
  `DERIVED`, chưa phải business policy được duyệt.
- Runtime: route, middleware path, module, SQL projection và TestClient tests đã
  được wired trong source local.
- Runtime boundary: tests dùng fake DB session. Migration 009 chưa được áp dụng
  hoặc live-verified; không có worker/provider Push/Email được xác minh.
- API #18 vẫn là contract generic riêng, chưa được nối với flow AC-25.

## Verification

| Check | Kết quả | Trạng thái |
|---|---|---|
| API #64 focused tests | `22 passed`; queued/sent/failed precedence, Operation mapping, auth/role/owner, malformed and missing IDs, legacy rows, invalid projections, safe query error, trace, no commit, OpenAPI. | PASS |
| Full Study suite | `660 passed`, one upstream Starlette/httpx deprecation warning. | PASS |
| Ruff | `uv run ruff check app tests` — all checks passed. | PASS |
| OpenAPI | GET path; optional Authorization header; `notification_id` integer/int64; responses exactly 200/401/403/404/500; no request body. | PASS |
| Route/middleware | Parameterized path is in `DESIGN_CONTRACT_PATHS`; raw path/header are read from Request so malformed path maps through catalog 404 and OpenAPI has no synthetic 422. | PASS |
| DD contract | 8 sheet statuses remain Draft; direct catalog response/error contract retained; local assumptions and open policy questions are labeled. | VERIFIED_STATIC |
| Live database/provider | No live DB, migration apply, worker or provider verification performed. | NOT_VERIFIED_HERE |

## Local implementation mapping

- One notification row is read with aggregate counts and maximum delivery
  `updated_at` from its channel outbox rows.
- Mentor ownership compares local `notifications.sender_id` with numeric JWT
  `sub`; a different sender returns 403. Missing notification or absent local
  dispatch state returns 404.
- Operation `id`, `kind`, `owner_id`, `submitted_at`, `updated_at` map from the
  local API #63 notification/outbox source. `status` is `QUEUED` when any
  channel remains queued, otherwise `FAILED` when any failed, otherwise `SENT`
  when all rows are sent. Partial success is summarized as `FAILED`.
- Optional `completed_at` and Payment-shaped `result` are omitted because no
  source semantics or persistence supports them. GET does not commit or call a
  delivery provider.

These mapping and authorization choices are DERIVED fallbacks documented in
the DD. They do not resolve the catalog's Operation-versus-delivery-summary
discrepancy.

## Remaining questions

- Confirm Operation response versus channel-level delivery summary and whether
  partial success needs an explicit state or counts.
- Confirm global Mentor authorization semantics and approval of the local
  `sender_id` relation.
- Confirm deployment of migration 009 and the worker/provider lifecycle that
  updates outbox state.
- Keep API #18's identity/lifecycle decisions separate until its diagram and
  persistence contract are reconciled.

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md),
[API #63 report](../63_mentor_notifications_create/VERIFICATION_REPORT.md) and
[API #62 report](../62_mentor_course_students/VERIFICATION_REPORT.md).
