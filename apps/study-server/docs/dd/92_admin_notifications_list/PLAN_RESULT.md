# Plan and Result — API #92 Lấy notification list

## Kế hoạch trước khi code

1. Giữ method/path/auth/query/success/error literals trực tiếp của catalog #92 và AC-36 flow.
2. Đọc diagram, legacy/V1-PILOT schemas, catalog/reusable Notification, API #43/#63/#64 và macro-review #92–#96; tách expected contract khỏi current source.
3. Chọn rõ fallback trong worklog trước code: Page<Notification>, legacy notification/outbox candidates, fixed 20-row page, local status aggregate và shared ADMIN guard; không thêm schema.
4. Implement module layers theo Study convention: models, API-specific validation, SQL constants và view orchestration; wire route/middleware; thêm HTTP tests.
5. Cập nhật DD/runtime/context sau khi kiểm tra implementation; giữ package Markdown, template appendices và `Draft — Needs Confirmation`.

## Kết quả

- Đã wire `GET /api/v1/admin/notifications` cùng module/read-only query, raw-query auth ordering và middleware contract path.
- Runtime trả `Page<Notification>` theo fallback DERIVED, lấy channel/status từ legacy delivery outbox; không trả recipient/sender/operation IDs.
- Direct catalog singleton response, Admin permission, Notification grain/enums, read/scheduled fields, 422/503 trigger và #93 Operation bridge vẫn là open questions.
- Focused HTTP suite, linked/full Study tests, Ruff, OpenAPI, DD package và context validator được ghi trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md) sau verification cuối.
