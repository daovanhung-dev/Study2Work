---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "37"
api_name: "Lấy tiến độ chi tiết course"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 37 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/users/me/progress/{course_id} |
| Purpose | Đọc tiến độ chi tiết của Student trong một khóa học theo AC-18. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Student role theo API catalog; điều kiện enrollment/course access chưa được chốt. |
| Basis | APPROVED_DESIGN_CONTRACT; AC-18; candidate DB design |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — Study Server hiện chưa có route/module/test cho API #37. |
| Transaction | N/A — GET read-only |
| Side effects | N/A — không có mutation được định nghĩa. |

## Sources

- [API catalog — API #37](../../../../../docs/lists/list_api.md) — method, path, actor, input, response và error contract.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — mục AC-18 xác nhận actor, precondition, postcondition và ba API của flow.
- [AC-18 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — luồng gọi API #37 sau khi chọn course và mô tả tổng hợp lesson, quiz, assignment.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — quan hệ và candidate columns cho progress/assessment.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate physical relations; ghi chú không có bảng course_progress.
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql) — design evidence, chưa xác minh với live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — ApiEnvelope, error envelope và trace ID.
- API #21 progress DD, [Cover](../21_users_me_progress/00_Cover.md) và [Response](../21_users_me_progress/04_Response.md) — adjacent draft có ghi nhận gap UserProfile/progress.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py) và [responses](../../../app/core/responses.py) — source hiện hành, không phải implementation của API #37.
- Canonical template: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/` — tám sheet theo thứ tự baseline.

## Tables read

- lesson_progress — candidate progress theo lesson của user.
- lessons — candidate relation lesson tới course.
- courses — candidate resource lookup theo course ID.
- quiz_attempts — candidate attempt/progress theo user và quiz.
- quizzes — candidate relation quiz tới course.
- assignment_submissions — candidate submission/progress theo user và assignment.
- assignments — candidate relation assignment tới course.

## Tables write

- N/A — API GET; không có insert, update hoặc delete.

## Mục chú ý

- AC-18 yêu cầu hiển thị dashboard tiến độ và thành tích; sau aggregate tiến độ tổng quan, Student chọn course để gọi API #37.
- AC-18 mô tả aggregate lesson + quiz + assignment progress, nhưng không định nghĩa output fields, công thức hoặc tập dữ liệu.
- Catalog giữ nguyên response `ApiEnvelope<UserProfile>`; schema UserProfile không có field tiến độ. Đây là contract gap, không được lấp bằng field suy đoán.
- Các bảng trong mục Tables read chỉ là nguồn đọc ứng viên theo DB design. Query, predicate và DDL đều DESIGN_ONLY; chưa có query runtime hay live schema verification.

## Assumptions

- Giữ nguyên contract API #37 trong catalog: Student Bearer JWT, path course_id:int64!, ApiEnvelope<UserProfile>, cùng HTTP/business code đã được liệt kê.
- Chỉ mô tả các bảng nguồn ứng viên được AC-18 và DB design hỗ trợ; không chốt SQL hoặc công thức tổng hợp.
- Mọi payload tiến độ, predicate truy cập khóa học và hành vi khi chưa có dữ liệu cần được xác nhận trước khi DD chuyển Ready/Final.

## Conflicts

- Catalog dùng ApiEnvelope<UserProfile>, trong khi AC-18 yêu cầu chi tiết tiến độ theo course; UserProfile không có field tiến độ.
- UserProfile có bio?:string, nhưng users trong DB guide/checked-in DDL không có cột bio; API #37 không có nguồn xác nhận cho projection UserProfile.
- ERD/table guide mô tả các quan hệ candidate; checked-in DDL cho phép NULL ở một số FK mà table guide mô tả là bắt buộc.

## Security note

- Path không nhận user_id; danh tính phải gắn với principal đã xác thực cho route /me, còn cách ánh xạ claim JWT sang user ID cần được xác nhận.
- Student role có trong catalog. Enrollment, ownership, course visibility và cách phân biệt 403 với 404 chưa được đặc tả.
- Không được dùng course_id từ path làm căn cứ duy nhất để tiết lộ tiến độ của user khác.

## Performance note

- Không có query hoặc workload/index target đã được xác nhận cho API #37.
- Candidate source có thể cần nhiều join/aggregate; cần chốt query shape và giới hạn kích thước course trước khi tối ưu hoặc cam kết latency.

---
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
