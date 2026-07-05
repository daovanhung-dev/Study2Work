# AUTH-LOGIN-001 — Đăng nhập

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/auth/login` |
| Module | 02. Tài khoản, xác thực và hồ sơ |
| Access | Bearer JWT khi endpoint không ghi rõ public |
| Actor | Guest, Learner, Content Admin, Learner Support, Community Moderator, Admin, Super Admin |
| Operation | WRITE |

## Mục tiêu

Đăng nhập. Rate limit và lockout theo chính sách

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
