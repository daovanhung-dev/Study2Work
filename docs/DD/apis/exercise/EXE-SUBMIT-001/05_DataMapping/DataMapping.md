# Data Mapping — EXE-SUBMIT-001

## 1. Aggregates / tables

`exercises, exercise_questions, exercise_attempts, exercise_submissions, submission_reviews, learner_scores`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| attemptId | attempt_id | Input DTO → application command | Validate + normalize |
| answers | answers | Input DTO → application command | Validate + normalize |
| submittedAt | submitted_at | Input DTO → application command | Validate + normalize |
| submissionId | - | Read model / response DTO | Filter by scope before serialization |
| status | - | Read model / response DTO | Filter by scope before serialization |
| score | - | Read model / response DTO | Filter by scope before serialization |
| feedback | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Thao tác ghi chạy trong transaction; validate authorization và state transition trước khi commit.
- Có log sự kiện nghiệp vụ theo người dùng và traceId.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
