---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
---

# Response

## Format

| Thuộc tính | Giá trị |
| --- | --- |
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json; charset=utf-8` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | `success` | Success flag | `success` | boolean | No | N/A | N/A | [4.1](./05_Data_Mapping.md#dm-4-1) | Fixed `true` hoặc `false` theo branch | Không omit | Canonical envelope. |
| 2 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | [4.1](./05_Data_Mapping.md#dm-4-1) | Success code SOURCE_REQUIRED; error code lấy từ Error case | Không blank | Success code chưa được định nghĩa. |
| 3 | `message` | Localized message | `message` | string | No | N/A | N/A | [4.1](./05_Data_Mapping.md#dm-4-1) | Message theo businessCode | Không blank | Exact message SOURCE_REQUIRED; không lộ email tồn tại. |
| 4 | `data` | Response data | `data` | object | Yes | N/A | N/A | [4.1](./05_Data_Mapping.md#dm-4-1) | Object mapping | Error có thể `null`; success object | Canonical envelope. |
| 4.1 | `data.verificationExpiresAt` | Verification expiry | `verificationExpiresAt` | string(date-time) | No | email_verification_tokens | expires_at | [4.1](./05_Data_Mapping.md#dm-4-1) | ISO-8601 UTC có `Z` | Không omit ở success mới/replay | Exact field được endpoint row nêu. Duplicate generic branch value policy SOURCE_REQUIRED. |
| 5 | `meta` | Metadata | `meta` | object | No | N/A | N/A | [4.1](./05_Data_Mapping.md#dm-4-1) | Fixed object | `{}` khi không có metadata | Canonical envelope. |
| 5.1 | `meta.fieldErrors` | Field validation errors | `fieldErrors` | array<object> | Yes | N/A | N/A | [4.3](./05_Data_Mapping.md#dm-4-3) | Generated from validation | Omit khi không có field error | Mỗi item có field/code/message theo canonical envelope. |
| 6 | `traceId` | Trace ID | `traceId` | string | No | N/A | N/A | [4.1](./05_Data_Mapping.md#dm-4-1) | Generated request trace ID | Không blank | Không chứa PII. |

> Success HTTP status, success businessCode và exact message là SOURCE_REQUIRED; ví dụ chỉ là Draft illustration.
> Không trả user/email existence, password hash, token hash, raw token hoặc audit payload.

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "SOURCE_REQUIRED",
  "message": "Generic registration accepted",
  "data": {
    "verificationExpiresAt": "2026-08-02T12:45:00Z"
  },
  "meta": {},
  "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "PASSWORD_POLICY_FAILED",
  "message": "SOURCE_REQUIRED",
  "data": null,
  "meta": {
    "fieldErrors": [
      {
        "field": "password",
        "code": "PASSWORD_POLICY_FAILED",
        "message": "SOURCE_REQUIRED"
      }
    ]
  },
  "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10"
}
```

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
