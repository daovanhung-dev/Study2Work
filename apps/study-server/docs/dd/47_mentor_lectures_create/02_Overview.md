---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 47 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/mentor/courses/{course_id}/lectures |
| Purpose | Tạo lecture thuộc course Mentor quản lý sau khi file đã được upload qua API #34. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; course phải thuộc quyền của principal. Candidate legacy check dùng courses.mentor_id; quyền theo assignment chưa có nguồn vật lý. |
| Basis | Contract/AC-21 là DIRECT; mapping sang lessons và direct-owner predicate là DERIVED; asset resolution là SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — Study router không có API #47 route/module/test source. |
| Transaction | Candidate transaction cho INSERT một dòng lessons; không bao gồm upload đã chạy ở API #34. |
| Side effects | Candidate tạo lessons row. Không tự tạo resources, uploads hoặc Content row khi chưa có nguồn xác nhận. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — #46–#50, Lecture, UploadAsset và bộ lỗi #47.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, bước AC-21 và liên kết #46–#48.
- [AC-21 và AC-22 diagrams](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — upload, tạo lecture, reload; phân biệt Content của AC-22.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy lessons/resources; không có lectures, contents hoặc uploads entity.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT courses/lessons/resources; chỉ là artifact, chưa xác nhận live.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) và [database context](../../../../../.agents/server-study/database.md) — schema UUID/versioned tách biệt và live schema chưa xác minh.
- [API guidelines](../../../../../contracts/api-guidelines/README.md), [response helper](../../../app/core/responses.py), [auth helper](../../../app/utils/auth.py) — envelope/error và giới hạn helper hiện tại.
- [API #46 DD](../46_mentor_courses/02_Overview.md), [#46 mapping](../46_mentor_courses/05_Data_Mapping.md), [#46 open questions](../46_mentor_courses/OPEN_QUESTIONS.md) — candidate ownership và schema boundary.
- [API #34 DD](../34_uploads/02_Overview.md), [#34 response](../34_uploads/04_Response.md), [#34 open questions](../34_uploads/OPEN_QUESTIONS.md) — API #34 không có DB asset persistence/lookup đã xác nhận.
- [API #9 mapping](../09_courses_curriculum/05_Data_Mapping.md) — legacy lessons-to-Lesson mapping precedent.
- [API #11 mapping](../11_courses_resources/05_Data_Mapping.md) — legacy resources relationship; API #11 là read-only.
- [Current Study router](../../../app/api/v1.py), [declared route status](../../../../../.agents/server-study/apis/declared-routes.md) — không có route API #47.

## Tables read

- courses — candidate lookup theo path ID và Mentor ownership.
- lessons — legacy candidate để lưu Lecture.
- resources — đọc schema để đánh giá asset association; không có mutation được chốt.
- V1-PILOT course_versions, lessons, content_blocks, file_objects — schema khác, không gộp với contract BIGINT.

## Tables write

- lessons — một INSERT candidate với trạng thái DERIVED; xem [07_lessons_insert.md](./07_lessons_insert.md).
- resources/uploads/contents — không ghi khi chưa có nguồn mapping cho asset refs hoặc Content.

## Mục chú ý

- Giữ nguyên contract #47: POST, response ApiEnvelope<Lecture>, HTTP 201 và đúng 401/403/404/422/500 codes.
- AC-21 nói Mentor sở hữu hoặc được phân công course. API #46 chỉ có candidate courses.mentor_id predicate; chưa có assignment relation.
- Không thêm điều kiện PUBLISHED: AC-21 là Mentor teaching flow, không phải public curriculum.
- Cụm “INSERT Lecture/Content” chưa xác định có phải một lesson row hay thêm Content resource. AC-22 là workflow Content riêng.
- content:int64 không khớp Lecture.content:string? và legacy lessons.content:TEXT. Chuyển int64 thành chuỗi thập phân chỉ là candidate DERIVED.
- asset refs là string nhưng chưa có format hay lookup đủ metadata; response assets:UploadAsset[] chưa thể tạo đầy đủ.

## Assumptions

- Legacy lessons là candidate tương thích nhất với API #47 int64 IDs và API #9 Lesson projection; chưa khẳng định đó là live schema.
- Nếu owner xác nhận content là nội dung chữ được mã hóa bằng int64, có thể ghi biểu diễn thập phân vào lessons.content. Nếu đây là ID, cần nguồn quan hệ riêng.
- Candidate insert bỏ cột status để nhận legacy default DRAFT; LessonStatus members chưa được định nghĩa.
- Candidate direct owner dùng cùng hướng với API #46; hỗ trợ course assigned cần relation và principal mapping đã xác nhận.
- Tên JSON asset_refs là suy luận từ nhãn catalog “asset refs”; phải xác nhận wire key và format.

## Conflicts

- API catalog/AC-21 request content:int64; Lecture schema và DB candidate dùng content string/TEXT.
- AC-21 nêu INSERT Lecture/Content nhưng ERD/legacy DDL chỉ có lessons; AC-22 định nghĩa Content riêng.
- API #34 trả UploadAsset nhưng ID generation, metadata persistence và lookup còn SOURCE_REQUIRED; legacy resources không chứa đủ UploadAsset fields.
- Legacy Study DDL dùng BIGINT lessons; V1-PILOT dùng UUID lessons theo course_versions/chapter_id và content_blocks. Live schema chưa xác minh.
- API guidelines yêu cầu data:null khi lỗi; current error_response() dùng {} khi data không được truyền.
- Timestamp legacy là TIMESTAMP không ghi timezone; response ISO-8601 cần quy tắc serialize.

## Security note

- Chỉ lấy Mentor identity từ Bearer JWT đã xác thực; không nhận owner ID từ request.
- Candidate ownership check phải gắn với principal; không tin asset URL hoặc metadata từ chuỗi refs khi chưa có resolver.
- Không mở đường sửa nội dung AC-22 hoặc publish lesson qua API tạo lecture này.

## Performance note

- Candidate flow gồm một course lookup và một lessons INSERT; không có query plan/index hoặc live schema evidence.
- Nếu asset resolution sau này yêu cầu nhiều refs, batch lookup và giới hạn kích thước phải được thiết kế từ contract đã duyệt, không suy ra ở DD này.

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
