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
| API ID | `8` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}` |
| Purpose | `Lấy thông tin chi tiết của một khóa học công khai` |
| Consumer/Actor | `Guest / course detail UI; Student enrollment flow` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public course access` |
| Basis | `DIRECT — approved API contract + AC-05 + AC-12 + DB_UNICA_ERD` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #8 endpoint, input, `ApiEnvelope<Page<Course>>` và status/error contract.
- [`AC_01_GUEST_ACCOUNT.drawio`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — AC-05 public course detail flow, published visibility và mentor summary.
- [`AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12 pre-enrollment course lookup reuse.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — `courses` fields và `courses.mentor_id → users.id`.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `courses` — đọc course theo `id`, chỉ expose `PUBLISHED`.
- `users` — đọc mentor summary qua `courses.mentor_id`.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- `Course detail UI dùng API này trước khi nạp curriculum/reviews bằng các API riêng.`
- `Contract trả Page<Course> dù endpoint không nhận pagination; DD dùng singleton page.`

## Assumptions

- `Một course thành công được đặt trong `data.items` với pagination cố định page=1, size=1, total=1, total_pages=1.`
- `courses.name` map sang contract field `Course.title` theo alias logic.`
- `Course.mentor` là object bắt buộc; dùng INNER JOIN tới users và không dựng mentor giả.`
- `Course.category` omit vì ERD chưa xác nhận category–course relation.`

## Conflicts

- `DISCREPANCY: diagram ghi nhánh 404/403 cho course không public, nhưng list_api.md chỉ khai báo 404/500; DD tuân theo contract list và gom non-PUBLISHED vào 404.`
- `DISCREPANCY/TBD: contract dùng Course.title, ERD dùng courses.name; mapping được ghi nhận là alias.`
- `RUNTIME_STATUS: chưa runtime/OpenAPI verified; tài liệu là design-only.`

## Security note

- `Endpoint public nhưng chỉ trả course có status = PUBLISHED; không leak draft/private existence.`
- `Không trả raw SQL, stack trace hoặc internal storage detail.`

## Performance note

- `Lookup theo primary key courses.id và join mentor theo users.id.`
- `Index/cache policy chưa được source xác nhận.`

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
