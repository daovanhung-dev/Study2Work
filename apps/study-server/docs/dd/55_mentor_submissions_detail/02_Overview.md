---
title: "Overview"
order: 2
dd_id: "55"
api_name: "Lấy bài làm và rubric Mentor"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 55 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | GET |
| Endpoint | `/api/v1/mentor/submissions/{submission_id}` |
| Purpose | Đọc một bài làm được chọn để Mentor xem nội dung trước khi gọi API #56 lưu điểm hoặc API #57 lưu feedback. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | AC-23 yêu cầu quyền chấm submission của course. `courses.mentor_id = authenticated Mentor ID` là candidate DERIVED; assigned Mentor chưa có relation nguồn. |
| Basis | Catalog và AC-23 là DIRECT; query/schema/ownership là design candidate. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — READ-ONLY API |
| Side effects | Không có INSERT/UPDATE/DELETE được khai báo. |

## Sources

- [API catalog: #55, #56, #57 và reusable Submission](../../../../../docs/lists/list_api.md).
- [AC/API index: AC-23 Chấm bài](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-23 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [ERD](../../diagrams/DB_UNICA_ERD.drawio).
- [Legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql) — không phải bằng chứng live schema.
- [V1-PILOT study DDL](../../../../../infra/postgres/02_study_db.sql) — rubric dùng UUID/assessment model riêng.
- [API #35 submission create DD](../35_assignments_submissions/02_Overview.md) và [data mapping](../35_assignments_submissions/05_Data_Mapping.md).
- [API #36 Student submission detail DD](../36_submissions_detail/02_Overview.md) và [open questions](../36_submissions_detail/OPEN_QUESTIONS.md).
- [API #46 Mentor course DD](../46_mentor_courses/OPEN_QUESTIONS.md), [API #47 Mentor lecture DD](../47_mentor_lectures_create/OPEN_QUESTIONS.md) và [API #54 submissions list DD](../54_mentor_submissions_list/02_Overview.md).
- [Current API router](../../../../../apps/study-server/app/api/v1.py), [auth helper](../../../../../apps/study-server/app/utils/auth.py), [middleware](../../../../../apps/study-server/app/core/middleware.py) và [response helper](../../../../../apps/study-server/app/core/responses.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) and [Study declared routes](../../../../../.agents/server-study/apis/declared-routes.md).
- [Study DD workflow](../../../../../.agents/server-study/workflows/README.md) and [createDD-markdown skill](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).

## Tables read

- `assignment_submissions` — legacy design candidate cho các field Submission.
- `assignments` — candidate relation lấy `course_id` từ `assignment_id`.
- `courses` — candidate relation kiểm tra direct Mentor ownership.
- Asset lookup — đọc `uploads` metadata theo fallback DERIVED URL/owner/purpose/course dùng ở API #54.
- Rubric lookup — SOURCE_REQUIRED; không nối rubric V1-PILOT vào legacy Assignment.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- AC-23 yêu cầu đọc `Submission + files + rubric`; reusable `Submission` trong catalog có `files:UploadAsset[]` nhưng không có field `rubric`.
- API #54 hiện trả `ApiEnvelope<Page<Submission>>` theo fallback DERIVED để luồng AC-23 chọn một ID rồi gọi API #55.
- API #54 resolve 0/1 `UploadAsset` bằng URL + owner + purpose + course; đây là fallback DERIVED, chưa có FK hoặc xác nhận từ API #35.
- `infra/postgres/02_study_db.sql` có `rubrics` và `rubric_criteria` gắn vào `assessments.id` bằng UUID; không có relation với legacy `assignments` hoặc `assignment_submissions` BIGINT.
- API #55 đứng giữa API #54 chọn submission và API #56/#57 ghi grade/feedback; API #55 không thực hiện mutation.
- Runtime hiện có route, module và TestClient tests cho API #55; tests dùng fake DB, chưa xác minh query trên live schema.

## Assumptions

- `submission_id` tra một submission theo khóa `assignment_submissions.id` là candidate từ contract/schema.
- Guard dùng JWT chuẩn Study: `sub` là numeric user ID, `roles` chứa `MENTOR`; current shared guard và các API #46–#55 dùng trực tiếp pattern này.
- Direct-owner predicate `courses.mentor_id = :mentor_id` là policy hiện hành của các API Mentor được triển khai; vẫn không bao phủ assigned Mentor.
- Tách submission không tồn tại → 404 và role/course không có quyền → 403 theo error set catalog; quy tắc che giấu sự tồn tại chưa được xác nhận.
- API #54 cung cấp Page<Submission>; #55 giữ `ApiEnvelope<Submission>` cho một item. Chưa thêm `rubric` vào Submission schema hoặc `meta`.

## Conflicts

- Diagram yêu cầu rubric nhưng reusable `Submission` không có rubric field; V1-PILOT rubric model không nối được vào legacy assignment submission.
- API #54 list response đã được chuyển sang Page<Submission> theo fallback AC-23; API #55 nhận ID của một item trong page.
- `Submission.files` dùng DERIVED URL/owner/purpose/course lookup qua API #34; DDL không có FK, nên không đảm bảo file từ API #35 đã được lưu theo URL này.
- DB table guide/ERD đánh dấu `assignment_id` và `user_id` bắt buộc; legacy DDL cho phép NULL.
- `Submission.score` là optional `decimal-string`; API #56 nhận `score:int32`, còn `Assignment.max_score` là `decimal-string`.
- API Guidelines and current `error_response()` both return `data:null`. API #55 route template is registered in middleware; direct view responses use the catalog 401/403/404/500 codes.

## Security note

- Không nhận Student ID từ request; chỉ dùng định danh từ access JWT đã xác thực.
- Đọc dữ liệu candidate nội bộ nhưng không serialize bất kỳ field submission nào trước khi quyền Mentor được kiểm tra.
- Current direct-owner access không chứng minh quyền của Mentor được phân công.
- Quy tắc trả 403 hay mask bằng 404 cho một submission thuộc course khác cần giữ nhất quán với API #54; #54 trả 403 cho course được chỉ định thuộc Mentor khác.

## Performance note

- Candidate truy vấn lookup một `submission_id`; ID là primary key trong legacy DDL.
- Các bảng/relationship chưa được xác nhận live; không có query plan hoặc latency target để tuyên bố hiệu năng.
- File lookup follows the DERIVED API #54 URL/owner/purpose/course fallback; rubric still lacks a relation/schema and no live query plan is available.

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
