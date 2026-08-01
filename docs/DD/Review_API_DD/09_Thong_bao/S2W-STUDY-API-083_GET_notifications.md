# Review API DD — S2W-STUDY-API-083

- DD nguồn: `docs/DD/Study2Work_DD_API/09_Thong_bao/S2W-STUDY-API-083_GET_notifications.xlsx`
- Endpoint: `GET /api/v1/notifications`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 083-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 083-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 083-03 | P0 | `1.Request!D21:D23`, `3.Data mapping!F12` | SEQ/SQL dùng `type` và `readStatus`; DD dùng `category` và `is_read`, rồi query các cột không tồn tại. Naming/semantics contract không khớp. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:41-53`; `docs/BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md:51-70`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-617` | Dùng camelCase `type/readStatus/priority/page/pageSize`, map `notifications.type/read_status/priority`. |
| 083-04 | P0 | `2.Response!C18:C22`, `2.Response!F18:G22` | Response `category/is_read/action` không map SQL `type/read_status/action_url`; read state không nên suy thành Boolean nếu enum còn HIDDEN. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:56-81`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:596-610` | Trả `type`, `readStatus`, `actionUrl`, `readAt`; map từng field thật và allowlist action route. |
| 083-05 | P0 | `1.Request!I21`, `2.Response!H18` | Ví dụ SEQ dùng type `EXERCISE` nhưng enum SQL không có; SQL dùng `ASSIGNMENT/REVIEW_RESULT`. DD lại bỏ hẳn accepted enum. | `docs/BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md:47-70`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:160-170` | Chốt một notification type taxonomy, migrate enum nếu cần và đồng bộ OpenAPI/filter/event producers. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

