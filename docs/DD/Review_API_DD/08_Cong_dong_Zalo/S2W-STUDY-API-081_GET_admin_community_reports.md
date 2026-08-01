# Review API DD — S2W-STUDY-API-081

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-081_GET_admin_community_reports.xlsx`
- Endpoint: `GET /api/v1/admin/community-reports`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 081-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 081-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 081-03 | P0 | `2.Response!F15:G20`, `3.Data mapping!D12:F12` | Admin queue phụ thuộc `study.community_reports`, bảng không tồn tại; filter status/issue_type/group_id không có schema hay index. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:111-133`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:619-657` | Bổ sung report entity, enums, reporter/group FK, timestamps, indexes và ownership/moderator scope. |
| 081-04 | P1 | `2.Response!C16` | Mỗi row chỉ là `report` String, thiếu issue reason/description/group/reporter/time/status cần để xử lý. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:111-121` | Định nghĩa typed queue DTO, minimal reporter data, safe text và pagination/sort SLA. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

