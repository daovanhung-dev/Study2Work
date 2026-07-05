# PRG-LESSON-UPDATE-001 — Cập nhật sự kiện tiến độ bài học

| Thuộc tính | Giá trị |
| --- | --- |
| Method | `PATCH` |
| Endpoint | `/api/v1/lessons/{lessonId}/progress` |
| Module | 07. Tiến độ và hoàn thành |
| Access | Bearer JWT; endpoint internal dùng service token |
| Actor | Learner, Internal Service, Admin |
| Operation | WRITE |

## Mục tiêu

Cập nhật sự kiện tiến độ bài học. Dedupe clientEventId; server quyết định completion

## Tài liệu thành phần

- [01. Overview](01_Overview/Overview.md)
- [02. History](02_History/History.md)
- [03. Request](03_Request/Request.md)
- [04. Response](04_Response/Response.md)
- [05. Data Mapping](05_DataMapping/DataMapping.md)
- [06. Error](06_Error/Error.md)
