# 13 — Register Flow Example

File này minh họa cách agent nên hiểu và implement API `/register` dựa trên source hiện tại. Đây là flow hướng dẫn; phải đối chiếu schema/business document trước khi thay đổi contract thực tế.

## Endpoint hiện tại

```text
POST /api/v1/register
```

Router nhận:

```text
RegisterRequest
├── display_name
├── email
├── phone
└── password
```

Router inject:

```text
db: Session = Depends(get_db)
```

## Flow chuẩn

```text
1. Router nhận RegisterRequest
2. Router gọi create_user(user_data, db)
3. View normalize:
   - display_name
   - email
   - phone
4. View gọi validate_user_create()
5. Nếu validation lỗi:
   - trả/raise error theo response contract chuẩn
6. Tạo user ID theo rule đã được schema/source xác nhận
7. Hash password bằng hash_password()
8. Thực hiện CREATE_USER
9. Lấy user_id RETURNING
10. Thực hiện CREATE_AUTH_CREDENTIAL
11. Nếu cả hai thành công:
    - db.commit()
12. Nếu IntegrityError/DB error sau mutation:
    - db.rollback()
    - map known error an toàn
13. Map response success
14. Trả response với traceId của request
```

## Dependency map

```text
api/v1.py
  ↓
auth/model.py
  ↓
auth/view.py
  ├─ auth/validate.py
  ├─ auth/query.py
  ├─ core/security.py
  ├─ core/database.py / injected Session
  └─ core/responses.py
```

## Query hiện có

`CREATE_USER` ghi:

```text
users.id
users.display_name
users.email
users.phone
users.created_at
users.updated_at
```

`CREATE_AUTH_CREDENTIAL` ghi:

```text
auth_credentials.user_id
auth_credentials.password_hash
auth_credentials.password_algorithm
auth_credentials.password_login_enabled
auth_credentials.must_change_password
auth_credentials.failed_login_attempts
auth_credentials.locked_until
auth_credentials.password_changed_at
auth_credentials.last_login_at
auth_credentials.created_at
auth_credentials.updated_at
```

## Transaction requirement

Nếu business rule coi user và auth credential là một registration record hoàn chỉnh, hai INSERT phải atomic:

```text
INSERT users
INSERT auth_credentials
COMMIT
```

Không commit `users` trước rồi để `auth_credentials` thất bại làm dữ liệu dở dang.

## Current gap

`auth/view.py` hiện rỗng, do đó `create_user` chưa tồn tại trong source snapshot.

Agent không được giả định API này đã hoàn thiện chỉ vì router đã được khai báo.
