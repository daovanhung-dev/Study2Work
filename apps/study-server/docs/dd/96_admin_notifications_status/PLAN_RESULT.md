# PLAN_RESULT — Study API #96

## Kết quả plan trước authoring

- Task `docs`, scope `server-study`; selector trả và đã đọc ba worklog `docs` #48–#50.
- Trước khi tạo DD #96: 95 DD folders #01–#95; 8 thiếu #96–#103. 83 folders có đủ 8 sheet + 3 report; 12 folder đời đầu có 8 sheet, chưa có 3 reports.
- Catalog có 103 method/path duy nhất; router hiện khớp 12 route catalog, 91 chưa có source implementation.
- Contract giữ `GET /api/v1/admin/notifications/{notification_id}/status`, Admin Bearer, `notification_id:int64!`, no body/query, `ApiEnvelope<Notification>`, HTTP 200 và exact errors 401/403/404/500.
- AC-36 node STATUS nối API #96 → “Đọc delivery aggregate” → “Reload notification management”. Giữ aggregate intent riêng với response contract; không thêm counts hoặc đổi response type.
- Legacy BIGINT `notifications` chỉ là candidate partial. V1-PILOT UUID delivery schema khác ID/grain; không coi là Admin target.

## Ma trận requirement

| Item | DIRECT/DERIVED/SOURCE_REQUIRED | Nội dung |
|---|---|---|
| Method/path/actor | DIRECT | GET status; Admin Bearer JWT. |
| Input | DIRECT | `notification_id:int64!`; không body/query. |
| Success | DIRECT | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Notification>`. |
| Errors | DIRECT | 401, 403, 404, 500 với đúng codes catalog. |
| Delivery aggregate step | DIRECT from AC-36 | Đọc aggregate rồi reload management. |
| Delivery-to-Notification projection | DERIVED proposal only | Có thể dùng field `Notification.status` hiện hữu nếu owner duyệt; không đổi schema. |
| Aggregate query/grain/rules | SOURCE_REQUIRED | Không có Admin relation, enum/rule hoặc phép tổng hợp được duyệt. |
| Mutation | N/A | GET read-only; không gọi delivery provider. |

## Sources đã đối chiếu

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) #96 và reusable `Notification`, `NotificationDelivery`, `OperationStatus`.
- [AC/API index AC-36](../../diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-36 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio).
- DD #92–#95 overview/request/response/mapping/open questions và reports; DD #64 làm precedent về delivery status mismatch.
- Legacy `DB.sql`, V1-PILOT `02_study_db.sql`, current Study router/middleware, API Guidelines.
- Registry-wired `createDD-markdown`, canonical 8 Markdown templates, Study Markdown-only workflow.

## Authoring boundary

Tạo tám sheet role và ba reports. `07_table.md` dùng `N/A — READ-ONLY API`; không tạo ZIP, runtime/schema/catalog/diagram changes. Sau static validation, macro-review #92–#96 ở mức tài liệu và giữ open questions chưa được nguồn giải đáp.
