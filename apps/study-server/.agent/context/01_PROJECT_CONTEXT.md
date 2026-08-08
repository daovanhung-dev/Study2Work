# 01 — Project Context

## Hệ thống

- Project: Study2Work (S2W).
- Context source hiện tại: backend FastAPI.
- Database: PostgreSQL qua SQLAlchemy.
- Password hashing: bcrypt.
- External AI hiện có: Ollama qua `httpx`.
- API prefix hiện tại: `/api/v1`.

## Mục tiêu codebase

Codebase được tổ chức để developer tập trung vào **business logic của API**, còn hạ tầng dùng chung nằm trong `core/` hoặc `service/`.

Mục tiêu phát triển:

```text
Developer viết nghiệp vụ
        ↓
module/<feature>
        ↓
core xử lý hạ tầng
        ↓
service xử lý external integration
```

## Triết lý thiết kế

### 1. Dễ đọc hơn abstraction phức tạp

Không tạo framework nội bộ quá sâu khi bốn file sau đã đủ biểu đạt module:

```text
model.py
validate.py
query.py
view.py
```

### 2. Business logic có một nơi điều phối chính

`view.py` là orchestration layer của module.

### 3. Infrastructure dùng chung không lặp lại theo module

Các concerns như DB connection, password hashing, JWT, Trace ID, response envelope, exception mapping phải được tập trung vào `core/`.

### 4. External integration được bao lại

Module không nên biết chi tiết `httpx`, base URL, timeout hoặc protocol của Ollama. Các chi tiết đó nằm trong `service/ai/`.

## Không được suy diễn

Source hiện tại không cung cấp đầy đủ bằng chứng cho:

- Flow frontend VueJS.
- JWT implementation hoàn chỉnh.
- Refresh token implementation.
- Trace middleware hoàn chỉnh.
- Global exception handler hoàn chỉnh.
- Business rule đầy đủ cho các module khác ngoài đoạn auth mẫu.

Khi cần các phần trên, phải đọc source/tài liệu mới được cung cấp hoặc triển khai theo yêu cầu rõ ràng của người dùng.
