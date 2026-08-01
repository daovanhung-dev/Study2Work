# Review API DD — S2W-STUDY-API-091

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-091_POST_admin_notifications.xlsx`
- Endpoint: `POST /api/v1/admin/notifications`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 091-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 091-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 091-03 | P0 | `1.Request!D23:D29`, `7.DB_Insert_Main!B8:B17` | Request/insert dùng `category`, `audience`, `channels`, `action`, `scheduled_at`, batch metadata; bảng notifications chỉ có per-user `type/action_url` và không có audience/channel/schedule/batch. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:84-115`; `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-610` | Thiết kế notification batch/recipient/delivery/outbox schema hoặc giới hạn endpoint; map type/actionUrl canonical. |
| 091-04 | P0 | `7.DB_Insert_Main!A6:B17`, `3.Data mapping!C15:G15` | INSERT `notifications` không cung cấp bắt buộc `user_id` và không thể fanout audience; synchronous generic side effect không đáp ứng dedup/retry. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:15-37`; `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:156-167`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-617` | Snapshot eligible recipients, persist batch/outbox, worker fanout per user với dedup key và retry sau commit. |
| 091-05 | P0 | `1.Request!I23:I24`, `2.Response!C17:C21` | Không khóa notification type/channel enum; response batch/status/delivery timestamps không có source. Taxonomy DD `category` cũng lệch SQL enum. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:24-30,34-46`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:160-177` | Chốt enums/OpenAPI + migration; response chỉ trả accepted batch/job state có persistence thật. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

