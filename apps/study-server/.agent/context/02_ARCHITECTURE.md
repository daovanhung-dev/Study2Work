# 02 — Backend Architecture

## Cấu trúc chính

```text
app/
├── main.py                 # Composition root của FastAPI
├── api/
│   └── v1.py               # HTTP routing
├── core/
│   ├── config.py           # Environment/settings
│   ├── database.py         # Engine, Session, DB primitive
│   ├── security.py         # Password/JWT/security primitive
│   ├── responses.py        # Response envelope
│   ├── middleware.py       # Cross-cutting HTTP middleware
│   ├── trace.py            # Trace ID primitive
│   └── exceptions.py       # Shared exception handling
├── module/
│   ├── auth/
│   ├── public/
│   └── ai/log/
└── service/
    └── ai/                  # Ollama adapter
```

## Dependency direction chuẩn

```text
main
 ↓
api
 ↓
module
 ├────────→ core
 └────────→ service
              ↓
        external system
```

`core` không được phụ thuộc business module.

`service` không được phụ thuộc router FastAPI.

`query.py` không được phụ thuộc router hoặc response HTTP.

## Boundary

### HTTP boundary

`api/` chuyển HTTP input thành lời gọi module.

### Business boundary

`module/<feature>/view.py` điều phối use case.

### Data boundary

`query.py` mô tả SQL; `core/database.py` quản lifecycle DB.

### Integration boundary

`service/` chịu trách nhiệm kết nối external systems.

### Application composition boundary

`main.py` cung cấp `create_app(settings)` để lắp middleware, exception
handlers, CORS, router và request-scoped database factory. Import `app.main`
không được tự mở kết nối database hoặc bắt buộc production settings ngay lập
tức.

`core/database.py` dùng SQLAlchemy `Session` đồng bộ. Engine và factory mặc
định được tạo lazy; app instance có thể giữ factory riêng trong `app.state`.

`core/security.py` là nơi duy nhất cho password/token primitives: Argon2id là
thuật toán ghi mới, bcrypt chỉ verify legacy; JWT key provider được inject khi
cần JWKS.

## Quy tắc dependency

### Được phép

```text
api -> module
module -> core
module -> service
service -> thư viện external
core -> thư viện framework/infrastructure
```

### Tránh

```text
core -> module
service -> api
query -> FastAPI HTTPException
model -> database
router -> SQL
router -> bcrypt
```

## Module chuẩn

Một module nghiệp vụ ưu tiên giữ dạng:

```text
module/<feature>/
├── model.py
├── validate.py
├── query.py
└── view.py
```

Chỉ tách thêm file khi module thực sự lớn; không tạo abstraction chỉ để tăng số layer.
