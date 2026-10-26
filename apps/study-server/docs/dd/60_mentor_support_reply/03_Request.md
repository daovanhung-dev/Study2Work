---
title: "Request"
order: 3
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | POST |
| URI | /api/v1/mentor/support/{request_id}/reply |
| Character encoding | UTF-8 |
| Content-Type | application/json — DERIVED because catalog does not state media type |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Shared MENTOR guard; numeric sub maps to current Mentor user ID. | [Data Mapping](./05_Data_Mapping.md) |
| 2 | Content type | Content-Type | Yes | application/json — DERIVED | Transport candidate for required string fields. | [Data Mapping](./05_Data_Mapping.md) |
| 3 | Trace ID | X-Trace-Id | No | UUID nếu gửi | Middleware validates/creates trace ID. | [Data Mapping](./05_Data_Mapping.md) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Support request ID | request_id | int64 | Yes | Không quy định | Không quy định | Signed 64-bit integer | Số nguyên trong miền int64 | Không có | Khóa request; fallback local là BIGSERIAL từ API #58. | [Data Mapping](./05_Data_Mapping.md) |

## Query parameters

N/A — API không khai báo query parameter.

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|
| 1 | Message | message | string | Yes | Không quy định | Không quy định | Unicode text | N/A | Nonblank string — DERIVED | N/A | Lưu nguyên text; chỉ dùng strip để từ chối rỗng/whitespace-only. Không đặt length limit. | [Data Mapping](./05_Data_Mapping.md) |
| 2 | Attachment references | attachment_refs — DERIVED wire key | string | Yes | N/A | N/A | ASCII JSON text | JSON array of signed int64 UploadAsset IDs — DERIVED from API #47 source | [] nghĩa không đính kèm; IDs unique | Không có | IDs phải resolve tới upload thuộc Mentor, cùng course, purpose LECTURE, status UPLOADED. | [Data Mapping](./05_Data_Mapping.md) |

> Catalog ghi logical label attachment refs:string!. attachment_refs là wire key DERIVED. JSON array string được chọn theo current API #47 source; không sửa API #35 hoặc #47 trong task này.

## Ví dụ Request data

~~~json
{
  "message": "Mình đã gửi hướng dẫn xử lý cho bạn.",
  "attachment_refs": "[81001,81002]"
}
~~~

Không đính kèm: attachment_refs là chuỗi JSON `"[]"`. IDs ví dụ chỉ minh họa; upload không tồn tại hoặc ngoài scope trả lỗi 404 chung.

## Validation

- Thiếu/sai kiểu request_id, message hoặc attachment_refs → 422 DESIGN_VALIDATION_ERROR.
- request_id sai format hoặc vượt signed int64 → 422; zero/negative là giá trị int64 hợp lệ nhưng không khớp BIGSERIAL row thì 404.
- message rỗng hoặc chỉ whitespace → 422; giá trị hợp lệ được lưu nguyên vẹn; không có min/max.
- attachment_refs phải là JSON array gồm unique integer values trong miền signed int64; object/string/null, malformed JSON, float, bool hoặc duplicate → 422.
- [] được chấp nhận. ID hợp lệ về cú pháp nhưng không resolve đúng owner/course/purpose/status → 404 chung; không trả asset URL ngoài scope.

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
