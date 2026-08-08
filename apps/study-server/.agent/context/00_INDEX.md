# S2W Agent Context Index

Đọc theo thứ tự sau:

| Thứ tự | File | Mục đích |
|---:|---|---|
| 1 | `01_PROJECT_CONTEXT.md` | Bối cảnh, phạm vi và mục tiêu codebase |
| 2 | `02_ARCHITECTURE.md` | Kiến trúc backend và dependency direction |
| 3 | `03_CODING_FLOW.md` | Luồng chạy của một HTTP request/API |
| 4 | `04_FOLDER_FILE_RESPONSIBILITY.md` | Trách nhiệm từng folder/file |
| 5 | `05_API_DEVELOPMENT_WORKFLOW.md` | Quy trình tạo/sửa một API |
| 6 | `06_CORE_CONTRACTS.md` | Contract của core dùng chung |
| 7 | `07_DATABASE_TRANSACTION_RULES.md` | DB Session, query và transaction |
| 8 | `08_AUTH_TRACE_RESPONSE_RULES.md` | Security, Trace ID, response, exception |
| 9 | `09_EXTERNAL_SERVICE_FLOW.md` | Cách module gọi AI/external service |
| 10 | `10_CURRENT_SOURCE_STATUS.md` | Hiện trạng source và các gap đang có |
| 11 | `11_AGENT_WORK_RULES.md` | Luật bắt buộc cho AI coding agent |
| 12 | `12_IMPLEMENTATION_CHECKLIST.md` | Checklist trước/sau khi code |
| 13 | `13_REGISTER_FLOW_EXAMPLE.md` | Ví dụ flow chuẩn cho `/register` |

## Cách sử dụng

Khi task nhỏ, vẫn phải đọc tối thiểu:

```text
AGENTS.md
00_INDEX.md
10_CURRENT_SOURCE_STATUS.md
11_AGENT_WORK_RULES.md
```

Sau đó đọc file context đúng layer bị tác động.

Khi task tạo API mới, đọc toàn bộ từ `01` đến `13`.
