---
title: "Overview"
order: 2
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 21 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/users/me/progress |
| Purpose | Lấy tiến độ tổng hợp theo user theo AC-18; AC-13 dùng progress để ghép với danh sách khóa học ở client |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | role=Student |
| Basis | DIRECT — approved design contract; AC-13/AC-18; checked-in DB design |
| Status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Transaction | N/A — read-only API |
| Side effects | N/A — không có DB mutation hoặc external side effect |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #21 contract, reusable schemas và business codes.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — mapping API trong AC-13 và AC-18.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-13 client merge và AC-18 luồng tổng hợp, chi tiết khóa học, achievement.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — quan hệ lesson_progress, lessons, courses và trạng thái query DESIGN_ONLY.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in DDL; không phải bằng chứng live schema.
- [v1.py](../../../app/api/v1.py) — current Study route inventory; không có API #21.
- [auth.py](../../../app/utils/auth.py) — shared Bearer/JWT và Student guard hiện tại; API #21 chưa gọi helper.
- [responses.py](../../../app/core/responses.py) — current Study response envelope; không chứng minh response runtime API #21.
- [API #20 DD](../20_users_me_courses/05_Data_Mapping.md) — AC-13 gọi riêng API #21 rồi client ghép course + progress.
- [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — quy tắc authoring DD.

## Tables read

- lesson_progress — DB design ghi API #21/#37 là SELECT DESIGN_ONLY; các cột/điều kiện của query API #21 chưa được xác nhận.
- lessons — quan hệ từ lesson_progress.lesson_id tới lessons.id; việc join runtime cho API #21 chưa được xác nhận.
- courses — lessons.course_id liên kết tới courses.id; việc dùng để gom tiến độ theo course chưa được xác nhận.
- quizzes và assignments — AC-18 nêu progress của chúng ở nhánh API #37 chi tiết; không suy ra API #21 đọc các bảng này.

## Tables write

- N/A — read-only API.

## Mục chú ý

- Giữ nguyên response ApiEnvelope<UserProfile> theo catalog; không đổi thành progress schema, Page<T> hoặc thêm field.
- Catalog ghi nguyên query phrase course_id list hoặc aggregate?:string; kiểu/grammar query và semantics chưa thể suy ra.
- AC-13 gọi API #20 để nạp Course, gọi API #21 để đọc lesson progress/completion, sau đó ghép course + progress tại client.
- AC-18 mô tả API #21 aggregate progress theo user; API #37 đọc tiến độ chi tiết lesson + quiz + assignment; API #38 đọc achievements. Ranh giới UI/API không làm rõ field hoặc công thức của API #21.
- DB_UNICA_TABLES.md đánh dấu query API #21/#37 là DESIGN_ONLY. Checked-in DB.sql chỉ là DDL trong repository; live DB chưa được kiểm tra.
- Không có route, module, query hoặc test hiện tại cho API #21. Runtime status: UNWIRED / NOT_FOUND.

## Assumptions

- Đây là DD-only; không sửa runtime, API catalog, diagram, DB schema hoặc migration.
- lesson_progress là bảng thiết kế có căn cứ trực tiếp cho progress; quan hệ lessons/courses chỉ được ghi như relationship evidence, chưa phải query đã chốt.
- Không tự tính phần trăm, trạng thái, phạm vi khóa học, dữ liệu quiz/assignment, query predicate, response fields hoặc empty result shape.
- Hành vi ghép Course + progress tại client được giữ theo AC-13; không chuyển merge vào API #21.

## Expected behavior

- Student gọi endpoint tổng hợp theo contract hiện có.
- Theo AC-18, response được dùng để hiển thị tiến độ tổng quát; khi chọn khóa học, flow tiếp tục bằng API #37 và có thể nạp achievement bằng API #38.
- Theo AC-13, API #20 và API #21 là hai request riêng; client ghép course và progress rồi hiển thị khóa học cùng phần trăm hoàn thành.
- Wire fields, query semantics, công thức tính và empty response chưa được đặc tả.

## Current behavior

- API #21 không có route/module/query/test đã xác minh trong Study Server.
- Shared auth helper hiện có thể xác thực Bearer/JWT, parse sub thành user ID số dương và yêu cầu role STUDENT; endpoint #21 chưa được wiring với helper này.
- Shared response helper hiện tạo envelope success/businessCode/message/data/meta/traceId; runtime mapping của API #21 chưa tồn tại.
- DB query trong tài liệu là DESIGN_ONLY; live schema và dữ liệu không được kiểm tra.

## Conflicts

- DISCREPANCY: Catalog response là ApiEnvelope<UserProfile>, trong khi AC-13/AC-18 yêu cầu thông tin progress; không có schema progress riêng cho API #21.
- DISCREPANCY: Query phrase “course_id list hoặc aggregate?:string” không xác định field grammar hoặc kiểu dữ liệu của course_id list.
- SOURCE_REQUIRED: Aggregate scope/formula, nguồn quiz/assignment, current-user predicate, empty-result wire shape và chính sách query validation.
- RUNTIME_STATUS: API #21 route/module/query/test là UNWIRED / NOT_FOUND; query DB chỉ DESIGN_ONLY.

## Security note

- Design contract yêu cầu Bearer JWT và role Student.
- Shared helper hiện xác thực token, parse JWT sub thành positive integer và kiểm tra STUDENT; API #21 chưa gọi helper này.
- API #21 không được đọc progress user khác; predicate gắn JWT user ID vào lesson_progress.user_id là candidate từ /me intent nhưng chưa được xác nhận trong endpoint source.

## Performance note

- DB design có quan hệ lesson_progress → lessons → courses; chưa có query, index, group/filter, cache hoặc performance target runtime được xác minh.
- Không đặt batching, pagination, aggregation strategy hoặc caching rule khi contract chưa chỉ định.

---
## Phụ lục đối chiếu template Markdown

- Template: [02_Overview.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md).
- Sheet nguồn: Overview.
