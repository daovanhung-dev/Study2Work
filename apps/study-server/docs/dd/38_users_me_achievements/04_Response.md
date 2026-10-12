---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "38"
api_name: "Lấy achievement/badge nếu có"
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
| Contract type | ApiEnvelope<Page<Achievement>> theo API catalog; contract design-only, chưa runtime-verified. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | success | Success | success | boolean | No | N/A | N/A | 5.1 | Theo ApiEnvelope<T>. | N/A | Field envelope theo catalog/guideline. |
| 2 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5.1 | DESIGN_RESOURCE_RETRIEVED khi thành công. | N/A | Mã success theo catalog. |
| 3 | message | Message | message | string | No | N/A | N/A | 5.1 | Message an toàn theo API guideline. | Nội dung endpoint chưa được đặc tả. | Không khóa wording trong DD. |
| 4 | data | Data | data | Page<Achievement> | No | Chưa xác định | Chưa xác định | 5.1 | Theo API catalog; nguồn achievement/page chưa được xác nhận. | N/A | Logical response schema. |
| 5 | data.items | Items | items | Achievement[] | No | Chưa xác định | Chưa xác định | 4.2 | Danh sách achievement theo Page<T>. | Empty state chưa được đặc tả. | Không giả định rule award hoặc ordering. |
| 6 | data.items[].id | Achievement ID | id | int64 | Chưa rõ | Chưa xác định | Chưa xác định | 4.2 | Theo Achievement schema. | Nguồn/format chưa xác định. | Không có achievement table trong ERD V1/DDL. |
| 7 | data.items[].code | Achievement code | code | string | Chưa rõ | Chưa xác định | Chưa xác định | 4.2 | Theo Achievement schema. | Nguồn/enum chưa xác định. | Code catalog/registry chưa được cung cấp. |
| 8 | data.items[].title | Achievement title | title | string | Chưa rõ | Chưa xác định | Chưa xác định | 4.2 | Theo Achievement schema. | Locale/translation rule chưa xác định. | Không tạo title hoặc badge definition. |
| 9 | data.items[].awarded_at | Award time | awarded_at | date-time | Chưa rõ | Chưa xác định | Chưa xác định | 4.2 | Theo Achievement schema. | Event/time source chưa xác định. | Không map sang event timestamp nếu chưa có rule. |
| 10 | data.items[].course_id | Course ID | course_id | int64 | Chưa rõ | Chưa xác định | Chưa xác định | 4.2 | Optional theo Achievement schema. | Optional/nullable/omit semantics chưa rõ. | Không giả định achievement luôn gắn với course. |
| 11 | data.pagination | Pagination | pagination | PageMeta | No | N/A | N/A | 4.3 | Theo Page<T>. | N/A | Request pagination controls chưa có trong catalog. |
| 12 | data.pagination.page | Page number | page | int32 | No | N/A | N/A | 4.3 | Theo PageMeta. | Giá trị/default chưa được đặc tả. | Không thêm page query parameter. |
| 13 | data.pagination.size | Page size | size | int32 | No | N/A | N/A | 4.3 | Theo PageMeta. | Giá trị/default chưa được đặc tả. | Không thêm size query parameter. |
| 14 | data.pagination.total | Total records | total | int64 | No | N/A | N/A | 4.3 | Theo PageMeta. | Tính count/predicate chưa được đặc tả. | |
| 15 | data.pagination.total_pages | Total pages | total_pages | int32 | No | N/A | N/A | 4.3 | Theo PageMeta. | Quy tắc khi size/total bằng 0 chưa được đặc tả. | |
| 16 | meta | Metadata | meta | object | No | N/A | N/A | 5.1 | Theo ApiEnvelope<T>. | Nội dung endpoint chưa được đặc tả. | Không thay pagination object của Page. |
| 17 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 5.1 | Theo ApiEnvelope<T>/guideline. | N/A | Trace ID theo policy chung. |

## Ví dụ thành công

Các giá trị trong ví dụ chỉ minh họa cấu trúc/type của contract; chúng không phải achievement thực tế và không định nghĩa default pagination.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Achievements retrieved",
  "data": {
    "items": [
      {
        "id": 1001,
        "code": "ACHIEVEMENT_CODE_EXAMPLE",
        "title": "Achievement title example",
        "awarded_at": "2026-10-12T09:00:00Z",
        "course_id": 42
      }
    ],
    "pagination": {
      "page": 1,
      "size": 1,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000038"
}
```

## Ví dụ lỗi

Ví dụ 401 minh họa envelope chung; business code/message cụ thể của từng nhánh phải giữ guideline và catalog.

```json
{
  "success": false,
  "businessCode": "DESIGN_AUTHENTICATION_REQUIRED",
  "message": "Authentication required",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000038"
}
```

## Response gap

- Catalog định nghĩa logical Achievement fields nhưng không có source table, award registry, calculation rule hoặc projection.
- DB guide nói achievements được tính từ dữ liệu hiện có; không nêu cách tạo id, code, title, awarded_at hoặc course_id.
- Response là Page<Achievement> nhưng catalog chỉ khai báo course_id trong request; page/size source/default, sort, total predicate và empty behavior chưa được xác nhận.
- Không thêm field, pagination query parameter, 404 hoặc validation code ngoài contract.
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
