# Review S2W-STUDY-API-150 — GET RBAC roles

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-150_GET_admin_rbac_roles.xlsx`
- Endpoint: `GET /api/v1/admin/rbac/roles`
- Kết luận: **CẦN SỬA — role model giữa BD, DD và schema chưa thống nhất**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 150-01 | P0 | `2.Response!A16:H20`, `3.Data mapping!A12:H20` | DD SELECT `role_code`, `description`, `risk_level`, `user_count` như cột `roles`; schema chỉ có `code`, `name`, `scope`, `active`, còn user count là aggregate (`schema_seed.sql:303-317`). | Map `code`, JOIN/count user_roles, dùng integer; bổ sung migration cho description/riskLevel hoặc bỏ field. |
| 150-02 | P0 | `Overview!A19:B20`, response | Danh sách role nghiệp vụ của BD gồm Guest, Learner, Content Admin, Learner Support, Community Moderator, Admin, Super Admin (`BD-13:23-33`), nhưng seed dùng SYSTEM_ADMIN, CONTENT_MANAGER, REPORT_VIEWER và không có Guest/Admin/Super Admin (`schema_seed.sql:857-873`). | Chốt authoritative role catalog/mapping và migration trước khi công bố API. |
| 150-03 | P1 | `3.Data mapping!A12:H17` | DD tham chiếu `permissions/role_permissions` dù schema không có hai bảng; rule one-ACTIVE/PUBLISHED không liên quan RBAC. | Bỏ join giả; chỉ liệt kê role từ schema đã chốt hoặc bổ sung đầy đủ permission model. |
| 150-04 | P0 | `2.Response!A9:E11`, sample success | Envelope cũ, snake_case và pagination giả trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn camelCase; pagination chỉ nếu request có page contract. |
| 150-05 | P1 | `Cover!B19`, `00.Hướng dẫn!A4:B18`, `Lịch sử!A4:F4` | DD đánh dấu VERIFIED và “không còn placeholder” dù model đang xung đột và review/approve chưa chỉ định. | Chuyển NEEDS_REVIEW; ghi quyết định role catalog là dependency bắt buộc. |

## Điều kiện duyệt lại

- Role catalog/code/scope giữa BD, seed và API được thống nhất.
- Query/mapping chỉ dùng field tồn tại và userCount được test.
