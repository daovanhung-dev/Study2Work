# Review API DD — S2W-STUDY-API-072

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-072_POST_community_groups_group_id_open_link.xlsx`
- Endpoint: `POST /api/v1/community-groups/{group_id}/open-link`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 072-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 072-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 072-03 | P0 | `1.Request!D22:D23`, `1.Request!A25` | Contract trực tiếp lệch SEQ-09: DD dùng `accepted_rules/rules_version`, bỏ `sourceScreen`; SEQ dùng `confirmedRules/sourceScreen`. Version có ích nhưng phải được chốt, không thể tự thay contract. | `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:41-55`; `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:87-98` | Chốt canonical camelCase gồm confirmation gắn current rules version/hash và sourceScreen. |
| 072-04 | P0 | `3.Data mapping!D14`, `5.DB_Update_Main!A6:B11`, `7.DB_Insert_Main!B8` | Open-link UPDATE `community_groups` bằng accepted_rules/rules_version; SQL yêu cầu INSERT `community_join_events(user_id,community_group_id,confirmed_rules,source_screen,opened_at)`. | `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:21-25`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:642-650` | INSERT join/open-intent event sau access/rule validation; không sửa group master. |
| 072-05 | P0 | `2.Response!C16:C19` | Response dùng `join_url` trong khi schema là `join_link`, và không giữ semantics `LINK_OPENED_ONLY`; server chỉ biết đã cấp/mở intent, không biết learner đã join. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:98,164-170`; `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:57-72` | Dùng controlled redirect/short-lived link, event id và meaning `LINK_ISSUED/OPEN_INTENT`; không tuyên bố membership. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

