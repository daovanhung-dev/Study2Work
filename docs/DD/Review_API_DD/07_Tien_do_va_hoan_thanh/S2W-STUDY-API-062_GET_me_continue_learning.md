# Review API DD — S2W-STUDY-API-062

- DD nguồn: `docs/DD/Study2Work_DD_API/07_Tien_do_va_hoan_thanh/S2W-STUDY-API-062_GET_me_continue_learning.xlsx`
- Endpoint: `GET /api/v1/me/continue-learning`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 062-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 062-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 062-03 | P0 | `2.Response!F15:G22`, `3.Data mapping!D12:F12` | Continue item được đọc từ `users.item_type/item_id/title/course_id/reason/route`; các cột này không tồn tại. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:75-84`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:387-440,539-555` | Tính từ active enrollment, last_accessed lesson, required incomplete items và curriculum order; map route ở application layer. |
| 062-04 | P0 | `3.Data mapping!C12:G13` | Không có thuật toán fallback “đang học gần nhất → required chưa hoàn thành đầu tiên → bài tập bắt buộc chưa đạt → summary khi path complete”. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:75-84`; `docs/BD/diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md:22-33` | Ghi decision table và tie-break/order cụ thể, kể cả no-active-path và completed-path case. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

