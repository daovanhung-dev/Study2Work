# 07 — Database & Transaction Rules

## Hiện trạng source

`core/database.py` hiện có cả:

```text
get_db() -> request-scoped Session
```

và:

```text
db = SessionLocal() -> global Session
query_one()
query_many()
```

Đây là hai lifecycle khác nhau.

## Quy ước develop chuẩn

**Ưu tiên duy nhất request-scoped Session cho HTTP API.**

```text
Request
 ↓
get_db()
 ↓
Session
 ↓
view
 ↓
DB operations
 ↓
commit / rollback
 ↓
request kết thúc
 ↓
close
```

## Cấm

Không sử dụng một global `Session` mutable dùng chung giữa concurrent requests.

Không tạo `SessionLocal()` mới rải rác trong từng view nếu router đã inject `db`.

## Query primitive

Read:

```python
result = db.execute(text(SQL), params)
row = result.mappings().first()
```

Read-many:

```python
rows = db.execute(text(SQL), params).mappings().all()
```

Write:

```python
db.execute(text(SQL), params)
```

## Transaction ownership

`query.py` không commit.

View/use-case layer quyết định transaction boundary vì nó biết toàn bộ business operation.

Ví dụ register cần tạo cả:

```text
users
+ auth_credentials
```

Nếu hai mutation là một use case atomic:

```text
INSERT users
INSERT auth_credentials
COMMIT
```

Nếu mutation 2 lỗi:

```text
ROLLBACK
```

Không commit giữa hai bước nếu business yêu cầu cả hai cùng thành công.

## IntegrityError

Khi bắt `IntegrityError`:

- rollback trước khi reuse Session.
- map known constraint sang business error khi constraint đã được xác nhận.
- không expose raw database error cho client.
- constraint name phải đến từ schema/source, không tự bịa.

## SQL safety

Luôn parameterize:

```sql
WHERE email = :email
```

Không:

```python
f"WHERE email = '{email}'"
```

## DB schema

Không tự tạo table/column trong code khi task chỉ yêu cầu API.

Nếu code cần column chưa có trong schema/tài liệu, báo gap thay vì âm thầm invent.
