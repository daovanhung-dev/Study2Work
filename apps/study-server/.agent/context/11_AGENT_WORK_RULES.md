# 11 — AI Agent Work Rules

## A. Trước khi code

1. Đọc `AGENTS.md`.
2. Đọc context liên quan.
3. Inspect source hiện tại; không code chỉ dựa trên context.
4. Xác định endpoint → module → dependencies.
5. Xác định source of truth cho business rule/schema.
6. Ghi nhận gap nếu thiếu bằng chứng quan trọng.

## B. Khi code

### Rule 01 — Giữ workflow folder

Không phá flow:

```text
api -> module -> core/service
```

### Rule 02 — Router mỏng

Không chuyển business logic lên router để “fix nhanh”.

### Rule 03 — View điều phối

Use case flow đặt trong `view.py`.

### Rule 04 — Query tách riêng

SQL của module đặt trong `query.py`.

### Rule 05 — Model rõ kiểu

Contract đã biết thì dùng kiểu cụ thể.

### Rule 06 — Validate đúng lớp

Validation thuần đặt `validate.py`; business check cần DB được orchestration ở view.

### Rule 07 — Core không biết business module

Không import module vào core.

### Rule 08 — Session theo request

Không sử dụng global SQLAlchemy Session trong HTTP business flow.

Engine/session factory mặc định phải lazy; test/runtime riêng có thể inject
factory qua `app.state`.

### Rule 09 — Transaction atomic

Use case nhiều mutation phụ thuộc phải rollback nếu một mutation thất bại.

### Rule 10 — Security tập trung

Hash/JWT/security helper ở core, không copy theo module.

Password mới dùng Argon2id; bcrypt chỉ verify dữ liệu cũ. Không tự triển khai
refresh-session persistence trong Study server khi chưa có Identity schema.

### Rule 11 — Trace nhất quán

Không hard-code trace ID.

### Rule 12 — Response nhất quán

Không trả random dict shape nếu project đã có response contract.

### Rule 13 — External service qua adapter

Không gọi Ollama/third-party trực tiếp từ router.

### Rule 14 — Không invent dữ liệu

Không tự tạo:

- table.
- column.
- constraint.
- business code.
- JWT claim.
- role/permission.
- endpoint semantics.

nếu task/source chưa xác nhận.

### Rule 15 — Sửa tối thiểu

Không refactor unrelated module trong task bug/API cụ thể trừ khi dependency chung là root cause.

### Rule 16 — Không che lỗi bằng fallback giả

Không return success giả khi DB/service lỗi.

### Rule 17 — Không nuốt exception

Không `except Exception: pass`.

### Rule 18 — Secret safety

Không log hoặc response password, password hash, token, DB password.

## C. Sau khi code

1. Kiểm tra imports.
2. Kiểm tra signature router ↔ view.
3. Kiểm tra query params ↔ SQL placeholders.
4. Kiểm tra commit/rollback.
5. Kiểm tra response/error flow.
6. Kiểm tra async/await.
7. Kiểm tra code không dùng global Session mới.
8. Chạy test/import/lint phù hợp nếu môi trường có.
9. Báo rõ phần đã test và phần chưa test.

## D. Khi source và context khác nhau

Source mới thắng context cũ, trừ khi người dùng nói source đang sai và tài liệu khác mới là baseline.

Agent phải nói rõ mismatch thay vì âm thầm áp context cũ.
