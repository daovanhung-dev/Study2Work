# Review API DD — S2W-STUDY-API-051

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-051_PUT_exercises_assignment_id_draft.xlsx`
- Endpoint: `PUT /api/v1/exercises/{assignment_id}/draft`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 051-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 051-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 051-03 | P0 | `3.Data mapping!D14`, `5.DB_Update_Main!A6:B14` | Lưu draft đang UPDATE `study.exercises` bằng `answers/text/links/file_ids/progress_notes`; đây là dữ liệu bài làm của learner, không phải định nghĩa exercise, và các cột đều không tồn tại. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:101-114`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:486-530` | UPSERT một `exercise_submissions` trạng thái `DRAFT` theo learner/exercise/attempt; không sửa master exercise. |
| 051-04 | P0 | `1.Request!D22:D26`, `5.DB_Update_Main!B8:B14` | Payload hỗ trợ quiz/file/link nhưng SQL chỉ có `text_answer/file_url/link_url`; chưa có question-answer schema hoặc controlled file asset, trong khi file chỉ được hỗ trợ khi storage sẵn sàng. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:34-43,103-108,118-124`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-519` | Khóa payload theo exercise type; bổ sung quiz/file asset schema hoặc giới hạn V1 vào các field thực có, kèm ownership/scan validation. |
| 051-05 | P1 | `1.Request!B11`, `3.Data mapping!F12:G15` | PUT draft không định nghĩa draft version/ETag hay quy tắc hai thiết bị ghi đồng thời; generic `status/version` không trỏ cột thật. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:110-114`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:529` | Định nghĩa idempotent upsert, optimistic version/updatedAt thực và test concurrent save. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

