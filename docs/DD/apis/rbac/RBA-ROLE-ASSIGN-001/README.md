# RBA-ROLE-ASSIGN-001 — Gán role cho người dùng

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/admin/users/{userId}/roles` |
| Module | 13. RBAC và Audit |
| Access | Bearer JWT |
| Actor | Admin, Super Admin |
| Operation | WRITE |

## Mục tiêu

Gán role cho người dùng. Không tự nâng quyền, separation of duty

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
