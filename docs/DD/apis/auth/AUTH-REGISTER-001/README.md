# AUTH-REGISTER-001 — Đăng ký tài khoản

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/auth/register` |
| Module | 02. Tài khoản, xác thực và hồ sơ |
| Access | Bearer JWT khi endpoint không ghi rõ public |
| Actor | Guest, Learner, Content Admin, Learner Support, Community Moderator, Admin, Super Admin |
| Operation | WRITE |

## Mục tiêu

Đăng ký tài khoản. Không tự cấp quyền admin

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
