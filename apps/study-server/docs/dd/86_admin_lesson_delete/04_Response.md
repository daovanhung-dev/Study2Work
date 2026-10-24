---
title: "Response"
order: 4
dd_id: "86"
api_name: "Xóa lesson"
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
| Success HTTP status | 200 DESIGN_RESOURCE_DELETED |
| Direct response type | ApiEnvelope<DeleteResult> theo catalog #86. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | Catalog | N/A | Branch | 200 success; 401/403/404/422/500 errors | N/A | Exact catalog status set. |
| 2 | success | Success flag | success | boolean | No | Envelope | N/A | Branch | true success; false error | Required | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog | N/A | Branch | Exact code per branch | Required | Không tạo code mới. |
| 4 | message | Message | message | string | No | Application | N/A | Branch | Safe localized text | Exact wording chưa đặc tả | Không trả raw DB error. |
| 5 | data | DeleteResult | data | object | No | Approved deletion operation | N/A | 5.1 | Một DeleteResult | Required on success | Physical mapping/source chưa được chọn. |
| 5.1 | data.id | Lesson ID | id | int64 | No | Approved lesson target | id candidate | 5.1 | Target ID sau mutation thành công | Required | Path ID direct; persisted target mapping candidate. |
| 5.2 | data.status | Delete status | status | literal "deleted" | No | Reusable DeleteResult | N/A | 5.1 | Exact lowercase literal deleted | Required | DIRECT schema literal. |
| 5.3 | data.deleted_at | Deletion timestamp | deleted_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 5.1 | Timestamp persisted by approved delete policy | Required | No legacy/V1 lesson marker; no inferred clock fallback. |
| 6 | meta | Metadata | meta | object | No | Envelope convention | N/A | Branch | Empty object candidate | {} candidate | No pagination/dependency payload. |
| 7 | traceId | Trace ID | traceId | uuid | No | Current trace middleware | X-Trace-Id or generated | 0/Branch | Propagate or generate UUID | Required | Route absent. |

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_DELETED",
  "message": "Đã xóa lesson theo policy.",
  "data": {
    "id": 501,
    "status": "deleted",
    "deleted_at": "2026-10-24T12:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000086"
}
```

Cấu trúc bám DeleteResult trực tiếp. Timestamp minh họa định dạng; nguồn persisted deleted_at chưa được chọn.

## Ví dụ lỗi dependency — HTTP 422 — DERIVED

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Không thể xóa lesson do policy dependency.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000086"
}
```

Đây là ví dụ candidate nếu policy được duyệt chặn xóa khi có progress/reference. Không trả dependency rows hoặc learner data.

API guideline yêu cầu error data:null; current error helper mặc định absent data thành {}. API #86 chưa được wire nên behavior này chưa được kiểm chứng cho endpoint.

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
