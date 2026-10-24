---
title: "Overview"
order: 2
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #65 |
| Module | MENTOR / TEACHING & SUPPORT — AC-26 |
| Method | GET |
| Endpoint | /api/v1/mentor/courses/{course_id}/progress |
| Purpose | Đọc tiến độ tổng hợp của người học trong một course để Mentor xem dashboard lớp. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor theo catalog; quyền trên course và liên kết principal với Mentor ID chưa có runtime source. |
| Basis | Method/path/input/response/status/errors DIRECT từ catalog; roster-level progress DIRECT ở mức mục tiêu AC-26; công thức và response thay thế DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route, module hay focused test API #65 trong Study source. |
| Transaction | N/A — API đọc dữ liệu; consistency/snapshot boundary chưa được quy định. |
| Side effects | Không có mutation hay lời gọi API #66/#67 được đặc tả trong #65. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #65–#67, ApiEnvelope<T>, Page<T>, PageMeta, Course, UserSummary.
- [AC/API index, AC-26](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và thứ tự API #65 → #66 → #67.
- [AC-26 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — mở progress dashboard, tải class progress, tải analytics, chọn Student rồi đọc progress chi tiết.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — #65/#67 có SELECT mapping ở trạng thái DESIGN_ONLY.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT relations courses, enrollments, users, lessons và lesson_progress; không phải live-schema proof.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned progress relations; khác ID contract int64 và không được trộn với legacy model.
- [API #9 curriculum](../09_courses_curriculum/02_Overview.md) và [API #25 progress](../25_lessons_progress/02_Overview.md) — published lesson/progress evidence; không chốt công thức class aggregate.
- [API #46 managed courses](../46_mentor_courses/02_Overview.md) và [API #62 course students](../62_mentor_course_students/02_Overview.md) — Mentor ownership/roster precedent và các identity/pagination gap.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint ở [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- courses — legacy candidate để xác định course và direct owner qua mentor_id.
- enrollments + users — legacy candidate để lập một dòng mỗi learner đã enroll.
- lessons — legacy candidate để đếm lesson thuộc course; lọc PUBLISHED là đề xuất DERIVED từ API #9.
- lesson_progress — legacy candidate chứa status/progress percent; enum, key và quy tắc tổng hợp chưa được xác nhận.
- Các quan hệ trên đều là design evidence; không xác nhận schema live hoặc tính duy nhất/nullable ở production.

## Tables/entities ghi

N/A — READ-ONLY API. Không có INSERT/UPDATE/DELETE được đặc tả.

## Mục chú ý

- Giữ direct contract từ catalog: response ApiEnvelope<Page<Course>>. Schema Course không có learner/progress fields, nên hiện không thể biểu diễn đúng mục tiêu AC-26.
- AC-26 tách #65 roster/progress, #66 learning-event analytics và #67 learner detail. Không nhập logic của hai API sau vào #65.
- Contract khai báo PageMeta nhưng không có query page/size. Đề xuất trả toàn bộ roster trong một page là DERIVED và có rủi ro không giới hạn kích thước.
- Candidate access predicate courses.mentor_id = Mentor principal ID cần xác nhận; assignment và JWT identity mapping chưa có nguồn.
- Không dùng schema UUID/versioned của V1-PILOT như thể tương thích với contract int64.

## Phương án DERIVED để review — không phải wire contract

| Thành phần | Đề xuất đơn giản | Cơ sở/trạng thái |
|---|---|---|
| Item | student:UserSummary, completed_lessons:int32, total_lessons:int32, progress_percent:int32 | Dạng tối thiểu để biểu diễn class progress; DERIVED. |
| Learner set | Một dòng cho mỗi user_id trong enrollment của course | AC-26 nói aggregate enrollment; chưa chốt enrollment status hoặc duplicate policy. |
| Denominator | Số lesson PUBLISHED thuộc course | DERIVED từ visibility của API #9; cần duyệt. |
| Completed | Đếm lesson có lesson_progress.status='COMPLETED' trong tập denominator | DERIVED; enum/status contract chưa được chứng minh. |
| Percent | floor(sum(COALESCE(progress_percent,0)) / total_lessons); trả 0 khi denominator bằng 0 | DERIVED; chưa có rule chính thức. |
| Pagination | Không có input nên đề xuất một page đầy đủ: page=1, size=total; empty: size=0,total_pages=0 | DERIVED; cần quyết định giới hạn/contract mới. |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #65 | AC-26 | Catalog trả Page<Course>; AC cần class progress. | Contract hiện tại không có field learner/progress. |
| PageMeta | Request catalog #65 | Cần page/size/total/total_pages nhưng request không nhận page/size. | Pagination behavior không thể suy ra là bounded. |
| Legacy DDL | V1-PILOT DDL | BIGINT enrollment/progress khác UUID/versioned facts/snapshots. | Không thể coi hai schema là một nguồn mapping. |
| API guidelines | Current helper | Guideline kỳ vọng error data=null; helper hiện chuyển absent data thành {}. | Ghi discrepancy; API #65 chưa có wire behavior. |

## Security note

- Catalog yêu cầu Bearer JWT và role Mentor.
- Xác minh course scope trước khi trả learner roster; không suy ra mentor_id từ path.
- Không tiết lộ course/roster nếu chưa xác định thứ tự 403/404 theo privacy policy.

## Reliability note

- Đây là read-only dashboard query; không kích hoạt tính toán nền hay gửi event được đặc tả.
- Không có freshness/SLA/snapshot contract cho progress cache hoặc learning events.
- Một page không giới hạn có thể tăng tải theo quy mô lớp; cần pagination decision trước runtime implementation.

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
