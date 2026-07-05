# PRG-RECALC-001 — Tính lại tiến độ nội bộ

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `POST` |
| Endpoint | `/internal/progress/recalculate` |
| Module | 07. Tiến độ và hoàn thành |
| Access | Bearer JWT; endpoint internal dùng service token |
| Actor | Learner, Internal Service, Admin |
| Operation | WRITE |

## Mục tiêu

Tính lại tiến độ nội bộ. Chỉ service token; không public qua frontend

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
