# Review API DD — S2W-STUDY-API-059

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-059_PATCH_admin_exercise_submissions_submission_id_review.xlsx`
- Endpoint: `PATCH /api/v1/admin/exercise-submissions/{submission_id}/review`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 059-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 059-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 059-03 | P0 | `5.DB_Update_Main!B8:B15` | DD update `result/rubric_scores/errors_to_fix/resubmit_deadline/updated_at/updated_by`, nhưng schema chỉ có `status/score/feedback/reviewed_at`; mapping không chạy được. | `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:90-123`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-528` | Map `result→status`, `allowResubmitUntil→` schema đã migration, set reviewed_at; bổ sung reviewer/history fields hoặc audit table. |
| 059-04 | P0 | `1.Request!D22:I27`, `3.Data mapping!C13:G15` | Không có validation score ≤ `exercises.max_score`, transition chỉ từ `UNDER_REVIEW`, reviewer scope, và progress chỉ đổi khi `PASSED`. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:136-150,210-217`; `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:36-42`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:496,512-528` | Định nghĩa state machine + score bounds + authorization; transaction update review/progress và outbox notification. |
| 059-05 | P1 | `2.Response!C16:C22` | Response `review_id/reviewed_by/progress_effect/notification_created` không có nguồn vật lý; dễ tuyên bố side effect đã hoàn tất dù chỉ mới enqueue. | `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:108-123`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-528` | Trả submission state bền vững; nếu có outbox chỉ trả accepted/event id, không Boolean giao thành công. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

