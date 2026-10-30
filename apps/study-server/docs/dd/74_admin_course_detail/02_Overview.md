---
title: "Overview"
order: 2
dd_id: "74"
api_name: "Lấy chi tiết course quản trị"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `#74` |
| Module | `ADMIN / SYSTEM MANAGEMENT — AC-32` |
| Method | `GET` |
| Endpoint | `/api/v1/admin/courses/{course_id}` |
| Purpose | Admin đọc thông tin khóa học đã chọn trước khi cập nhật nội dung, đổi trạng thái hoặc xóa theo policy. |
| Consumer/Actor | Admin có quyền course management |
| Authentication | Bearer JWT |
| Authorization | Shared JWT guard yêu cầu role `ADMIN`; dedicated course-management permission chưa có policy source và chưa được kiểm tra riêng. |
| Direct response | `ApiEnvelope<Page<Course>>` |
| Basis | Method/path/auth/path/response/status/errors DIRECT; truy vấn, page singleton và status visibility DERIVED; counter mapping chưa có nguồn. |
| Status | `Draft — Needs Confirmation` |
| Current local source state | `VERIFIED_LOCAL_SOURCE` — route, module, middleware route-template mapping và focused tests đã có; live DB/deployment chưa xác minh. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không ghi dữ liệu. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #74, `ApiEnvelope`, `Page`, `PageMeta`, `Course`, `UserSummary`.
- [AC/API index, AC-32](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có quyền course management; luồng APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #73 → #74 đọc course/owner/counters → chọn #75/#76/#77 → reload danh sách.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — quan hệ legacy `courses`/`users`; mapping được ghi `DESIGN_ONLY`.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT `courses`/`users`; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `courses` và versioned `course_versions`, khác API contract BIGINT.
- [API #08 query/view/model](../../../app/modules/guest/api_08_courses_detail/) và [shared Course mapping](../../../app/modules/guest/_shared/course_catalog/) — current single-course projection/Page precedent; API #08 chỉ public `PUBLISHED`.
- [API #08 tests](../../../tests/modules/guest/api_08_courses_detail/test_courses_detail.py) — current source precedent cho invalid/missing detail, query/mapping errors và singleton Page; không chạy trong task này.
- [API #06 shared Course mapping](../../../app/modules/guest/_shared/course_catalog/helpers.py) — decimal-string price và required mentor mapping.
- [API #69 Admin detail DD](../69_admin_user_detail/02_Overview.md) và [API #73 Admin list DD](../73_admin_courses_list/02_Overview.md) — Admin authorization boundary, Course field mapping và AC-32 continuity.
- [Current auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [error response](../../../app/core/responses.py) — shared role-aware JWT guard, FastAPI route-template allowlist matching và lỗi mặc định `data:null`.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — chuẩn lỗi yêu cầu `data:null`.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `courses` | `id`, `mentor_id`, `name`, `description`, `thumbnail_url`, `price`, `status` | Candidate theo DDL và API #06/#08 source; live schema chưa xác minh. |
| Legacy `users` | `id`, `full_name`, `avatar_url` | Candidate `Course.mentor` projection qua `courses.mentor_id`; chỉ lấy UserSummary. |
| V1-PILOT `courses`/`course_versions` | UUID owner/version relations | Mô hình khác; không map sang Course BIGINT contract. |

## Tables write

Không có — API GET chỉ đọc.

## Mục chú ý

- Catalog và diagram khai báo `ApiEnvelope<Page<Course>>` cho detail path; giữ nguyên contract và đề xuất Page một phần tử theo precedent API #08.
- AC-32 yêu cầu đọc course, owner và counters; response `Course` không khai báo counter. Không tạo field, `meta` counter hoặc aggregate query khi chưa có contract.
- Admin quản lý nhiều trạng thái qua #73/#76; không áp dụng filter `PUBLISHED` của API #08.
- `Course.category` optional nhưng legacy schema không có quan hệ course-category; proposal là omit field.
- `Course.mentor` bắt buộc nhưng legacy DDL cho phép `mentor_id` NULL; API #08 hiện coi thiếu mentor là lỗi toàn vẹn 500.
- CourseStatus enum members/casing chưa thống nhất; #76 nêu `draft/published/suspended`, legacy/API #08 dùng `DRAFT`/`PUBLISHED`.

## Assumptions

- Q1 đọc một row theo `courses.id`, dùng LEFT JOIN `users` để map owner; query/schema là candidate, không phải live-schema claim.
- Page detail được tạo từ một course: `items` có đúng một phần tử và `pagination={page:1,size:1,total:1,total_pages:1}`. Đây là `DERIVED` từ direct Page contract và API #08 precedent.
- Không lọc status; Admin có thể đọc course ở mọi trạng thái để tiếp tục nhánh update/status/delete của AC-32. Đây là `DERIVED` từ workflow.
- Course thiếu mentor hoặc price bắt buộc được candidate ánh xạ 500 `DESIGN_INTERNAL_ERROR` theo API #06/#08 mapping precedent; cần xác nhận với chủ sở hữu dữ liệu.
- Invalid path ID có thể ánh xạ 404 như API #08 vì catalog #74 không có 422; không tự thêm minimum hoặc rule ngoài int64.
- Nullable description/thumbnail/mentor avatar được candidate serialize thành `null` theo model #08; contract null-vs-omit cần chốt.

## Conflicts

- AC-32 diagram nói đọc “counters”, nhưng API #74 response schema không có field counter.
- `courses.mentor_id` được DB guide mô tả required nhưng legacy `DB.sql` cho phép NULL.
- Legacy BIGINT schema và V1-PILOT UUID/versioned schema không tương đương; live DB chưa xác minh.
- `ApiEnvelope<Page<Course>>` dùng cho detail path; API #08 có singleton Page precedent nhưng vẫn cần xác nhận wrapper chung ở macro-review.
- Shared guard kiểm tra role `ADMIN`, nhưng không có dedicated course-management permission policy. Middleware nhận diện route template qua `request.scope.route.path`; helper lỗi hiện dùng `data:null`.

## Security note

- Local fallback chỉ yêu cầu JWT role `ADMIN` trước khi parse ID hoặc truy vấn course; không khẳng định đã enforce dedicated course-management permission.
- Current Student guard không thay thế Admin guard; nguồn claim/permission chưa xác định.
- Query chỉ lấy `Course` và `UserSummary`; không đọc email, phone, password hash, token hoặc dữ liệu học viên.
- Không trả course existence trước bước authorization.

## Performance note

- Q1 giới hạn theo khóa `courses.id` và đọc tối đa một row.
- LEFT JOIN chỉ lấy ba field `UserSummary`; không cần count query cho contract hiện tại.
- Counter yêu cầu trong diagram chưa có định nghĩa/đích response; không truy vấn thêm đến khi được chốt.
- Index/live query plan chưa được xác minh.
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
