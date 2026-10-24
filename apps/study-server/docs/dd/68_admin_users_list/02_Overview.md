---
title: "Overview"
order: 2
dd_id: "68"
api_name: "Lấy danh sách user"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #68 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Method | GET |
| Endpoint | /api/v1/admin/users |
| Purpose | Lấy danh sách user để Admin tra cứu và chọn user hoặc thao tác quản trị. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin và quyền user management theo catalog/AC-31; current Study chưa có Admin guard. |
| Basis | Method/path/auth/query/status/response/errors DIRECT; filter, pagination và Page response proposal DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route, module hoặc test API #68. |
| Transaction | N/A — chỉ đọc. |
| Side effects | Không ghi dữ liệu; không đọc password_hash. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #68, ApiEnvelope, UserProfile, Page, PageMeta.
- [AC/API index, AC-31](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có quyền user management; APIs #68–#72.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — danh sách, query + pagination, chọn user, nhánh thao tác rồi reload.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — legacy users fields và trạng thái DESIGN_ONLY.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — users fields, BIGSERIAL ID và quan hệ user_id 1:N.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT users; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — identity_projections, learner_profiles và service role tables dùng UUID; khác model legacy.
- [API #4 source query](../../../app/modules/guest/api_04_users_me/query.py) và [model](../../../app/modules/guest/api_04_users_me/models.py) — projection profile an toàn hiện có.
- [API #14 source query](../../../app/modules/guest/api_14_users_me_profile/query.py) — cùng projection sau cập nhật profile.
- [API #07 source](../../../app/modules/guest/api_07_courses_search/view.py) — page size cố định 20 và PageMeta là source precedent, không phải contract #68.

## Tables read

| Relation | Fields candidate | Basis/status |
|---|---|---|
| Legacy users | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | Candidate theo DB.sql, DB table guide và API #4/#14; live schema chưa xác minh. |
| V1-PILOT identity_projections | UUID subject, account_status, email_verified, display_name | Schema khác; không map trực tiếp vào UserProfile int64. |
| V1-PILOT learner_profiles | UUID subject, full_name, avatar_file_id, headline, bio, visibility, deleted_at | Schema khác; chưa có email/role trong profile row. |

## Tables write

Không có — API GET chỉ đọc.

## Mục chú ý

- Diagram mô tả danh sách và phân trang nhưng contract trực tiếp là ApiEnvelope<UserProfile>, không có items hoặc PageMeta.
- Query có page nhưng không có size/default/minimum. Page<UserProfile>, default page 1 và size 20 chỉ là proposal DERIVED.
- UserProfile có bio?; legacy users và current API #4 model không có bio source.
- Reusable UserProfile dùng UserRole/UserStatus nhưng catalog không liệt kê enum members; current API #4 model dùng str.
- Role/status value set và quy tắc xóa/ẩn user chưa được định nghĩa.

## Assumptions

- Q1/Q2 trên legacy users chỉ là query candidate, không phải runtime SQL đã duyệt.
- Candidate keyword tìm không phân biệt hoa thường trên full_name hoặc email; role/status dùng exact equality.
- Candidate page mặc định 1, size cố định 20 như precedent API #07; cần cập nhật catalog/response trước khi implement.

## Conflicts

- Catalog và diagram ghi response UserProfile trong khi AC-31 action là list/pagination.
- Legacy BIGINT users và V1-PILOT UUID identity/profile/role model không tương đương.
- Current Study profile model không có bio dù reusable UserProfile khai báo optional bio.
- Reusable schema dùng UserRole/UserStatus nhưng enum members chưa có; API #4 current model serialize strings.
- Catalog không liệt kê 422 cho page không hợp lệ; không tự thêm code/status.

## Security note

- Chỉ Admin đã xác thực và được cấp quyền user management mới được xem danh sách.
- Email và phone là PII trong UserProfile; cần xác nhận phạm vi hiển thị/audit theo chính sách Admin.
- Chỉ SELECT allowlist profile fields; tuyệt đối không lấy password_hash, refresh token, token hash hoặc credential.
- Admin identity/role guard hiện chưa có source trong Study.

## Performance note

- Candidate count và data query phải dùng cùng predicates.
- Keyword hai cột có thể cần index khi triển khai; không đề xuất migration/index khi chưa có workload/schema owner.
- Page size 20 và order id ASC là đề xuất DERIVED; không được xem là SLA hoặc catalog contract.

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
