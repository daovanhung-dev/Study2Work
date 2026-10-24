---
title: "Overview"
order: 2
dd_id: "82"
api_name: "Lấy danh sách lesson"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #82 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-34 |
| Method | GET |
| Endpoint | `/api/v1/admin/lessons` |
| Purpose | Admin tra cứu lesson để chọn lesson cần xem hoặc quản lý. |
| Consumer/Actor | Admin có quyền quản lý bài học |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog và quyền lesson management theo tiền điều kiện AC-34; guard/policy hiện chưa có trong Study source. |
| Basis | Method/path/query/response/status/errors DIRECT; filter, collection shape, order và empty result là DERIVED hoặc cần xác nhận. |
| Status | Draft — Needs Confirmation |
| Current implementation | `UNWIRED / NOT_FOUND`: không có route, module hoặc test API #82 trong current source. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không ghi dữ liệu; các thao tác detail/update/status/delete thuộc API #83–#86. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #82, `Lesson`, `ApiEnvelope<T>`, business codes.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, permission precondition và nhóm API #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — Admin mở lesson management, query danh sách, chọn thao tác tiếp theo và reload.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT table `lessons`.
- [Study schema tables](../../diagrams/DB_UNICA_TABLES.md) and [ERD](../../diagrams/DB_UNICA_ERD.drawio) — design artifacts, chưa chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — model UUID/versioned khác contract BIGINT.
- [API #09 Lesson model/query/view](../../../app/modules/guest/api_09_courses_curriculum/) — precedent map field công khai; predicate `PUBLISHED` không được chuyển sang Admin list.
- [API #73 Admin list DD](../73_admin_courses_list/02_Overview.md) and [API #78 queue DD](../78_admin_content_pending/02_Overview.md) — precedent ghi rõ mismatch list và response singleton.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `lessons` | `id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status` | Candidate BIGINT DDL; `name -> title`, `sort_order -> order`; live schema chưa xác minh. |
| V1-PILOT `lessons` | UUID `id`, `chapter_id`, `course_version_id`, `title`, `summary`, `position`, `estimated_minutes`, `is_preview` | Khác ID và response fields; không map trực tiếp sang `Lesson` BIGINT. |
| `resources`, `lesson_progress` | References to lesson | Diagram relations only; không cần join cho response #82. |

## Tables write

Không có — GET chỉ đọc.

## Mục chú ý

- Catalog khai báo response `ApiEnvelope<Lesson>` (một object), trong khi tên API và AC-34 mô tả lấy danh sách. Đây là `DISCREPANCY`. DD giữ contract trực tiếp và chỉ đề xuất `ApiEnvelope<Lesson[]>` như phương án cần owner xác nhận; không tự chuyển thành `Page<Lesson>`.
- Query `course`, `status`, `type` là các field trực tiếp. Exact-match `course`/`status` là semantics `DERIVED`; legacy DDL không có cột `type` cho Lesson nên filter đó là `SOURCE_REQUIRED`.
- Không thêm `page`, `size`, `sort` vì catalog không khai báo. Pagination và collection limit chưa được đặc tả.
- Admin list không dùng predicate `PUBLISHED` của API #09; khi không có `status`, proposal là không lọc trạng thái để Admin thấy mọi trạng thái.
- API #86 có proposal soft-delete nhưng chưa có deletion marker hoặc visibility policy được chọn. #82 không tự kết luận lesson đã xóa sẽ được đưa vào hay loại khỏi danh sách.
- Legacy DDL cho phép `course_id` NULL nhưng reusable `Lesson.course_id` bắt buộc; live schema chưa xác minh.
- LessonStatus members/casing chưa được liệt kê đầy đủ; không tự tạo enum hoặc validation whitelist.

## Assumptions

- `course` và `status` dùng exact equality nếu được truyền; vắng mặt thì không thêm predicate tương ứng. Đây là `DERIVED`, cần xác nhận.
- Candidate stable order cho list: `course_id ASC, sort_order ASC, id ASC`; không có order contract trực tiếp.
- Nếu collection được duyệt, kết quả rỗng dự kiến trả 200 với `data: []`; đây là proposal, không diễn đạt được bằng response singleton hiện tại.
- Query `type` phải chờ nguồn field/relation và quy tắc so khớp; không bỏ qua âm thầm.

## Conflicts

- Catalog response singleton đối lập với list intent từ tên/AC-34.
- Legacy BIGINT schema và V1-PILOT UUID/versioned model không tương đương; live database chưa kiểm chứng.
- `course_id` nullable trong legacy DDL nhưng required trong reusable `Lesson` schema.
- Có query `type` nhưng không có Lesson type trong reusable schema/DDL đã kiểm tra.
- Admin guard/permission source chưa tồn tại trong Study source. Middleware hiện tại không allowlist API #82 và không chứng minh catalog error codes.
- Current helper có thể serialize `data={}` cho lỗi, trong khi API guideline chỉ định `data:null` cho error; phải thống nhất khi tích hợp.

## Security note

- Chỉ principal có Bearer JWT hợp lệ, role Admin và lesson-management permission mới được đọc dữ liệu.
- Authorization phải hoàn tất trước query; không dùng `course` filter để thay quyền truy cập.
- Không đưa thông tin học viên hoặc progress/resources vào projection khi API chỉ trả reusable `Lesson`.
- Không áp dụng Student guard cho Admin endpoint.

## Performance note

- Không có pagination, maximum result count, SLA hoặc index contract trong catalog/AC-34; response volume cần owner xác nhận trước khi triển khai.
- Candidate SQL dùng bound parameters; không nối query values trực tiếp vào SQL.
- `course_id ASC, sort_order ASC, id ASC` chỉ là thứ tự ổn định đề xuất; index/workload chưa được kiểm chứng.

## Contract interpretation

- DIRECT: method, path, authentication, role, query names/types, declared `ApiEnvelope<Lesson>`, HTTP 200 and exact 401/403/500 codes.
- DERIVED: exact-match behavior, all-status default, collection cardinality proposal, empty collection and candidate ordering.
- SOURCE_REQUIRED: `type` mapping, live/selected schema, Admin guard implementation, LessonStatus values and error-envelope integration.

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
