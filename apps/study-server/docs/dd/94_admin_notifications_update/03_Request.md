---
title: "Request"
order: 3
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PUT |
| URI | /api/v1/admin/notifications/{notification_id} |
| Character encoding | UTF-8 |
| Authentication | Bearer JWT |
| Role | Admin theo catalog; runtime dùng shared ADMIN guard. Finer permission chưa xác minh. |
| Content-Type | Catalog không khai báo body; runtime fallback nhận application/json. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description |
|---:|---|---|---:|---|---|
| 1 | Authorization | Authorization | Yes | Bearer <token> | Direct auth contract; role guard chạy trước parse path/body. |
| 2 | Content type | Content-Type | DERIVED | application/json | Cần cho body fallback; không phải body được catalog duyệt. |
| 3 | Trace ID | X-Trace-Id | No | UUID | Correlation theo shared Study convention. |

## Path parameters

| No | Logical name | Physical name | Type | Required | Runtime rule | Status |
|---:|---|---|---|---:|---|---|
| 1 | Notification ID | notification_id | int64 | Yes | Số nguyên dương trong miền int64. | Type DIRECT; positivity/runtime parse DERIVED. |

## Query parameters

Không có query parameter trong catalog hoặc AC-36 diagram.

## Request body

**Direct contract:** Catalog #94 và AC-36 diagram không khai báo request body. Runtime dùng fallback DERIVED `{title, content}` vì đây là hai cột text có thể cập nhật trên legacy BIGINT candidate. Unknown fields bị từ chối; body không đổi recipients, channels hoặc schedule.

| Field | Type | Required | Runtime rule | Status |
|---|---|---:|---|---|
| title | string | Yes | Strict string, nonblank sau kiểm tra `strip()`, tối đa 200 ký tự; giá trị gốc được giữ nguyên. | DERIVED từ legacy `VARCHAR(200)`. |
| content | string | Yes | Strict string, nonblank sau kiểm tra `strip()`; giá trị gốc được giữ nguyên. | DERIVED từ legacy `TEXT`. |
| recipients/segment/channels/scheduled_at | N/A | No | Không được gửi; field ngoài schema trả 422. | Không có physical mapping/scheduler được duyệt. |

### Ví dụ body runtime fallback — DERIVED

~~~json
{
  "title": "Lịch học đã cập nhật",
  "content": "Thời gian học đã được điều chỉnh."
}
~~~

## Thứ tự xử lý và lỗi input

1. Shared ADMIN guard chạy trước khi parse path/body hoặc query database.
2. Path không phải số dương trong int64 hoặc body JSON sai/thiếu/thừa field trả 422 `DESIGN_VALIDATION_ERROR`.
3. `title`/`content` rỗng hoặc chỉ whitespace trả 422; whitespace quanh giá trị hợp lệ không bị trim khi lưu.
4. Body hợp lệ mới bắt đầu transaction và khóa target.
5. Quy tắc trên là runtime fallback DERIVED; catalog/diagram chưa được cập nhật để khai báo body.

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
