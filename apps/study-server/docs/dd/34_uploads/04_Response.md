---
title: "Response"
order: 4
dd_id: "34"
api_name: "Upload file"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5 | Fixed by branch | N/A | Protocol status, not a JSON property. Success is 201; errors use only catalog statuses 401/403/422/503/500. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5 | true on success; false on error | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5 | Fixed by branch | N/A | Use DESIGN codes from API #34 catalog. |
| 4 | message | Message | message | string | No | N/A | N/A | 5 | Fixed safe message by branch | Text always present | Exact localized wording is not defined. |
| 5 | data | Upload asset | data | object / null | Yes | N/A | N/A | 5 | ApiEnvelope<UploadAsset> on success; null on error | null on error | Error envelope rule from API Guidelines. |
| 5.1 | data.id | Asset ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by logical schema | Catalog does not define an ID generator or physical source. |
| 5.2 | data.name | File name | name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by logical schema | Whether this is the submitted filename or a normalized name is open. |
| 5.3 | data.url | Asset URL | url | uri | No | Object Storage (candidate) | SOURCE_REQUIRED | 4 | Return URL from the storage/upload flow | Required by logical schema | Public URL versus signed URL, expiry and access policy are undefined. |
| 5.4 | data.content_type | Content type | content_type | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by logical schema | Detection/trust policy and supported MIME values are undefined. |
| 5.5 | data.size_bytes | File size in bytes | size_bytes | int64 | No | Upload bytes (candidate) | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by logical schema | Counting/limit rules are not defined. |
| 5.6 | data.status | Upload status | status | UploadStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by logical schema | UploadStatus values and lifecycle are not defined. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 5 | Empty object unless envelope adds supported metadata | {} in examples | No upload-specific metadata shape is defined. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 5 | Request correlation UUID | Always present | API Guidelines require trace propagation. |

## Ví dụ thành công — HTTP 201

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Upload accepted (illustrative text).",
  "data": {
    "id": 34001,
    "name": "example.bin",
    "url": "https://storage.example.test/resource",
    "content_type": "application/octet-stream",
    "size_bytes": 1,
    "status": "SOURCE_REQUIRED"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000034"
}
~~~

All sample values are illustrative. SOURCE_REQUIRED is a visible placeholder, not an allowed UploadStatus; the sample MIME type and URL do not define an allowlist or storage URL policy. The id value does not define how an asset ID is generated.

## Ví dụ lỗi — HTTP 503

~~~json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "Upload dependency unavailable (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000035"
}
~~~

Error example illustrates the shared envelope and catalog code only. Exact provider-failure mapping and message text remain open.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
