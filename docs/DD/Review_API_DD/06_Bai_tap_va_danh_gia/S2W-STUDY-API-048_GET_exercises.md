# Review API DD — S2W-STUDY-API-048

- DD nguồn: `docs/DD/Study2Work_DD_API/06_Bai_tap_va_danh_gia/S2W-STUDY-API-048_GET_exercises.xlsx`
- Endpoint: `GET /api/v1/exercises`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 048-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 048-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 048-03 | P0 | `1.Request!D24:F24`, `3.Data mapping!F12` | `due_before` bị khai `Object` rồi dùng như cột `exercises.due_before`; `status` cũng không chỉ rõ là trạng thái publish hay trạng thái submission. Bảng `exercises` chỉ có `due_at` và `publish_status`. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:68-85`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:486-500` | Đổi thành `dueBefore` kiểu date-time map vào `due_at`; tách `publishStatus` khỏi `submissionStatus` và join latest submission theo learner. |
| 048-04 | P0 | `2.Response!C18:C22`, `2.Response!F15:G25` | `scope`, `submission_status`, `latest_result`, `allowed_actions` bị khai như cột của `exercises`, trong khi trạng thái/kết quả hiện tại thuộc attempt của learner và cần join `exercise_submissions`. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:77-84`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:508-537` | Định nghĩa query grain một dòng/exercise cho learner, join latest attempt có thứ tự ổn định và map từng field về nguồn thật. |
| 048-05 | P1 | `4.Error!E13:E14` | API chỉ đọc danh sách nhưng mang lỗi `SUBMISSION_NOT_ALLOWED` và `REVIEW_ALREADY_FINALIZED`; thiếu lỗi/filter contract thực sự. | `docs/BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md:68-85,206-217` | Bỏ lỗi của submit/review; thêm invalid filter/page và safe access/locked-content behavior. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

