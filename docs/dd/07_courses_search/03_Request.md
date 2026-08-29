---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `GET` |
| URI | `/api/v1/courses/search` |
| Character encoding | `UTF-8` |
| Content-Type | `N/A — request không có body` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | `No` | `N/A — public endpoint` | Không yêu cầu Bearer token | [`0.1`](./05_Data_Mapping.md#01-public-endpoint) |
| 2 | Content type | `Content-Type` | `No` | `N/A — request không có body` | GET không có request body theo contract | [`1.1`](./05_Data_Mapping.md#11-get-request-header) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có path parameter | `N/A` |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Search keyword | `q` | `string` | `No` | `TBD` | `TBD` | Trimmed text | `TBD — keyword length chưa đặc tả` | `N/A — blank means no text predicate` | Contains, không phân biệt hoa thường trên `courses.name` khi có giá trị | [`2.1`](./05_Data_Mapping.md#21-validate-q) |
| 2 | Category filter | `category` | `int64` | `No` | `TBD` | `TBD` | Integer | `TBD — category relation chưa có source` | `N/A` | Filter category theo contract; predicate physical đang TBD | [`2.2`](./05_Data_Mapping.md#22-validate-category) |
| 3 | Page number | `page` | `int32` | `No` | `1` | `TBD` | Integer | `>= 1` design-only | `1` | Trang cần lấy | [`2.3`](./05_Data_Mapping.md#23-validate-page) |
| 4 | Sort expression | `sort` | `string` | `No` | `TBD` | `TBD` | String | `TBD — allow-list chưa đặc tả` | `N/A — default order TBD` | Thứ tự sắp xếp qua mapping allow-list, không nhận raw SQL | [`2.4`](./05_Data_Mapping.md#24-validate-sort) |

> API #7 không nhận query `size`; backend dùng page size design-only `20`.

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | GET endpoint không có request body | `N/A` |

> Mỗi field phải nằm trên một row riêng. Không gộp nhiều field trong một row.

## Ví dụ Request

```http
GET /api/v1/courses/search?q=programming&page=1&sort=name_asc HTTP/1.1
Host: api.example.test
Accept: application/json
```

> `sort=name_asc` chỉ là giá trị minh họa; allow-list thực tế cần được xác nhận trước implementation.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Danh sách vùng merge</summary>

- `S16:T16`
- `U16:V16`
- `W18:X18`
- `W19:X19`
- `U19:V19`
- `S19:T19`
- `U18:V18`
- `S17:T17`
- `S18:T18`
- `AK18:BA18`
- `S15:T15`
- `U15:V15`
- `W15:X15`
- `U14:V14`
- `W14:X14`
- `W17:X17`
- `S13:T14`
- `U17:V17`
- `W16:X16`
- `Y13:AA14`
- `AB14:AD14`
- `AE14:AG14`
- `AB13:AG13`
- `AH13:AJ14`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 2 | `L2` | GET/POST |  |
| 3 | `B3` | URI |  |
| 4 | `B4` | Code ký tự |  |
| 4 | `L4` | UTF-8 |  |
| 6 | `B6` | Request header |  |
| 11 | `B11` | Request data |  |
| 25 | `B25` | Ví dụ về Request data |  |

</details>
