---
title: "Overview"
order: 2
dd_id: "75"
api_name: "Cập nhật metadata khóa học Admin"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `#75` |
| Module | `ADMIN / SYSTEM MANAGEMENT — AC-32` |
| Method | `PUT` |
| Endpoint | `/api/v1/admin/courses/{course_id}` |
| Purpose | Admin cập nhật metadata của khóa học đã chọn. |
| Consumer/Actor | Admin có quyền course management |
| Authentication | Bearer JWT |
| Authorization | Runtime hiện gọi shared `validate_current_user_request(..., role="ADMIN")`; riêng permission course management chưa có policy source. |
| Direct request | `path{course_id:int64!}`; catalog/diagram không khai báo body hoặc query. |
| Proposed request | JSON full replacement gồm `title`, `description`, `thumbnail_url`, `price`; toàn bộ body là `DERIVED`. |
| Direct response | `ApiEnvelope<Page<Course>>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401, 403, 404, 422, 500 với đúng `DESIGN_*` code trong catalog. |
| Basis | Method/path/auth/path type/response/status/error set DIRECT; body, query/update projection, singleton Page và persistence là DERIVED hoặc SOURCE_REQUIRED. |
| Status | `Draft — Needs Confirmation` |
| Current runtime state | Route/module/test được wire locally; 27 focused HTTP tests pass. Fake DB không xác minh live schema/deployment. |
| Transaction | Current view UPDATE và SELECT projection trong cùng Session; commit sau khi mapping hợp lệ, rollback khi lỗi. Đây là fallback `DERIVED`. |
| Side effects | Cập nhật candidate metadata và `updated_at`; giữ nguyên status/mentor và không ghi audit trong API #75. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #75, `Course`, `Page`, `PageMeta`, `UserSummary`.
- [AC/API index, AC-32](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có quyền course management; nhóm APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #73 → #74 → nhánh #75/#76/#77 → reload.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy relations `courses`/`users`; design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT `courses`; live schema chưa xác minh.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `courses` và versioned `course_versions`, không tương đương API BIGINT.
- [API #70 Admin update](../70_admin_user_update/02_Overview.md) — precedent giữ body thiếu trong catalog thành proposal `DERIVED`.
- [API #73 Admin list](../73_admin_courses_list/02_Overview.md) và [API #74 Admin detail](../74_admin_course_detail/02_Overview.md) — Course projection, response Page và AC-32 boundary.
- [API #14 profile update source](../../../app/modules/guest/api_14_users_me_profile/) — transaction/update pattern; không phải Admin policy.
- [Current router](../../../app/api/v1.py), [API #75 view](../../../app/modules/admin/api_75_admin_course_update/view.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py) và [response helper](../../../app/core/responses.py) — runtime implementation boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope guideline.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `courses` | `id`, `mentor_id`, `name`, `description`, `thumbnail_url`, `price`, `status`, `updated_at` | DDL candidate; live schema chưa xác minh. |
| Legacy `users` | `id`, `full_name`, `avatar_url` | Candidate projection qua `courses.mentor_id`; required `Course.mentor` gặp nullable legacy FK. |
| V1-PILOT `courses` / `course_versions` | UUID owner/version fields | Schema model khác; không map vào API #75 BIGINT. |

## Tables write

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `courses` | `name`, `description`, `thumbnail_url`, `price`, `updated_at` | Candidate từ metadata proposal; physical mapping `DERIVED`, live schema chưa xác minh. |

## Mục chú ý

- Catalog và diagram không khai báo body; node chỉ ghi `UPDATE course metadata`. Đề xuất bốn field trong request là `DERIVED`, chưa phải contract được duyệt.
- `status` thuộc API #76; #75 không cập nhật trạng thái. AC-32 gắn audit log với nhánh #76, không thêm audit vào #75.
- `Course.mentor` là required nhưng legacy `courses.mentor_id` nullable; `Course.price` required nhưng legacy DDL không đánh dấu `price` NOT NULL.
- `Course.category` optional nhưng không có quan hệ course-category được xác nhận; proposal omit field. Diagram #74 nhắc counters nhưng response không khai báo counter.
- Direct output là `Page<Course>`; proposal trả một item và `PageMeta` 1/1/1/1 theo singleton pattern của #74.
- Legacy BIGINT DDL và V1-PILOT UUID/versioned model là hai nguồn khác nhau; live database chưa xác minh.
- Current source wire API #75 với shared ADMIN role guard, strict body model, SQL-only update constant và transaction-owning view. HTTP tests dùng fake DB; chúng không chứng minh live schema/deployment.

## Assumptions

- `title`, `description`, `thumbnail_url`, `price` là metadata editable candidate theo reusable `Course` và legacy columns; từng field là `DERIVED`.
- Runtime hiện yêu cầu đủ bốn key (full replacement), từ chối field lạ; `description` và `thumbnail_url` nhận null để xóa. Đây là fallback `DERIVED`, chờ owner xác nhận.
- Q1 candidate UPDATE theo `courses.id`, giữ nguyên `status`/`mentor_id`; Q2 candidate đọc updated Course + UserSummary.
- Response Page có đúng một item; `category` bị omit khi không có nguồn. Null serialization và mentor integrity cần owner xác nhận.
- UPDATE không trả row thì runtime trả 404; projection Q2 thiếu/sai hoặc commit lỗi trả 500 và rollback. Đây là fallback `DERIVED`; live transaction behavior chưa được xác minh.

## Conflicts

- Request body chưa có trong catalog/diagram, trong khi AC-32 nói “UPDATE course metadata”: body field/semantics là `DISCREPANCY` cần duyệt.
- Legacy schema dùng BIGINT `courses.id`; V1-PILOT dùng UUID `courses.id` và `course_versions`; live schema chưa được xác minh.
- Legacy DDL cho phép `mentor_id` và `price` NULL trong khi reusable `Course` yêu cầu mentor và price.
- Direct `ApiEnvelope<Page<Course>>` không xác định cardinality cho PUT-by-ID; singleton Page là `DERIVED` theo #74.
- API #74 hiện có shared `ADMIN` guard và dynamic route-template mapping; dedicated course-management permission policy vẫn chưa có source. `error_response` hiện trả `data:null`.

## Security note

- Chỉ Admin đã xác thực và có course-management permission mới được cập nhật course; claim/policy/guard mapping chưa có nguồn trong Study.
- Kiểm tra quyền trước khi truy vấn/ghi course; không dùng Student guard hiện tại thay cho Admin authorization.
- Không đưa email, phone, credential hoặc dữ liệu người học vào projection Course.
- Không trả kết quả course trước khi hoàn thành authorization.

## Performance note

- Candidate UPDATE được giới hạn theo `courses.id`; dự kiến một row, nhưng live key/index/query plan chưa được xác minh.
- Candidate response projection dùng một SELECT theo course ID với LEFT JOIN `users`; không thêm count/counter/category queries.
- Chưa có live query plan/latency evidence; local code dùng một UPDATE và một SELECT theo ID trong cùng transaction.
---
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
