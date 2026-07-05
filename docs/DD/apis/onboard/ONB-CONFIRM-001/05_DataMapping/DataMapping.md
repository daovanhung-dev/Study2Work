# Data Mapping — ONB-CONFIRM-001

## 1. Aggregates / tables

`onboarding_sessions, onboarding_answers, learner_profiles, learning_path_recommendations`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| selectedPathId | selected_path_id | Input DTO → application command | Validate + normalize |
| confirmProfile | confirm_profile | Input DTO → application command | Validate + normalize |
| onboardingStatus | - | Read model / response DTO | Filter by scope before serialization |
| learnerProfile | - | Read model / response DTO | Filter by scope before serialization |
| eligibleToActivate | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Thao tác ghi chạy trong transaction; validate authorization và state transition trước khi commit.
- Có log sự kiện nghiệp vụ theo người dùng và traceId.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
