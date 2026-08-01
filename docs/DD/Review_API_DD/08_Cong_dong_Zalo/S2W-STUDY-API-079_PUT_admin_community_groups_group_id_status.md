# Review API DD — S2W-STUDY-API-079

- DD nguồn: `docs/DD/Study2Work_DD_API/08_Cong_dong_Zalo/S2W-STUDY-API-079_PUT_admin_community_groups_group_id_status.xlsx`
- Endpoint: `PUT /api/v1/admin/community-groups/{group_id}/status`
- Verdict: **CẦN SỬA**

## Findings

| ID | Mức độ | Sheet + cell | Phát hiện | Căn cứ BD/SQL | Cách sửa |
|---|---|---|---|---|---|
| 079-01 | P0 | `2.Response!D9:D11`, các ô ví dụ success/error | Envelope `{data, meta}` / `{error}`, snake_case `request_id` và pagination phẳng không theo canonical API contract của kiến trúc hợp nhất. | `docs/BD/base/0. Study2Work_System_Architecture.md:652-721` | Đổi sang `success/businessCode/message/data/errors/traceId`, camelCase; list mới dùng `meta.pagination`. |
| 079-02 | P1 | `Cover!G15`, `Cover!C16`, `Cover!B19`, `Overview!F5:J5`, `00.Hướng dẫn!A4:B18` | Review/Approve đều chưa chỉ định nhưng status vẫn `VERIFIED`; checklist nói không có placeholder/schema trong khi DDL hiện đã tồn tại và DD còn dùng mapping đề xuất. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Đưa về DRAFT/NEEDS_REVIEW, cập nhật nguồn 48 file, xóa placeholder và chỉ duyệt sau OpenAPI/schema/test. |
| 079-03 | P0 | `5.DB_Update_Main!B8:B11` | Chỉ `status` tồn tại; `reason/updated_at/updated_by` không có trên group. DD chưa tách state change khỏi audit metadata. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:151-158,164-172`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:623-637` | UPDATE status bằng enum, ghi reason/actor/before-after vào audit relation; optimistic check trên trạng thái hiện tại. |
| 079-04 | P0 | `2.Response!C18:C21`, `3.Data mapping!C15:G15` | `affected_learners_count/notification_created/audit_id` không có nguồn; khi PAUSED/ARCHIVED phải ẩn join action và notification chỉ enqueue sau commit. | `docs/BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md:151-158`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:192-197,623-637` | Định nghĩa impact query và outbox semantics; response chỉ nói trạng thái/job đã commit. |

## Điều kiện duyệt lại

- [ ] Hai lỗi chung về canonical envelope và trạng thái review/source đã được xử lý.
- [ ] Toàn bộ findings đặc thù endpoint ở trên có contract, mapping và test chứng minh.
- [ ] Request/response enum, kiểu dữ liệu, ownership và business state khớp BD/SEQ.
- [ ] Mọi table/column/JOIN/WHERE ghi trong DD tồn tại trong migration/schema hiện hành; không còn pseudo-column hay placeholder.
- [ ] Error catalog chỉ chứa tình huống thực của endpoint và có test negative/concurrency/idempotency phù hợp.
- [ ] Reviewer và approver được chỉ định; OpenAPI, DD và implementation test cùng một contract.

