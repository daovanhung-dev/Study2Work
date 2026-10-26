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
| Authorization | Shared JWT guard yêu cầu claim ADMIN trước DB; ánh xạ claim này thành quyền user management là fallback DERIVED giống API #68. |
| Direct response | ApiEnvelope<UserProfile> |
| Basis | Method/path/auth/path type/status/response/errors DIRECT; legacy query, ADMIN-claim mapping, invalid-path 404 và no-row 404 là DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | SOURCE_BACKED_WITH_DERIVED_MAPPING — route/module/test được wire; legacy target và path/no-row mappings là DERIVED. |
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
- [Current auth helper](../../../app/utils/auth.py) — role-aware shared guard; API #68 dùng `role="ADMIN"` trước DB access.
- [API #68 Overview/Response](../68_admin_users_list/02_Overview.md) và [Response](../68_admin_users_list/04_Response.md) — API #68 hiện trả `Page<UserProfile>`; API #69 vẫn là detail đơn.

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
- AC-31 yêu cầu Admin đăng nhập và có quyền user management. Runtime dùng shared role-aware guard với claim `ADMIN`, nhất quán API #68; permission relation riêng/tenant/MFA policy không có source.
- Legacy users là nguồn candidate; DDL/schema artifact không chứng minh relation tồn tại trong live DB.
- UserProfile.bio là optional nhưng không có cột trong legacy users hoặc field trong API #4/#14 projection; runtime omit field này thay vì ghép UUID pilot profile.
- UserRole và UserStatus không có danh sách enum members trong catalog; source profile model dùng string.
- Email và phone là PII; chỉ được đọc/trả sau khi Admin được xác thực và có quyền.

## Runtime mapping — legacy candidate, DERIVED

Q1 đọc một row theo `users.id = :user_id` và chỉ lấy profile allowlist hiện có trong API #04/#14. Runtime dùng shared `ADMIN` guard trước lookup, malformed/out-of-int64 path và no-row đều trả 404 theo error set catalog. Query target và hai nhánh 404 vẫn là DERIVED; live schema chưa xác minh.

## Conflicts

- Legacy schema dùng BIGINT users; V1-PILOT dùng UUID identity/profile/role relations và không cùng một UserProfile projection.
- Reusable UserProfile có bio?, nhưng legacy users và current API #4/#14 source không có bio.
- Catalog dùng UserRole/UserStatus nhưng không định nghĩa enum members.
- Shared guard có thể yêu cầu claim `ADMIN`; policy riêng ngoài claim này chưa có source.
- `error_response` hiện serialize data vắng mặt thành JSON null; runtime API #69 giữ convention đó.
- API #68 list/pagination đã được đồng bộ riêng trong catalog và diagram; API #69 giữ contract detail `UserProfile`.

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
