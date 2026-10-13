---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 20 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/users/me/courses |
| Purpose | Nạp danh sách khóa học Student đã đăng ký |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | role=Student |
| Basis | DIRECT — approved design contract; AC-13 flow; checked-in DB design evidence |
| Status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Transaction | N/A — read-only API |
| Side effects | N/A — không có DB mutation hoặc external side effect |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #20 contract, shared schemas và business codes.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API mapping trong AC-12 và AC-13.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-13 sequence: courses, progress, client merge và empty state.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — Enrollment/Course relations và trạng thái query design.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in columns cho courses, enrollments và lesson_progress.
- [v1.py](../../../app/api/v1.py) — current route inventory; chưa có endpoint #20.
- [auth.py](../../../app/utils/auth.py) — current reusable Bearer/JWT và Student guard.
- [responses.py](../../../app/core/responses.py) — current Study response envelope implementation.
- [API #4 UserProfile model](../../../app/modules/guest/api_04_users_me/models.py) — current profile model; API #20 remains unwired.
- [API #19 DD](../19_courses_enrollments/05_Data_Mapping.md) — enrollment create flow; không mở rộng mutation sang API #20.

## Tables read

- enrollments — quan hệ user/course; API catalog DB guide đánh dấu query #20 là DESIGN_ONLY.
- courses — thông tin khóa học; AC-13 yêu cầu JOIN với Enrollment.
- users — chưa được xác định là bảng đọc của endpoint; không suy ra chỉ từ response type UserProfile.

## Tables write

- N/A — read-only API.

## Mục chú ý

- Giữ response type ApiEnvelope<UserProfile> đúng catalog; không thay bằng Page<Course> hoặc thêm progress.
- AC-13 gọi API #21 riêng để lấy progress rồi client ghép với khóa học. API #21 nằm ngoài scope DD này.
- Contract không xác định status filter áp lên Enrollment hay Course, giá trị hợp lệ, cách phân trang, thứ tự kết quả hoặc shape khi rỗng.
- Current helper có thể parse JWT sub là số dương và yêu cầu role STUDENT; việc dùng user ID đó làm predicate enrollments.user_id của API #20 chưa được runtime xác minh.
- Catalog UserProfile gồm bio optional; current API #4 UserProfile model không khai báo bio. API #20 chưa có model riêng nên không kế thừa im lặng một trong hai shape.
- Không có route, module hoặc test hiện tại cho API #20. Trạng thái runtime: UNWIRED / NOT_FOUND.

## Assumptions

- Đây là DD-only, không sửa catalog, diagram, schema, migration hoặc runtime.
- Enrollment và Course là các bảng thiết kế cần đọc theo AC-13; câu query và projection chi tiết chưa được xác nhận.
- Không áp đặt filter Course PUBLISHED, enum status, default, page size, order, hoặc response pagination.
- Empty state là hành vi UI trong diagram; wire response rỗng của endpoint chưa được mô tả.

## Conflicts

- DISCREPANCY: API #20 trả ApiEnvelope<UserProfile> theo catalog, trong khi tên API và AC-13 yêu cầu danh sách khóa học.
- DISCREPANCY: AC-13 ghép Course + progress tại client; không có căn cứ để chuyển trách nhiệm merge hoặc % completion vào API #20.
- DISCREPANCY: reusable UserProfile schema trong catalog và current API #4 Pydantic model khác nhau ở bio; API #20 chưa có model để xác nhận shape runtime.
- SOURCE_REQUIRED: status filter, pagination, empty response và predicate từ JWT sang enrollments.user_id.
- RUNTIME_STATUS: API #20 không có route/module/query/test đã xác minh; DB query chỉ DESIGN_ONLY.

## Security note

- Design contract yêu cầu Bearer JWT và role Student.
- Current shared helper xác thực token, parse subject số dương thành user ID và kiểm tra STUDENT; API #20 chưa gọi helper này.
- Response của API #20 không được tự thêm thông tin profile hoặc user ngoài schema contract đang khai báo.

## Performance note

- AC-13 mô tả join Enrollment + Course; không có query, index, sort hoặc page-size policy runtime đã xác minh.
- Không đưa ra LIMIT/OFFSET, caching hoặc performance target khi contract chưa chỉ định.

---
## Phụ lục đối chiếu template Markdown

- Template: [02_Overview.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md).
- Sheet nguồn: Overview.
