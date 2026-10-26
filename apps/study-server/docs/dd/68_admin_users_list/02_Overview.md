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
| Authorization | Shared role-aware guard yêu cầu claim ADMIN trước query; không có permission relation riêng trong checked-in DDL. |
| Success response | ApiEnvelope<Page<UserProfile>>; đồng bộ với list + pagination trong AC-31. |
| Direct errors | 401, 403, 422, 500 theo catalog đã đồng bộ; 422 dùng cho page sai. |
| Basis | Method/path/auth/query/status/success/errors DIRECT; filter normalization, page default/size, order và ADMIN-claim-to-user-management mapping DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | SOURCE_BACKED_WITH_DERIVED_CONTRACT — route/module/test được wire; query dùng legacy users candidate; live schema chưa xác minh. |
| Transaction | Read-only; view không commit. |
| Side effects | Không ghi dữ liệu; không đọc password_hash hoặc token credentials. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #68, UserProfile, Page và PageMeta.
- [AC/API index, AC-31](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có quyền user management; APIs #68–#72.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — danh sách, query + pagination, chọn user, nhánh thao tác rồi reload.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy users fields ở trạng thái design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT users query candidate; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — identity/profile/role UUID model khác legacy.
- [API #4 profile query/model](../../../app/modules/guest/api_04_users_me/query.py) và [model](../../../app/modules/guest/api_04_users_me/models.py) — safe projection và nullable fields hiện có.
- [API #07 source](../../../app/modules/guest/api_07_courses_search/view.py) — size 20, PageMeta và page validation precedent.
- [API #68 module](../../../app/modules/admin/api_68_admin_users_list/view.py) và [HTTP tests](../../../tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py) — current source/test evidence.

## Tables read

| Relation | Fields | Basis/status |
|---|---|---|
| Legacy users | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | Runtime query candidate from checked-in DB.sql; live schema unknown. |
| V1-PILOT identity_projections | UUID subject, account_status, email_verified, display_name | Different identity model; not joined to int64 users. |
| V1-PILOT learner_profiles | UUID subject, full_name, avatar_file_id, headline, bio, visibility, deleted_at | Different profile model; not joined to legacy users. |

## Tables write

Không có — API GET chỉ đọc.

## Mục chú ý

- Response Page<UserProfile> khớp list/pagination trong AC-31; catalog và node diagram API #68 hiện khai báo collection.
- Query nhận role/status/keyword/page; không thêm size hoặc sort input.
- Page mặc định 1, size cố định 20 theo precedent API #07; order ổn định users.id ASC.
- Role/status dùng exact equality, không whitelist enum vì UserRole/UserStatus chưa có member list.
- Keyword được trim/lowercase; POSITION tìm substring literal trên full_name hoặc email, không diễn giải %/_ thành wildcard.
- API #04 UserProfile là source model: bao gồm email/phone nullable, không có bio; không chọn password_hash.
- Empty result là items=[] và total=0 với HTTP 200. Page không hợp lệ trả 422 DESIGN_VALIDATION_ERROR theo precedent API #07.
- API #69 detail và #70/#71/#72 mutations giữ boundary riêng; #68 không đọc detail relation hoặc thực hiện thay đổi account.

## Assumptions

- Role ADMIN trong JWT được dùng làm quyền user-management vì AC-31 không cung cấp bảng permission/tenant trong checked-in source. Đây là fallback DERIVED.
- Legacy BIGINT users là query target phù hợp path/profile hiện tại; không khẳng định relation đang tồn tại live.
- Không có deletion column trong legacy users candidate, nên query không tự thêm deleted predicate; status filter là tùy chọn.
- PII email/phone được trả bởi reusable UserProfile sau ADMIN guard. Audit/visibility policy vẫn cần xác nhận.

## Conflicts

- Catalog trước đó ghi ApiEnvelope<UserProfile> dù diagram step nói query danh sách + pagination; catalog response đã được đồng bộ thành ApiEnvelope<Page<UserProfile>>.
- Catalog trước đó thiếu 422 cho page int32 invalid; 422 DESIGN_VALIDATION_ERROR đã được thêm dựa trên API #07.
- Legacy BIGINT users và V1-PILOT UUID identity/profile model khác nhau; live schema chưa xác minh.
- Catalog UserRole/UserStatus không liệt kê enum members; current API #04 model dùng string.
- UserProfile có bio optional nhưng current legacy/API #04 projection không có nguồn bio; API #68 bỏ field đó.
- Không có Admin permission relation hoặc deletion lifecycle column trong legacy users candidate.

## Security note

- Shared role-aware JWT guard yêu cầu ADMIN trước query count/page.
- Role claim là Admin permission fallback; separate user-management permission, tenant boundary và access audit chưa có source.
- Email và phone là PII trong reusable UserProfile; chỉ trả qua API Admin này.
- SQL chỉ lấy allowlist profile fields; không chọn password_hash, refresh_tokens hoặc token_hash.
- Logs và lỗi 500 không chứa query parameters hay profile data.

## Performance note

- Count và page dùng cùng filter predicates; list order là users.id ASC và size cố định 20.
- Keyword dùng LOWER + POSITION trên full_name/email; không đề xuất index/migration khi chưa có workload/schema owner.
- Hai SELECT chạy trong transaction do Session sở hữu; test không chứng minh live concurrency, schema hoặc query plan.

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
