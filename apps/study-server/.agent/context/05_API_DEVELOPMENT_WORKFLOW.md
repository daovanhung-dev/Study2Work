# 05 — API Development Workflow

## Mục tiêu

Khi người dùng yêu cầu tạo một API, agent phải phát triển theo cùng một quy trình để giữ code dễ hiểu và nhất quán.

## Bước 1 — Xác định contract

Khóa tối thiểu:

- Method.
- Endpoint.
- Auth requirement.
- Request fields.
- Response fields.
- Business rule.
- DB tables/query.
- Error cases.

Nếu DD/BD/schema/source được cung cấp, không tự sáng tạo contract ngoài bằng chứng.

## Bước 2 — Xác định module

Ví dụ:

```text
POST /register
→ module/auth/
```

Không tạo module mới khi API thuộc module hiện có.

## Bước 3 — Model

Tạo/chỉnh `model.py` trước để contract request rõ.

Mỗi field nên có type đúng. Không dùng `Any` khi schema đã biết.

## Bước 4 — Validation

Tạo validation cho:

- required/blank.
- format.
- length.
- range.

Không truy vấn DB trong validation thuần nếu không cần.

## Bước 5 — Query

Tạo SQL constant trong `query.py`.

Ví dụ:

```sql
SELECT id
FROM users
WHERE email = :email;
```

Không interpolate string trực tiếp.

## Bước 6 — Implement view

Khung mutation:

```text
1. normalize input
2. validate input
3. business checks
4. prepare generated/system values
5. execute mutation(s)
6. commit
7. build response
8. on DB/business failure: rollback if needed
```

Khung read:

```text
1. normalize input
2. validate
3. execute query
4. handle not-found/empty
5. map result
6. build response
```

## Bước 7 — Router

Router chỉ nối HTTP contract vào view.

## Bước 8 — End-to-end review

Rà theo chuỗi:

```text
Router
→ Request Model
→ View signature
→ Validation
→ Query parameters
→ DB schema
→ Response
→ Error path
```

## Bước 9 — Test tối thiểu

Nếu môi trường cho phép:

- Import test.
- Start app/import app.
- Happy path.
- Validation failure.
- DB conflict/not-found.
- Transaction rollback với mutation nhiều bước.

Không ghi “đã chạy thành công” nếu chỉ đọc source.

## Quy tắc sửa API cũ

Trước khi sửa:

1. Trace endpoint tới view.
2. Trace view tới validate/query/core/service.
3. Xác định root cause thuộc layer nào.
4. Sửa layer chịu trách nhiệm nhỏ nhất.
5. Rà side effects các endpoint dùng chung helper đó.
