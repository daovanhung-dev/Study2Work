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
| Authorization | Role Mentor theo catalog; quyền course và việc Student thuộc roster của course cần cùng policy với #65. |
| Basis | Method/path/auth/input/response/status/errors DIRECT từ catalog; #67 đọc tiến độ Student DIRECT ở mức mục tiêu AC-26; field và formula chi tiết DERIVED/SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route, module hoặc focused test API #67 trong Study source. |
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
- [API #9 focused test source](../../../tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py) — test source có; chưa chạy trong task này.
- [AC-14 học bài](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) và [API #25 progress DD](../25_lessons_progress/05_Data_Mapping.md) — tiến độ cập nhật ở lesson; API #25 mapping vẫn là design-only.
- [API #65 overview/response](../65_mentor_course_progress/02_Overview.md) / [response](../65_mentor_course_progress/04_Response.md) — candidate class summary, published lesson denominator và formula đang chờ duyệt.
- [API #66 overview](../66_mentor_course_analytics/02_Overview.md) — course-level learning-event analytics là miền riêng.
- [API #21 progress](../21_users_me_progress/02_Overview.md), [API #37 detail progress](../37_users_me_progress_course/02_Overview.md) và [API #62 roster](../62_mentor_course_students/02_Overview.md) — precedent có giới hạn; không thay contract #67.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [response helper](../../../app/core/responses.py), [middleware](../../../app/core/middleware.py), [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprints ở [PLAN_RESULT](./PLAN_RESULT.md).

## Tables read

- `courses`, `enrollments`, `users`, `lessons`, `lesson_progress` — legacy BIGINT read candidates only; actual schema and query remain unverified.
- `course_enrollments`, `lessons`, `lesson_progress_facts`, `progress_snapshots`, `learner_profiles` — V1-PILOT UUID candidates; not compatible with int64 path without an approved mapping.
- API #9's `lessons` PUBLISHED result is current source evidence for API #9, not runtime proof for API #67.

## Tables write

N/A — READ-ONLY API. API #67 không tạo, sửa hoặc xóa dữ liệu.

## Mục chú ý

- Giữ contract trực tiếp `ApiEnvelope<Page<Course>>`; Course không có Student progress fields nên đây là DISCREPANCY với AC-26.
- PageMeta yêu cầu page/size nhưng API #67 không khai báo query parameter; không tự thêm page/size hoặc pagination default.
- Candidate response `StudentCourseProgress` ở [04_Response](./04_Response.md) chỉ là DERIVED proposal và cần contract approval.
- Để đồng bộ với #65, candidate tính summary từ cùng tập lesson PUBLISHED và công thức đang DERIVED ở #65; #67 thêm chi tiết mỗi lesson.
- #67 đọc state progress hiện tại; không tính lại learning events hoặc dùng progress state làm nguồn cho #66.
- Candidate roster membership phải theo cùng eligibility policy của #65; enrollment status và Mentor assignment chưa được chốt.
- API #37 trong AC-18 có scope lesson + quiz + assignment; AC-26 không nêu các loại đó. Candidate #67 giữ lesson-level để phù hợp nhóm #65–#67, cần xác nhận nếu muốn mở rộng.
- Current auth helper chỉ có Student guard; Mentor guard/identity mapping chưa có source. Middleware allowlist chưa có path #67.

## Assumptions

- DERIVED: candidate detail gồm summary và một item cho mỗi lesson PUBLISHED, cùng sort order với API #9.
- DERIVED: lesson không có progress row được hiển thị là NOT_STARTED với progress_percent bằng 0.
- DERIVED: summary dùng cùng denominator/formula với #65; formula chưa được domain owner phê duyệt.
- Không chọn schema legacy hay V1-PILOT làm live schema; không tạo SQL vật lý hoặc giả định unique progress row.

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #67 | AC-26 | Catalog trả Page<Course>; AC yêu cầu tiến độ một Student. | Contract trực tiếp không thể biểu diễn drill-down. |
| PageMeta | Request #67 | Schema có page/size nhưng request không có pagination input. | Không có cách client yêu cầu trang tiếp theo. |
| Legacy DDL | V1-PILOT DDL | BIGINT user/lesson progress khác UUID enrollment/facts/snapshots. | Chưa thể chốt một truy vấn vật lý cho path int64. |
| API #25/AC-14 | #67 query | Progress update có percent/completed intent nhưng physical mapping và unique user/lesson key chưa được xác nhận. | Field/formula candidate có thể không tương thích với live data. |
| #65/#66/#67 catalog | AC-26 | Cả ba response trực tiếp là Page<Course> dù phục vụ ba kết quả khác nhau. | Cần owner cập nhật đồng bộ contract trước implementation. |

## Security note

- Xác minh role Mentor và quyền course trước khi đọc learner progress.
- Kiểm tra Student thuộc cùng roster/eligibility scope với #65; không dùng student_id path làm căn cứ quyền duy nhất.
- Mentor assignment, principal-to-ID mapping, learner visibility và thứ tự 403/404 chưa được xác nhận.
- Chỉ trả UserSummary tối thiểu theo candidate; không lộ email, quiz answers hoặc assignment submission content.

## Performance note

- Candidate trả tất cả lesson PUBLISHED trong course vì request không có pagination; số lượng lớn có thể làm response không giới hạn.
- Không có freshness, snapshot, cache, SLA hoặc consistency boundary được định nghĩa.
- Legacy DDL không khai báo unique `(user_id, lesson_id)`; duplicate progress rows có thể làm sai summary nếu chưa có policy.

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
