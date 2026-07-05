# NOTI-ADMIN-SEND-001 — Gửi thông báo

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/admin/notifications/{notificationId}/send` |
| Module | 09. Thông báo nghiệp vụ |
| Access | Bearer JWT |
| Actor | Learner, Content Admin, Learner Support, Admin |
| Operation | WRITE |

## Mục tiêu

Gửi thông báo. Idempotent send và audit

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
