---
title: "Response"
order: 4
dd_id: "90"
api_name: "Xóa quiz"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success HTTP status | 200 `DESIGN_RESOURCE_DELETED` |
| Direct response type | `ApiEnvelope<DeleteResult>` theo catalog #90. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | Catalog | N/A | Branch 5 | 200 success; 401/403/404/422/500 errors | N/A | Giữ exact status set. |
| 2 | `success` | Success flag | `success` | boolean | No | Envelope | N/A | Branch 5 | true success; false error | Required | ApiEnvelope field. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | N/A | Branch 5 | Exact code theo branch | Required | Không tạo code mới. |
| 4 | `message` | Message | `message` | string | No | API #90 view | N/A | Branch 5 | `Quiz deleted.` | Runtime text; catalog không cố định wording | Không trả raw DB error. |
| 5 | `data` | Delete result | `data` | object | No | Completed delete operation | N/A | Branch 5.1 | Một `DeleteResult` | Required on success | Physical source phụ thuộc nhánh. |
| 5.1 | `data.id` | Quiz ID | `id` | int64 | No | Legacy `quizzes` candidate | `id` | Q1 / branch 5.1 | Target quiz ID | Required | Candidate BIGINT mapping; live schema chưa xác minh. |
| 5.2 | `data.status` | Delete status | `status` | literal `"deleted"` | No | Reusable `DeleteResult` | N/A | Branch 5.1 | Constant lowercase literal | Required | DIRECT schema. |
| 5.3 | `data.deleted_at` | Deletion timestamp | `deleted_at` | date-time | No | Legacy `quizzes` candidate / database clock | `updated_at` hoặc `CURRENT_TIMESTAMP` | Branch 5.1 | Soft/repeat: `updated_at`; hard delete: `CURRENT_TIMESTAMP` returned by DELETE | Required | Runtime mapping là local source; legacy `TIMESTAMP` candidate không lưu timezone nên offset/RFC3339 normalization vẫn chưa chốt. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope convention | N/A | Branch 5 | Empty object candidate | `{}` candidate | Không có pagination/dependency payload. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Current trace middleware | `X-Trace-Id` hoặc generated | Branch 5 | Propagate hoặc generate UUID | Required | Route #90 dùng trace middleware hiện hành. |

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_DELETED",
  "message": "Quiz deleted.",
  "data": {
    "id": 501,
    "status": "deleted",
    "deleted_at": "2026-10-24T10:30:00"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000090"
}
```

Timestamp minh họa local runtime serialization. Runtime dùng DB `updated_at` cho nhánh soft/repeat và `CURRENT_TIMESTAMP` từ hard-delete statement. Legacy DDL dùng `TIMESTAMP` không có timezone; chuẩn hóa offset theo `date-time` contract chưa được xác minh.

## Ví dụ lỗi — HTTP 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Quiz not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000090"
}
```

Error response của API #90 dùng `data:null` theo `error_response`; focused HTTP tests kiểm tra trường này.

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
