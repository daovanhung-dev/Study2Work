# SUP-EXCEPTION-DECIDE-001 — Duyệt hoặc từ chối ngoại lệ lộ trình

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/api/v1/admin/learner-path-exceptions/{exceptionId}/decision` |
| Module | 11. Admin học viên, hỗ trợ và ngoại lệ |
| Access | Bearer JWT |
| Actor | Learner, Learner Support, Admin, Super Admin |
| Operation | WRITE |

## Mục tiêu

Duyệt hoặc từ chối ngoại lệ lộ trình. Cho phép chuyển lộ trình chỉ khi decision approved

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
