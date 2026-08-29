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
| Purpose | `Tìm course public theo từ khóa và filter` |
| Consumer/Actor | `Guest / course discovery UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public catalog` |
| Basis | `DIRECT — approved design contract + AC-04 + DB_UNICA_ERD` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #7 endpoint, query, response và business codes.
- [`AC-04 Tìm kiếm khóa học`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — Guest precondition, debounce/normalize, published-course search và empty state.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — `courses` fields và `courses.mentor_id → users.id`.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `courses` — đọc published course và count.
- `users` — đọc mentor summary qua `courses.mentor_id`.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- `AC-04` yêu cầu kết quả phù hợp từ khóa/bộ lọc cho Guest và UI có thể debounce/normalize trước khi gọi API.
- Chỉ lấy course có `status = PUBLISHED`; không trả draft/private course.
- Khi `q` có giá trị, tìm contains không phân biệt hoa thường trên `courses.name`.
- Khi `q` thiếu hoặc rỗng sau trim, bỏ text predicate và trả published courses theo filter còn lại.
- `page` mặc định `1`; page size cố định design-only là `20` vì contract không có query `size`.
- `category` có trong contract nhưng quan hệ category–course chưa tồn tại trong ERD; không dựng JOIN hoặc cột giả.
- `sort` chỉ được map qua allow-list an toàn; allow-list và thứ tự mặc định chưa được contract xác nhận.
- HTTP `200` là protocol status; không thêm `HTTPStatus` vào JSON envelope.

## Assumptions

- `page = 1` khi query không gửi `page`.
- `size = 20` là default design-only cho `PageMeta.size` và `total_pages`.
- `q` được trim và case-fold trước khi áp dụng contains predicate.
- `Course.title` map từ physical `courses.name`.
- `Course.mentor` là object bắt buộc nên dùng `INNER JOIN users`; thiếu mentor của published course đi tới lỗi integrity `500`.
- Empty result trả `200` với `data.items = []` và `total = 0`; gợi ý UI thuộc AC-04, không thêm field ngoài contract.

## Conflicts

- `DISCREPANCY/TBD: contract có category filter và Course.category nhưng DB_UNICA_ERD chưa có bảng hoặc quan hệ category–course.`
- `DISCREPANCY/TBD: contract có sort nhưng chưa đặc tả allow-list, mapping hoặc default order.`
- `DESIGN-ONLY: contains/case-insensitive search trên courses.name được chốt theo yêu cầu authoring, chưa runtime-verified.`
- `RUNTIME_STATUS: chưa có runtime/OpenAPI course-search endpoint được xác minh.`

## Security note

- Endpoint public nhưng chỉ expose course ở trạng thái `PUBLISHED` và mentor summary cần thiết.
- Không trả password, raw SQL, stack trace, secret hoặc internal storage detail.
- Không nội suy trực tiếp `sort` hoặc `q` vào SQL; dùng parameter binding và allow-list cho sort.

## Performance note

- Query page và count phải dùng cùng published/search/filter predicates.
- `LIMIT = 20` và `OFFSET = (page - 1) * 20` theo design-only default.
- Index/search strategy, cache policy, sort allow-list và maximum page chưa được source xác nhận.

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
