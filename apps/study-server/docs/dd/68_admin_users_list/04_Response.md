---
title: "Response"
order: 4
dd_id: "68"
api_name: "Lấy danh sách user"
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
| HTTP status | 200 |
| Direct contract type | ApiEnvelope<Page<UserProfile>> theo catalog đã đồng bộ với AC-31 list/pagination. |

## Success response

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5.1 | 200 | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5.1 | true khi thành công | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog | N/A | 5.1 | DESIGN_RESOURCE_RETRIEVED | N/A | Direct success code. |
| 4 | message | Message | message | string | No | N/A | N/A | 5.1 | Users retrieved hoặc No users found | N/A | Exact message chưa được catalog quy định. |
| 5 | data.items[] | User profile | items | UserProfile[] | No | users candidate | Safe projection | 5.1 | Map mỗi row bằng API #04 UserProfile | Empty array khi không có match | Page collection theo AC-31. |
| 5.1 | items[].id | User ID | id | int64 | No | users candidate | id | 4.1 | Integer ID | Bắt buộc | BIGINT candidate; live schema unknown. |
| 5.2 | items[].full_name | Full name | full_name | string | No | users candidate | full_name | 4.1 | Direct value | Bắt buộc | API #04/#14 source model. |
| 5.3 | items[].email | Email | email | email | No | users candidate | email | 4.1 | Direct value | Bắt buộc | PII; chỉ truy cập qua ADMIN guard. |
| 5.4 | items[].role | Role | role | UserRole/string | No | users candidate | role | 4.1 | Stored string | Bắt buộc | Enum members chưa có source; model hiện tại dùng string. |
| 5.5 | items[].avatar_url | Avatar URL | avatar_url | uri? | Yes | users candidate | avatar_url | 4.1 | API #04 model | Serialize null nếu source null | Optional reusable field. |
| 5.6 | items[].phone | Phone | phone | string? | Yes | users candidate | phone | 4.1 | API #04 model | Serialize null nếu source null | PII; optional reusable field. |
| 5.7 | items[].status | Account status | status | UserStatus/string | No | users candidate | status | 4.1 | Stored string | Bắt buộc | Enum members chưa có source; model hiện tại dùng string. |
| 5.8 | items[].created_at | Created time | created_at | date-time | No | users candidate | created_at | 4.1 | ISO-8601 JSON mapping | Bắt buộc | Legacy source candidate. |
| 5.9 | items[].updated_at | Updated time | updated_at | date-time | No | users candidate | updated_at | 4.1 | ISO-8601 JSON mapping | Bắt buộc | Legacy source candidate. |
| 6 | data.pagination.page | Page | page | int32 | No | Query | page | 1.4/5.1 | Requested valid page; default 1 | >=1 | Fixed one-based paging. |
| 7 | data.pagination.size | Page size | size | int32 | No | API #07 precedent | N/A | 5.1 | Constant 20 | 20 | DERIVED; no size query. |
| 8 | data.pagination.total | Total | total | int64 | No | Count query | COUNT(*) | 5.1 | Same predicates as list query | >=0 | Legacy users count candidate. |
| 9 | data.pagination.total_pages | Total pages | total_pages | int32 | No | Count query | total | 5.1 | ceil(total / 20); 0 when total=0 | >=0 | DERIVED. |
| 10 | meta | Metadata | meta | object | No | N/A | N/A | 5.1 | Empty object | {} | Current success helper convention. |
| 11 | traceId | Trace ID | traceId | uuid | No | Middleware | X-Trace-Id | 0.1/5.1 | Validated or generated UUID | Bắt buộc | Current middleware convention. |
| Excluded | items[].bio | Biography | bio | string? | N/A | No source | N/A | N/A | Omitted | Omit optional field | Current API #04/legacy users projection has no bio. |
| Excluded | password_hash | Credential | password_hash | string | N/A | users | password_hash | N/A | Never selected or serialized | Excluded | Security invariant. |

## Ví dụ success

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Users retrieved.",
  "data": {
    "items": [
      {
        "id": 1001,
        "full_name": "Ada Lovelace",
        "email": "ada@example.test",
        "role": "STUDENT",
        "avatar_url": null,
        "phone": null,
        "status": "ACTIVE",
        "created_at": "2026-09-15T12:00:00",
        "updated_at": "2026-09-23T10:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

## Ví dụ lỗi

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {
    "fieldErrors": [
      {
        "field": "page",
        "code": "GREATER_THAN_EQUAL",
        "message": "Input should be greater than or equal to 1"
      }
    ]
  },
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

Current error_response mặc định data:null; trace ID được giữ trong envelope và X-Trace-Id.

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
