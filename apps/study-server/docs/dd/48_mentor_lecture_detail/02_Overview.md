---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "48"
api_name: "Tải lại lecture vừa tạo"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 48 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | GET |
| Endpoint | /api/v1/mentor/lectures/{lecture_id} |
| Purpose | Đọc lại chi tiết lecture trong luồng Mentor đăng bài giảng AC-21. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; local source kiểm tra direct `courses.mentor_id` owner theo API #46/#47. Assigned-course support và identity mapping vẫn cần xác nhận. |
| Request | Path lecture_id:int64!; không có body/query theo catalog. |
| Response | ApiEnvelope<Lecture> |
| Success | HTTP 200 DESIGN_RESOURCE_RETRIEVED |
| Errors | Chỉ 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 500 DESIGN_INTERNAL_ERROR. |
| Current runtime state | WIRED — route, module và focused HTTP tests có trong source; checked-in schema/migration được đối chiếu, live DB/deployment chưa xác minh. |
| Transaction | Không có mutation; read-only. |
| Side effects | Không có. |

### Expected behavior

Catalog và AC-21 yêu cầu Mentor đọc lecture vừa tạo theo lecture_id và hiển thị trong course. Candidate response phải giữ đủ các trường Lecture theo schema dùng lại.

### Current behavior

