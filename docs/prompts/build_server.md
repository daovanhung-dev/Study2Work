# Lệnh chạy server

> Cột **Lệnh build dịch vụ** được điền bằng lệnh khởi động local đã ghi trong README của từng server. Chạy lệnh từ đúng thư mục dự án con ghi ở cột tên dịch vụ, không cần đứng tại root repository.

| STT | Tên dịch vụ | Công nghệ | Lệnh build dịch vụ | Địa chỉ dịch vụ |
|---:|---|---|---|---|
| 1 | Study API ([apps/study-server/](../../apps/study-server/)) | FastAPI, Python 3.12, SQLAlchemy, PostgreSQL/Neon | `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 3003` | `http://127.0.0.1:3003` |
| 2 | Work API ([apps/work-server/](../../apps/work-server/)) | Node.js, TypeScript, Express, Prisma, PostgreSQL/Neon | `npm run s2w` | `http://127.0.0.1:3002` |
| 3 | AI API ([apps/ai-server/](../../apps/ai-server/)) | FastAPI, Python 3.12, httpx, Ollama | `uv run uvicorn app.main:app --host 127.0.0.1 --port 3000` | `http://127.0.0.1:3000` |

Các lệnh giả định dependencies và cấu hình runtime của từng dự án đã sẵn sàng. AI API dùng Ollama như một dịch vụ riêng; API có prefix `/api/v1`.
