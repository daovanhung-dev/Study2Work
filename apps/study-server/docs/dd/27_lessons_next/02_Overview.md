---
title: "Overview"
order: 2
dd_id: "27"
api_name: "Tìm bài tiếp theo theo curriculum"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 27 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/lessons/{lesson_id}/next |
| Purpose | Tìm Lesson kế tiếp theo curriculum để điều hướng sau khi xem nội dung lesson hiện tại; thuật toán chọn chưa được nguồn chốt. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student; AC-15 yêu cầu Student có quyền xem lesson. Predicate và cách kiểm tra khi gọi trực tiếp chưa được xác nhận. |
| Basis | DIRECT — API catalog và AC-15; mapping lessons là candidate từ DB design. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET chỉ đọc theo contract. |
| Side effects | N/A — không có mutation hoặc external side effect được mô tả. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — method, path, Student Bearer, Lesson response và các status/business code của API #27.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-15 precondition “Student có quyền xem lesson” và postcondition hiển thị điều hướng bài tiếp theo.
- [AC-15 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — node API #27 và bước “Đọc thứ tự curriculum”; diagram không mô tả predicate hoặc nhánh terminal.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md), [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) và [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — candidate lessons fields/relationship; design-only.
- [API #9 curriculum Data Mapping](../09_courses_curriculum/05_Data_Mapping.md) — adjacent design precedent cho sort_order/status; không tự động xác lập policy cho API #27.
- [Current router](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — tìm trạng thái wiring hiện tại.

## Tables read

- lessons — candidate source cho current lesson và Lesson response; query API #27 chưa được xác nhận.
- courses và enrollments — có thể liên quan entitlement/publish policy; API #27 không chỉ định predicate hoặc query đọc các bảng này.

## Tables write

- N/A — read-only API; không có DB mutation.

## Mục chú ý

- Contract khai báo HTTP 200 DESIGN_RESOURCE_RETRIEVED và các lỗi 401/403/404/500 với business code tương ứng.
- AC-15 diagram đặt API #27 sau khi đọc lesson resources và ghi “Đọc thứ tự curriculum”; thứ tự gọi từ client không xác lập authorization cho lời gọi API độc lập.
- Reusable Lesson gồm id, course_id, title, content?, video_url?, order và status; status enum values không được liệt kê trong catalog.
- DB design ghi lessons.sort_order là thứ tự bài trong curriculum; checked-in DDL đặt default 0 nhưng không tạo unique key cho thứ tự.
- Checked-in DDL cho lessons.course_id không ghi NOT NULL, trong khi ERD mô tả quan hệ course là bắt buộc và logical Lesson.course_id là required.
- Không có bằng chứng về live schema, query API #27 hoặc runtime route.

## Assumptions

- Giữ đúng path, actor, response type và status/business-code set trong API catalog.
- Chỉ ghi lessons là candidate read source; không chốt SQL, filter, tie-break hoặc behavior khi không có next lesson.
- Các giá trị minh họa trong JSON không định nghĩa enum hoặc lesson-selection policy.

## Conflicts

- SOURCE_REQUIRED: “Đọc thứ tự curriculum” không định nghĩa same-course predicate, thứ tự tăng, tie-break, status filter hoặc kết quả cuối curriculum.
- SOURCE_REQUIRED: Student entitlement, JWT identity binding, publish rule và 403/404 masking chưa được đặc tả.
- DISCREPANCY: Logical Lesson yêu cầu course_id; checked-in DDL để lessons.course_id nullable. Live schema chưa được xác minh.
- UNWIRED / NOT_FOUND: Không tìm thấy route, module hoặc test API #27 trong Study runtime hiện tại.

## Security note

- Không nhận user_id từ client; request chỉ có lesson_id.
- Không suy đoán JWT claim name, enrollment policy hoặc publish predicate.
- Không coi client đã gọi API #22/#24 trước đó là bằng chứng cho authorization của API #27 khi được gọi trực tiếp.

## Performance note

- Contract không quy định latency, cache, index, pagination hoặc query plan.
- Không đề xuất index hoặc SQL tối ưu khi predicate/order chưa được xác nhận.
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
