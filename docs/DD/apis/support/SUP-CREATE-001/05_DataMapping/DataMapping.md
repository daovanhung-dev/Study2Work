# Data Mapping — SUP-CREATE-001

## 1. Aggregates / tables

`support_requests, support_comments, learner_support_profiles, learner_path_exceptions, learner_flags, audit_logs`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| category | category | Input DTO → application command | Validate + normalize |
| subject | subject | Input DTO → application command | Validate + normalize |
| description | description | Input DTO → application command | Validate + normalize |
| attachments | attachments | Input DTO → application command | Validate + normalize |
| id | - | Read model / response DTO | Filter by scope before serialization |
| status | - | Read model / response DTO | Filter by scope before serialization |
| createdAt | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Thao tác ghi chạy trong transaction; validate authorization và state transition trước khi commit.
- Có log sự kiện nghiệp vụ theo người dùng và traceId.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
