# Review API DD — S2W-STUDY-API-071

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-071_GET_community_groups_group_id.xlsx`
- Endpoint: `GET /api/v1/community-groups/{group_id}`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 071-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 071-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 071-03 | P0 | `Overview!D5`, `2.Response!C20`, `2.Response!A24` | Endpoint N/A auth trả `data.join_link` trực tiếp; guest không được xem private link và SEQ chỉ trả link qua open-link sau khi xác nhận rules. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:78-98`; `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:21-26,102-105` | Loại join link khỏi detail; trả access state + open-link action, projection theo optional learner auth. |
| 071-04 | P0 | `3.Data mapping!F12`, `2.Response!C17:C20` | WHERE dùng `community_group_id` thay vì SQL `id`; `rules` bị khai Array trong khi schema là TEXT, access_state là derived field chưa có rule. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:44-53,69-85`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:623-637` | Dùng cột thật, khóa representation/version của rules và tính access từ scope/status/enrollment. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

