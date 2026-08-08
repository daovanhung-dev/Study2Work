# 03 — Coding / Runtime Flow

## Luồng request chuẩn

```text
1. Client gửi HTTP request
2. FastAPI nhận request
3. Middleware tạo/đọc trace ID
4. Auth dependency/middleware xác thực nếu API yêu cầu
5. Router parse request bằng model
6. Router inject DB Session qua Depends(get_db)
7. Router gọi module view
8. View gọi validate
9. View điều phối query/business rule/service
10. DB mutation commit hoặc rollback theo transaction boundary
11. View tạo response chuẩn
12. Middleware/exception layer hoàn tất response
13. Client nhận response có traceId
```

## Luồng source tương ứng

```text
main.py
  ↓
api/v1.py
  ↓
module/<feature>/model.py
  ↓
module/<feature>/view.py
  ├─ module/<feature>/validate.py
  ├─ module/<feature>/query.py
  │      ↓
  │  core/database.py
  └─ service/<integration>/
  ↓
core/responses.py
```

## Router phải mỏng

Router chỉ nên làm các việc thuộc HTTP layer:

- Path/method.
- Dependency injection.
- Request schema binding.
- Gọi view/use case.
- Trả kết quả.

Không đặt trong router:

- Business rule.
- SQL.
- Hash password.
- Transaction orchestration.
- Mapping lỗi DB phức tạp.

## View là orchestration layer

`view.py` có thể:

- Normalize input.
- Gọi validation.
- Đọc current user/context.
- Gọi query.
- Gọi security helper.
- Gọi external service.
- Điều phối transaction.
- Map result thành response.

View không nên:

- Tự tạo engine.
- Tự đọc `.env`.
- Tự mở global DB connection.
- Copy/paste thuật toán infrastructure đã có trong core.

## Validation flow

Validation phải phân biệt:

1. Input validation: format, required, length.
2. Business validation: duplicate, state, permission, existence.

Input validation thường nằm trong `validate.py`.
Business validation có thể cần query và được orchestration từ `view.py`.

## Read API flow

```text
router
 ↓
view
 ↓
validate
 ↓
SELECT query
 ↓
map response
 ↓
return
```

## Mutation API flow

```text
router
 ↓
view
 ↓
validate
 ↓
business checks
 ↓
BEGIN logical transaction
 ↓
mutation 1
 ↓
mutation 2...
 ↓
commit
 ↓
response

Nếu lỗi sau khi mutation bắt đầu:
rollback
 ↓
map lỗi chuẩn
```
