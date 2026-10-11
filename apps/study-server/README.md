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
- Success envelope dùng `success_response()`; lỗi dùng `error_response(...)`, hàm
  trả trực tiếp `JSONResponse` với status, envelope và trace header.
- Chuẩn hóa input dùng chung nằm trong `app/utils/validate.py`; helper
  Bearer/JWT/token dùng chung nằm trong `app/utils/auth.py`. API có rule input
  riêng đặt trong `validate.py`; API #4 dùng auth guard chung trực tiếp.
- Password mới dùng Argon2id. Bcrypt chỉ được verify cho dữ liệu legacy.
- Refresh token mới phải là opaque token; app dùng `hash_refresh_token()` qua
  `app/utils/auth.py` để lưu hash, không lưu raw token. Primitive HMAC nằm trong
  `app/core/security/refresh_token.py`.

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
