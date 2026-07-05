# Data Mapping — RBA-PERMISSION-LIST-001

## 1. Aggregates / tables

`roles, permissions, user_roles, role_permissions, audit_logs`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| items | - | Read model / response DTO | Filter by scope before serialization |
| pagination | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Query read-only; áp dụng scope/visibility trước khi trả kết quả.
- Có. Hành động admin hoặc thay đổi quyền/nội dung/ngoại lệ phải ghi `actor`, `action`, `reason`, `before`, `after`.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
