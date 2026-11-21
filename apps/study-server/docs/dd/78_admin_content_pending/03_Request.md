---
title: "Request"
order: 3
dd_id: "78"
api_name: "Lấy pending content"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | `/api/v1/admin/content/pending` |
| Character encoding | UTF-8 |
| Content-Type | N/A — không có request body. |
| Authentication | Bearer JWT |
| Role | Admin theo catalog. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|
| 1 | Authorization | `Authorization` | Yes | Bearer JWT | Shared `validate_current_user_request(..., role="ADMIN")` xác thực principal trước khi parse query hoặc đọc queue. | [Data Mapping](./05_Data_Mapping.md#0-check-quyen) |
| 2 | Trace ID | `X-Trace-Id` | No | UUID | Shared middleware validate hoặc tạo correlation ID; không phải field nghiệp vụ. | [Data Mapping](./05_Data_Mapping.md#0-check-quyen) |

## Path parameters

N/A — catalog không khai báo path parameter.

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Content type | `type` | string | No | Không áp dụng | Không áp dụng | Query string | Mọi chuỗi; exact match | Không có | Exact filter trên `contents.content_type`; không whitelist enum hoặc normalize. | [Data Mapping](./05_Data_Mapping.md#1-validate-data-input) |
| 2 | Course ID | `course` | int64 | No | -2^63 | 2^63-1 | Signed 64-bit integer | Mọi signed-int64 | Không có | Exact filter trên `contents.course_id`; sai format/range trả derived 422. | [Data Mapping](./05_Data_Mapping.md#1-validate-data-input) |
| 3 | Page | `page` | int32 | No | 1 | 2^31-1 | Số nguyên 32-bit | Positive int32 | 1 — DERIVED | Page 1-based; fixed size 20, `id ASC`; sai format/range trả derived 422. | [Data Mapping](./05_Data_Mapping.md#1-validate-data-input) |

Catalog không khai báo `size` hoặc `sort`; không thêm hai query này vào contract.

## Request body

N/A — catalog và AC-33 diagram không khai báo request body.

## Ví dụ Request data

```text
GET /api/v1/admin/content/pending?type=SOURCE_REQUIRED&course=501&page=1
Authorization: Bearer <admin-access-token>
```

`type=QUIZ` minh họa một exact string filter từ current test fixture, không xác nhận bộ ContentType enum. Page default/range là fallback DERIVED; response runtime dùng Page trong khi catalog còn khai báo Content đơn.

## Quy tắc input đang mở

- `type` giữ nguyên chuỗi và exact-match `content_type`; enum members/casing vẫn chưa được owner xác nhận.
- `course` phải parse thành signed int64; không áp đặt positive-only rule; malformed/overflow trả derived 422.
- `page` là positive int32; default 1, size cố định 20 và page ngoài range trả derived 422 theo convention API #73.
- Catalog #78 không liệt kê HTTP 422; runtime dùng 422 `DESIGN_VALIDATION_ERROR` như derived fallback cho numeric query validation. Cần owner đồng bộ catalog.
- Runtime đã chọn `Page<Content>` DERIVED để biểu diễn queue; giữ catalog trực tiếp như cũ và yêu cầu owner đồng bộ cardinality/pagination.

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
- `U13:X13`
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
| 7 | `B7` | Name |  |
| 7 | `J7` | Field name |  |
| 7 | `V7` | Giá trị |  |
| 7 | `AK7` | Giải thích |  |
| 8 | `B8` | Contents type |  |
| 8 | `J8` | Content-Type |  |
| 8 | `V8` | application/json |  |
| 8 | `AK8` | Thực hiện request bằng json data |  |
| 9 | `B9` | Basic authen |  |
| 9 | `J9` | Authorization |  |
| 9 | `V9` | Token |  |
| 11 | `B11` | Request data |  |
| 12 | `B12` | No |  |
| 12 | `C12` | Key name |  |
| 12 | `S12` | Nội dung check |  |
| 12 | `AK12` | Giải thích |  |
| 13 | `S13` | Bắt buộc |  |
| 13 | `U13` | Số ký tự |  |
| 13 | `Y13` | Loại ký tự |  |
| 13 | `AB13` | Format |  |
| 13 | `AH13` | Giá trị hợp lệ |  |
| 14 | `C14` | Logic |  |
| 14 | `K14` | Vật lý |  |
| 14 | `U14` | Tối thiểu |  |
| 14 | `W14` | Tối đa |  |
| 15 | `B15` | 1 |  |
| 15 | `S15` | ○ |  |
| 15 | `U15` | 1 |  |
| 15 | `W15` | 20 |  |
| 15 | `Y15` | halfsize |  |
| 16 | `B16` | 2 |  |
| 16 | `S16` | ○ |  |
| 16 | `U16` | 1 |  |
| 16 | `W16` | 8 |  |
| 16 | `Y16` | halfsize |  |
| 16 | `AB16` | datetime |  |
| 16 | `AE16` | yyyyMMdd |  |
| 17 | `S17` | ○ |  |
| 17 | `U17` | 1 |  |
| 17 | `W17` | 1 |  |
| 17 | `Y17` | halfsize |  |
| 17 | `AB17` | numberic |  |
| 17 | `AH17` | 2,3,4 |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | 1 |  |
| 18 | `Y18` | fullsize |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | 1 |  |
| 25 | `B25` | Ví dụ về Request data |  |
| 26 | `L26` | { |  |
| 27 | `M27` | "tnorsh_pln_id" : "0000000001", |  |
| 28 | `M28` | "yt_ymd":" 20201001", |  |
| 29 | `M29` | "yt_hmi":" 0830", |  |
| 30 | `M30` | "excpt_id":" 001", |  |
| 31 | `M31` | "bik_desc":" 計画削除" |  |
| 32 | `L32` | } |  |

</details>