Study Server hiện có route và module API #48. API #34 lưu UploadAsset metadata trong legacy `uploads`; API #47 ghi asset refs đã xác thực vào `lesson_uploads`; API #48 đọc theo thứ tự liên kết. DDL/migration trong checkout không chứng minh schema live đã áp dụng.

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — dòng API #48 và schema Lecture/UploadAsset.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition và vị trí API #48 trong AC-21.
- [AC-21 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — #46 → upload/Object Storage → #47 → #48.
- [AC-22 activity diagram cùng tệp](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — Content là workflow quản lý riêng.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — lessons/resources là thiết kế legacy, không có entity Uploads.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT courses/lessons/resources; không chứng minh schema live.
- [Migration 004 uploads](../../../../../infra/postgres/study-server/migrations/004_uploads.sql) và [migration 005 lesson uploads](../../../../../infra/postgres/study-server/migrations/005_lesson_uploads.sql) — checked-in metadata and ordered lecture-to-upload relation; không chứng minh migration đã chạy live.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) và [database context](../../../../../.agents/server-study/database.md) — schema UUID/versioned khác; live schema chưa xác minh.
- [API guidelines](../../../../../contracts/api-guidelines/README.md), [response helper](../../../app/core/responses.py), [auth helper](../../../app/utils/auth.py) — envelope convention và current helper boundary.
- [API #46 overview](../46_mentor_courses/02_Overview.md), [#46 mapping](../46_mentor_courses/05_Data_Mapping.md), [#46 open questions](../46_mentor_courses/OPEN_QUESTIONS.md) — course owner candidate và assignment gap.
- [API #47 overview](../47_mentor_lectures_create/02_Overview.md), [#47 mapping](../47_mentor_lectures_create/05_Data_Mapping.md), [#47 open questions](../47_mentor_lectures_create/OPEN_QUESTIONS.md) — create/read contract, candidate lessons mapping và asset gap.
- [API #34 response](../34_uploads/04_Response.md) và [#34 open questions](../34_uploads/OPEN_QUESTIONS.md) — API upload chưa xác định ID, metadata persistence hay lookup.
- [API #9 mapping](../09_courses_curriculum/05_Data_Mapping.md) và [API #26 mapping](../26_lessons_resources/05_Data_Mapping.md) — lesson/resource precedents; không áp dụng public PUBLISHED filter hay suy ra UploadAsset.
- [Current Study router](../../../app/api/v1.py), [API #48 view](../../../app/modules/mentor/api_48_mentor_lecture_detail/view.py), [declared route status](../../../../../.agents/server-study/apis/declared-routes.md) — local route/module wiring and response behavior.

## Tables read

- lessons — candidate legacy source cho Lecture fields id, course_id, name, content, sort_order, status.
- courses — candidate legacy source để xác định course cha và direct owner.
- lesson_uploads — ordered association between legacy lesson and upload IDs, introduced by migration 005.
- uploads — API #34 metadata source for UploadAsset.
- resources — chỉ được xem xét để đối chiếu; không đủ field tạo UploadAsset.
- V1-PILOT courses, course_versions, lessons, content_blocks, file_objects — schema khác, không được trộn vào candidate BIGINT.

## Tables write

- N/A — API #48 là GET/read-only; không có INSERT, UPDATE hoặc DELETE.

## Mục chú ý

- Giữ nguyên response ApiEnvelope<Lecture> và đúng 4 business error codes trong catalog.
- Local source dùng direct-owner rule với #46/#47; AC-21 còn hỗ trợ course được phân công nhưng chưa có assignment relation hay confirmed identity binding.
- Query preserves the stored status but excludes the API #86 local tombstone `DELETED`; other status values are not filtered.
- Lecture.content là nullable string; source giữ SQL NULL thành JSON null.
- assets là mảng bắt buộc; API #47 persists ordered IDs in `lesson_uploads`, and API #48 resolves metadata from `uploads` scoped by owner/purpose/course. Empty list follows #47's empty-ref request.
- Không trả video_url vì field này không thuộc reusable Lecture schema.
- AC-21 ghi INSERT Lecture/Content, còn AC-22 là Content CRUD riêng; API #48 chỉ đọc Lecture theo catalog.

## Assumptions

- Candidate Q1 dùng legacy lessons LEFT JOIN courses theo lessons.course_id; đây không phải xác nhận schema live.
- Missing lesson dùng 404; owner mismatch theo candidate dùng 403; row không có parent course hợp lệ là integrity failure candidate dùng 500 vì không thể dựng course_id bắt buộc.
- Role Mentor and numeric principal come from the shared auth helper; whether this matches deployed Mentor identity remains unverified.
- Direct owner uses `courses.mentor_id = authenticated principal`, matching #46/#47; assigned-course access is not implemented.
- Q1 excludes only status `DELETED` to hide API #86 tombstones. API #47 currently inserts `PUBLISHED`; other stored statuses are returned without enum conversion.

## Conflicts

- Legacy DDL dùng BIGINT courses/lessons và lessons.course_id có thể NULL; DB table guide mô tả course_id bắt buộc. Live schema chưa xác minh.
- V1-PILOT dùng UUID, lessons gắn chapter/course_version và content_blocks; file_objects có metadata khác contract UploadAsset. Không gộp với legacy schema.
- API #47's local JSON-array asset_refs format and API #34 persistence are now source-backed; deployment and business ownership of this relation remain unconfirmed.
- Legacy resources thiếu content_type, size_bytes và UploadStatus nên không đủ projection cho assets.
- Error guideline yêu cầu data:null; current error_response() trả {} khi data không được truyền.
- Catalog does not define LessonStatus/UploadStatus members or malformed lecture_id mapping. Current source maps malformed/out-of-range values to catalog 404 by implementation decision.

## Security note

- Không nhận mentor_id hoặc owner từ request; lấy principal từ JWT đã xác thực.
- Áp dụng cùng course scope với API #46/#47. Không coi việc biết lecture_id là quyền truy cập.
- Không tin asset URL hoặc metadata trong asset refs nếu chưa có resolver được duyệt.
- Không đưa thông tin nội bộ, claim nhạy cảm hay SQL vào response lỗi.

## Performance note

- Candidate read trả tối đa một lecture row; không cần pagination hoặc sort.
- Query the lesson/course parent and then the ordered linked uploads; enforce owner, purpose and course on the upload lookup.
- Không có live query plan/index evidence; không đề xuất migration từ DD này.

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
