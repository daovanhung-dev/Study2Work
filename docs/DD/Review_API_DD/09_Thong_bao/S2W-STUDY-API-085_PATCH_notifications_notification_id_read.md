# Review API DD — S2W-STUDY-API-085

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-085_PATCH_notifications_notification_id_read.xlsx`
- Endpoint: `PATCH /api/v1/notifications/{notification_id}/read`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 085-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 085-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 085-03 | P0 | `5.DB_Update_Main!B8`, `3.Data mapping!F12` | API direct từ SEQ nhưng DB Update ghi N/A; WHERE dùng `notification_id` thay vì SQL `id`. Không có mapping `read_status='READ', read_at=NOW()`. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:25-32`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-610` | Thêm UPDATE thật theo `(id,user_id)`, set read_status/read_at; affected row + safe 404. |
| 085-04 | P0 | `2.Response!C16:C17`, `2.Response!F16:G17` | Response dùng `is_read` Boolean trong khi schema là enum `read_status`; contract không xử lý HIDDEN/already READ. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:51-70`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:179-183,603-609` | Trả `readStatus/readAt`; đã READ phải idempotent và không đổi readAt nếu policy không yêu cầu. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

