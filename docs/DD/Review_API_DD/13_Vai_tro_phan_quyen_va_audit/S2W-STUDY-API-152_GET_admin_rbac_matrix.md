# Review S2W-STUDY-API-152 — GET RBAC matrix

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-152_GET_admin_rbac_matrix.xlsx`
- Endpoint: `GET /api/v1/admin/rbac/matrix`
- Kết luận: **CẦN SỬA — không thể dựng matrix từ schema hiện tại**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 152-01 | P0 | `2.Response!A16:H18`, `3.Data mapping!A12:H20` | Matrix phụ thuộc `permissions/role_permissions`, nhưng hai relation không tồn tại. SQL `SELECT roles, permissions, grants FROM roles` không hợp lệ. | Chốt permission model/owner, viết JOIN thật và version của matrix. |
| 152-02 | P1 | `2.Response!A16:H18` | `roles[]`, `permissions[]` không có item schema; `grants[{role_code, permission_code}]` không biểu đạt scope, effect allow/deny, inherited/default hay role inactive. | Định nghĩa item và semantics rõ; nếu V1 chỉ allow-list thì ghi invariant, không ngụ ý deny/inheritance. |
| 152-03 | P0 | `Overview!A19:B20` | Role catalog trong BD và seed đang khác nhau (`BD-13:23-33`; `schema_seed.sql:857-873`), nên matrix có thể gán quyền cho code không tồn tại hoặc sai ý nghĩa. | Phê duyệt role-code mapping trước, rồi tạo migration/seed nhất quán. |
| 152-04 | P1 | `3.Data mapping!A13:H17` | Rule one-ACTIVE/PUBLISHED/ownership và idempotency side effect là template không liên quan endpoint read. | Thay bằng least privilege, active-role filtering, deterministic ordering và cache/version/ETag nếu cần. |
| 152-05 | P0 | `2.Response!A9:E11` | Envelope cũ và pagination giả trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn; matrix singleton không có pagination. |

## Điều kiện duyệt lại

- Role/permission/grant model và owner được chốt.
- Matrix có schema item, query thực thi và tests cho inactive/missing grant.
