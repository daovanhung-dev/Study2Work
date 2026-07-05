# Data Mapping — EXE-REVIEW-001

## 1. Aggregates / tables

`exercises, exercise_questions, exercise_attempts, exercise_submissions, submission_reviews, learner_scores`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| score | score | Input DTO → application command | Validate + normalize |
| feedback | feedback | Input DTO → application command | Validate + normalize |
| status | status | Input DTO → application command | Validate + normalize |
| reason | reason | Input DTO → application command | Validate + normalize |
| submissionId | - | Read model / response DTO | Filter by scope before serialization |
| status | - | Read model / response DTO | Filter by scope before serialization |
| score | - | Read model / response DTO | Filter by scope before serialization |
| reviewedAt | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Thao tác ghi chạy trong transaction; validate authorization và state transition trước khi commit.
- Có. Hành động admin hoặc thay đổi quyền/nội dung/ngoại lệ phải ghi `actor`, `action`, `reason`, `before`, `after`.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
