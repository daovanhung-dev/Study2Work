---
title: "Overview"
order: 2
dd_id: "83"
api_name: "Lấy lesson detail"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #83 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-34 |
| Method | GET |
| Endpoint | `/api/v1/admin/lessons/{lesson_id}` |
| Purpose | Admin đọc thông tin một lesson được chọn để tiếp tục quản lý. |
| Consumer/Actor | Admin có lesson-management permission |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog và lesson-management permission theo tiền điều kiện AC-34; guard/policy chưa có trong Study source. |
| Direct response | `ApiEnvelope<Lesson>` |
| Basis | Method/path/auth/path/response/status/errors DIRECT; query/schema mapping candidate; invalid-ID mapping DERIVED. |
| Status | Draft — Needs Confirmation |
| Current implementation | `UNWIRED / NOT_FOUND` — current Study source không có route, module hoặc test API #83. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không ghi dữ liệu; update/status/delete thuộc các API #84–#86. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #83, `ApiEnvelope<T>`, `Lesson`.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin lesson-management permission và nhóm API #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #83 detail, bước “Đọc lesson + dependencies”, chọn update/status/delete, reload list.
- [AC delivery README](../../diagrams/AC_UNICA/README.md) — convention một AC có thể chứa nhiều API.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT `lessons`, `resources`, `lesson_progress`.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) and [ERD](../../diagrams/DB_UNICA_ERD.drawio) — design relationships, không phải live-schema proof.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned lesson model khác response contract.
- [API #09 Lesson model/query/view](../../../app/modules/guest/api_09_courses_curriculum/) and [focused test](../../../tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py) — field alias/null handling and public-only filter precedent; Admin #83 does not inherit `PUBLISHED` predicate.
- [API #74 Admin detail DD](../74_admin_course_detail/02_Overview.md) — Admin detail workflow, read-only mapping and derived invalid-path handling precedent.
- [API #82 Admin lesson list DD](../82_admin_lessons_list/02_Overview.md) — same AC-34 permission, status/schema and error-envelope gaps.
- [Auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [error helper](../../../app/core/responses.py) and [API guidelines](../../../../../contracts/api-guidelines/README.md) — current guard/error integration boundary.

## Tables read

| Relation | Candidate fields/relationship | Basis/status |
|---|---|---|
| Legacy `lessons` | `id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status` | Candidate BIGINT DDL; `name -> title`, `sort_order -> order`; live schema chưa xác minh. |
| Legacy `resources` | `lesson_id` FK to `lessons.id` | Dependency relation visible in DDL/ERD; no dependency fields in `Lesson` response. |
| Legacy `lesson_progress` | `lesson_id` FK to `lessons.id` | Dependency relation visible in DDL/ERD; no dependency fields in `Lesson` response. |
| V1-PILOT `lessons` | UUID `id`, `chapter_id`, `course_version_id`, `title`, `summary`, `position`, `estimated_minutes`, `is_preview` | Model does not match BIGINT `Lesson`; do not map implicitly. |

## Tables write

Không có — GET chỉ đọc.

## Mục chú ý

- API #83 trả một `Lesson`, đúng với path detail và catalog; không dùng wrapper Page hay array.
- AC-34 node n5 ghi “Đọc lesson + dependencies”, nhưng catalog `Lesson` không có resources/progress/dependency fields và diagram không mô tả chúng. DD giữ đúng response hiện tại, không thêm truy vấn vô mục đích; cần xác nhận dependency data có thuộc #83 hay không.
- `resources` và `lesson_progress` là quan hệ tồn tại trong legacy artifacts. API #86 còn phải kiểm tra progress/reference tại thời điểm xóa; không dựa vào dữ liệu detail cũ để quyết định delete.
- Admin detail không áp dụng `PUBLISHED` predicate từ API #09; AC-34 cần đọc lesson trước nhánh đổi trạng thái.
- Legacy `course_id` nullable trong DDL trong khi reusable `Lesson.course_id` required; active schema/live metadata chưa xác minh.
- `LessonStatus` members/casing chưa có danh sách chuẩn; không tự tạo enum hoặc filter.
- API #86 có thể xóa mềm hoặc cứng theo policy; marker và việc #83 có ẩn lesson đã xóa chưa được định nghĩa.

## Assumptions

- Q1 đọc một row theo `lessons.id = :lesson_id` từ legacy DDL candidate; không join course/resources/progress khi response không yêu cầu fields từ các bảng đó.
- Nếu lesson không tồn tại, trả 404 `DESIGN_RESOURCE_NOT_FOUND` theo catalog.
- Path value không chuyển được thành int64 được đề xuất ánh xạ 404 để giữ đúng error set catalog, tương tự proposal ở API #74; cần custom integration nếu framework mặc định 422.
- Admin xem được lesson ở mọi status; không dùng public API #09 filter `PUBLISHED`. Đây là `DERIVED` từ AC-34 flow.
- Optional `content` và `video_url` serialize `null` khi legacy column NULL theo API #09 model/test precedent; cần xác nhận nếu contract muốn omit.

## Conflicts

- AC-34 detail step yêu cầu đọc dependencies nhưng response/API contract không có trường phụ thuộc hoặc quy tắc query.
- Legacy BIGINT lesson model và V1-PILOT UUID/versioned model không tương đương; live DB chưa kiểm chứng.
- Legacy DDL cho phép `course_id` NULL nhưng Lesson schema yêu cầu int64.
- Current Study auth chỉ có Student guard; Admin role/permission source chưa có.
- Middleware allowlist không chứa API #83; malformed-path and unhandled errors would use generic codes unless future route integration changes it.
- Error guideline yêu cầu `data:null`; `error_response` hiện default `data:{}` khi không truyền.
- Soft-delete visibility của #83 chưa có marker/policy được duyệt.

## Security note

- Xác thực Bearer, role Admin và lesson-management permission trước khi lookup lesson.
- Không trả dependency/student progress, thông tin người học hay PII qua `Lesson` response.
- Không tiết lộ lesson tồn tại cho caller chưa vượt authorization.
- Không dùng Student guard thay cho Admin policy.

## Performance note

- Candidate Q1 lọc theo khóa chính `lessons.id`, chỉ cần tối đa một row.
- Không chạy COUNT, join hoặc query dependency khi contract chưa định nghĩa dữ liệu cần trả.
- Index/live query plan chưa được xác minh; DDL candidate khai báo primary key trên `id`.

## Contract interpretation

- DIRECT: method/path, Bearer JWT, role Admin, `lesson_id:int64!`, `ApiEnvelope<Lesson>`, HTTP 200 và đúng lỗi 401/403/404/500.
- DERIVED: one-row legacy lookup, no public status filter, malformed path -> 404, optional NULL serialization.
- SOURCE_REQUIRED: Admin permission implementation, active schema/live DB, dependency detail, status enum, soft-delete visibility and error middleware integration.

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
