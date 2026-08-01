# Review API DD — S2W-STUDY-API-053

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-053_GET_exercises_assignment_id_submissions_latest.xlsx`
- Endpoint: `GET /api/v1/exercises/{assignment_id}/submissions/latest`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 053-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 053-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 053-03 | P0 | `2.Response!F15:G26`, `3.Data mapping!D12` | Latest submission lại map toàn bộ `submission_id/attempt_no/status/score/feedback` từ `exercises`, thay vì `exercise_submissions`. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:153-162`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-530` | Query latest attempt của learner theo attempt_no/submitted_at từ `exercise_submissions`; join exercise chỉ lấy metadata. |
| 053-04 | P0 | `2.Response!C22:C25` | `result`, `errors_to_fix`, `resubmit_deadline` không có schema; SQL dùng `status` làm kết quả và không lưu deadline/history reviewer. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:144-162`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:512-520` | Hoặc bổ sung review/history schema và migration, hoặc thu hẹp response về field đang lưu; không khai pseudo-column là nguồn vật lý. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

