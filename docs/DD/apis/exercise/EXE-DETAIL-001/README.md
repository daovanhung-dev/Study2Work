# EXE-DETAIL-001 — Lấy đề bài theo quyền learner

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `GET` |
| Endpoint | `/api/v1/exercises/{exerciseId}` |
| Module | 06. Bài tập và đánh giá |
| Access | Bearer JWT |
| Actor | Learner, Content Admin, Learner Support, Admin |
| Operation | READ |

## Mục tiêu

Lấy đề bài theo quyền learner. Không trả đáp án hoặc rubric nội bộ khi chưa được phép

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
