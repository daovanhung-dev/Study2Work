# Business Code Delta — Plan 20 — RBAC and Audit

| API | Success code | Meaning |
|---:|---|---|
| 150 | `ADMIN_RBAC_ROLES_RETRIEVED` | Lấy danh sách vai trò nghiệp vụ. thành công. |
| 151 | `ADMIN_RBAC_PERMISSIONS_RETRIEVED` | Lấy danh mục quyền chức năng. thành công. |
| 152 | `ADMIN_RBAC_MATRIX_RETRIEVED` | Lấy ma trận vai trò-quyền để kiểm thử và quản trị. thành công. |
| 153 | `ADMIN_USERS_ROLES_RETRIEVED` | Xem vai trò quản trị của một người dùng. thành công. |
| 154 | `ADMIN_USERS_ROLES_CREATED` | Cấp vai trò Admin/Support/Moderator/Content Admin. thành công. |
| 155 | `ADMIN_USERS_ROLES_ROLE_CODE_DELETED` | Thu hồi vai trò quản trị. thành công. |
| 156 | `AUDIT_LOGS_LISTED` | Tìm audit log theo đối tượng, người thực hiện, hành động và thời gian. thành công. |
| 157 | `ADMIN_AUDIT_LOGS_RETRIEVED` | Xem chi tiết một bản ghi audit. thành công. |

Shared error codes: `REQUEST_REQUIRED`, `REQUEST_INVALID_FORMAT`, `METHOD_NOT_ALLOWED`, `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `RESOURCE_NOT_FOUND`, `BUSINESS_RULE_VIOLATION`, `CONCURRENT_UPDATE_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `RATE_LIMIT_EXCEEDED`, `DEPENDENCY_UNAVAILABLE`, `INTERNAL_ERROR`.
