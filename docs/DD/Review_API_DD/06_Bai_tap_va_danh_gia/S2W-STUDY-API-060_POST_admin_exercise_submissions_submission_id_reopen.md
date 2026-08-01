# Review API DD — S2W-STUDY-API-060

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-060_POST_admin_exercise_submissions_submission_id_reopen.xlsx`
- Endpoint: `POST /api/v1/admin/exercise-submissions/{submission_id}/reopen`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 060-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 060-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 060-03 | P0 | `5.DB_Update_Main!B8:B11`, `3.Data mapping!D14` | Reopen ghi `reason/allowed_until/updated_at/updated_by` vào `exercise_submissions`, nhưng schema không có các cột này và không có review/reopen history. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:153-162,216-217`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-530` | Bổ sung reopen/review history + allowed-resubmit-until bằng migration, hoặc lưu reason/before-after ở audit và update field thật. |
| 060-04 | P0 | `1.Request!D22:D23`, `4.Error!E14:E17` | Chưa khóa trạng thái nào được reopen, ai có scope, max attempts/deadline precedence và tính idempotent khi đã reopen. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:153-162`; `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:126-130` | Định nghĩa transition từ final status, reviewer/admin scope, attempt policy, conflict/idempotency và audit bắt buộc. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

