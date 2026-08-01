# Review API DD — S2W-STUDY-API-090

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-090_POST_admin_notifications_recipient_preview.xlsx`
- Endpoint: `POST /api/v1/admin/notifications/recipient-preview`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 090-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 090-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 090-03 | P0 | `1.Request!D21:F22`, `1.Request!I21:I22` | `audience_type` bị khai Object dù format là enum, còn `filters` là String; không biểu diễn target path/course/assignment/content có cấu trúc. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152`; `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:84-100` | Dùng target object discriminated union, IDs UUID, structured filters và permission/ownership validation. |
| 090-04 | P0 | `3.Data mapping!D14`, `5.DB_Update_Main!B8:B11` | Preview lại UPDATE `notifications` bằng audience/filter fields không tồn tại; preview phải read-only và chưa tạo notification. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152`; `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:34-37` | Query eligible learner set/count read-only; không ghi DB, không audit như send trừ access log. |
| 090-05 | P1 | `2.Response!C17:C20` | Sample recipients chưa nêu masking/PII limit; counts/exclusion reasons là aggregates chứ không phải notification columns. | `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:137-152,166-167` | Trả aggregate và mẫu tối thiểu/masked theo permission; ghi expression/source. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

