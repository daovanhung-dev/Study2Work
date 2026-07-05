# Data Mapping — COM-ADMIN-UPDATE-001

## 1. Aggregates / tables

`community_groups, community_group_scopes, community_link_open_logs, community_reports, moderation_actions`

## 2. Field mapping

| API field | Persistence / projection | Application handling | Rule |
| --- | --- | --- | --- |
| name | name | Input DTO → application command | Validate + normalize |
| description | description | Input DTO → application command | Validate + normalize |
| externalUrl | external_url | Input DTO → application command | Validate + normalize |
| scopeType | scope_type | Input DTO → application command | Validate + normalize |
| scopeId | scope_id | Input DTO → application command | Validate + normalize |
| status | status | Input DTO → application command | Validate + normalize |
| reason | reason | Input DTO → application command | Validate + normalize |
| id | - | Read model / response DTO | Filter by scope before serialization |
| updatedAt | - | Read model / response DTO | Filter by scope before serialization |


## 3. Persistence behavior

- Thao tác ghi chạy trong transaction; validate authorization và state transition trước khi commit.
- Có. Hành động admin hoặc thay đổi quyền/nội dung/ngoại lệ phải ghi `actor`, `action`, `reason`, `before`, `after`.
- Sensitive values phải được masking/encryption/hashing theo loại dữ liệu.
- Đồng thời ghi `traceId`, actor và source context vào observability metadata khi phù hợp.

## 4. Side effects

- Có thể phát domain event để cập nhật notification, progress projection, report snapshot hoặc audit pipeline.
- Side effect bất đồng bộ phải idempotent và không làm thay đổi response contract đã trả về.
