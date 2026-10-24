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
| Direct contract type | ApiEnvelope<UserProfile> theo catalog. |

## Contract trực tiếp từ catalog

Giữ response đơn UserProfile đúng catalog. Đây chưa phải một response list có pagination và không khớp ý định AC-31.

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5.1/5.2/5.3 | 200/401/403/500 theo nhánh | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5.1/5.2/5.3 | true khi success, false khi error | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5.1/5.2/5.3 | Code theo catalog | N/A | Direct errors: 401/403/500. |
| 4 | message | Message | message | string | No | N/A | N/A | 5.1/5.2/5.3 | Branch message | Chưa đặc tả | Không trả raw DB detail. |
| 5 | data | User profile | data | object | No | users candidate | Safe projection | 5.1 | Map UserProfile | Direct schema không định nghĩa empty-list behavior | Catalog response đơn. |
| 5.1 | data.id | User ID | id | int64 | No | users candidate | id | 4.1 | Direct candidate mapping | Bắt buộc khi success | Legacy BIGINT candidate; pilot UUID khác. |
| 5.2 | data.full_name | Full name | full_name | string | No | users candidate | full_name | 4.1 | Direct candidate mapping | Bắt buộc khi success | API #4/#14 projection precedent. |
| 5.3 | data.email | Email | email | email | No | users candidate | email | 4.1 | Direct candidate mapping | Bắt buộc khi success | PII; Admin-only. |
| 5.4 | data.role | Role | role | UserRole | No | users candidate | role | 4.1 | Direct candidate mapping | Bắt buộc khi success | Catalog dùng UserRole nhưng không liệt kê enum members. |
| 5.5 | data.avatar_url | Avatar URL | avatar_url | uri? | Yes | users candidate | avatar_url | 4.1 | Direct candidate mapping | Null/omit semantics cần chốt | API #4 model hiện serialize null. |
| 5.6 | data.bio | Biography | bio | string? | Yes | SOURCE_REQUIRED | N/A | 4.1 | Không tạo giá trị | Omit chỉ sau khi owner xác nhận | Reusable schema có field; legacy/current model không có source. |
| 5.7 | data.phone | Phone | phone | string? | Yes | users candidate | phone | 4.1 | Direct candidate mapping | Null/omit semantics cần chốt | PII; API #4 model hiện serialize null. |
| 5.8 | data.status | Account status | status | UserStatus | No | users candidate | status | 4.1 | Direct candidate mapping | Bắt buộc khi success | Catalog dùng UserStatus nhưng không liệt kê enum members. |
| 5.9 | data.created_at | Created time | created_at | date-time | No | users candidate | created_at | 4.1 | ISO-8601 candidate | Bắt buộc khi success | Live schema chưa xác minh. |
| 5.10 | data.updated_at | Updated time | updated_at | date-time | No | users candidate | updated_at | 4.1 | ISO-8601 candidate | Bắt buộc khi success | Live schema chưa xác minh. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 5.1/5.2/5.3 | Empty object theo current helper convention | {} | Page metadata không có trong direct response. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | X-Trace-Id/middleware | 0.1/5.1/5.2/5.3 | Validated or generated UUID | Bắt buộc trong envelope | Current middleware convention. |

Không select hoặc trả password_hash, refresh token, token hash hay credential.

## Ví dụ success theo contract trực tiếp

Ví dụ dưới đây minh họa ApiEnvelope<UserProfile> như catalog ghi. Nó là một UserProfile đơn và vì vậy không thể biểu diễn danh sách/pagination trong AC-31.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "User retrieved.",
  "data": {
    "id": 1001,
    "full_name": "Nguyen Van A",
    "email": "user@example.test",
    "role": "STUDENT",
    "avatar_url": null,
    "phone": null,
    "status": "ACTIVE",
    "created_at": "2026-09-15T12:00:00Z",
    "updated_at": "2026-09-23T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

bio được omit vì optional field này chưa có source trong current Study profile model hoặc legacy users schema.

## Đề xuất response list — DERIVED, chưa phải contract

AC-31 yêu cầu danh sách và pagination. Proposal cần owner phê duyệt và sửa catalog đồng bộ trước implementation:

Candidate collection type: Page<UserProfile>, bọc trong ApiEnvelope<Page<UserProfile>>. Type này không thay direct ApiEnvelope<UserProfile> đang có trong catalog.

| Candidate path | Type | Source/transform | Status |
|---|---|---|---|
| data.items[] | UserProfile[] | Q1 candidate safe user projection | DERIVED |
| data.pagination.page | int32 | Query page sau khi áp dụng default | DERIVED |
| data.pagination.size | int32 | Fixed size 20 theo API #07 precedent | DERIVED |
| data.pagination.total | int64 | Q2 count với cùng filter | DERIVED |
| data.pagination.total_pages | int32 | ceil(total / size), total=0 thì 0 | DERIVED |

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Users retrieved.",
  "data": {
    "items": [
      {
        "id": 1001,
        "full_name": "Nguyen Van A",
        "email": "user@example.test",
        "role": "STUDENT",
        "avatar_url": null,
        "phone": null,
        "status": "ACTIVE",
        "created_at": "2026-09-15T12:00:00Z",
        "updated_at": "2026-09-23T10:00:00Z"
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

Đây là ví dụ proposal DERIVED, không phải JSON theo direct response catalog. Field bio được omit do chưa có source.

## Ví dụ lỗi theo catalog

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Access denied.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

Mẫu data lỗi {} phản ánh current error_response helper; API guideline kỳ vọng null. API #68 chưa wired nên đây là discrepancy, không phải runtime observation.

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
