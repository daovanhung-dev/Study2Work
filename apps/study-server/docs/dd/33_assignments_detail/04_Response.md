---
title: "Response"
order: 4
dd_id: "33"
api_name: "Lấy đề bài/rule/deadline"
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
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5.1 | Fixed by response branch. | N/A | Success 200; errors follow API #33 catalog. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5.1 | true on success; false on error. | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5.1 | `DESIGN_RESOURCE_RETRIEVED` on success. | N/A | API catalog. |
| 4 | message | Message | message | string | No | N/A | N/A | 5.1 | Safe client message. | Exact wording/localization SOURCE_REQUIRED. | ApiEnvelope field. |
| 5 | data.id | Assignment ID | id | int64 | No | assignments | id | 4 | Candidate direct projection. | N/A | Logical Assignment field; design-only mapping. |
| 6 | data.course_id | Course ID | course_id | int64 | No | assignments | course_id | 4 | Candidate direct projection. | Contract requires a value; checked-in DDL permits NULL. | `DISCREPANCY / DESIGN_ONLY`; live schema not verified. |
| 7 | data.title | Title | title | string | No | assignments | name | 4 | Map physical `name` to logical `title`. | N/A | Logical/physical names differ in DB table notes. |
| 8 | data.description | Description | description | string | Yes | assignments | description | 4 | Candidate direct projection. | Omit/null behavior SOURCE_REQUIRED. | Nullable in checked-in DDL. |
| 9 | data.due_at | Deadline | due_at | date-time | Yes | assignments | due_at | 4 | Candidate timestamp projection. | Omit/null behavior and timezone serialization SOURCE_REQUIRED. | DDL uses `TIMESTAMP`; no timezone rule is defined. |
| 10 | data.max_score | Maximum score | max_score | decimal-string | No | assignments | max_score | 4 | Candidate decimal projection. | Contract requires a value; DDL permits NULL and sets default 10. | `DISCREPANCY / DESIGN_ONLY`; decimal formatting not specified. |
| 11 | meta | Metadata | meta | object | No | N/A | N/A | 5.1 | Envelope metadata. | Empty object when no metadata is supplied. | ApiEnvelope field. |
| 12 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 5.1 | Propagated/generated under shared API convention. | N/A | API #33 runtime serialization is not verified. |

### Ví dụ thành công — Assignment có deadline minh họa

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Assignment retrieved (illustrative text).",
  "data": {
    "id": 3301,
    "course_id": 701,
    "title": "Bài tập minh họa",
    "description": "Nội dung đề bài minh họa.",
    "due_at": "2026-10-20T23:59:00Z",
    "max_score": "10.00"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000033"
}
~~~

> Giá trị là dữ liệu minh họa. Ví dụ không chốt timezone/format timestamp, precision decimal hoặc cách biểu diễn field optional khi NULL.

### Ví dụ lỗi — Assignment không tìm thấy

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Assignment not found (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000033"
}
~~~

> Error example chỉ minh họa envelope và code trong catalog; message chính xác chưa được quy định.
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

