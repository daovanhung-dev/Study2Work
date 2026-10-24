---
title: "Overview"
order: 2
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #70 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Method | PUT |
| Endpoint | /api/v1/admin/users/{user_id} |
| Purpose | Admin cập nhật thông tin/profile và role của user. |
| Consumer/Actor | Admin có quyền quản lý user theo precondition AC-31. |
| Authentication | Bearer JWT |
| Authorization | Role Admin; permission user-management theo AC-31. Current Study chưa có Admin guard/policy. |
| Direct request | `path{user_id:int64!}`; body chưa đặc tả. |
| Direct response | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401, 403, 404, 422, 500 với mã trong catalog. |
| Basis | Method/path/auth/path type/response/status/error set DIRECT; body/query/mutation mapping DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — route, module và focused test chưa có. |
| Transaction | Candidate transaction theo API #14 precedent; ownership chưa có source cho #70. |
| Side effects | Candidate cập nhật user/profile/role. Audit và token/session effects chưa được định nghĩa. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #70, ApiEnvelope, UserProfile, UserRole và UserStatus.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — Admin update user/profile, sau đó reload list/detail.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT users candidate; không phải live-schema evidence.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID-oriented identity/profile/role relations khác legacy users.
- [API #14 source](../../../app/modules/guest/api_14_users_me_profile/query.py) — hiện update full_name, phone, avatar_url, updated_at; không update role/bio.
- [API #14 validation](../../../app/modules/guest/api_14_users_me_profile/validate.py) — Student guard và profile normalization hiện tại; không phải Admin policy.
- [Current auth helper](../../../app/utils/auth.py) — `validate_current_user_request` hiện yêu cầu Student.
- [API #68 Overview](../68_admin_users_list/02_Overview.md) và [API #69 Overview](../69_admin_user_detail/02_Overview.md) — cùng AC-31; response/list discrepancies giữ riêng.

## Tables read

| Relation | Fields candidate | Basis/status |
|---|---|---|
| Legacy users | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | Candidate theo DDL và API #14 projection; live schema chưa xác minh; không có bio. |
| V1-PILOT identity/profile/role relations | UUID subject, account/profile fields, service roles/permissions | Mô hình khác; không map trực tiếp sang int64 UserProfile; không JOIN ngầm. |

## Tables write

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy users | full_name, phone, avatar_url, role, updated_at | `DERIVED CANDIDATE` từ intent #70, API #14 precedent và legacy DDL; body/schema chưa được duyệt. |

## Mục chú ý

- Catalog và diagram không khai báo body schema; không hiểu path-only notation là bằng chứng API không nhận body.
- Tên API/AC-31 cho phép suy ra role thuộc intent; exact writable fields và PUT replacement semantics vẫn cần xác nhận.
- Status thuộc API #71; không cập nhật status trong #70.
- UserProfile.bio không có cột trong legacy users hoặc trong API #14 query hiện tại.
- UserRole/UserStatus là named types; enum members chưa được định nghĩa.
- Email/phone là PII; response chỉ được cấp sau khi policy Admin phù hợp được xác nhận.

## Candidate mapping — DERIVED

Candidate full-replacement body: `full_name`, `phone`, `avatar_url`, `role`. Candidate SQL có thể cập nhật bốn trường đó và `updated_at`, lọc theo `users.id`, rồi `RETURNING` safe UserProfile fields. Từng quyết định body requiredness/nullability, role policy, live table, audit và transaction cần xác nhận trước implementation.

## Conflicts

- API #70 catalog/diagram không liệt kê body, trong khi tên và AC-31 nói update user/profile/role: body là `SOURCE_REQUIRED`; candidate fields chỉ mang nhãn `DERIVED`.
- UserProfile có `bio?`, nhưng legacy DDL/API #14 không có nguồn bio: không persist hoặc tạo giá trị bio.
- Legacy DDL dùng BIGINT users; V1-PILOT dùng UUID projections/roles: không trộn hai mô hình.
- API #68 list response và #69 detail/list intent có discrepancy riêng; không giải quyết trong #70.

## Security note

- Xác thực và kiểm tra Admin/user-management permission trước khi đọc hoặc ghi user row.
- Current helper chỉ cấp Student; không tái sử dụng guard đó cho API Admin.
- Không đọc/trả password_hash; email/phone cần PII policy phù hợp.
- Diagram không yêu cầu revoke session ở #70; không tự thêm side effect đó.

## Performance note

Candidate UPDATE theo primary key `users.id` dự kiến một row; primary-key/index behavior phải xác minh trên live schema. Không có pagination hoặc bulk mutation trong contract #70.

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
