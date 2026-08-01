# Review API DD — S2W-STUDY-API-052

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-052_POST_exercises_assignment_id_submissions.xlsx`
- Endpoint: `POST /api/v1/exercises/{assignment_id}/submissions`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 052-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 052-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 052-03 | P0 | `1.Request!D22:I23`, `1.Request!A26` | Contract ghi `draft_id` là Array và `confirm_submit` là String, lệch trực tiếp SEQ-07 vốn yêu cầu `mode=SUBMIT`, structured answers, text/file/link payload. Đây không phải sai khác naming đơn thuần mà làm mất nội dung bài nộp. | `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:47-69`; `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:116-132` | Chốt một contract canonical với SEQ/OpenAPI; dùng đúng kiểu (`draftId` UUID nếu submit draft, boolean/mode đúng enum) và payload theo loại exercise. |
| 052-04 | P0 | `3.Data mapping!D14`, `5.DB_Update_Main!A6:B11`, `7.DB_Insert_Main!B8` | Nộp bài lại UPDATE `study.exercises` và không INSERT gì; SEQ yêu cầu tạo submission/attempt, SQL có bảng `exercise_submissions` riêng. | `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:23-34`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-530` | INSERT `exercise_submissions(exercise_id,user_id,status,attempt_no,...,submitted_at)` trong transaction; server sinh attempt/status/timestamp. |
| 052-05 | P0 | `2.Response!C16:G21`, `2.Response!A25` | Response lấy submission fields từ `study.exercises`; ví dụ trả status `ACTIVE`, không thuộc enum submission. SEQ trả `submissionId/exerciseId/status/attemptNo/submittedAt`. | `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:71-87`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:143-151,508-530` | Map từ row submission vừa tạo, trả status hợp lệ `SUBMITTED/UNDER_REVIEW/PASSED/FAILED`, bỏ `ACTIVE` và field không có nguồn. |
| 052-06 | P0 | `3.Data mapping!C15:G15` | Auto-grade/progress/reviewer notification chỉ được ghi bằng câu template; chưa đảm bảo attempt + grade + required-progress condition + outbox nhất quán. | `docs/BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md:27-42`; `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:126-150,210-217` | Mô tả transaction/outbox cụ thể, duplicate-submit key, rollback và progress chỉ cập nhật khi `PASSED`. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

