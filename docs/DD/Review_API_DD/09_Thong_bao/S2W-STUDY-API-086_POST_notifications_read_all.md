# Review API DD — S2W-STUDY-API-086

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-086_POST_notifications_read_all.xlsx`
- Endpoint: `POST /api/v1/notifications/read-all`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 086-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 086-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 086-03 | P0 | `1.Request!D21`, `5.DB_Update_Main!B8:B10` | Bulk read nhận `category` tự do rồi UPDATE `category/updated_at/updated_by`, đều không tồn tại; field phải là optional `type`, còn cột cần đổi là read_status/read_at. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:51-70`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-610` | Validate type enum; bulk UPDATE rows actor-owned UNREAD, set READ/read_at, không sửa category. |
| 086-04 | P1 | `2.Response!C16:C17`, `3.Data mapping!F12` | Không quy định count chỉ gồm row vừa chuyển, hidden/đã read, hay idempotency; WHERE thiếu `read_status='UNREAD'`. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:53-60`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:603-617` | Định nghĩa affected count và repeat-call behavior; dùng predicate/index thật. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

