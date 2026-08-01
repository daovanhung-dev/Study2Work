# Review API DD — S2W-STUDY-API-073

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-073_POST_community_groups_group_id_reports.xlsx`
- Endpoint: `POST /api/v1/community-groups/{group_id}/reports`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 073-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 073-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 073-03 | P0 | `2.Response!F15:G18`, `3.Data mapping!D12:D14`, `5.DB_Update_Main!A6` | Báo cáo lại target một view `study.vw_report_community` và UPDATE nó; DDL không có view hay bảng community report. Nghiệp vụ/SEQ yêu cầu tạo report. | `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:28-36,75-99`; `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:111-121`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:619-657` | Bổ sung `community_reports` table/status/audit bằng migration và INSERT report, hoặc chưa phát hành endpoint. |
| 073-04 | P0 | `1.Request!D22:I24` | `issue_type` là String tự do, không khóa các reason nghiệp vụ (broken link, wrong group, spam/scam, moderator, unclear rules); `evidence_url` chưa có safety policy. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:111-121`; `docs/BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md:75-84` | Dùng enum reason canonical, bounds/HTML sanitization, URL allowlist và rate-limit duplicate abuse. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

