# Lệnh chạy server và web

> Cột **Lệnh chạy local** ghi lệnh khởi động từ package hoặc README của từng dự án. Chạy lệnh từ đúng thư mục con ghi trong tên dịch vụ/dự án, không cần đứng tại root repository.

| STT | Tên dịch vụ/dự án                                         | Công nghệ                                           | Lệnh chạy local                                                     | Địa chỉ local          |
| --: | -------------------------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- | ------------------------- |
|   1 | Study API ([apps/study-server/](../../apps/study-server/))      | FastAPI, Python 3.12, SQLAlchemy, PostgreSQL/Neon     | `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 3003` | `http://127.0.0.1:3003` |
|   2 | Work API ([apps/work-server/](../../apps/work-server/))         | Node.js, TypeScript, Express, Prisma, PostgreSQL/Neon | `npm run s2w`                                                       | `http://127.0.0.1:3002` |
|   3 | AI API ([apps/ai-server/](../../apps/ai-server/))               | FastAPI, Python 3.12, httpx, Ollama                   | `uv run uvicorn app.main:app --host 127.0.0.1 --port 3000`          | `http://127.0.0.1:3000` |
|   4 | Study Web ([apps/study-client/](../../apps/study-client/))      | Angular 22, TypeScript                                | `npm start`                                                         | `http://localhost:4200` |
|   5 | Work Web ([apps/work-client/web/](../../apps/work-client/web/)) | React, TypeScript, Vite                               | `npm run dev`                                                       | `http://127.0.0.2:3001` |

Các lệnh giả định dependencies và cấu hình runtime của từng dự án đã sẵn sàng. Study Web proxy `/api/v1` tới Study API tại cổng `3003`; Work Web proxy `/api`, `/uploads` và `/img` tới Work API tại cổng `3002`, nên cần chạy API tương ứng khi dùng các đường dẫn này. AI API dùng Ollama như một dịch vụ riêng; API có prefix `/api/v1`.
prompt build server:
Ví dụ user là s2w_server

```Shell
sudo -u s2w_server -H bash -c '
set -ecd /opt/apps/s2w/Study2Workecho "========== 1. STUDY CLIENT =========="
npm ci --prefix apps/study-clientecho "========== 2. WORK SERVER =========="
npm ci --prefix apps/work-serverecho "========== 3. WORK CLIENT =========="
npm install --prefix apps/work-client/webecho "========== 4. STUDY SERVER =========="
uv sync --project apps/study-serverecho "========== 5. AI SERVER =========="
uv sync --project apps/ai-serverecho "========== 6. PRISMA CLIENT =========="
npm run prisma:generate --prefix apps/work-serverecho "========== INSTALLATION COMPLETE =========="
'
```
