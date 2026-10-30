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
| Purpose | AC-26 yêu cầu tổng hợp hoạt động học của một course. Runtime cục bộ hiện tổng hợp dấu truy cập lesson từ trạng thái tiến độ legacy; đây là proxy, không phải event history. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT; shared guard yêu cầu role MENTOR. |
| Authorization | Runtime cục bộ chỉ cho Mentor trực tiếp sở hữu course theo courses.mentor_id. Đây là fallback DERIVED từ legacy DDL, không xác nhận assignment hoặc schema live. |
| Basis | Endpoint, actor, input, success/error set DIRECT từ diagram/catalog. Aggregate learning events DIRECT từ AC-26. Ba chỉ số proxy và response object DERIVED do không có learner event ledger. |
| Status | Draft — Needs Confirmation |
| Current runtime state | SOURCE_BACKED locally; route, module và HTTP tests được thêm trong task hiện tại. Fake DB tests không xác minh schema live/deployment. |
| Transaction | N/A — API chỉ đọc. |
| Side effects | Không mutation và không gọi #65/#67 server-to-server. |

## Sources

- API catalog và reusable schemas — #65–#67, ApiEnvelope<T>, Page<T>, PageMeta và Course.
- AC/API index và AC-26 activity diagram — thứ tự #65 progress roster → #66 Aggregate learning events → chọn Student → #67 progress detail.
- DB table guide — lesson_progress là progress state; last_accessed_at là mốc truy cập gần nhất.
- Legacy Study DDL — courses.mentor_id, lessons.course_id/status và lesson_progress.user_id/lesson_id/last_accessed_at.
- V1-PILOT DDL — UUID progress facts/snapshots cùng last_event_id marker; không có event row history và khác key type với API int64.
- API #65 — owner check và PUBLISHED lesson convention; #67 vẫn là endpoint drill-down riêng.

## Tables/entities đọc

- courses — tìm course và kiểm tra direct owner qua id, mentor_id.
- lessons — nối lesson vào course và chỉ lấy status PUBLISHED.
- users — xác nhận actor có role STUDENT.
- lesson_progress — lấy cặp user_id/lesson_id cùng last_accessed_at hiện có.
- Không có bảng learning-event ledger được xác nhận trong hai DDL đã rà soát.
- Không dùng last_event_id, progress_snapshots, audit_events hoặc outbox_events làm event history.

## Tables/entities ghi

N/A — READ-ONLY API. Không có INSERT, UPDATE hoặc DELETE.

## Mục chú ý

- Diagram/catalog khai báo ApiEnvelope<Page<Course>>, nhưng Page<Course> không có analytics fields. Local runtime trả một summary object để thực hiện mục tiêu AC-26; đây là DISCREPANCY và DERIVED response, không thay catalog contract.
- Diagram yêu cầu aggregate learning events; DDL không lưu các event rows. Runtime vì vậy trả tracked_lesson_accesses: số cặp Student/lesson phân biệt có last_accessed_at; không gọi chỉ số này là event count.
- students_with_activity đếm Student phân biệt trong các cặp proxy có dấu truy cập; không phải enrollment count.
- last_activity_at là MAX(last_accessed_at) của các cặp được chọn; đây là mốc gần nhất còn lưu trong progress state.
- Request không có query hoặc page/size. Không thêm pagination hay time-window filter.
- Owner scope dùng courses.mentor_id theo legacy DDL; assignment và live DB chưa xác nhận.
- Middleware design path #66 được thêm cùng route. Shared auth helper có Mentor guard; shared error helper serializes missing error data as null.

## Local DERIVED activity projection

| Field | Định nghĩa runtime | Giới hạn |
|---|---|---|
| tracked_lesson_accesses | COUNT của các cặp user_id/lesson_id phân biệt trên lesson PUBLISHED với last_accessed_at khác null. | Đếm cặp tiến độ có mốc truy cập, không đếm số lần truy cập hoặc learning events. |
| students_with_activity | COUNT DISTINCT user_id trong các cặp trên, với users.role = STUDENT. | Không chứng minh Student còn enrollment ACTIVE. |
| last_activity_at | MAX last_accessed_at trên các cặp trên; null khi không có cặp. | Chỉ là dấu thời gian gần nhất còn lưu ở current-state progress. |
| Window | Toàn bộ dấu thời gian hiện lưu; request không có from/to. | DERIVED; không phải retention-bounded event history. |
| Response shape | MentorCourseActivityAnalytics object trong ApiEnvelope. | DERIVED để đáp ứng mục tiêu AC; direct catalog vẫn Page<Course>. |

## Processing

1. Xác thực Bearer JWT và role Mentor trước database.
2. Parse raw course_id thành signed int64; giá trị không parse/range được trả catalog 404.
3. Tìm course; trả 404 nếu không có, 403 nếu mentor_id không trùng JWT sub.
4. Aggregate các cặp Student/lesson trên PUBLISHED lessons, có last_accessed_at, đồng thời lặp owner predicate trong SQL.
5. Trả count 0 và timestamp null khi không có activity proxy; mapping/query lỗi trả safe 500.
6. Không đọc/ghi event, audit, outbox hoặc progress snapshot.

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| AC-26 mục tiêu | DDL được rà soát | AC yêu cầu learning events; DDL chỉ có current progress/access state. | Runtime chỉ có thể cung cấp proxy và phải giữ discrepancy. |
| Diagram/catalog response | Mục tiêu AC-26 | Page<Course> không biểu diễn analytics. | Local summary object là DERIVED; contract cần được owner xác nhận. |
| PageMeta | Request #66 | Có metadata pagination nhưng không có page/size request. | Runtime summary không dùng pagination. |
| Legacy DDL | V1-PILOT DDL | BIGINT relationships khác UUID/versioned facts. | API #66 dùng legacy source pattern cùng API #65; không kết hợp schema pilot. |

## Reliability and security

- Tổng hợp theo toàn bộ dấu truy cập còn lưu; chưa có window, retention, cache hoặc freshness SLA.
- Không suy luận tần suất truy cập, retry, event taxonomy hoặc lịch sử đã bị ghi đè.
- Xác minh role và direct course owner trước khi trả aggregate.
- Không trả raw learner identifiers, payload, SQL hoặc stack trace.

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
