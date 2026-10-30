---
title: "Response"
order: 4
dd_id: "62"
api_name: "Lấy tập người nhận"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| HTTP success | 200 `DESIGN_RESOURCE_RETRIEVED` |
| Contract type | `ApiEnvelope<UserSummary[]>` — DERIVED fallback, owner confirmation pending |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | integer | No | N/A | N/A | 5 | Fixed by branch | N/A | Success 200; errors 401/403/404/500. |
| 2 | `success` | Success | `success` | boolean | No | N/A | N/A | 5 | `true` on success | Required | Standard envelope. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | literal | 5 | `DESIGN_RESOURCE_RETRIEVED` | Required | Catalog code retained. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | 5 | Safe success message | Required | Empty roster uses “No students found.” |
| 5 | `data` | Recipient roster | `data` | `UserSummary[]` | No | Query result | distinct rows | 4 | Map each eligible Student once | Empty roster is `[]` | No pagination because request has no page/size input. |
| 5.1 | `data[].id` | User ID | `id` | int64 | No | `users` | `id` | 4 | Direct numeric mapping | Required | Student identity sent to the recipient picker. |
| 5.2 | `data[].full_name` | Full name | `full_name` | string | No | `users` | `full_name` | 4 | Direct mapping | Required | No extra profile fields are exposed. |
| 5.3 | `data[].avatar_url` | Avatar URI | `avatar_url` | uri | Yes | `users` | `avatar_url` | 4 | Direct mapping | Omit when SQL value is NULL | Implementation preserves the stored string; it does not revalidate the URI. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope | N/A | 5 | `{}` | Required | No pagination metadata. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Request trace | trace ID | 5 | Propagate request trace | Required | Also returned in `X-Trace-Id`. |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Students retrieved.",
  "data": [
    {
      "id": 2001,
      "full_name": "Nguyễn An",
      "avatar_url": "https://cdn.example.test/avatar/2001.png"
    },
    {
      "id": 2002,
      "full_name": "Trần Bình"
    }
  ],
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000000"
}
```

Ví dụ chỉ minh họa schema. `avatar_url` bị lược khi nguồn là NULL; response không có trường email hoặc phone.

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Course not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000000"
}
```

## Contract discrepancy

Diagram/catalog ban đầu khai báo `ApiEnvelope<Page<Course>>`. API #62 cần trả learner recipients và không nhận pagination input. Fallback dùng `ApiEnvelope<UserSummary[]>`; API catalog và AC-25 node đã được đồng bộ. Đây là quyết định DERIVED, giữ DD `Draft — Needs Confirmation`.
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
