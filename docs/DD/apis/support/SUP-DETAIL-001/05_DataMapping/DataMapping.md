# Data Mapping — SUP-DETAIL-001

## 1. Aggregates / tables

`support_requests, support_comments, learner_support_profiles, learner_path_exceptions, learner_flags, audit_logs`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| request | - | Read model / response DTO | Filter by scope before serialization |
| comments | - | Read model / response DTO | Filter by scope before serialization |
| statusHistory | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Query read-only; áp dụng scope/visibility trước khi trả kết quả.
- Không tạo audit mutation; access log vẫn được ghi.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
