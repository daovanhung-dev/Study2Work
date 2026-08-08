# Study API

FastAPI foundation for the Study subsystem.

## Commands

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
uv run uvicorn app.main:app --reload
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

## Environment

Copy `.env.example` thành `.env` rồi cấu hình database, Redis và key JWT.
ES256 là cấu hình mặc định; HS256 chỉ dùng cho compatibility ở môi trường
chuyển tiếp.
