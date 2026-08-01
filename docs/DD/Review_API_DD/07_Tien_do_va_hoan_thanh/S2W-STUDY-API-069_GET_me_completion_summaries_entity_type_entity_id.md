# Review API DD — S2W-STUDY-API-069

- DD nguồn: `docs/DD/Study2Work_DD_API/07_Tien_do_va_hoan_thanh/S2W-STUDY-API-069_GET_me_completion_summaries_entity_type_entity_id.xlsx`
- Endpoint: `GET /api/v1/me/completion-summaries/{entity_type}/{entity_id}`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 069-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 069-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 069-03 | P0 | `2.Response!F15:G22`, `3.Data mapping!D12:F12` | Completion summary được đọc từ `users.entity_type/entity_id/completion_time/...`; toàn bộ các cột này không tồn tại và sai entity owner. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:111-139`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:239-256,387-440` | Route theo entity type sang actor-owned course/path enrollment và aggregate submissions/completions. |
| 069-04 | P0 | `1.Request!D21:I22`, `3.Data mapping!F12` | `entity_type` không có enum/allowed values, còn ownership chỉ là pseudo-condition trên users; dễ IDOR hoặc nhận entity không hỗ trợ. | `docs/BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md:34-46,141-151` | Giới hạn `COURSE` hoặc `LEARNING_PATH` (hoặc contract rõ), validate UUID + actor ownership và safe 404. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.
