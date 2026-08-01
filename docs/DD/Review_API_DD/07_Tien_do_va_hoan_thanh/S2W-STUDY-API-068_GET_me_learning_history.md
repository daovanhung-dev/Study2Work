# Review API DD — S2W-STUDY-API-068

- DD nguồn: `docs/DD/Study2Work_DD_API/07_Tien_do_va_hoan_thanh/S2W-STUDY-API-068_GET_me_learning_history.xlsx`
- Endpoint: `GET /api/v1/me/learning-history`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 068-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 068-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 068-03 | P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | History filter dùng `lesson_progress.type/from/to`; các cột không tồn tại và lesson_progress chỉ lưu snapshot, không phải event history. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:141-151`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:539-555` | Thiết kế history source/UNION từ enrollments, submissions và activity/audit table; filter timestamp thật. |
| 068-04 | P0 | `2.Response!C16:C20`, `2.Response!F16:G20` | `event_type/entity/occurred_at/metadata` bị khai là cột lesson_progress dù schema không có; lịch sử BD còn yêu cầu path/course/submission/review. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:141-151`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:387-440,508-555` | Định nghĩa event DTO và persistence/grain; giữ endpoint read-only, không suy diễn event từ snapshot thiếu timestamp. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

