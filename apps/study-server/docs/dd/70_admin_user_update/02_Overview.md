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
| Authorization | Shared JWT guard yêu cầu claim `ADMIN`; mapping này theo fallback #68/#69. Permission/tenant/MFA policy riêng chưa có nguồn. |
| Direct request | `path{user_id:int64!}`; catalog/diagram không khai báo body. |
| Runtime request fallback | JSON full-replacement: required `full_name:string`, `phone:string|null`, `avatar_url:string|null`, `role:STUDENT\|MENTOR\|ADMIN`; extra fields bị từ chối. `DERIVED`. |
| Direct response | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401, 403, 404, 422, 500 với mã trong catalog. |
| Basis | Method/path/auth/path type/response/status/error set DIRECT; body/query/mutation mapping DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | Route/module/focused HTTP tests được wire local; live schema/deployment chưa xác minh. |
| Transaction | `view.py` sở hữu UPDATE, commit sau khi map response hợp lệ và rollback no-row/query/mapping/commit failure; pattern theo API #14. |
| Side effects | Cập nhật full_name, phone, avatar_url, role, updated_at. Giữ email/status; không audit hoặc revoke session. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #70, ApiEnvelope, UserProfile, UserRole và UserStatus.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — Admin update user/profile, sau đó reload list/detail.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT users candidate; không phải live-schema evidence.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID-oriented identity/profile/role relations khác legacy users.
- [API #14 source](../../../app/modules/guest/api_14_users_me_profile/query.py) — hiện update full_name, phone, avatar_url, updated_at; không update role/bio.
- [API #14 validation](../../../app/modules/guest/api_14_users_me_profile/validate.py) — Student guard và profile normalization hiện tại; không phải Admin policy.
- [Current auth helper](../../../app/utils/auth.py) — `validate_current_user_request` hiện yêu cầu Student.
- [API #68 Overview](../68_admin_users_list/02_Overview.md) và [API #69 Overview](../69_admin_user_detail/02_Overview.md) — cùng AC-31; #68 là list `Page<UserProfile>`, #69 là detail và #70 là mutation.

## Tables read

| Relation | Fields candidate | Basis/status |
|---|---|---|
| Legacy users | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | Candidate theo DDL và API #14 projection; live schema chưa xác minh; không có bio. |
| V1-PILOT identity/profile/role relations | UUID subject, account/profile fields, service roles/permissions | Mô hình khác; không map trực tiếp sang int64 UserProfile; không JOIN ngầm. |

## Tables write

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy users | full_name, phone, avatar_url, role, updated_at | Runtime fallback `DERIVED` từ intent #70, API #14 precedent và checked-in legacy DDL; live schema chưa xác minh. |

## Mục chú ý

- Catalog và diagram không khai báo body schema; runtime dùng fallback body để làm rõ thao tác PUT.
- Fallback yêu cầu đủ bốn field; nullable `phone`/`avatar_url` được trim và chuỗi trắng thành null; `full_name` dùng API #14 rules.
- Role fallback giới hạn `STUDENT`, `MENTOR`, `ADMIN`, là các nhãn hiện được dùng trong source; enum/transition policy vẫn cần owner xác nhận.
- Status thuộc API #71; không cập nhật status trong #70.
- UserProfile.bio không có cột trong legacy users hoặc trong API #14 query hiện tại.
- UserRole/UserStatus là named types; enum members chưa được định nghĩa.
- Email/phone là PII; runtime trả theo `UserProfile` sau ADMIN claim; masking, audit và field-level policy còn mở.

## Candidate mapping — DERIVED

Runtime full-replacement body: `full_name`, `phone`, `avatar_url`, `role`. SQL cập nhật bốn trường và `updated_at`, lọc theo `users.id`, rồi `RETURNING` safe UserProfile fields. Các quyết định body/role/schema là fallback `DERIVED`; permission policy, live table, audit/PII và token effect vẫn cần xác nhận.

## Conflicts

- API #70 catalog/diagram không liệt kê body, trong khi tên và AC-31 nói update user/profile/role: runtime chọn body full-replacement là `DERIVED`; client phải dùng schema OpenAPI hiện tại.
- UserProfile có `bio?`, nhưng legacy DDL/API #14 không có nguồn bio: không persist hoặc tạo giá trị bio.
- Legacy DDL dùng BIGINT users; V1-PILOT dùng UUID projections/roles: không trộn hai mô hình.
- API #68 list contract đã đồng bộ thành `Page<UserProfile>`; API #69 detail và #70 mutation giữ scope riêng.

## Security note

- Xác thực và kiểm tra Admin/user-management permission trước khi đọc hoặc ghi user row.
- Shared ADMIN guard chạy trước path parsing và DB access; permission/tenant/MFA mapping riêng chưa được chứng minh.
- Không đọc/trả password_hash; email/phone cần PII policy phù hợp.
- Diagram không yêu cầu revoke session ở #70; không tự thêm side effect đó.

## Performance note

UPDATE theo primary key `users.id` dự kiến một row; primary-key/index behavior phải xác minh trên live schema. Không có pagination hoặc bulk mutation trong contract #70.

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
