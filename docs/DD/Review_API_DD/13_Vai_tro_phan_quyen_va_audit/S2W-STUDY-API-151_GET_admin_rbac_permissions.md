# Review S2W-STUDY-API-151 — GET RBAC permissions

- DD nguồn: `docs/DD/Study2Work_DD_API/13_Vai_tro_phan_quyen_va_audit/S2W-STUDY-API-151_GET_admin_rbac_permissions.xlsx`
- Endpoint: `GET /api/v1/admin/rbac/permissions`
- Kết luận: **CẦN SỬA — target relation không tồn tại**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 151-01 | P0 | `2.Response!A15:H21`, `3.Data mapping!A12:H20` | `study.permissions` và `study.role_permissions` không tồn tại trong schema; SQL SELECT `permission_code/name/group/description/risk_level` từ bảng giả. | Thiết kế permission catalog + role-permission relation, PK/FK/unique/index/migration, hoặc xác định catalog nằm ở Authorization Service và gọi/read projection từ đó. |
| 151-02 | P0 | toàn workbook | DD dùng các permission code như `study.rbac.manage`, trong khi SEQ-14 yêu cầu `audit.read` và BD mới chỉ mô tả nhóm quyền nghiệp vụ, không có catalog kỹ thuật (`BD-13:37-140`, `SEQ-14:33-38`). | Chốt naming convention và danh mục quyền authoritative; map từng role theo least privilege. |
| 151-03 | P1 | `1.Request!A21:J21` | `group` là String tự do và trùng từ khóa SQL; không có enum/scope semantics. | Đổi `permissionGroup`/`scope`, chốt enum và unknown behavior. |
| 151-04 | P0 | `2.Response!A9:E11`, sample success | Envelope/pagination cũ trái `System_Architecture.md:632-700`; response list không có request pagination nhưng sample vẫn chèn page. | Dùng envelope chuẩn; hoặc thêm page/pageSize contract thật, hoặc bỏ pagination. |
| 151-05 | P1 | `00.Hướng dẫn!A10:B18`, `Lịch sử!A4:F4` | Checklist xác nhận đã review schema dù target table không có. | Hạ trạng thái và chỉ verify sau khi permission persistence/owner được phê duyệt. |

## Điều kiện duyệt lại

- Có permission catalog authoritative và persistence/integration contract.
- Có test uniqueness, grouping, least-privilege và response contract.
