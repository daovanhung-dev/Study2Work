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
| URI | `/api/v1/courses/{course_id}/curriculum` |
| Character encoding | `UTF-8` |
| Content-Type | `N/A — request không có body` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | `No` | `N/A — public endpoint` | Không yêu cầu Bearer token | [`0.1`](./05_Data_Mapping.md#01-public-endpoint) |
| 2 | Content type | `Content-Type` | `No` | `N/A — request không có body` | GET không có request body theo contract | [`1.1`](./05_Data_Mapping.md#11-get-request-path) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Course ID | `course_id` | `int64` | `Yes` | `N/A — chưa đặc tả` | `N/A — chưa đặc tả` | Integer path segment | `N/A` | `N/A` | ID của khóa học cần lấy curriculum | [`1.1/1.2`](./05_Data_Mapping.md#11-get-request-path) |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có query pagination/filter | `N/A` |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | GET endpoint không có request body | `N/A` |

> Mỗi field phải nằm trên một row riêng. Không gộp nhiều field trong một row.

## Ví dụ Request

```http
GET /api/v1/courses/101/curriculum HTTP/1.1
Host: api.example.test
Accept: application/json
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Bản ghi đối chiếu</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 3 | `B3` | URI |  |
| 6 | `B6` | Request header |  |
| 11 | `B11` | Request data |  |

</details>
