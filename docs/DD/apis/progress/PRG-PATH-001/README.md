# PRG-PATH-001 — Lấy tiến độ theo lộ trình

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `GET` |
| Endpoint | `/api/v1/progress/learning-paths/{pathId}` |
| Module | 07. Tiến độ và hoàn thành |
| Access | Bearer JWT; endpoint internal dùng service token |
| Actor | Learner, Internal Service, Admin |
| Operation | READ |

## Mục tiêu

Lấy tiến độ theo lộ trình. Chỉ owner hoặc role có quyền support

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
