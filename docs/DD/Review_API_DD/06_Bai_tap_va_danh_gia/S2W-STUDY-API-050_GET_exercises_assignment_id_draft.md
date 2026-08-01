# Review API DD — S2W-STUDY-API-050

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-050_GET_exercises_assignment_id_draft.xlsx`
- Endpoint: `GET /api/v1/exercises/{assignment_id}/draft`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 050-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 050-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 050-03 | P0 | `2.Response!F15:G23`, `3.Data mapping!D12` | Draft được lấy từ `study.exercises` với các cột `draft_id/answer_payload/attachments/...` không tồn tại; draft là trạng thái/attempt của `exercise_submissions`. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:101-114`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-530` | Query submission `status=DRAFT` theo `(exercise_id,user_id)` và định nghĩa payload storage/version rõ ràng. |
| 050-04 | P0 | `3.Data mapping!F12`, `3.Data mapping!A20` | Truy vấn chỉ ràng buộc exercise, không có `user_id`; endpoint `me` có nguy cơ trả draft của learner khác. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:28,101-114`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:510-512,529` | Bắt buộc ownership `exercise_submissions.user_id=:auth_user_id`, chọn attempt hiện hành deterministically và safe 404 nếu ngoài phạm vi. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

