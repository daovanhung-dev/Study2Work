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
| API ID | `10` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}/reviews` |
| Purpose | `Lấy danh sách đánh giá/review và replies public của một khóa học` |
| Consumer/Actor | `Guest / course detail UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public course access` |
| Basis | `DIRECT — approved API contract + AC-05 + DB_UNICA_ERD; review/rating parts contain discrepancies` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #10 endpoint, request, `ApiEnvelope<Page<Discussion>>` và status/error contract.
- [`AC_01_GUEST_ACCOUNT.drawio`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — AC-05 precondition course public và flow “Đọc review + aggregate rating”.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `courses`, `discussions`, `users` và quan hệ `parent_id`, `course_id`, `user_id`.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `courses` — kiểm tra `course_id` tồn tại và có `status = 'PUBLISHED'`.
- `discussions` — đọc review gốc và replies theo `parent_id`.
- `users` — map `Discussion.author` và `DiscussionComment.author`.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- API được gọi trong AC-05 sau khi course detail đã xác nhận khóa học public.
- Kết quả không có review vẫn là success `200` với `data.items = []`.
- Pagination dùng `page` từ contract; page size `20` là design-only convention giống API list gần nhất.

## Assumptions

- Review gốc là `discussions.parent_id IS NULL`; chỉ lấy `status = 'ACTIVE'` để không expose nội dung bị ẩn, cần xác nhận.
- Replies là rows có `parent_id` trỏ tới review gốc và cũng được lọc `status = 'ACTIVE'`.
- Sort mặc định `created_at DESC`, tie-break bằng `id DESC`; đây là design-only để pagination deterministic.
- `page` mặc định `1`; `size` không nhận từ client và cố định `20`.

## Conflicts

- `DISCREPANCY: AC-05 yêu cầu aggregate rating và query rating filter, nhưng contract chỉ trả Page<Discussion> và ERD không có cột/bảng rating; DD không thêm field hoặc predicate rating giả.`
- `DISCREPANCY: Discussion.title là required trong contract nhưng ERD discussions không có cột title; giữ row TBD, không suy diễn content thành title.`
- `DISCREPANCY/TBD: Contract ghi literal “rating filter”; DD chuẩn hóa query key minh họa thành rating và ghi rõ cần xác nhận tên vật lý.`
- `DISCREPANCY/TBD: Contract không khai báo 422 cho query malformed; không tự thêm business code hoặc HTTP branch.`
- `RUNTIME_STATUS: chưa runtime/OpenAPI verified; tài liệu là design-only.`

## Security note

- Chỉ đọc review của course `PUBLISHED` và không yêu cầu Bearer token.
- Không trả raw SQL, stack trace hoặc thông tin storage nội bộ.
- Chỉ expose `UserSummary`; không map email/password hoặc cột ngoài contract.

## Performance note

- Course visibility, review page và count query dùng cùng điều kiện scope.
- Comments được nạp theo các review ID của page, tránh join làm nhân bản pagination rows.
- Index/cache policy chưa được source xác nhận.

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
