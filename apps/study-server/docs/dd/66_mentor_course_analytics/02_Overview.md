---
title: "Overview"
order: 2
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #66 |
| Module | MENTOR / TEACHING & SUPPORT — AC-26 |
| Method | GET |
| Endpoint | /api/v1/mentor/courses/{course_id}/analytics |
| Purpose | Cung cấp analytics tổng hợp của learning events trong một course cho dashboard Mentor. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor theo catalog; quyền xem course theo AC-26; Mentor identity và course assignment chưa có runtime source. |
| Basis | Method/path/input/response/status/errors DIRECT từ catalog; mục tiêu aggregate learning events DIRECT từ AC-26; metric cụ thể DERIVED/SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route, module hoặc focused test API #66 trong Study source. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không có mutation; API #66 không gọi #65/#67 server-to-server. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #65–#67, ApiEnvelope<T>, Page<T>, PageMeta, Course, UserSummary.
- [AC/API index, AC-26](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — precondition Mentor có quyền xem course analytics; ba API của flow.
- [AC-26 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — #65 aggregate enrollment/progress → #66 aggregate learning events → chọn Student → #67 đọc progress.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — có SELECT mapping design-only cho #65/#67 progress; không có event analytics mapping cho #66.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — có courses/enrollments/lessons/lesson_progress state; không có learning event history table.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned progress facts/snapshots và event IDs; khác contract int64, không chứng minh có event log hoặc live schema.
- [API #65 overview/response](../65_mentor_course_progress/02_Overview.md) / [response](../65_mentor_course_progress/04_Response.md) — class progress là API riêng và catalog Page<Course> cũng không biểu diễn progress.
- [API #62 overview](../62_mentor_course_students/02_Overview.md) — Mentor course-scope và Page<Course> mismatch precedent.
- [API #21 progress](../21_users_me_progress/02_Overview.md) và [API #25 lesson progress](../25_lessons_progress/02_Overview.md) — current-state progress không đồng nghĩa event history.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [response helper](../../../app/core/responses.py), [middleware](../../../app/core/middleware.py), [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprints ở [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- courses — legacy candidate để tìm course và direct owner; dùng cùng boundary question của #65, chưa phải live mapping.
- Không tìm thấy relation được phê duyệt lưu learning event history trong legacy Study DDL hoặc V1-PILOT.
- lesson_progress và pilot progress facts/snapshots là state/fact snapshots; không mặc nhiên dùng chúng làm event ledger.
- audit_events/outbox_events là cơ chế audit/integration tổng quát; không có evidence rằng chúng ghi learner learning events, nên không dùng làm nguồn analytics #66.

## Tables/entities ghi

N/A — READ-ONLY API. API #66 không tạo, sửa hoặc xóa dữ liệu.

## Mục chú ý

- Giữ response trực tiếp của catalog là ApiEnvelope<Page<Course>>. Course và PageMeta không chứa learning-event metrics; đây là DISCREPANCY với mục tiêu AC-26.
- AC-26 tách riêng class progress (#65), learning-event analytics (#66) và progress một Student (#67). Không đưa progress measures của #65/#67 vào #66.
- PageMeta có page/size nhưng request #66 không có query pagination. Không thêm paging parameters hoặc pagination default.
- Current auth helper chỉ có Student guard; Mentor guard/identity mapping chưa có trong Study source.
- Middleware design-code allowlist chưa có path #66; helper error response mặc định data thành {} khi không truyền giá trị, còn API guideline yêu cầu data:null. Đây là discrepancy có điều kiện cho lần wiring sau.
- V1-PILOT có last_event_id trong progress facts nhưng không có event records để đếm; không suy diễn event history từ ID đó.

## Đề xuất DERIVED để review — không phải wire contract

| Metric đề xuất | Định nghĩa khái niệm | Cơ sở và giới hạn |
|---|---|---|
| total_learning_events | Tổng số learning event của course từ đầu đến hiện tại | DERIVED từ “Aggregate learning events”; event taxonomy/source/dedup/retention chưa có. |
| students_with_learning_events | Số Student duy nhất có ít nhất một learning event của course | DERIVED; event actor-to-Student mapping và eligibility SOURCE_REQUIRED. |
| last_activity_at | Thời điểm lớn nhất của event thuộc course; null khi không có event | DERIVED; event timestamp/source SOURCE_REQUIRED. |
| Time window | All-time-to-date vì request không có from/to | DERIVED đề xuất đơn giản; owner cần xác nhận nếu cần khoảng thời gian. |
| Shape đề xuất | Một summary object CourseLearningAnalytics, không phải collection | DERIVED vì endpoint scoped một course và không có paging/filter; cần sửa contract nếu chấp nhận. |

## Candidate business behavior

1. Xác thực Bearer JWT và role Mentor theo contract.
2. Xác định course trong scope Mentor; predicate và identity mapping cần quyết định.
3. Đọc nguồn learning-event đã được phê duyệt theo course.
4. Tính các metric đã chốt; nếu không có event, trả count bằng 0 và last_activity_at null theo candidate.
5. Trả response theo contract đã được duyệt; hiện catalog Page<Course> không chứa các metrics đề xuất.

Các bước 2–5 chưa có implementation/API #66 source; đây là candidate flow, không phải current behavior.

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #66 | AC-26 | Catalog trả Page<Course>; AC yêu cầu aggregate learning events. | Direct contract không có event metrics. |
| PageMeta | Request catalog #66 | PageMeta cần page/size nhưng request không khai báo pagination. | Không thể tuyên bố paging bounded hay có default. |
| Legacy/V1-PILOT DB | AC-26 | Không có approved learning-event history relation trong reviewed schema artifacts. | Không thể viết physical event query hoặc mapping. |
| API #65/#67 sequence | Catalog | Flow cần progress + analytics + drill-down, nhưng cả ba catalog response đều Page<Course>. | Cần macro-review/contract decision sau khi #67 DD tồn tại. |
| API guidelines | Current helper | Error data:null khác với helper default {}; path #66 chưa thuộc allowlist. | Future wiring phải đồng bộ error mapping. |

## Security note

- Không trả analytics trước khi xác minh role Mentor và course scope.
- Không suy diễn Mentor ID từ path; không trả event data ngoài quyền.
- Không đưa raw event payload, learner identifier không cần thiết, SQL hoặc stack trace vào response.

## Reliability note

- Không có freshness, aggregation schedule, cache, retention, time-window hay latency contract.
- All-time aggregate có thể tăng chi phí khi event volume lớn; cần source/index/snapshot decision trước khi chốt implementation.
- Không tính audit/outbox/progress-state rows như learning events nếu chưa được domain owner chỉ định.

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
