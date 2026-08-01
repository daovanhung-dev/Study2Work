# Review API DD — S2W-STUDY-API-078

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-078_PATCH_admin_community_groups_group_id.xlsx`
- Endpoint: `PATCH /api/v1/admin/community-groups/{group_id}`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 078-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 078-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 078-03 | P0 | `1.Request!D22`, `1.Request!A24` | PATCH group chỉ nhận `reason`, không có bất kỳ field cập nhật nào; không thể thực hiện update link/description/rules mà BD cho phép. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:123-133`; `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:33-35` | Khai partial fields được sửa cùng validation; reason là audit metadata, không phải payload duy nhất. |
| 078-04 | P0 | `5.DB_Update_Main!B8:B10`, `3.Data mapping!D14` | DB sheet chỉ ghi `reason/updated_at/updated_by`, đều không tồn tại trên `community_groups`, và không update field nghiệp vụ. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:123-133`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:623-637` | UPDATE cột group thật; lưu reason/before-after vào audit log trong cùng transaction. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

