# Review API DD — S2W-STUDY-API-092

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-092_GET_admin_notifications.xlsx`
- Endpoint: `GET /api/v1/admin/notifications`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 092-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 092-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 092-03 | P0 | `1.Request!D21:D24`, `3.Data mapping!F12` | Query dùng `status/category/from/to` như cột notification; SQL chỉ có type, priority, read_status, created_at và không có batch status. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-617` | Nếu list per-user notification, dùng cột thật; nếu list admin batches, tạo/query batch entity riêng với createdAt range. |
| 092-04 | P0 | `2.Response!C16:C19`, `2.Response!F16:G19` | Response `batch/recipient_count/delivery_stats/created_by` không tồn tại trên notifications; endpoint đang mô tả một entity chưa có schema. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:102-115`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-617` | Bổ sung batch/delivery model và typed metrics, hoặc bỏ endpoint khỏi contract hiện tại. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

