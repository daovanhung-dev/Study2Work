---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "38"
api_name: "Lấy achievement/badge nếu có"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 38 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/users/me/achievements |
| Purpose | Đọc các achievement đã mở khóa của Student theo AC-18. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Student role theo API catalog; course-level access chưa được đặc tả. |
| Basis | APPROVED_DESIGN_CONTRACT; AC-18; DB design evidence |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — Study Server hiện chưa có route/module/test cho API #38. |
| Transaction | N/A — GET read-only |
| Side effects | N/A — không có mutation được định nghĩa. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #38 contract, reusable Achievement/Page schemas và business codes.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-18 actor, precondition, postcondition và API list.
- [AC-18 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — flow progress, API #37 course detail, API #38 unlocked achievements.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — V1 note rằng achievements/analytics được tính từ dữ liệu hiện có; không chỉ định award rules/source projection.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — ERD V1 không có physical achievement table.
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql) — schema design trong repository, không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, error data và trace ID.
- [Progress overview DD](../21_users_me_progress/05_Data_Mapping.md) — giữ API #38 là lời gọi achievements riêng trong AC-18.
- [Progress detail DD](../37_users_me_progress_course/OPEN_QUESTIONS.md) — ghi nhận các bảng lesson/quiz/assignment chỉ là nguồn progress candidate.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py) và [response helper](../../../app/core/responses.py) — current runtime boundary; không phải implementation của API #38.
- Canonical DD template: .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — tám sheet theo thứ tự baseline.

## Tables read

- Chưa xác định bảng nguồn achievement.
- lesson_progress, lessons, quiz_attempts, quizzes, assignment_submissions và assignments chỉ là nguồn dữ liệu ứng viên nếu award rules xác nhận; không được coi là query/API #38 đã duyệt.

## Tables write

- N/A — API GET; không có insert, update hoặc delete.

## Mục chú ý

- API ID #38 là GET /api/v1/users/me/achievements thuộc AC-18. AC-38 là use case Admin báo cáo tác động cộng đồng, không phải API này.
- API catalog được đánh dấu APPROVED_DESIGN_CONTRACT; giữ nguyên Student Bearer JWT, query course_id?:int64, ApiEnvelope<Page<Achievement>> và đúng status/business code 200/401/403/500.
- Schema Achievement trong catalog có id, code, title, awarded_at và course_id?; không có persistence mapping được xác nhận.
- DB design nói achievements được tính từ dữ liệu hiện có và không mặc định thêm bảng; tiêu chí trao và nguồn projection chưa được đặc tả.
- Page response có PageMeta nhưng request API #38 chỉ khai báo course_id; không tự thêm page, size, sort hoặc default.
- Course filter, behavior với achievement không gắn course và empty result cần xác nhận trước khi DD chuyển Ready/Final.

## Assumptions

- Giữ nguyên API #38 trong approved catalog; DD này không sửa API catalog, AC diagrams, ERD, DDL hoặc runtime.
- Ghi schema Achievement/Page theo catalog; các giá trị ví dụ trong Response chỉ minh họa kiểu dữ liệu.
- Các progress/assessment tables chỉ là read candidates, không phải nguồn award đã được xác nhận.
- Phạm vi là tài liệu design-only; trạng thái Draft — Needs Confirmation; không tạo ZIP theo workflow Study Server.

## Conflicts

- Catalog định nghĩa logical Achievement response nhưng DB guide/ERD V1 không có bảng achievements; DB guide chỉ nói tính achievements từ dữ liệu hiện có, không định nghĩa rule hoặc projection.
- Catalog response là Page<Achievement> với PageMeta, trong khi request API #38 không khai báo pagination controls.
- course_id? có ở request và Achievement schema nhưng chưa rõ filter có bao gồm achievement toàn cục không gắn course.

## Security note

- Route /me chỉ cho Student theo catalog; dữ liệu dự kiến phải gắn với principal đã xác thực.
- Current shared auth helper chuẩn hóa JWT sub thành numeric user_id và kiểm tra Student role, nhưng API #38 chưa gọi helper vì chưa có route.
- Predicate course ownership/enrollment/access chưa được API catalog hoặc AC-18 xác định.

## Performance note

- Chưa có query shape, result-size limit, pagination input, index target hoặc latency target cho API #38.
- Không cam kết strategy sắp xếp hoặc paging khi request contract chưa định nghĩa controls.
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
