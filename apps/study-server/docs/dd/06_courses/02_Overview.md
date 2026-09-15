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
| API ID | `6` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/courses` |
| Purpose | `Nạp danh sách khóa học công khai theo filter và pagination` |
| Consumer/Actor | `Guest / course discovery UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public catalog` |
| Basis | `DIRECT — approved design contract + AC-03 + DB_UNICA_ERD` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect được source xác nhận` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #6 endpoint, query, response và business codes.
- [`AC-03 Xem danh sách khóa học`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — public course precondition, published filter, filter/pagination flow và empty state.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — `courses` fields và `courses.mentor_id → users.id`.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `courses` — đọc course public và pagination result.
- `users` — đọc `mentor` qua `courses.mentor_id`.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- `AC-03 yêu cầu hệ thống có khóa học ở trạng thái công khai; flow hiển thị filter/pagination cho Guest.`
- `Chỉ lấy course có status = PUBLISHED; không trả draft/private course.`
- `Query category được giữ theo contract nhưng ERD chưa có bảng hoặc quan hệ category–course.`
- `page, size và sort là optional; contract chưa đặc tả default, range hoặc sort allow-list.`
- `HTTP 200 là protocol status; không thêm HTTPStatus vào JSON envelope.`

## Assumptions

- `courses.name` được map sang `Course.title` vì contract dùng tên logic title còn ERD dùng physical column name.`
- `mentor` là field bắt buộc của Course nên dùng INNER JOIN tới users; dữ liệu thiếu mentor được coi là lỗi integrity và đi tới 500.`
- `Khi không có record phù hợp, trả 200 với data.items = []; quy ước total_pages cho empty page vẫn là TBD.`
- `Course.category` là optional và được omit cho tới khi có source xác nhận quan hệ category–course.`

## Conflicts

- `DISCREPANCY/TBD: contract có query category và Course.category nhưng DB_UNICA_ERD chưa có bảng/khóa category.`
- `DISCREPANCY/TBD: contract dùng Course.title; ERD dùng courses.name, mapping được ghi nhận là alias logic.`
- `DISCREPANCY/TBD: page/size default, min/max, sort allow-list và empty total_pages chưa được contract xác nhận.`
- `RUNTIME_STATUS: chưa có runtime/OpenAPI course endpoint được xác minh; DD là design-only.`

## Security note

- `Endpoint public nhưng chỉ expose course có status PUBLISHED.`
- `Không trả raw SQL, stack trace, credentials hoặc internal storage detail.`
- `sort không được nội suy trực tiếp vào SQL; allow-list/mapping cần được xác nhận trước implementation.`

## Performance note

- `Pagination được áp dụng khi page/size có mặt; count query phải dùng cùng status/category filter.`
- `Index, cache policy, page-size limit và sort strategy chưa được source xác nhận.`

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
