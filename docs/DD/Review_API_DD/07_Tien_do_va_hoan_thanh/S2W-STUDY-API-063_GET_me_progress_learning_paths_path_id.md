# Review API DD — S2W-STUDY-API-063

- DD nguồn: `docs/DD/Study2Work_DD_API/07_Tien_do_va_hoan_thanh/S2W-STUDY-API-063_GET_me_progress_learning_paths_path_id.xlsx`
- Endpoint: `GET /api/v1/me/progress/learning-paths/{path_id}`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 063-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 063-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 063-03 | P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | DD lọc `learning_paths.user_id`, nhưng ownership/progress nằm ở `learning_path_enrollments(user_id,learning_path_id)`. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:125-139`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-338,387-414` | Bắt đầu từ enrollment thuộc actor rồi join path/courses/completion; chống IDOR bằng safe 404. |
| 063-04 | P0 | `2.Response!C17:C20` | `required_courses_completed` và `required_courses_total` bị khai Boolean dù là số lượng; `percent/status/completed_at` cũng thuộc enrollment, không phải path master. | `docs/BD/diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md:50-78`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:387-403` | Dùng Integer counts và map `progressPercent/status/completedAt` từ enrollment; trả remaining required items. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

