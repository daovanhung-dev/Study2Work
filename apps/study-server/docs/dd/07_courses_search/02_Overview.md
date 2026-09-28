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
| API ID | `7` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/search` |
| Purpose | `Tìm course public theo từ khóa, page và sort` |
| Consumer/Actor | `Guest / course discovery UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public catalog` |
| Basis | `DIRECT — approved design contract + AC-04 + DB_UNICA_ERD` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect` |

## Sources

- [`00_AC_API_INDEX.md`](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API #7 endpoint, query, response và business codes.
- [`AC-04 Tìm kiếm khóa học`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — Guest precondition, debounce/normalize, published-course search và empty state.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — `courses` fields và `courses.mentor_id → users.id`.
- [`createDD-markdown skill`](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — cấu trúc 8 file DD.

## Tables read

- `courses` — đọc published course và count.
- `users` — đọc mentor summary qua `courses.mentor_id`.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- `AC-04` yêu cầu kết quả phù hợp từ khóa/bộ lọc cho Guest và UI có thể debounce/normalize trước khi gọi API.
- Chỉ lấy course có `status = PUBLISHED`; không trả draft/private course.
- Khi `q` có giá trị, backend trim/lowercase và tìm contains không phân biệt hoa thường trên `courses.name` bằng parameter binding.
- Khi `q` thiếu hoặc rỗng sau trim, bỏ text predicate và trả published courses theo filter còn lại.
- `page` mặc định `1`; page size cố định là `20` vì contract không có query `size`.
- `category` nếu được gửi sẽ trả `422 DESIGN_VALIDATION_ERROR` trước khi query vì quan hệ category–course chưa source-backed.
- `sort` dùng allow-list `id|name|price|created_at` với direction `asc|desc` và format `field:direction`.
- Sort mặc định là `c.created_at DESC, c.id ASC`.
- Published course thiếu mentor được phát hiện qua `LEFT JOIN` integrity check và map thành `500 DESIGN_INTERNAL_ERROR`.
- HTTP `200` là protocol status; không thêm `HTTPStatus` vào JSON envelope.

## Assumptions

- `page = 1` khi query không gửi `page`.
- `size = 20` là fixed page size cho `PageMeta.size` và `total_pages`.
- `q` được trim và lowercase trước khi áp dụng contains predicate.
- `Course.title` map từ physical `courses.name`.
- `Course.mentor` là object bắt buộc; implementation dùng `LEFT JOIN users` để phát hiện mentor thiếu và trả lỗi integrity `500`.
- Empty result trả `200` với `data.items = []` và `total = 0`; gợi ý UI thuộc AC-04, không thêm field ngoài contract.

## Conflicts

- `DISCREPANCY: contract có category filter và Course.category nhưng DB_UNICA_ERD chưa có bảng hoặc quan hệ category–course; runtime từ chối category bằng 422.`
- `RESOLVED_FOR_IMPLEMENTATION: sort dùng lại allow-list và default order source-backed của API #6.`
- `RESOLVED_FOR_IMPLEMENTATION: q search dùng LOWER(c.name) LIKE :q_pattern; query page/count dùng cùng predicate.`
- `RUNTIME_STATUS: route, focused tests và current source đã được verify; live DB metadata chưa được verify.`

## Security note

- Endpoint public nhưng chỉ expose course ở trạng thái `PUBLISHED` và mentor summary cần thiết.
- Không trả password, raw SQL, stack trace, secret hoặc internal storage detail.
- Không nội suy trực tiếp `sort` hoặc `q` vào SQL; dùng parameter binding và allow-list cho sort.

## Performance note

- Query page và count phải dùng cùng published/search/filter predicates.
- `LIMIT = 20` và `OFFSET = (page - 1) * 20` theo design-only default.
- Index/search strategy, cache policy và live database availability chưa được source xác nhận.

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
