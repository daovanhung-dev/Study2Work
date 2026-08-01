# Review S2W-STUDY-API-153 — GET user roles

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-153_GET_admin_users_user_id_roles.xlsx`
- Endpoint: `GET /api/v1/admin/users/{user_id}/roles`
- Kết luận: **CẦN SỬA — effective permissions chưa có nguồn**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 153-01 | P0 | `3.Data mapping!A12:H20` | DD JOIN `permissions` nhưng schema không có permission/role_permission; `SELECT user_summary, roles, effective_permissions FROM user_roles` không hợp lệ. | JOIN `users → user_roles → roles` cho role; chỉ trả effective permissions sau khi có catalog/authorization owner và thuật toán rõ. |
| 153-02 | P1 | `2.Response!A16:H18` | `user_summary` bị khai báo String và gán nguồn user_roles; arrays không có item/active/scope/assignedAt. | Định nghĩa object tối thiểu, tránh PII thừa; map code/name/scope/active/assignedAt đúng bảng. |
| 153-03 | P0 | `Overview!A19:B20` | Role codes BD và seed không khớp (`BD-13:23-33`; `schema_seed.sql:857-873`), nên effective role có thể sai semantic. | Chốt role mapping/migration trước khi API được VERIFIED. |
| 153-04 | P1 | `1.Request!A10:D10` | Mọi read đều dùng quyền quản trị `study.rbac.manage`; chưa tách `rbac.read` khỏi grant/revoke, trái least privilege `RBAC-01` (`BD-13:213-223`). | Tách read permission và giới hạn user/tenant/scope; thêm chống user enumeration. |
| 153-05 | P0 | `2.Response!A9:E11` | Envelope/pagination giả trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn camelCase; bỏ pagination singleton. |

## Điều kiện duyệt lại

- Có role catalog thống nhất và nguồn/thuật toán effective permissions.
- Có test read-only permission, missing user, inactive role và PII minimization.
