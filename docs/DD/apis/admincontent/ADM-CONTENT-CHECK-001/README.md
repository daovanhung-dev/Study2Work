# ADM-CONTENT-CHECK-001 — Kiểm tra trước khi publish

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/admin/content/{contentType}/{contentId}/pre-publish-check` |
| Module | 10. Admin quản trị nội dung |
| Access | Bearer JWT |
| Actor | Content Admin, Admin, Super Admin |
| Operation | WRITE |

## Mục tiêu

Kiểm tra trước khi publish. Không publish nếu passed=false

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
