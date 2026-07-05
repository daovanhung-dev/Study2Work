# RBA-ROLE-REVOKE-001 — Thu hồi role của người dùng

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `DELETE` |
| Endpoint | `/api/v1/admin/users/{userId}/roles/{roleId}` |
| Module | 13. RBAC và Audit |
| Access | Bearer JWT |
| Actor | Admin, Super Admin |
| Operation | WRITE |

## Mục tiêu

Thu hồi role của người dùng. Không được xóa role cuối gây mất quyền quản trị theo policy

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
