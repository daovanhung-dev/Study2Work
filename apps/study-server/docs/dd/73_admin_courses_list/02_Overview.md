---
title: "Overview"
order: 2
dd_id: "73"
api_name: "Lấy danh sách khóa học Admin"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #73 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-32 |
| Method | GET |
| Endpoint | `/api/v1/admin/courses` |
| Purpose | Admin tra cứu và chọn khóa học cần xem hoặc quản lý. |
| Consumer/Actor | Admin có quyền course management |
| Authentication | Bearer JWT |
| Authorization | Shared JWT role `ADMIN`; quyền course-management riêng trong AC-32 chưa có source check. |
| Basis | Method/path/query/response/status/errors DIRECT; filter semantics và pagination DERIVED có đánh dấu. |
| Status | Draft — Needs Confirmation |
| Current runtime state | `SOURCE_BACKED_LOCAL` — route/module/focused tests tồn tại; fake DB không chứng minh live schema hoặc deployment. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không ghi dữ liệu. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #73, `Course`, `Page`, `PageMeta`, `ApiEnvelope`.
- [AC/API index, AC-32](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có quyền course management; APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — mở danh sách, query courses, mở detail, chọn update/status/delete rồi reload.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT `courses`, `users`, `categories`.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — versioned course model dùng UUID.
- [API #06 source](../../../app/modules/guest/api_06_courses/) — current `CoursePage`, `PageMeta`, mentor projection và decimal price conversion; public-only behavior không áp dụng cho #73.
- [API #06 tests](../../../tests/modules/guest/api_06_courses/test_courses.py) — source precedent cho page default, empty page, category gap và mentor integrity.
- [API #73 tests](../../../tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py) — local HTTP/OpenAPI tests với fake DB; không xác minh schema live.
- [API #68 Admin list DD](../68_admin_users_list/02_Overview.md) — proposal pagination và authorization boundary cho Admin.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `courses` | `id`, `mentor_id`, `name`, `description`, `thumbnail_url`, `price`, `status` | DDL artifact; live schema chưa xác minh. |
| Legacy `users` | `id`, `full_name`, `avatar_url` | Candidate `Course.mentor` projection qua `courses.mentor_id`. |
| Legacy `categories` | `id`, `name`, `slug`, `description` | Bảng có tồn tại nhưng không có relation source-backed tới `courses`. |
| V1-PILOT `courses`/`course_versions` | UUID owner/version model | Khác identifier và data contract; không map sang API BIGINT. |

## Tables write

Không có — API GET chỉ đọc.

## Mục chú ý

- API #73 contract trực tiếp đã trả `ApiEnvelope<Page<Course>>`; đây không phải discrepancy cardinality như API #68.
- Query có `page` nhưng không có `size` hoặc `sort`; `PageMeta` lại yêu cầu `size`. Proposal là page 1-based mặc định 1, size cố định 20 và thứ tự `courses.id ASC`, cần owner xác nhận.
- Admin list không áp dụng predicate `PUBLISHED` của API #06; khi không truyền status, proposal là không lọc status để quản lý mọi lifecycle.
- Catalog khai báo filter `category`, nhưng legacy/pilot DDL không có quan hệ course-category; API #06 từ chối category. API #73 dùng cùng pattern và trả 422 `DESIGN_VALIDATION_ERROR` cho category int64 hợp lệ trước DB; đây là fallback `DERIVED`, không phải behavior catalog-approved.
- Catalog `Course.category` là optional; reusable runtime `Course` model hiện không khai báo field đó nên response omit field này. `Course.mentor` required trong khi legacy `courses.mentor_id` nullable; runtime phát hiện missing mentor qua count và trả safe 500 theo precedent #06.
- `CourseStatus` enum members/casing chưa có contract thống nhất; #76 ghi draft/published/suspended, legacy/API #06 có `DRAFT`/`PUBLISHED`.

## Assumptions

- Status, mentor và category dùng equality khi được truyền; không chuẩn hóa hoặc tự tạo whitelist status. Đây là semantics proposal `DERIVED`.
- Không có status filter thì lấy mọi status có trong nguồn; không dùng `PUBLISHED` mặc định.
- `page` mặc định 1; fixed size 20 theo API #06 và proposal API #68; empty/out-of-range page trả 200 theo API #06 precedent.
- Order mặc định `courses.id ASC` để pagination ổn định; catalog không có sort query.
- Nếu course thiếu mentor, candidate trả safe `500 DESIGN_INTERNAL_ERROR` theo API #06 integrity rule thay vì bịa UserSummary; cần owner xác nhận ảnh hưởng tới khả năng Admin sửa dữ liệu mồ côi.
- Category request hợp lệ bị từ chối bằng 422 trước DB; khi chưa có category, query chỉ dùng status/mentor.

## Conflicts

- Legacy schema BIGINT và V1-PILOT UUID/versioned course model không tương đương; live DB chưa xác minh.
- Legacy `courses` không có category FK, API #73 vẫn khai báo category filter và Course schema có category optional.
- Status filter là string nhưng CourseStatus enum/casing chưa liệt kê; catalog #76 và DDL/runtime có biểu diễn khác nhau.
- Runtime dùng shared `ADMIN` guard và middleware contract-path mapping; không kiểm tra permission course-management riêng. `error_response` hiện serialize `data:null`.
- API #74 cùng AC-32 khai báo `ApiEnvelope<Page<Course>>` cho endpoint detail; cần rà macro nhóm #73–#77, không sửa contract trong DD #73.

## Security note

- Runtime chỉ xác minh JWT role `ADMIN` qua shared guard. Mapping role này sang AC-32 course-management permission là fallback `DERIVED`; nguồn permission/scope riêng vẫn cần owner xác nhận.
- Query chỉ lấy Course fields và `UserSummary`; không chọn email, phone, password hash, token hoặc PII khác.
- Category relation gap không được giải quyết bằng JOIN tùy ý.

## Performance note

- Q1 page query và Q2 count query phải dùng cùng filter predicates.
- Chỉ dùng bound parameters cho status, mentor, limit/offset; category bị từ chối trước query và không được nội suy vào SQL.
- `courses.id ASC` là default order proposal; index/workload chưa được xác minh.
- Page size 20 là proposal, không phải catalog SLA hoặc runtime setting.

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
