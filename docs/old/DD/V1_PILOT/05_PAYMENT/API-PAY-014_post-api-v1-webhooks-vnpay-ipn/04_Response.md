---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: "markdown"
dd_id: "API-PAY-014"
api_name: "POST /api/v1/webhooks/vnpay/ipn"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
| ---: | --- |
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json; charset=utf-8` |
| HTTP status | Source-confirmed by branch; it is not a JSON response field. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `success` | Success | `success` | `boolean` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | Fixed by branch | N/A | BD §2.1 envelope. |
| 2 | `businessCode` | Business code | `businessCode` | `string` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | Source-confirmed or SOURCE_REQUIRED | N/A | BD §2.1 envelope. |
| 3 | `message` | Safe message | `message` | `string` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | Safe localized message | N/A | BD §2.1 envelope. |
| 4 | `data` | Response data | `data` | `object \| array \| null` | Yes | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | xác nhận theo yêu cầu nhà cung cấp | SOURCE_REQUIRED for nested shape | Catalog output phrase retained below. |
| 5 | `meta` | Metadata | `meta` | `object` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | Pagination/field errors when applicable | {} | BD §2.1 envelope. |
| 6 | `traceId` | Trace ID | `traceId` | `string` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | Trace propagation/generation | N/A | BD §2.1 envelope. |

## Output contract from API catalog

> xác nhận theo yêu cầu nhà cung cấp

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "<SOURCE_REQUIRED>",
  "message": "<SOURCE_REQUIRED>",
  "data": {},
  "meta": {},
  "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "PAYMENT_AMOUNT_MISMATCH",
  "message": "<SOURCE_REQUIRED>",
  "data": null,
  "meta": {
    "fieldErrors": []
  },
  "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/04_Response.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `2.Response`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
