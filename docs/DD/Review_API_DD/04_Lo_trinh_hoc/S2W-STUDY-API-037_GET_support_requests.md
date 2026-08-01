# Review API DD — S2W-STUDY-API-037

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-037_GET_support_requests.xlsx`
- Endpoint: `GET /api/v1/support-requests`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | WHERE chỉ lọc status, không có `support_requests.user_id=:auth_user_id`; có thể trả yêu cầu của learner khác. | `docs/BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md:57-76`; SQL `:662-689` | Bắt buộc owner predicate trước mọi filter/paging. |
| P0 | `2.Response!A16:H22` | `request_id,current_path,target_path,submitted_at,decision_summary` bị coi là cột; schema dùng `id`, path IDs, `admin_decision`, `resolved_at` và không có submitted time. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:662-682` | Trả fields/cột thật, JOIN titles nếu cần; thêm migration timestamp nếu business cần. |
| P1 | `1.Request!A21:J23` | Status free text, page min mâu thuẫn (0 và ≥1), không liệt kê enum `OPEN/IN_REVIEW/...`. | SQL `:207-214`; `docs/BD/base/0. Study2Work_System_Architecture.md:702-721` | Enum canonical, page min 1/cap, stable sort/tie-breaker. |
| P1 | `4.Error!A9:H12` | Không có ownership/privacy negative case; generic validation không đủ cho danh sách cá nhân. | `docs/BD/11. Study2Work_Study_BasicDesign_Admin_Quan_Ly_Hoc_Vien_Ho_Tro_Ngoai_Le.md:58-72` | Test actor A không bao giờ xem request actor B; safe errors. |
| P0 | `2.Response!A9:E11`, `A23:H26` | Envelope/pagination snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-721` | `meta.pagination`, camelCase và `traceId`. |

## Điều kiện duyệt lại

- [ ] Owner filter bắt buộc và có negative test.
- [ ] Response/status/timestamps dùng schema thật.
- [ ] Pagination/envelope canonical.
- [ ] Endpoint suy dẫn được phê duyệt.
