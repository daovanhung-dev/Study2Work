# CNT-RESOURCE-DOWNLOAD-001 — Xin signed URL tải tài liệu

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/lesson-resources/{resourceId}/download-url` |
| Module | 05. Khóa học và nội dung học |
| Access | Bearer JWT cho nội dung học; catalog công khai tách riêng |
| Actor | Learner, Content Admin, Admin |
| Operation | WRITE |

## Mục tiêu

Xin signed URL tải tài liệu. Log download intent, enforce quyền truy cập

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
