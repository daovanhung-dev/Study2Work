# Data Mapping — CNT-BOOKMARK-001

## 1. Aggregates / tables

`courses, course_modules, lessons, lesson_resources, content_versions, learner_lesson_access`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| positionSeconds | position_seconds | Input DTO → application command | Validate + normalize |
| note | note | Input DTO → application command | Validate + normalize |
| id | - | Read model / response DTO | Filter by scope before serialization |
| positionSeconds | - | Read model / response DTO | Filter by scope before serialization |
| updatedAt | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Thao tác ghi chạy trong transaction; validate authorization và state transition trước khi commit.
- Có log sự kiện nghiệp vụ theo người dùng và traceId.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
