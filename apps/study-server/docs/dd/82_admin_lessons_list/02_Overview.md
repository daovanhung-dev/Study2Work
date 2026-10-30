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
| Consumer/Actor | Admin có quyền quản lý bài học theo tiền điều kiện AC-34. |
| Authentication | Bearer JWT qua shared guard. |
| Authorization | Runtime yêu cầu role `ADMIN`; quyền lesson-management riêng chưa có policy source. |
| Basis | Method/path/query, reusable schemas và catalog status/error là DIRECT. Collection, exact filters, ordering và malformed-input 422 là DERIVED để khớp list intent và schema sẵn có. |
| Status | Draft — Needs Confirmation |
| Current implementation | Wired locally; route, module, query và HTTP tests tồn tại. Runtime test dùng fake DB, không xác minh live schema/deployment. |
| Transaction | N/A — API chỉ đọc; khi query/projection lỗi, view rollback an toàn. |
| Side effects | Không ghi dữ liệu; các thao tác detail/update/status/delete thuộc API #83–#86. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #82, `Lesson`, `ApiEnvelope<T>`, business codes.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, permission precondition và nhóm API #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — Admin mở lesson management, query danh sách, chọn thao tác tiếp theo và reload.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT table `lessons`; không xác nhận live schema.
- [Study schema tables](../../diagrams/DB_UNICA_TABLES.md) and [ERD](../../diagrams/DB_UNICA_ERD.drawio) — design artifacts, chưa chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned lesson model khác reusable BIGINT contract.
- [API #09 Lesson model/query/view](../../../app/modules/guest/api_09_courses_curriculum/) — reusable projection; `name -> title`, `sort_order -> order`. Predicate `PUBLISHED` chỉ thuộc public curriculum.
- [API #78 Admin list DD](../78_admin_content_pending/02_Overview.md) — precedent cho việc ghi rõ list-shape discrepancy và DERIVED choice.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy `lessons` | `id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status` | Candidate BIGINT DDL; `name -> title`, `sort_order -> order`; live schema chưa xác minh. |
| V1-PILOT `lessons` | UUID `id`, `chapter_id`, `course_version_id`, `title`, `summary`, `position`, `estimated_minutes`, `is_preview` | Khác ID và response fields; không map trực tiếp sang reusable `Lesson`. |
| `resources`, `lesson_progress` | References to lesson | Diagram relations only; không cần join cho response #82. |

## Tables write

Không có — GET chỉ đọc.

## Mục chú ý

- Catalog khai báo `ApiEnvelope<Lesson>` nhưng tên API và AC-34 yêu cầu danh sách. Runtime chọn `ApiEnvelope<Lesson[]>` làm fallback DERIVED để thể hiện list intent; discrepancy với catalog vẫn phải được owner xác nhận.
- Query `course`, `status`, `type` có trong catalog. Runtime dùng exact equality cho `course -> course_id` và `status -> status`. Legacy candidate không có `type`; nếu client gửi `type`, runtime trả HTTP 422 `DESIGN_VALIDATION_ERROR` (`UNSUPPORTED_FILTER`) thay vì âm thầm bỏ filter.
- Không có `page`, `size`, `sort`, Page metadata, count query hay giới hạn kết quả được khai báo. Runtime trả toàn bộ kết quả khớp filter theo thứ tự ổn định `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`.
- Khi không truyền `status`, không áp dụng mặc định `PUBLISHED`; Admin có thể thấy các trạng thái lưu trong nguồn. API #09 public curriculum có predicate riêng và không được dùng lại ở đây.
- API #86 chọn local DERIVED marker `status='DELETED'`; #82 loại tombstone khỏi mọi list query, kể cả khi client gửi `status=DELETED`.
- Legacy DDL cho phép `course_id`, `sort_order`, `status` NULL trong khi reusable `Lesson` yêu cầu các giá trị tương ứng. Projection không hợp lệ trả 500 an toàn; không loại row hay tự gán giá trị.
- LessonStatus members/casing chưa được liệt kê đầy đủ; endpoint nhận chuỗi status và dùng exact equality, không tự tạo whitelist.

## Assumptions

- `course` parse thành signed int64; query sai định dạng hoặc ngoài range trả 422 `DESIGN_VALIDATION_ERROR` (`INT_PARSING`) sau khi xác thực Admin.
- `course` và `status` dùng exact equality; khi vắng mặt không thêm predicate. Đây là fallback DERIVED.
- Kết quả rỗng trả HTTP 200 với `data: []`. Response không có pagination metadata.
- Shared guard yêu cầu role `ADMIN`; riêng AC-34 lesson-management permission chưa có executable policy source.

## Conflicts

- Catalog singleton `ApiEnvelope<Lesson>` đối lập với list intent; runtime chọn array fallback và DD vẫn Draft.
- Legacy BIGINT schema và V1-PILOT UUID/versioned model không tương đương; live database chưa kiểm chứng.
- `course_id`, `sort_order`, `status` nullable trong legacy DDL nhưng fields của reusable `Lesson` required.
- Query có `type` nhưng không có Lesson type trong reusable schema/DDL đã kiểm tra; runtime trả explicit unsupported-filter validation error.
- AC-34 nêu lesson-management permission, còn executable shared guard chỉ kiểm tra role `ADMIN`; permission chuyên biệt vẫn chưa được implement/source-backed.

## Security note

- Shared JWT guard yêu cầu Bearer token hợp lệ và role `ADMIN` trước query validation/DB access.
- Authorization không dựa vào `course` filter. Không đưa thông tin học viên, progress hoặc resources vào projection.
- AC-34 fine-grained permission chưa được chứng minh bởi shared role guard.

## Performance note

- Không có pagination, maximum result count, SLA hoặc index contract trong catalog/AC-34; runtime có thể trả mọi row khớp filter.
- SQL bind parameters cho filters; không nối query values trực tiếp vào SQL.
- Thứ tự `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC` bảo đảm kết quả ổn định; index/workload chưa được kiểm chứng.

## Contract interpretation

- DIRECT: method, path, Bearer authentication, role Admin, query names/types, catalog `ApiEnvelope<Lesson>`, HTTP 200 và exact 401/403/500 codes.
- DERIVED: collection response để khớp list intent, exact-match `course`/`status`, all-status default, empty array, stable ordering, và 422 khi query không parse được hoặc `type` chưa có mapping.
- SOURCE_REQUIRED: live/selected DB schema, dedicated lesson-management permission, LessonStatus enum đầy đủ và pagination/result cap. Tombstone visibility is implemented locally but remains DERIVED.

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
