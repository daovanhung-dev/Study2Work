# OPEN QUESTIONS

- `Q-01` — `authVersion` được yêu cầu bởi API/rule nhưng không có cột vật lý canonical; không ánh xạ ngầm sang `session_epoch`.
- `Q-02` — Password history chưa có table/schema để thực hiện `PASSWORD_REUSED`.
- `Q-03` — `GET /me` yêu cầu agreements nhưng database chưa có agreement table.
- `Q-15` — Event payload/version chưa có schema đầy đủ cho nhiều endpoint.
- `Q-16` — Field-level JSON Schema request/response chưa đầy đủ cho toàn bộ API catalog.
