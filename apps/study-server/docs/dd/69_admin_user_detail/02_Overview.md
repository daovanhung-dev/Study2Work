---
title: "Overview"
order: 2
dd_id: "69"
api_name: "Lấy chi tiết user"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #69 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Method | GET |
| Endpoint | /api/v1/admin/users/{user_id} |
| Purpose | Đọc chi tiết một user đã được Admin chọn. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin và quyền user management theo catalog/AC-31; current Study chưa có Admin guard. |
| Direct response | ApiEnvelope<UserProfile> |
| Basis | Method/path/auth/path type/status/response/errors DIRECT; query và no-row branch là candidate DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route, module hoặc test API #69. |
| Transaction | N/A — chỉ đọc. |
| Side effects | Không ghi dữ liệu; không đọc password_hash. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #69, ApiEnvelope, UserProfile.
- [AC/API index, AC-31](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin đăng nhập, có quyền user management; flow gồm #68–#72.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — chọn user → GET detail → đọc user/profile/role → chọn update/status/delete.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy users fields, được đánh dấu design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT users; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID identity/profile/role relations khác model legacy.
- [API #4 profile query/model](../../../app/modules/guest/api_04_users_me/query.py) — safe projection hiện có; bio không được chọn.
- [API #14 profile query](../../../app/modules/guest/api_14_users_me_profile/query.py) — fields trả về sau cập nhật profile.
- [Current auth helper](../../../app/utils/auth.py) — guard hiện tại yêu cầu Student; không có Admin guard.
- [API #68 Overview/Response](../68_admin_users_list/02_Overview.md) và [Response](../68_admin_users_list/04_Response.md) — phần list/pagination mismatch giữ riêng ở #68.

## Tables read

| Relation | Fields candidate | Basis/status |
|---|---|---|
| Legacy users | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | Candidate theo DB.sql và API #4/#14; không có bio; live schema chưa xác minh. |
| V1-PILOT identity_projections | UUID subject, account_status, email_verified, display_name | Mô hình khác; không map trực tiếp sang UserProfile int64. |
| V1-PILOT learner_profiles | UUID subject, full_name, avatar_file_id, headline, bio, deleted_at | Không có email/role trong profile row; không được nối ngầm với legacy users. |

## Tables write

Không có — API GET chỉ đọc.

## Mục chú ý

- Catalog và diagram cùng mô tả một user detail với ApiEnvelope<UserProfile>; API #69 không có pagination.
- AC-31 yêu cầu Admin đăng nhập và có quyền user management; Study hiện chỉ có shared Student guard.
- Legacy users là nguồn candidate; DDL/schema artifact không chứng minh relation tồn tại trong live DB.
- UserProfile.bio là optional nhưng không có cột trong legacy users hoặc field trong API #4/#14 projection.
- UserRole và UserStatus không có danh sách enum members trong catalog; source profile model dùng string.
- Email và phone là PII; chỉ được đọc/trả sau khi Admin được xác thực và có quyền.

## Candidate mapping — DERIVED

Candidate Q1 đọc một row theo users.id = :user_id và chỉ lấy profile allowlist hiện có trong API #4/#14. Nếu không có row, ánh xạ sang 404 là đề xuất phù hợp với detail resource contract. Cả query lẫn nhánh này đều chưa chạy trong API #69.

## Conflicts

- Legacy schema dùng BIGINT users; V1-PILOT dùng UUID identity/profile/role relations và không cùng một UserProfile projection.
- Reusable UserProfile có bio?, nhưng legacy users và current API #4/#14 source không có bio.
- Catalog dùng UserRole/UserStatus nhưng không định nghĩa enum members.
- Current Student-only guard không thực hiện authorization Admin theo AC-31.
- Error guideline yêu cầu data null; current helper thay data vắng mặt bằng {}.
- API #68 list vẫn có discrepancy list/pagination; API #69 direct detail response không tự sửa contract của #68.

## Security note

- Không đọc profile trước khi hoàn tất xác thực và authorization Admin.
- Email và phone là PII; giới hạn truy cập theo quyền user management và xác nhận audit policy trước implementation.
- Chỉ SELECT field allowlist; tuyệt đối không lấy password_hash, refresh token, token hash hoặc credential.
- Không log token, email, phone hoặc payload profile.

## Performance note

- Query candidate giới hạn tối đa một row bằng khóa id.
- Không cần count, pagination hay join cho contract detail.
- Index availability và live query plan chưa được xác minh.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
