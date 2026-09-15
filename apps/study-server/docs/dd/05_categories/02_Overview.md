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
| API ID | `5` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/categories` |
| Purpose | `Nạp danh mục đang hoạt động cho bộ lọc course/search` |
| Consumer/Actor | `Guest / course discovery UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public catalog metadata` |
| Basis | `DIRECT — approved design contract + AC-03 + AC-04` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect được source xác nhận` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #5 endpoint, query, response và business codes.
- [`AC-03 Xem danh sách khóa học`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — cache-first category loading và active-category read trước course list.
- [`AC-04 Tìm kiếm khóa học`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — category loading trước course search.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `N/A — physical Categories table/store chưa được ERD/contract xác nhận`.

## Tables write

- `N/A — read-only API; không có DB mutation được source xác nhận`.

## Mục chú ý

- `API #5 được dùng chung bởi AC-03 và AC-04 để nạp filter category.`
- `UI áp dụng cache-first: cache hit thì không gọi API; cache miss mới gọi GET /api/v1/categories.`
- `API chỉ có query locale?; không thêm page/size/sort vào request contract.`
- `HTTP 200 là protocol status; không thêm HTTPStatus vào JSON envelope.`

## Assumptions

- `Page<Category> được biểu diễn như một trang ngầm định vì request không có page/size: page=1, size=total, total_pages=1.`
- `Danh sách category rỗng vẫn trả 200 với items=[] và tổng bằng 0; đây là quy ước design-only vì diagram không khai báo nhánh 404.`
- `meta` dùng `{}` vì API #5 không khai báo metadata ngoài pagination nằm trong data.`

## Conflicts

- `DISCREPANCY/TBD: list_api.md nêu Categories là schema design-only và chưa xác nhận physical persistence mapping.`
- `DISCREPANCY/TBD: locale không có enum, format chi tiết hoặc translation fallback được đặc tả.`
- `DISCREPANCY/TBD: cache TTL, cache headers và invalidation policy chưa được source xác nhận.`

## Security note

- `Không yêu cầu Bearer token; chỉ trả category metadata public.`
- `Không trả raw SQL, stack trace hoặc internal storage detail trong response.`

## Performance note

- `Category lookup là read-only; cache-first ở UI có thể giảm request lặp.`
- `Không tự đặt cache TTL, page-size limit hoặc refresh interval.`


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
