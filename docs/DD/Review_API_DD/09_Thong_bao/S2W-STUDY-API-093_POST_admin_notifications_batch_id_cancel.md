# Review API DD — S2W-STUDY-API-093

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-093_POST_admin_notifications_batch_id_cancel.xlsx`
- Endpoint: `POST /api/v1/admin/notifications/{batch_id}/cancel`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 093-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 093-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 093-03 | P0 | `3.Data mapping!F12`, `5.DB_Update_Main!A6:B11` | Cancel dùng `notifications.batch_id` và update reason/status/timestamps, nhưng SQL không có batch_id, lifecycle batch hay các cột này. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-617` | Thiết kế notification_batch/outbox job với cancellable states và migration trước khi duyệt endpoint. |
| 093-04 | P0 | `1.Request!D21:D22`, `2.Response!C16:C18` | Không định nghĩa chỉ batch SCHEDULED/QUEUED mới hủy được, race với worker, partial sends và semantics khi đã gửi một phần. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152,156-167`; `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:118-121` | Định nghĩa state machine, atomic compare-and-set cancel, audit reason, partial result và idempotent retry. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

