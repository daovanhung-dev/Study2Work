# AUTH-ME-001 — Lấy hồ sơ người dùng hiện tại

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `GET` |
| Endpoint | `/api/v1/users/me` |
| Module | 02. Tài khoản, xác thực và hồ sơ |
| Access | Bearer JWT khi endpoint không ghi rõ public |
| Actor | Guest, Learner, Content Admin, Learner Support, Community Moderator, Admin, Super Admin |
| Operation | READ |

## Mục tiêu

Lấy hồ sơ người dùng hiện tại. Không trả secret hoặc token

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
