# Data Mapping — AUTH-ME-001

## 1. Aggregates / tables

`users, user_profiles, contact_verifications, refresh_tokens, auth_sessions`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| id | - | Read model / response DTO | Filter by scope before serialization |
| email | - | Read model / response DTO | Filter by scope before serialization |
| fullName | - | Read model / response DTO | Filter by scope before serialization |
| roles | - | Read model / response DTO | Filter by scope before serialization |
| contactStatus | - | Read model / response DTO | Filter by scope before serialization |
| onboardingStatus | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Query read-only; áp dụng scope/visibility trước khi trả kết quả.
- Không tạo audit mutation; access log vẫn được ghi.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
