# Review API DD — S2W-STUDY-API-074

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-074_GET_me_community_reports.xlsx`
- Endpoint: `GET /api/v1/me/community-reports`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 074-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 074-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 074-03 | P0 | `2.Response!F15:G25`, `3.Data mapping!D12:F12` | Toàn API dựa vào `study.community_reports`, relation không tồn tại trong DDL; status/response/resolved_at cũng chưa có lifecycle. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:111-121`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:619-657` | Thiết kế/migrate report entity và state machine trước; query bắt buộc theo reporter `user_id`. |
| 074-04 | P1 | `2.Response!C17:C22` | `group_summary` và `response` là String mơ hồ, không định nghĩa field nào của moderator được hiển thị cho learner hay safe resolution text. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:111-121`; `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:86-99` | Định nghĩa typed summary, status enum, timestamps và public-safe resolution; không lộ nội bộ/audit. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

