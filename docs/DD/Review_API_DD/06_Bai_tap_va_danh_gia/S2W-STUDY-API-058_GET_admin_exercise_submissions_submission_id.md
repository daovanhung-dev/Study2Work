# Review API DD — S2W-STUDY-API-058

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-058_GET_admin_exercise_submissions_submission_id.xlsx`
- Endpoint: `GET /api/v1/admin/exercise-submissions/{submission_id}`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 058-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 058-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 058-03 | P0 | `2.Response!C16:C22`, `2.Response!F16:G22` | `assignment/learner/submission_payload/attachments/rubric/previous_attempts/prior_reviews` đều là pseudo-column; SQL chưa có review-history/attachment relation. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:134-162`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:486-530` | Thiết kế aggregate DTO với nguồn từng field; bổ sung schema review/asset/history hoặc loại field chưa triển khai. |
| 058-04 | P0 | `3.Data mapping!F12`, `Overview!D5` | Chỉ lọc submission id, chưa kiểm reviewer permission/scope và không mô tả trường nào mentor được xem. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:24-30,134-150`; `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:36-42` | Thêm scoped reviewer authorization, safe 404, field-level PII rule và audit access nếu cần. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

