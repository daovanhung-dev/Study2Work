---
title: "Request"
order: 3
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---


# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `GET` |
| URI | `/api/v1/mentor/notifications/{notification_id}/status` |
| Character encoding | UTF-8 |
| Content-Type | N/A — GET không có request body |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | Có | Bearer JWT | Catalog yêu cầu Mentor; shared guard lấy principal numeric từ JWT. | 0.1 |
| 2 | Trace ID | `X-Trace-Id` | Không | UUID nếu gửi | Trace header theo API Guidelines. | 0.2 |

## Path parameters

| No | Logical name | Field | Type | Required | Range/format | Rule | Data Mapping reference | Status |
|---:|---|---|---|---:|---|---|---|---|
| 1 | Notification ID | `notification_id` | int64 | Có | Signed decimal int64 | Kiểu DIRECT; malformed/out-of-range path trả catalog 404 theo local fallback; 0/negative được parse nhưng tự nhiên không match BIGINT identity. | 1.1, 2.1 | Parse rule DERIVED. |

## Query parameters

N/A — catalog không khai báo query parameter.

## Request body

N/A — GET endpoint không có request body.

## Quy ước query/path

- Không thêm `operation_id`, `course_id`, `sender_id`, `status`, page hoặc filter ngoài path.
- Không lấy owner từ input; sender scope dùng principal JWT.
- API #63 `meta.notification_ids` cung cấp path key cho notification vừa dispatch; Operation UUID không thay thế key này.
- Dùng raw path string ở route để giữ lỗi parse trong catalog error set và khai báo OpenAPI schema là integer/int64.

## Validation

| Field/condition | Check | Status |
|---|---|---|
| Bearer/JWT | Token hợp lệ và có role MENTOR trước DB access. | Auth/role DIRECT; shared helper current source. |
| `notification_id` | Parse signed int64; overflow/non-decimal path trả 404 `DESIGN_RESOURCE_NOT_FOUND`. | int64 DIRECT; HTTP mapping DERIVED vì catalog không liệt kê 400/422. |
| Notification sender | `sender_id` phải bằng numeric Mentor JWT `sub`; khác sender trả 403. | DERIVED từ API #63 insert binding và Mentor ownership pattern. |
| Operation/outbox | Notification cần có UUID `operation_id` và tối thiểu một delivery row. | DERIVED local API #63 dispatch boundary; nếu thiếu, 404 status resource. |

## Ví dụ request

```http
GET /api/v1/mentor/notifications/123/status HTTP/1.1
Host: api.example.test
Authorization: Bearer <token>
```

`123` chỉ minh họa int64 path; giá trị thực tế được lấy từ API #63 `meta.notification_ids[]`.

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
