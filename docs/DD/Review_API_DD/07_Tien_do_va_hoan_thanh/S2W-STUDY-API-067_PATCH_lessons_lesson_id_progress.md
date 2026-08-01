# Review API DD — S2W-STUDY-API-067

- DD nguồn: `docs/DD/Study2Work_DD_API/07_Tien_do_va_hoan_thanh/S2W-STUDY-API-067_PATCH_lessons_lesson_id_progress.xlsx`
- Endpoint: `PATCH /api/v1/lessons/{lesson_id}/progress`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 067-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 067-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 067-03 | P0 | `3.Data mapping!D14`, `5.DB_Update_Main!A6:B16` | Endpoint evidence progress lại UPDATE `lessons` bằng event payload; các cột không tồn tại và vi phạm nguyên tắc learner không sửa trực tiếp progress/master content. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:157-167,183-190`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:458-469,539-555` | Validate evidence rồi UPSERT `lesson_progress`; server tính status/percent, không tin client gửi completion. |
| 067-04 | P0 | `1.Request!D22:D28`, `3.Data mapping!C12:G15` | `occurred_at` do client gửi nhưng không có idempotency/event id, clock bound hay xử lý out-of-order; video percent cũng chưa tính/bound 0..100. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:86-96,157-167`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:544-555` | Thêm event/dedup key, validate timestamp/resource ownership/duration và monotonic progress; transaction/reconciliation cho cascade. |
| 067-05 | P0 | `2.Response!C19:C23` | DD hứa chapter/course/path update trong response nhưng không chứng minh cascade đã durable; PRG-05 yêu cầu cập nhật các cấp liên quan. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:105-139,185-190`; `docs/BD/diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md:14-33` | Chọn transaction hoặc eventual consistency có job/outbox/status; chỉ trả trạng thái đã commit. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

