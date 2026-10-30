---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "46"
api_name: "Lấy course Mentor được quản lý"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 46 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | `GET` |
| Endpoint | `/api/v1/mentor/courses` |
| Purpose | Liệt kê course Mentor có thể chọn để đăng bài giảng. |
| Consumer/Actor | `Mentor` |
| Authentication | Bearer JWT |
| Authorization | Role `Mentor`; danh sách phải giới hạn theo principal hiện tại. Cách xác định sở hữu/phân công còn là `DERIVED / SOURCE_REQUIRED`. |
| Basis | Catalog trực tiếp; query, pagination và owner predicate có phần `DERIVED`. |
| Status | Draft — Needs Confirmation |
| Current runtime state | `UNWIRED / NOT_FOUND` — chưa có route/module/test API #46 trong Study source. |
| Transaction | Không có mutation; query read-only. |
| Side effects | Không có. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #46–#48, `Course`, `Page`, status và error contract.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor và flow AC-21.
- [AC-21 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — chọn course, xác nhận quyền, tạo lecture và reload.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy course ownership fields.
- [Legacy Study Server DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT course/user model; live schema chưa xác minh.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID owner model khác; không gộp hai schema.
- [Database context](../../../../../.agents/server-study/database.md) — DDL artifact không chứng minh live database.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace và error convention.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py) và [response helper](../../../app/core/responses.py) — API #46 chưa wired; auth helper hiện tại là Student-specific.
- [API #6 course list DD](../06_courses/02_Overview.md), [request](../06_courses/03_Request.md), [response](../06_courses/04_Response.md), [mapping](../06_courses/05_Data_Mapping.md) — projection, Page và pagination precedent.
- [API #47 DD](../47_mentor_lectures_create/02_Overview.md) tạo lecture và [API #48 DD](../48_mentor_lecture_detail/02_Overview.md) tải lại lecture trong cùng AC-21; macro-review #46–#48 được ghi tại [PLAN_RESULT](../48_mentor_lecture_detail/PLAN_RESULT.md).
- [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) — các quyết định còn thiếu.

## Tables read

- `courses` — legacy candidate để lọc theo Mentor và đọc thuộc tính course.
- `users` — legacy candidate cho `Course.mentor` summary.
- `course_versions` — xuất hiện trong V1-PILOT, nhưng không được join vào legacy candidate vì schema/ID khác.

## Tables write

- N/A — API #46 là read-only.

## Mục chú ý

- Giữ nguyên contract `ApiEnvelope<Page<Course>>`, default `page=1`, `size=20` và danh sách lỗi 401/403/422/500.
- Không áp dụng bộ lọc `PUBLISHED` từ API #6: AC-21 cần Mentor chọn course để quản lý bài giảng; rule trạng thái chưa được contract chốt.
- `courses.mentor_id = principal_id` chỉ là candidate cho course sở hữu trực tiếp; AC-21 còn nói course được phân công nhưng chưa có relation nguồn.
- `Course.category` là optional; không tạo category object nếu chưa có relation course-category.
- Thiếu giá, status hoặc thông tin Mentor bắt buộc trong legacy row là integrity gap; không tự điền giá trị.

## Assumptions

- `page >= 1`, `size` trong `1..100`, sort mặc định `created_at DESC, id ASC` là `DERIVED` theo API #6; chưa phải contract API #46.
- Q1 và Q2 dùng cùng ownership/status predicates. Danh sách rỗng trả 200 với `items: []`.
- `total_pages=0` khi `total=0`; optional category bị omit.
- Cần xác nhận identity mapping, schema đang chạy, course assignment và enum values trước khi implementation.

## Conflicts

- Legacy DDL/ERD dùng `courses.id BIGSERIAL` và `mentor_id BIGINT`; V1-PILOT dùng `courses.id UUID`, `owner_subject_id UUID`, versioned status và không có `mentor_id`.
- Legacy DDL cho phép `mentor_id`, `price`, `status` NULL trong khi Course contract yêu cầu mentor, price và status.
- Catalog khai báo `CourseStatus` nhưng không có member list.
- Error guideline yêu cầu `data: null`; current `error_response()` trả `{}` khi không truyền data.

## Security note

- Principal phải lấy từ Bearer JWT đã xác thực; không nhận mentor ID từ query/body.
- Luôn áp dụng owner/assignment scope trong query data và count; direct-owner predicate hiện chỉ là candidate.
- Không trả raw SQL, token claims, stack trace hoặc chi tiết DB.

## Performance note

- Page query và count query có cùng predicate; có thể cần index theo ownership/status khi schema được xác nhận.
- Không có live query plan, kích thước bảng hoặc index evidence; DD không đề xuất migration.
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
