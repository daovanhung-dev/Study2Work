# Study API

FastAPI foundation for the Study subsystem.

## Commands

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 3003
```

## Health

- `GET /health/live`
- `GET /health/ready`

## Core conventions

- Tạo app bằng `create_app(Settings(...))` trong test hoặc môi trường cần
  cấu hình riêng.
- Dùng `Depends(get_db)` để nhận một SQLAlchemy `Session` theo request; view
  sở hữu `commit()` và `rollback()`.
- Response mới dùng `success_response()` và `error_response()` trong
  `app.core.responses`. Các helper `success_payload()` và `error_payload()`
  vẫn được giữ để chuyển tiếp code cũ.
- Password mới dùng Argon2id. Bcrypt chỉ được verify cho dữ liệu legacy.
- Refresh token mới phải là opaque token; chỉ lưu hash bằng
  `hash_refresh_token()`, không lưu raw token.

## Configuration

Runtime defaults được khai báo trực tiếp trong
`app/core/constants.py`; ứng dụng không tự đọc `.env` hoặc biến môi trường.
Database runtime dùng `URL_DATABASE` của Neon; các field DB local cũ chỉ còn
để tương thích khi truyền `Settings(...)`. Test/runtime vẫn có thể truyền
override tường minh qua `Settings(...)`.
ES256 là cấu hình mặc định; HS256 chỉ dùng cho compatibility ở môi trường
chuyển tiếp.
Ollama cũng lấy URL, model và timeout từ `app/core/constants.py`; chỉ
override trực tiếp qua `OllamaService(...)` được hỗ trợ. File `.env.example`
chỉ là tài liệu tham khảo và không được runtime đọc.
