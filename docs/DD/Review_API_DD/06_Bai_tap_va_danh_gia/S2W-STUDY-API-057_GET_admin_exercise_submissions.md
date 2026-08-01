# Review API DD — S2W-STUDY-API-057

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-057_GET_admin_exercise_submissions.xlsx`
- Endpoint: `GET /api/v1/admin/exercise-submissions`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 057-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 057-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 057-03 | P0 | `1.Request!D22:D25`, `3.Data mapping!F12` | Queue filter dùng `course_id` và `due_before` như cột của `exercise_submissions`; hai cột không tồn tại, deadline nằm trên `exercises.due_at`. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:134-150`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:486-506,508-537` | Join submissions→exercises→course; filter status `UNDER_REVIEW`, due_at và reviewer scope bằng cột thật. |
| 057-04 | P1 | `2.Response!C16:C19`, `2.Response!F16:G19` | `waiting_time`, `rubric`, `learner_summary` bị khai là cột submission; đây là calculated/join fields và cần định nghĩa tránh lộ PII. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:28-30,136-150`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:496-498,508-520` | Ghi rõ expression/join, kiểu duration, projection learner tối thiểu và sort SLA ổn định. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

