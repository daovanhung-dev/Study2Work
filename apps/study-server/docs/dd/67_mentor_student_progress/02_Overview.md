---
title: "Overview"
order: 2
dd_id: "67"
api_name: "Lấy tiến độ Student"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #67 |
| Module | MENTOR / TEACHING & SUPPORT — AC-26 |
| Method | GET |
| Endpoint | /api/v1/mentor/courses/{course_id}/students/{student_id}/progress |
| Purpose | Đọc tiến độ hiện trạng của một Student trong một course để hiển thị drill-down từ dashboard AC-26. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Shared MENTOR guard; fallback direct-owner theo `courses.mentor_id = JWT sub` và Student ACTIVE roster như #65. |
| Basis | Method/path/auth/input/status/errors DIRECT từ catalog; AC-26 purpose DIRECT; response StudentCourseProgress và các query/rules là DERIVED fallback được implement. Page<Course> direct vẫn là DISCREPANCY. |
| Status | Draft — Needs Confirmation |
| Current runtime state | WIRED / SOURCE_BACKED — route, module, middleware allowlist và HTTP tests API #67 hiện có; fake DB tests không xác minh live schema/deployment. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không có mutation; #67 không gọi #65 hoặc #66 server-to-server. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #65–#67, ApiEnvelope<T>, Page<T>, PageMeta, Course, Lesson, Enrollment, UserSummary.
- [AC/API index, AC-26](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Mentor có quyền xem analytics course; chọn Student rồi đọc progress.
- [AC-26 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — thứ tự #65 class progress → #66 learning events → #67 progress theo Student.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — #65/#67 SELECT là DESIGN_ONLY; bảng lesson_progress lưu current progress state.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT courses, enrollments, users, lessons, lesson_progress; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID course_enrollments, lesson_progress_facts, progress_snapshots; schema khác contract int64.
- [API #9 curriculum SQL](../../../app/modules/guest/api_09_courses_curriculum/query.py) và [view](../../../app/modules/guest/api_09_courses_curriculum/view.py) — current source lọc course/lesson PUBLISHED và sort theo sort_order, id.
- [API #9 focused test source](../../../tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py) — API #9 route/source test nằm trong full Study suite đã chạy.
- [AC-14 học bài](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) và [API #25 progress DD](../25_lessons_progress/05_Data_Mapping.md) — tiến độ cập nhật ở lesson; API #25 mapping vẫn là design-only.
- [API #65 overview/response](../65_mentor_course_progress/02_Overview.md) / [response](../65_mentor_course_progress/04_Response.md) — candidate class summary, published lesson denominator và formula đang chờ duyệt.
- [API #66 overview](../66_mentor_course_analytics/02_Overview.md) — course-level learning-event analytics là miền riêng.
- [API #21 progress](../21_users_me_progress/02_Overview.md), [API #37 detail progress](../37_users_me_progress_course/02_Overview.md) và [API #62 roster](../62_mentor_course_students/02_Overview.md) — precedent có giới hạn; không thay contract #67.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [response helper](../../../app/core/responses.py), [middleware](../../../app/core/middleware.py), [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [API #67 module](../../../app/modules/mentor/api_67_mentor_student_progress/) và [focused HTTP tests](../../../tests/modules/mentor/api_67_mentor_student_progress/test_mentor_student_progress.py) — implementation fallback hiện tại; tests dùng fake DB.
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprints ở [PLAN_RESULT](./PLAN_RESULT.md).

## Tables read

- `courses`, `enrollments`, `users`, `lessons`, `lesson_progress` — legacy BIGINT relations hiện được query source #67 dùng; live schema/deployment remain unverified.
- `course_enrollments`, `lessons`, `lesson_progress_facts`, `progress_snapshots`, `learner_profiles` — V1-PILOT UUID candidates; not compatible with int64 path without an approved mapping.
- API #9 source orders lessons by `sort_order ASC, id ASC`; API #67 implements this order in its local query.

## Tables write

N/A — READ-ONLY API. API #67 không tạo, sửa hoặc xóa dữ liệu.

## Mục chú ý

- Giữ contract trực tiếp `ApiEnvelope<Page<Course>>`; Course không có Student progress fields nên đây là DISCREPANCY với AC-26.
- PageMeta yêu cầu page/size nhưng API #67 không khai báo query parameter; không tự thêm page/size hoặc pagination default.
- Runtime fallback `StudentCourseProgress` ở [04_Response](./04_Response.md) là DERIVED và cần contract approval.
- Để đồng bộ với #65, runtime tính summary từ cùng tập lesson PUBLISHED và formula floor-average; #67 thêm chi tiết từng lesson.
- #67 đọc state progress hiện tại; không tính lại learning events hoặc dùng progress state làm nguồn cho #66.
- Runtime roster membership dùng `enrollments.status='ACTIVE'` và `users.role='STUDENT'` như #65; business approval cho rule này vẫn cần xác nhận.
- API #37 trong AC-18 có scope lesson + quiz + assignment; AC-26 không nêu các loại đó. Runtime #67 giữ lesson-level để phù hợp nhóm #65–#67; cần xác nhận nếu muốn mở rộng.
- Current shared auth helper hỗ trợ role `MENTOR` và trả `sub` dạng integer; #65/#66 dùng `courses.mentor_id = sub` làm local direct-owner policy. #67 tái sử dụng chính sách đó, vẫn là DERIVED từ pattern hiện tại chứ chưa được business owner xác nhận.
- Middleware design-code allowlist hiện đã gồm route #67; `error_response` mặc định `data: null`.

## Assumptions

- DERIVED / IMPLEMENTED: detail gồm summary và một item cho mỗi lesson PUBLISHED, sort theo `sort_order ASC, id ASC` như API #9.
- DERIVED / IMPLEMENTED: lesson không có progress row được hiển thị là NOT_STARTED với progress_percent bằng 0; timestamp null được giữ trong JSON.
- DERIVED / IMPLEMENTED: summary dùng cùng denominator/formula với #65; tính floor average và zero khi không có lesson PUBLISHED. Domain owner chưa phê duyệt formula.
- DERIVED / IMPLEMENTED: Student phải có `enrollments.status = 'ACTIVE'` và `users.role = 'STUDENT'`, cùng roster rule #65; course phải thuộc trực tiếp Mentor hiện tại qua `courses.mentor_id = sub`.
- DERIVED / IMPLEMENTED: duplicate legacy progress rows chọn latest `last_accessed_at DESC NULLS LAST`, rồi `id DESC`, giống #65.
- Runtime dùng tên bảng/cột trong legacy DDL để khớp #65; đây không phải xác nhận live schema. Không giả định unique progress row.

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Diagram/catalog #67 | AC-26 purpose | Diagram/catalog type `Page<Course>`; AC yêu cầu progress của một Student. | Runtime dùng singular `StudentCourseProgress` DERIVED fallback; catalog/diagram chưa được sửa nên contract approval còn mở. |
| PageMeta | Request #67 | Schema có page/size nhưng request không có pagination input. | Không có cách client yêu cầu trang tiếp theo. |
| Legacy DDL | V1-PILOT DDL | BIGINT user/lesson progress khác UUID enrollment/facts/snapshots. | Chưa thể chốt một truy vấn vật lý cho path int64. |
| API #25/AC-14 | Legacy #67 query | Progress update có percent/completed intent nhưng live physical mapping và unique user/lesson key chưa được xác nhận. | Implementation dùng checked-in legacy candidate cùng tie-break như #65; live schema chưa xác minh. |
| #65/#66/#67 catalog | AC-26/runtime | Cả ba response trực tiếp là Page<Course> dù phục vụ ba kết quả khác nhau. | #67 đã dùng singular DERIVED response; cần owner cập nhật đồng bộ contract trước khi coi là chuẩn. |

## Security note

- Shared guard xác minh role Mentor trước DB; direct-owner lookup được thực hiện trước Student lookup.
- Kiểm tra Student thuộc ACTIVE roster có role STUDENT như #65; không dùng student_id path làm căn cứ quyền duy nhất.
- Owner mismatch trả 403; course hoặc Student ngoài eligible roster trả 404 theo fallback. Privacy policy chưa được business owner xác nhận.
- Chỉ trả `id`, `full_name`, `avatar_url`; không lộ email, quiz answers hoặc assignment submission content.

## Performance note

- Runtime trả tất cả lesson PUBLISHED trong course vì request không có pagination; số lượng lớn có thể làm response không giới hạn.
- Không có freshness, snapshot, cache, SLA hoặc consistency boundary được định nghĩa.
- Legacy DDL không khai báo unique `(user_id, lesson_id)`; runtime dùng latest timestamp/id giống #65 để chọn một state, nhưng schema policy chưa được phê duyệt.

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
